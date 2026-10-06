# David Q&A prep: the 20 hardest questions (with honest answers)

Answers come from the repo, tests and evidence as of 2026-10-05. Tags: REAL = actually tested; DEMO/MOCK = canned data; DOCUMENTED = vendor says so, untested; WAITING = needs access. See `reports/PEÇASAUTO_DEMO_REVIEW.md` for the demo issues that must be fixed before showing this.

**1. Why FastAPI?**
Python is where the provider adapters, normalisation and benchmark code already live (46 + 7 tests), the OpenAPI/Swagger UI makes the contract testable from a terminal, Pydantic gives strict typed models for vehicle/fitment, and we can swap the web layer without touching the domain code (`app/`, `providers/`). Alternatives (NestJS etc.) would mean rewriting that code. Honest caveat: the prototype uses SQLite and no auth; production needs Postgres, auth, migrations.

**2. Why Next.js?**
Portuguese-first SEO for category/product pages (SSR/ISR), a good cart/checkout ecosystem, and the same React skills David may already have. The frontend only ever calls our own API (verified: the only `fetch` base is `API_URL`; no provider hostnames in `apps/web`). Honest caveat: the demo is client-heavy; SEO/caching strategy isn't built.

**3. What happens without TecDoc?**
We can launch search, garage, stock/pricing, checkout and *manual-confirmation* flows. We **cannot** say "this part fits your car" automatically. Products show "Confirmar compatibilidade" and staff/customer confirm. A narrow category set (filters, brakes) can use staff-curated fitment lists. No automatic COMPATIBLE exists today.

**4. What happens if the plate returns multiple cars?**
The system is designed to show all candidates with precision and source, and make the customer choose (and save the choice as USER_CONFIRMED). In the demo this path is shown for one canned case (3008 vs 5008). **No real plate provider has returned anything yet.**

**5. What is a K-Type?**
TecDoc's numeric vehicle ID (make + model + engine + year range). A catalogue links parts to K-Types. Example from our evidence: 130708 = Peugeot 3008 SUV 1.5 BlueHDi 130 (cross-checked in Autodoc and a Schaeffler listing); 130738 = Peugeot 5008 II 1.5 BlueHDi 130. A K-Type from a third-party decoder is only a *candidate* until validated.

**6. Where does fitment actually come from?**
From a licensed catalogue (TecDoc via direct licence, reseller or Tips4y), possibly with partslink24 as human validation. Today there is **no** fitment source. The fitment labels in the demo catalogue are **static demo values** (they do not change with the selected car).

**7. What happens if provider X disappears?**
Providers sit behind adapters and a configurable cascade; failures are isolated (timeouts, 401/429, malformed) and the next step or manual selection takes over. Customer-confirmed vehicles live in our own garage, independent of provider caches. Risk: a vehicle-ID mapping learned from a vendor's K-Type must be re-derivable; keep `match_method` and source with every record.

**8. How do we avoid wrong parts?**
Hard gates: COMPATIBLE needs ENGINE+ identity, a unique catalogue bridge, a licensed MATCH, no restrictions, no conflicts; disagreement → CONFLICT/review; text-match can never claim compatibility. **Known gaps (red-team):** fitment doesn't yet take the bridge result; ENGINE_CODE bridge can auto-claim although 3008 and 5008 share engine code YHZ; the demo's per-product states are hard-coded. These must be fixed before anyone trusts "Compatível".

**9. How will Primavera integrate?**
Through an `InventoryProvider`/`PricingProvider` boundary (docs/primavera_integration_contract.md): stock, price, customers, orders, invoices. Primavera never supplies identity or fitment. Status: **interface and contract only. Version, modules and API access unknown (WAITING for Fahad).** Likely routes (to confirm): Primavera Web API/REST on newer versions, or a middleware/DB-sync layer.

**10. Why not just use partslink24?**
Its public ToS prohibits integrating it into our own online service, automated extraction/storage, and sublicensing; vehicle queries must relate to a real customer order. It is excellent as Fahad's staff tool and as ground truth for our tests. Backend use would need written permission from LexCom. It also covers OEM catalogues only, not aftermarket parts.

**11. What costs money?**
Published prices (ex-VAT): plate lookups €0.10 (Tips4y pack, TecDoc customers only), €0.12–0.25 (TelePeças), €0.18–0.20 (Matricula.co.pt), Openapi €0.18–0.40; Autoways **price unknown** (20 free credits); Vincario €0.22–0.49/VIN; TecDoc licence **QUOTE REQUIRED** (biggest cost); Primavera integration work unknown; GLS contract dependent; hosting/payment fees. Everything else (frontend, backend) is our time.

**12. What is currently real?**
**REAL TESTED DATA:** the vPIC result for the client VIN (BASIC only), 71 Python tests, 3 frontend tests, the production frontend build, and the local FastAPI/Strapi/PostgreSQL execution paths. **UNVERIFIED RESEARCH:** the Autofrance/K-Type material; it is not licensed provider evidence and is absent from the customer flow. **NOT LIVE:** every plate result, any Auto Ways/TIPS4Y/TelePeças/Matricula.co.pt response, all demo products, fitment, stock, delivery timing, payment and GLS data.

**13. How long does Phase 1 take?**
Not committed by the evidence; a reasonable split: platform (accounts, garage, search, cart, checkout, admin, config-driven cascade, Postgres, auth) is independent of vendors and can start now; provider adapters follow within days of real responses; licensed fitment depends on the TecDoc contract and onboarding (unknown, QUOTE REQUIRED). Do not promise a launch date until the TecDoc route and timeline are known.

**14. What are the biggest blockers?**
(1) No licensed fitment source / TecDoc quote. (2) No Portuguese plate result from any provider (accounts/tokens needed). (3) Rights to cache/store provider data unknown for all. (4) Primavera version/API unknown. (5) Test-car conflict (3008 vs 5008) unresolved: needs plate result, registration certificate or partslink24 output.

**15. Why is the 3008/5008 case still open if the K-Type says 3008?**
The VIN prefix and chassis codes are shared by both models; the K-Type came from a research-only storefront lookup that also answers fake VINs confidently. Two independent catalogue sources confirm what 130708 *is*, and the VIN descriptor suggests 3008, but no authoritative Portuguese source has confirmed the car. The client expectation is kept visible, not overwritten.

**16. Can we cache plate/VIN lookups to cut cost?**
Customer-confirmed vehicles in our garage: yes (our data, GDPR-governed). Provider results: **no, until written terms allow** (`ProviderPolicy` disables caching when terms are unverified). Cost scenarios with and without caching are in `reports/FINAL_PRE_TECDOC_DATA_STRATEGY.md`.

**17. How do you handle bad/spoofed input and abuse?**
Plate/VIN normalisation and validation exist (PT formats, VIN structure without mandatory EU checksum). Rate-limiting, auth, bot protection and per-user garages are **not** built (admin and garage endpoints are open in the prototype).

**18. Is the checkout secure/real?**
No. DEMO ONLY: no payment, no card data, no GLS call. **Known flaw:** the order endpoint trusts client-supplied prices (I created an order at €0.01 × 3); needs server-side pricing from the catalogue/Primavera. Stock isn't decremented; shipping is a flat demo number.

**19. How does GDPR affect this?**
Plates/VINs linked to customers are personal data: define lawful basis, retention, redaction of raw provider payloads (currently not persisted), DPA with each provider (Autoways' legal entity and data source are unknown), and a privacy notice. Not yet addressed in code beyond not storing raw payloads.

**20. What would make you (David) trust this for launch?**
Evidence: ≥2 Portuguese plate providers returning ENGINE+K-Type on ≥20 verified Portuguese cars with a false-confident rate near zero; licensed catalogue fitment with restrictions; written caching/commercial rights; server-side pricing and Primavera sync; auth, audit logs, Postgres, monitoring; a returns policy tied to confirmed vehicles.
