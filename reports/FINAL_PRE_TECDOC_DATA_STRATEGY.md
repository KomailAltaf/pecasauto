# Final pre-TecDoc data strategy — Portugal-only evidence round

Date: 2026-10-05. This is the strongest evidence currently possible without creating accounts in Komail/Fahad's name, obtaining client credentials, accepting commercial contracts, or paying for access. Total spend: **€0**.

## Executive position

There is a workable **prototype** route, not yet a production-validated stack:

```text
PT matrícula
  → TelePeças / Matricula.co.pt / Openapi / Tips4y (benchmark still required)
VIN research
  → Autofrance VIN→KType oracle (research only; never production routing)
Both
  → normalized vehicle candidates + provenance
  → manual one-more-field confirmation when ambiguous
  → licensed catalogue vehicle ID / KType
  → licensed fitment + restrictions
  → Primavera stock / price
  → checkout / GLS
```

No provider may produce `COMPATIBLE` from vehicle identity alone.

## 1. Best matrícula solution

**DOCUMENTED CAPABILITY — TelePeças is the strongest Portugal-specific candidate to test first**, because its official material covers Portuguese plate/VIN decoding, OEM/compatibility and catalogue fields that include TelePeças IDs, TecDoc model IDs and optional KType. **WAITING FOR ACCESS:** OAuth seller/integrator credentials and commercial terms.

**DOCUMENTED CAPABILITY — Tips4y is the strongest explicit plate→VIN/KType→TecDoc bridge candidate**, but price, response and contract are untested.

**UNVERIFIED:** no plate provider has returned data for `CG-17-GC`. There is therefore no production matrícula winner yet.

## 2. Best VIN solution

**PARTIALLY VERIFIED — Autofrance research endpoint** returned ENGINE-level identity and KType `130708` for the real PT client VIN. Independent public catalogue references cross-check `130708` as Peugeot 3008 SUV / 1.5 BlueHDi 130 / 96 kW. The VIN→KType assignment remains partial, conflicts with the client's Peugeot 5008 expectation and comes from an endpoint with no VIN-existence check or production licence. It is excluded from the production cascade.

## 3. Best free route

**PARTIALLY VERIFIED for research only:** local structural VIN validation → Autofrance VIN→KType → manual confirmation demonstrates the mechanics, but is not a deployable data stack. vPIC can be a BASIC cross-check but adds no model/engine value on this case. Self-hosting vPIC improves latency/control, not Portuguese coverage. No production-licensed free identity route has been found.

## 4. Best cheap paid route

**DOCUMENTED CAPABILITY / UNVERIFIED:** Matricula.co.pt is the cheapest clear first test at 10 free lookups then advertised €0.20/call. Openapi PT-car documents richer PT fields and costs €0.40 PAYG / €0.18–€0.37 at published annual tiers. Neither has been tested on the real plate, so this is a test priority, not a production recommendation.

## 5. Best future premium route

**DOCUMENTED CAPABILITY:** TecAlliance Vehicle Identification + TecDoc Catalogue provides the cleanest direct VIN/VRM→KType/NType→aftermarket linkage route. **WAITING FOR ACCESS:** Portugal coverage, 83-brand scope, price, API, caching/storage and lead time.

## 6. Best vehicle→catalogue bridge

**PARTIALLY VERIFIED:** Autofrance returned actual KType `130708`; independent public catalogue references cross-check what that KType represents, but not the provider's assignment of this VIN. **DOCUMENTED CAPABILITY:** TelePeças and Tips4y expose/advertise KType-based bridges. A direct provider ID/KType is safer than fuzzy text mapping, but it still requires a licensed catalogue and validation. Text matching never produces compatibility.

## 7. partslink24 role

**DOCUMENTED CAPABILITY:** manual VIN/OE/genuine-parts validation and benchmark ground truth through Fahad's existing account. **WAITING FOR ACCESS/RIGHTS:** backend API, export, ecommerce display, caching and storage. Do not automate the browser or assume it replaces TecDoc aftermarket fitment.

## 8. Primavera role

**VERIFIED CLIENT CONTEXT:** Primavera/Cegid is the current operational system. Intended boundary: stock, prices, customers, orders and invoices. Exact version, modules, API and data structure are **WAITING FOR HUMAN ACCESS**. Keep identity/fitment outside Primavera.

## 9. Fitment status

**NOT VERIFIED for production.** No licensed client-specific product fitment has been tested. Autofrance's KType page states that parts are linked using manufacturer/TecDoc data, but reuse rights and the model conflict prevent production use. `1K1614724E` and `2K1614723` public checks show that OE references can carry PR-code, VIN-range, side and steering restrictions; reference search alone is not fitment.

## 10. Result for CG-17-GC

**WAITING FOR ACCESS.** Matricula.co.pt rejected the unauthenticated request with `Your username is incorrect`. TelePeças OAuth returned `invalid_client`. No vehicle payload was obtained. The plate remains an accepted PT campaign input, not independently verified ground truth.

## 11. Result for VF3MCYHZUPS034433

- **PARTIALLY VERIFIED:** public vPIC and self-hosted vPIC return only `PEUGEOT`; BASIC_ONLY; no model/engine/fuel/power.
- **PARTIALLY VERIFIED:** Autofrance returns Peugeot 3008 SUV, 1.5 BlueHDi 130, diesel, 96 kW/131 hp, 1499 cc, KType 130708; ENGINE_LEVEL.
- **IDENTITY CROSS-CHECKED:** public catalogue references identify KType 130708 as the same 3008 engine and KType 130738 as the comparable 5008.
- **LIKELY / DISPUTED:** evidence leans toward 3008, but the client supplied 5008 II. A plate, OEM, partslink24 or registration-document result is required before changing ground truth.

## 12. Cost per 1k

- Free stack: **€0 API fee**, but no independently verified correct ENGINE result yet.
- Matricula.co.pt advertised public rate: **€200**.
- Openapi PT-car PAYG: **€400**; applicable annual tier may reduce it.
- TelePeças/Tips4y/TecAlliance: **quote required**.

## 13. Cost per 10k

- Free stack: **€0 API fee**, subject to permission/rate limits/infrastructure.
- Matricula.co.pt advertised public rate: **€2,000**.
- Openapi PT-car PAYG: **€4,000**; published 10k annual tier is €0.30/call, but monthly equivalence must not be assumed.
- Cost per correct ENGINE or EXACT result is not calculable until verified PT benchmark outcomes exist.

## 14. What can be built now

**VERIFIED engineering foundation:** provider interfaces, normalized nullable vehicle model, provenance, PT plate/VIN normalization, configurable cascades, safe cache policy, multi-source disagreement, manual one-more-field UX, customer-confirmed garage, bridge methods, fitment hard gates, raw-evidence replay, cost/report generation.

**PARTIALLY VERIFIED research prototype:** Autofrance VIN adapter and KType bridge, with a visible `REVIEW` state for the client conflict. It is excluded from the production cascade.

## 15. What needs human access

- Matricula.co.pt free test account.
- TelePeças seller/integrator OAuth credentials.
- Fahad's current vehicle-identification software demonstration/API/export details.
- Fahad's permitted partslink24 output and package/rights.
- 10–20 independently verified Portuguese vehicle records.
- Openapi/Vincario/other free-trial accounts if selected.
- Primavera version/modules/API inspection.

## 16. What must wait

**WAITING FOR ACCESS:** production provider choice, exact PT plate precision, final caching/storage policy, programmatic partslink24 use, production fitment, provider SLAs and final routing economics. TecDoc is not required to continue architecture, but a licensed fitment source is required before automatic compatibility claims.

## 17. What to tell Fahad

1. Free US-oriented VIN data identified only Peugeot and is insufficient.
2. A free European parts API found a detailed engine and catalogue KType, but it says 3008 while the supplied expectation says 5008; this is exactly why independent validation is required.
3. We need 10–20 real Portuguese vehicles and permitted partslink24/registration-document truth.
4. Please provide TelePeças/current-software access routes and partslink24 package/rights.
5. Until fitment is licensed and validated, uncertain products will show `Confirmar compatibilidade`, not a false green tick.

## 18. What to tell David

The provider abstraction and safety model are ready. The most valuable next engineering work is a real-response Matricula/TelePeças adapter and KType bridge benchmark, not more generic VIN parsing. Treat Autofrance as an excellent evidence-generating prototype source with unresolved commercial rights and a deliberate conflict case.

## 19. Risks

- **HIGH — false confident identity:** actual 3008-vs-5008 conflict.
- **HIGH — fitment licensing:** identity/KType is not permission to reuse catalogue links.
- **HIGH — small sample:** n=1 PT client input; independently verified production-score n=0.
- **HIGH — fitment restrictions:** PR codes, chassis ranges, side, LHD/RHD and equipment can survive ENGINE-level identity.
- **MEDIUM — provider dependency:** plate providers need credentials/contracts.
- **MEDIUM — economics:** advertised request price is not cost per correct engine/variant or purchase.
- **MEDIUM — privacy:** plate/VIN raw retention needs an agreed GDPR policy.

## 20. Next actions

1. Fahad manually confirms this VIN in partslink24 and provides permitted evidence.
2. Komail creates the Matricula.co.pt free test account and stores one raw `CG-17-GC` response.
3. Request TelePeças sandbox/OAuth and Tips4y commercial response.
4. Contact Autofrance for written production reuse, cache/storage, Portugal and 83-brand coverage terms.
5. Collect 10–20 verified PT vehicles, then expand to 100–500 PT-only records.
6. Re-run matrix and calculate false-confident rate and cost per correct ENGINE/EXACT result.
7. Select a licensed fitment path; keep TecAlliance as premium baseline.

## Stop-condition assessment

Accessible automated routes that could lawfully be tested without creating accounts were exercised: local parser, public vPIC, self-hosted vPIC and the Autofrance research endpoint. Catalogue identity cross-checks were added. Remaining decisive routes require accounts, contracts, client credentials, or human screenshots/manual account use. Raw evidence exists for each actual automated test, the Portugal-only gate is enforced, and the bridge and fallback safety rules are implemented. Manual public-site plate checks remain a human action and are not presented as automated provider validation.



---

# ROUND 6 ADDENDUM (Claude, 2026-10-05): K-Type result cross-checked

- **VERIFIED (reproduced):** `api.autofrance.se` VIN `VF3MCYHZUPS034433` → K-Type 130708, "Peugeot 3008 SUV 1.5 BlueHDi 130, 96 kW".
- **VERIFIED identity of K-Type 130708** by two independent public TecDoc-style sources (Autodoc, Schaeffler listing): 3008 SUV 1.5 BlueHDi 130, YHZ (DV5RC). **K-Type 130738** = 5008 II 1.5 BlueHDi 130, VDS MCYHZJ/R/X.
- **PARTIALLY VERIFIED:** the VIN is a **3008** (VDS MCYHZ**U** is not in the 5008 list; Autofrance's plant rule S→3008). The client's "5008" is the likely outlier; resolve with the plate (human lookups) or partslink24.
- **Warning:** Autofrance answers confidently for non-existent VINs (synthetic serial 000001). Never a sole source; storefront backend, research use only.
- Best bridge for the client case now: **VIN → K-Type 130708 (cross-checked) → TecDoc-licensed catalogue**; fitment still NOT SOLVED.
See `reports/autofrance_ktype_investigation.md`, `reports/ktype_crosscheck.csv`.

## ROUND 6: COST UPDATE (Tips4y)
- **Plate lookup ≈ €0.10 + VAT (Pack 300 = €30)**, DOCUMENTED, bundled to Tips4y TecDoc customers, not for resale. Per 1,000 lookups ≈ €100; per 10,000 ≈ €1,000.
- Scenario spend at €0.10 (same assumptions as before; ASSUMPTIONS): A all paid 10k/50k/100k searches = €1,000 / €5,000 / €10,000; B free-first €950 / €4,750 / €9,500; C cache-first (rights unknown) €380 / €1,900 / €3,800; D plate-only no cache €665 / €3,325 / €6,650; D with saved vehicles €266 / €1,330 / €2,660.
- **Best documented Portuguese route to a catalogue vehicle ID:** Tips4y plate → TecDoc Vehicle ID + Tips4y TecDoc WebService (one vendor). **Best documented route that also covers VIN K-Type:** Autoways/Vincario (unverified for PT). Neither is verified on `CG-17-GC`; Tips4y trial/quote is P0.
