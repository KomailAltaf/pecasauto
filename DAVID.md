# PeçasAuto / Portugal Automotive Ecommerce Platform
## Technical, Data, Product and Commercial Handoff for David

> **Purpose:** internal single source of truth for Komail, David, and any senior engineer or agent supporting them. This is not the final proposal to Fahad and Ayaz.

| Item | Current position |
|---|---|
| Last updated | 6 October 2026 |
| Current git commit at drafting | `95e37abefdcda4ff4cb016a29957339fa9f8c0c2` (`main`); this is the parent of the documentation commit because a committed file cannot contain its own final hash |
| Repository | `https://github.com/KomailAltaf/pecasauto` |
| Prototype status | Full-stack local implementation prototype; customer journey is clickable; external operational integrations remain mostly demo or access-blocked |
| Demo approval | **READY TO SHOW DAVID** — confirmed by `collaboration/READY_TO_SHOW_DAVID` on 6 October 2026 |
| Production status | **NOT production-ready** |
| Current data recommendation | Free-first identity routing, low-cost Portuguese identity provider where needed, customer confirmation for ambiguity, and a licensed catalogue/fitment source before positive compatibility claims |

## Evidence vocabulary

These labels are deliberate and must not be weakened in a proposal or demo:

| Label | Meaning |
|---|---|
| **VERIFIED** | Confirmed by authoritative evidence or independently reproduced evidence appropriate to the claim. |
| **TESTED** | We executed a real request or workflow and retained evidence. Tested does not automatically mean accurate or production-approved. |
| **DOCUMENTED CAPABILITY** | The vendor's official material describes the capability. We have not proved it on our Portuguese cases. |
| **RESEARCH ONLY** | Useful for investigation or cross-checking, but no production licence, reliability, or reuse right has been established. |
| **DEMO** | Deliberately fabricated or seeded application data used to demonstrate a workflow. |
| **MOCK** | A simulated provider or component used for automated tests. It is not a real external response. |
| **WAITING FOR CREDENTIALS** | Adapter and/or test path exists, but no authorised key/account is available. |
| **QUOTE REQUIRED** | No current contractual price is available. Do not invent or infer one. |
| **UNVERIFIED** | A claim, result, mapping, or assumption still requires independent confirmation. |

---

## 1. Executive summary

Fahad and Ayaz want to launch a separate, Portugal-first automotive-parts ecommerce company. It is not a redesign of Castelo Peças and must have its own Portuguese brand, `.pt` domain, identity, customer experience, and commercial positioning. **PeçasAuto** is only the prototype name.

The initial launch catalogue is intended to focus on:

- filters;
- brake pads (`pastilhas de travão`);
- brake discs (`discos de travão`).

The long-term reference is the ease and breadth of an AUTODOC-style purchasing journey, not a clone of AUTODOC's design, code, content, or complete launch scope. The product needs to let a Portuguese customer start with information they already know—matrícula, VIN, vehicle details, or an OE/reference number—and reach a safe purchasable part.

### Where we are today

1. **VERIFIED:** a provider-independent domain model and replaceable provider interfaces exist.
2. **VERIFIED:** a local full-stack prototype exists with Next.js, FastAPI, Strapi, SQLAlchemy, SQLite/PostgreSQL boundaries, and a clickable commerce journey.
3. **TESTED:** Portuguese plate and VIN normalization, provider failure isolation, candidate handling, manual confirmation, garage persistence, fitment safety, server-side pricing, and authentication have automated coverage.
4. **TESTED:** public and self-hosted vPIC returned only Peugeot/manufacturer-level data for the client VIN; this is `BASIC`, not fitment-grade.
5. **RESEARCH ONLY:** an Autofrance storefront backend returned Peugeot 3008, 1.5 BlueHDi 130, 96 kW, and K-Type `130708`; the endpoint also answers synthetic VINs confidently and has no production licence.
6. **UNVERIFIED:** the client's stated Peugeot 5008 identity conflicts with the research result. The platform must not silently choose either vehicle.
7. **WAITING FOR CREDENTIALS:** no authorised Portuguese matrícula provider has returned a real vehicle payload for `CG-17-GC`.
8. **DOCUMENTED CAPABILITY:** Auto Ways, TIPS4Y, TelePeças, OpenAPI Portuguese Car Check, Matricula.co.pt, Vincario, One Auto API, and TecAlliance provide potentially useful components, but capability and legal rights vary.
9. **NOT VERIFIED:** no production fitment source has been connected. Therefore the prototype never presents demo products as positively compatible.
10. **VERIFIED CLIENT CONTEXT:** Fahad already uses partslink24 and Primavera/Cegid. Their exact packages, APIs, versions, and reuse rights remain to be inspected.
11. **DEMO:** catalogue products, prices, stock, delivery estimates, checkout payment, and GLS timings are explicitly demo data.
12. **VERIFIED:** Strapi edits and publishes the homepage hero and product editorial content; other CMS models are not yet rendered.
13. **VERIFIED:** security review fixed CMS data leakage, public browser credentials, session forgery, garage duplication, client-controlled order prices, and misleading provenance/fitment labels.
14. **READY TO SHOW DAVID:** the prototype is approved as an honest architecture/product demo, not as evidence that live providers or operations are integrated.
15. **Commercially open:** David is considering a three-month engineering engagement framed around roughly €10,000 per month. This is a working discussion point, not an agreed customer price.

The platform eventually needs Portuguese matrícula search, VIN search, manual selection, OEM/reference search, catalogue and fitment, stock and pricing, cart and checkout, GLS, accounts, admin/CMS, Primavera integration, supplier feeds, and later B2B workflows.

---

## 2. Client context

- **Fahad and Ayaz** operate an established automotive-parts business.
- **Castelo Peças** is the existing operational business; it is not the new consumer-facing ecommerce brand.
- Existing assets may include inventory, supplier relationships, purchasing knowledge, staff, premises, fulfilment processes, customer relationships, and operational systems.
- Fahad already has **partslink24 access**. Its current value is manual VIN/OE/genuine-parts validation. Programmatic integration rights are not established.
- Fahad already uses **Primavera/Cegid**. This is the confirmed operational system, but the version, modules, API, hosting, database, price lists, customer structure, and invoice workflow are still unknown.
- The new business should have a separate Portuguese name and `.pt` domain. Neither is final.
- Temporary prototype name: **PeçasAuto**.
- Initial geographic focus: **Lisbon**, followed by Portugal-wide delivery.
- Initial catalogue scope: filters, brake pads, and brake discs.
- Approximately **83 brands** have been discussed, subject to catalogue availability, data rights, and final client prioritisation.
- Shipping is expected to use **GLS**.
- Customer support should be Portuguese-speaking.
- Product development and marketing/customer acquisition are separate workstreams. No marketing performance commitment exists.

---

## 3. Original data idea

### Initial hypothesis

The original hypothesis was:

```text
free/open vehicle data
→ normalize vehicles into our own internal model
→ build a reusable vehicle database
→ map vehicles to catalogue/inventory
→ avoid TecDoc at the beginning
→ plug TecDoc or another licensed source in later
```

This was technically reasonable to investigate because:

- vehicle identity, catalogue data, fitment, stock, and price are separate data problems;
- free VIN data could potentially remove some paid calls;
- a provider-independent internal model prevents vendor lock-in;
- customer-confirmed vehicles can be reused where storage is legally permitted;
- a narrow launch with three categories might support more manual validation than a full catalogue;
- the client already has operational knowledge and software that might contain useful data;
- TecDoc access and commercial negotiation can take time.

### What changed after validation

Validation showed that **free-first remains useful, but free-only is not a safe production strategy**.

- Free VIN decoding can validate structure or identify a manufacturer.
- It did not identify the exact Portuguese-market model/engine/variant for our real VIN.
- A detailed vehicle identity still does not prove that a product fits.
- Catalogue identifiers such as K-Type are useful bridges, but they require validation and a licensed catalogue relationship.
- Fitment restrictions may depend on chassis range, PR code, steering side, brakes/equipment, production date, or other details beyond the visible engine label.
- The cost of wrong parts, returns, support, and lost trust can exceed the price of reliable licensed data.

The recommendation is therefore:

```text
FREE FIRST where useful and lawful
→ CHEAP PORTUGUESE IDENTITY PROVIDER when needed
→ CUSTOMER/STAFF CONFIRMATION when ambiguous
→ LICENSED CATALOGUE/FITMENT SOURCE for compatibility
```

---

## 4. What the validation taught us

### Do not confuse these problems

| Vehicle identification | Vehicle fitment |
|---|---|
| Question: **What exact vehicle is this?** | Question: **Does this exact product fit this exact vehicle?** |
| Inputs: matrícula, VIN, manual selection | Inputs: normalized vehicle/catalogue ID plus product ID |
| Outputs: make, model, generation, year, engine, code, power, fuel, variant, provider ID | Outputs: `MATCH`, `NO_MATCH`, `UNKNOWN`, or `CONFLICT`, including restrictions |
| Possible sources: vPIC, Auto Ways, OpenAPI, Matricula.co.pt, TIPS4Y, TelePeças, TecAlliance | Possible sources: TecDoc/TecAlliance, licensed supplier/manufacturer data, validated internal mapping |

Free identification can reduce lookup cost. It does **not** replace fitment data.

### Precision levels

- `BASIC`: manufacturer/basic identity only.
- `MODEL`: make + model + year/generation.
- `ENGINE`: exact engine family plus power/fuel.
- `EXACT_VARIANT`: engine code/exact variant plus an authoritative provider/catalogue identity.

Even `ENGINE` or `EXACT_VARIANT` identity does not automatically permit a `COMPATIBLE` claim. The fitment provider must independently return a trusted match with no unresolved restriction.

### Multiple candidates are normal

One plate or VIN can return several possible engines/versions. That is not necessarily a provider error.

```text
VIN or matrícula
→ several normalized candidates
→ customer confirms engine/version
→ confirmed vehicle saved in garage
→ catalogue vehicle ID / K-Type resolved
→ licensed parts search and fitment
```

One provider returning several variants is labelled **MULTIPLE / several versions found**. A **provider conflict** is reserved for incompatible answers from different providers.

### CLIENT-OPERATIONAL FEEDBACK

Feedback attributed to Anas is that real-world lookup often involves narrowing several plausible variants rather than receiving one perfectly resolved vehicle immediately. That is operational feedback, not formal provider proof. It supports designing confirmation as a normal product state rather than treating ambiguity as a system failure.

---

## 5. Real test case

| Field | Current evidence |
|---|---|
| Portuguese matrícula | `CG-17-GC` — client-provided pairing; no authorised API vehicle result yet |
| VIN | `VF3MCYHZUPS034433` — client-provided |
| Client expectation | Peugeot 5008 II, 1.5 BlueHDi 130 |
| vPIC public/self-hosted | **TESTED:** Peugeot/manufacturer only; `BASIC`; no useful model/engine/variant |
| Autofrance research endpoint | **RESEARCH ONLY / TESTED:** Peugeot 3008 SUV, 1.5 BlueHDi 130, 96 kW, K-Type `130708` |
| K-Type cross-check | **PARTIALLY VERIFIED:** independent public catalogue references identify `130708` as a Peugeot 3008 SUV 1.5 BlueHDi 130 and `130738` as the comparable 5008 II identity |
| Authoritative resolution | **UNVERIFIED:** no permitted plate-provider, registration document, OEM, or partslink24 evidence has settled the VIN/plate pairing |

### Current resolution status

Evidence leans toward **Peugeot 3008**, but the client supplied **Peugeot 5008**. These are separate claims:

1. `K-Type 130708` represents a 3008 configuration — identity cross-checked.
2. This VIN maps to `130708` — only partially verified through a research-only endpoint.
3. This matrícula and VIN belong to the same physical car — client-provided, not independently verified.

Therefore the current state is:

> **LIKELY 3008 / DISPUTED / NEEDS PLATE, REGISTRATION DOCUMENT, OEM, OR PARTSLINK24 CONFIRMATION.**

The conflict was valuable: it proved that detailed-looking provider output can still be wrong, misapplied, or inconsistent with client data. The application must preserve disagreement, request confirmation, and avoid false compatibility.

---

## 6. Providers and data sources researched

The table distinguishes real testing from vendor documentation. “Yes” under capability columns often means documented, not validated.

| Provider/source | Primary role | PT plate | VIN | Engine/code/power | K-Type/catalogue ID | Fitment | Evidence status | Public price position | Commercial/data rights | Notes |
|---|---|---:|---:|---|---|---:|---|---|---|---|
| NHTSA vPIC public | Free VIN router/basic decoder | No | Yes | Poor on client EU VIN | No | No | **TESTED — BASIC only** | Free | Public service; US-intended data limits apply | Returned Peugeot only for real VIN. |
| Self-hosted vPIC | Local copy of same data | No | Yes | Same ceiling as public vPIC | No | No | **TESTED — BASIC only** | Infrastructure only | Open-source/self-hosted rights documented | Improves control/latency, not PT coverage. |
| Auto Ways / AutoNow PT | Vehicle identity and bridge | Documented | Documented | Vendor spec lists engine code/kW/version | Vendor spec lists K-Type/TecDoc-style IDs | No | **DOCUMENTED CAPABILITY / WAITING FOR CREDENTIALS** | 20 free credits documented; paid price **QUOTE REQUIRED** | Ecommerce/reuse/cache rights **UNVERIFIED** | No retained real Auto Ways response exists. A stale draft claimed otherwise and is superseded by the evidence register and final review. |
| OpenAPI Portuguese Car Check | Low-cost Portuguese plate identity | Yes | VIN can appear in response | Version, fuel, displacement, horsepower; no engine code/K-Type documented | ABI code only; bridge not proven | No | **DOCUMENTED CAPABILITY / UNTESTED** | €0.40 PAYG; annual volume tiers below | Commercial API; caching/storage terms still need written confirmation | Strong transparent plate-pricing candidate. |
| Matricula.co.pt / RegCheck | Portuguese plate identity/cross-check | Yes | Returned as field where available; not a VIN-input route in our adapter | Make/model/engine size/fuel documented; exact PT depth unknown | ABI; no K-Type documented | No | **ACCESS TESTED; DATA UNTESTED / WAITING FOR CREDENTIALS** | €0.20; 10 free credits; 10% discount over 1,000-credit packs | Cache/resale rights not found | Unauthenticated request correctly returned username error. |
| TIPS4Y | PT plate identity plus TecDoc bridge/catalogue | Documented | Documented in marketing | Detailed vehicle data claimed | TecDoc Vehicle ID documented | Via bundled TecDoc offering | **DOCUMENTED CAPABILITY / QUOTE REQUIRED** | Repository evidence: Pack 300 €30 + VAT for eligible TecDoc customers; human reconfirmation required | Pack says not for resale; B2C display/API/storage rights require contract | Commercially important because one vendor may cover identity + catalogue. |
| TelePeças | Local plate/VIN identity, marketplace/catalogue | Yes | Yes | Technical vehicle data documented | API docs describe K-Type/TecDoc/provider IDs | Compatibility service exists, but backend scope untested | **ENDPOINT/AUTH TESTED; DATA UNTESTED / WAITING FOR CREDENTIALS** | Public packages and decode prices below | Integrator/ecommerce/cache rights **UNVERIFIED**; competing marketplace | OAuth returned `invalid_client`, proving access boundary only. |
| TecAlliance / TecDoc | Premium vehicle identity, catalogue, OE and fitment | VIN/VRM service documents Portugal-capable global route; exact package to confirm | Yes | Harmonised vehicle data | Native K-Type/NType | Yes | **DOCUMENTED CAPABILITY / WAITING FOR CONTRACT** | **QUOTE REQUIRED** | Rights defined by licence | Premium baseline; no direct contract yet. |
| partslink24 | OEM/genuine-parts lookup and validation | No production plate API established | Manual VIN use | OEM vehicle context | OEM catalogue context, not a proven TecDoc bridge | OEM/genuine application context | **VERIFIED CLIENT ACCESS / MANUAL ONLY** | Existing client subscription | Public terms do not permit assumed scraping/backend reuse | Ask for package, API/export rights, and permitted evidence. |
| Autofrance public lookup | Research VIN-to-K-Type oracle | No | Reachable | Returned engine/fuel/power | Returned K-Type | Storefront catalogue associations only | **RESEARCH ONLY / TESTED** | No API fee observed | No production API/licence; no existence validation | Confidently answered synthetic VINs; excluded from production cascade. |
| Vincario | EU-focused VIN fallback | No PT plate route proved | Yes | EU detail/variant marketed | K-Type/TecDoc mapping claimed | No | **DOCUMENTED CAPABILITY / UNTESTED** | 20 free; published VIN tiers below | Enterprise caching/terms require contract | Worth benchmarking on 20 verified PT VINs. |
| One Auto API | Aggregated PT vehicle data/VIN/OE lookup | No PT matrícula endpoint proved in reviewed Portugal list | Yes | VIN and OE/build products | No K-Type claim confirmed | No aftermarket fitment claim confirmed | **DOCUMENTED CAPABILITY / UNTESTED** | Portugal plans/prices below | Sandbox and contract terms apply | Newly researched comparator; not implemented in repo. |
| VehicleDatabases EU VIN | EU VIN/specification data | Not proved | Documented | Detailed EU specification claims | No K-Type proven | No | **RESEARCH ONLY / UNTESTED** | Pricing not relied upon for PT decision | Contract required | Broader service; Portugal depth not established. |
| Munic / Ekko | Fleet/telematics VIN description | Not proved | Europe decode documented | Rich description | GraphQL schema includes K-Type | No aftermarket fitment proof | **DOCUMENTED CAPABILITY / UNTESTED** | **QUOTE REQUIRED** | Enterprise credentials/company onboarding likely required | Fleet/telematics product, not yet justified for launch. |
| Existing Fahad software | Possible cheapest identity source | Unknown | Unknown | Unknown | Unknown | Unknown | **WAITING FOR CLIENT TECHNICAL REVIEW** | Possibly already paid | Export/API/reuse rights unknown | Must be demonstrated before paying for duplicate capability. |
| IMT / IRN / AT official routes | Administrative/official evidence | Manual/admin services | Not ecommerce VIN API | Official certificate context | No catalogue bridge | No | **PARTIALLY RESEARCHED** | Manual/unknown | Restricted/administrative | No public high-volume ecommerce identity API found; private B2B route still to ask about. |
| Auto Delta | Supplier/local aftermarket reference | No public API proved | No public API proved | Supplier catalogue context | No public bridge proved | No public fitment API proved | **REFERENCE/SUPPLIER RESEARCH ONLY** | **QUOTE REQUIRED** | Account/contract dependent | Relevant operational reference, not currently a data-provider integration. |
| Solutions4yb | TecDoc/webshop integrator | Plate source unclear | Marketing mentions VIN | Unknown | TecDoc integration advertised | Via TecDoc offering | **DOCUMENTED CAPABILITY / UNTESTED** | **QUOTE REQUIRED** | Contract required | Secondary Portuguese integrator; Primavera not listed in material reviewed. |
| MatriculAZ | Future Portuguese plate API | Planned | Unknown | Version/power fields documented | No proven K-Type | No | **DOCUMENTED BUT NOT AVAILABLE** | Not publicly priced; **QUOTE REQUIRED** if launched | Terms require specific commercial agreement; automation otherwise prohibited | Monitor only. |
| One Auto/Fleet-style enterprise onboarding | Contracted data access | Depends on product | Depends on product | Depends on product | Depends on product | Depends on product | **WAITING FOR CLIENT BUSINESS DETAILS** | Plan or quote | Legal company name, registration number, billing identity, and use case may be required | The new PeçasAuto legal entity/details are not final; do not invent them during signup. |

No credible repository evidence was found for a separate provider literally called “One Auto” before this handoff. The official **One Auto API** Portugal product was researched for this document and remains untested.

---

## 7. Provider pricing and commercial access

All figures exclude VAT unless explicitly stated otherwise. Public price is not the same as a production contract, and price per request is not price per correct ENGINE or fitment result.

### Current public prices verified for this handoff

#### OpenAPI Portuguese Car Check

Verified 6 October 2026 on the official [Portuguese Car Check page](https://openapi.com/products/portuguese-car-check):

| Package | Price per request | Billing condition |
|---|---:|---|
| Single/PAYG | €0.40 + VAT | Per request |
| 1,000 calls/year | €0.37 + VAT | Paid annually |
| 5,000 calls/year | €0.33 + VAT | Paid annually |
| 10,000 calls/year | €0.30 + VAT | Paid annually |
| 25,000 calls/year | €0.28 + VAT | Paid annually |
| 50,000 calls/year | €0.24 + VAT | Paid annually |
| 200,000 calls/year | €0.18 + VAT | Paid annually |

The annual tiers must not be represented as monthly volume pricing. The documented response includes make/model/version/fuel/displacement/horsepower and may include VIN; not every field is guaranteed for every car.

#### Matricula.co.pt

Verified 6 October 2026 on the official [Matricula.co.pt page](https://www.matricula.co.pt/):

- €0.20 per lookup.
- Minimum paid purchase: 100 credits (€20).
- 10 free test searches after account/email verification.
- 10% discount advertised for packages above 1,000 credits, implying approximately €0.18 per lookup where applicable.
- Exact engine code, K-Type, caching, storage, and ecommerce reuse are not established.

#### TelePeças

Verified 6 October 2026 on the official [TelePeças price page](https://www.telepecas.com/precos/). Values are stated by TelePeças as VAT-inclusive:

| Product | Public price |
|---|---:|
| 100 matrícula/VIN decodes | €25 total (€0.25 each) |
| 500 decodes | €100 total (€0.20 each) |
| 1,000 decodes | €175 total (€0.175 each) |
| 5,000 decodes | €615 total (€0.123 each) |
| “Serve no meu carro?” single | €1.99 |
| “Serve no meu carro?” company volume | €0.25 down to €0.16 each depending on package |
| OEM/OE references | Public packs exist; integration use remains contract-dependent |
| API/integrator access | **QUOTE REQUIRED** |

The public page says API access is for seller/integrator accounts. A competing ecommerce platform must obtain explicit written permission.

#### Vincario

Verified 6 October 2026 on Vincario's official [pricing material](https://vincario.com/pricing/) and published 2026 pricing guide:

| VIN volume | Advertised price per valid lookup |
|---|---:|
| Free demo | Up to 20 API lookups |
| 100 | €0.49 |
| 500 | €0.298 |
| 1,000 | €0.249 |
| 5,000 | €0.22 |
| 10,000+ | Custom / **QUOTE REQUIRED** |

Invalid/unrecognised VINs are advertised as not charged. Portugal-specific accuracy and K-Type output remain untested.

#### One Auto API — Portugal

Verified 6 October 2026 on the official [Portugal pricing page](https://www.oneautoapi.com/pricing/?country=PT):

| Plan | Base fee | VIN Decoder | OE VIN Lookup Europe |
|---|---:|---:|---:|
| PrePay | €29 initial top-up; no monthly fee | €0.18 | €0.36 |
| Business | €29/month + calls | €0.11 | €0.24 |
| Enterprise | €119/month + calls | €0.04 | €0.12 |
| Bespoke | **QUOTE REQUIRED** | **QUOTE REQUIRED** | **QUOTE REQUIRED** |

The reviewed Portugal page advertises a free sandbox and 23 compatible endpoints. It does not prove Portuguese matrícula lookup, K-Type, or aftermarket fitment for our use case.

### Prices requiring human confirmation or quote

| Provider | Current price status |
|---|---|
| TIPS4Y | Repository research from 5 October records Pack 300 at €30 + VAT (≈€0.10/lookup), restricted to eligible TIPS4Y TecDoc customers and “not for resale”. Reconfirm directly before proposal. Full TecDoc/API bundle: **QUOTE REQUIRED**. |
| Auto Ways | 20 free credits documented; production price not reliably retrievable: **QUOTE REQUIRED**. |
| TecAlliance direct | No public comparable licence price: **QUOTE REQUIRED**. |
| Fahad's existing TecDoc/reseller quote | Not present in repository: **CLIENT DOCUMENT REQUIRED**. |
| Solutions4yb | **QUOTE REQUIRED**. |
| Munic/Ekko, VehicleDatabases enterprise, other fleet/data suppliers | **QUOTE REQUIRED** and likely company onboarding. |
| Primavera/Cegid integration/licensing | **CLIENT/CEGID CONFIRMATION REQUIRED**. |
| GLS | Contract rates and API access **CLIENT CONFIRMATION REQUIRED**. |
| Payment provider | Provider and Portuguese payment methods not selected. Fees **TO VERIFY**. |

### Cost principle

The real metric is:

```text
provider spend ÷ independently correct ENGINE/EXACT results
```

not simply price per request. We cannot calculate this until at least 10–20 verified Portuguese vehicles have been benchmarked.

---

## 8. Direct TecDoc / TecAlliance strategy

Fahad has previously received TecDoc-related quotations, but the quote and exact scope are not in this repository. We are investigating direct TecAlliance access and Portuguese partner/reseller routes to avoid unnecessary markup while comparing like-for-like scope.

### What has been done

- TecAlliance direct product and Vehicle Identification Service material researched.
- Direct versus reseller/partner structure documented.
- TIPS4Y and Solutions4yb identified as local integration candidates; their formal authorised-partner status has not been confirmed.
- Provider outreach templates prepared.
- Alternative plate/VIN providers researched so platform work does not stop while TecDoc access is pending.
- No direct TecAlliance contract, quote, sandbox, or production credential has been obtained.

### Minimum request to TecAlliance

Ask for a narrowly scoped Portugal-first package:

- Portugal only;
- Vehicle Identification Service;
- VIN lookup;
- VRM/matrícula lookup for Portugal;
- K-Type/NType or equivalent catalogue vehicle identifier;
- TecDoc Web Service for the ecommerce backend;
- vehicle-to-article/product linkages and restrictions;
- OE/reference data required for search and validation;
- article basics, technical criteria, images, and brands for launch scope;
- filters, brake pads, and brake discs first;
- the intended 83-brand shortlist, subject to rights/coverage;
- startup/ramp or usage-based commercial structure;
- sandbox and onboarding timeline;
- caching, storage, garage reuse, public ecommerce display, and termination rights.

TecAlliance's official [Vehicle Identification Service](https://www.tecalliance.net/products?family=tecdoc&solution=catalogue-ecommerce) documents VIN/VRM lookup and K-Type/NType output. Its official [TecDoc Web Service](https://www.tecalliance.net/products/cards/tecdoc-web-service) documents vehicle, product, linkage, OE, and ecommerce API use. Pricing remains **QUOTE REQUIRED**.

---

## 9. Current recommended data architecture

```text
CUSTOMER INPUT
  ├─ Portuguese matrícula
  ├─ VIN / chassis
  ├─ manual vehicle selection
  └─ OEM / manufacturer / part reference
                ↓
FASTAPI VehicleIdentificationService
                ↓
PROVIDER CASCADE
  1. free/open source where useful
  2. low-cost Portuguese/EU provider where needed
  3. premium/licensed provider when required
  4. manual selection fallback
                ↓
ZERO / ONE / SEVERAL / PARTIAL CANDIDATES
                ↓
CUSTOMER CONFIRMATION IF AMBIGUOUS
                ↓
NORMALIZED INTERNAL VehicleIdentity
  + field provenance
  + precision
  + verification state
  + provider/external IDs
                ↓
CATALOGUE VEHICLE BRIDGE
  K-Type / NType / provider catalogue ID
  or confirmed canonical-field candidate mapping
                ↓
LICENSED CatalogueProvider + FitmentProvider
                ↓
PRODUCT CATALOGUE
                ↓
PRIMAVERA/Cegid stock + price
  and later supplier offers
                ↓
CART → CHECKOUT → PAYMENT → GLS
```

### Architectural rules

1. The frontend never calls TecDoc, Auto Ways, TIPS4Y, Matricula.co.pt, TelePeças, or another data vendor directly.
2. Providers implement internal interfaces and can be replaced through configuration.
3. Missing fields remain null; normalization never fabricates data.
4. A provider response is evidence, not fitment proof.
5. A K-Type is preserved with its source and verification status.
6. Customer confirmation is a first-class state.
7. No positive compatibility claim is shown without a trusted fitment match.
8. Provider data is cached or stored only where contractual rights allow it.
9. Customer-confirmed garage records are logically separate from provider caches.
10. Primavera remains operational truth for stock/pricing/orders/invoices, not vehicle identity or fitment.

---

## 10. Current software architecture

### Next.js / React / TypeScript

Owns the customer experience and demo admin views:

- Portuguese-first storefront;
- search route selection;
- vehicle candidate confirmation;
- garage;
- catalogue/product presentation;
- cart and checkout UI;
- login/session boundary;
- provider status and architecture views.

### FastAPI / Python / Pydantic / SQLAlchemy

Owns business logic and operational truth:

- vehicle identity orchestration;
- provider cascades;
- normalization and precision;
- catalogue and OE/reference search API;
- fitment state and safety rules;
- customer garage API;
- server-side prices and order totals;
- admin/provider status;
- future Primavera, supplier, GLS, and payment integrations.

### Strapi

Owns editable editorial content only. It must not become the source of truth for live price, stock, fitment, vehicle resolution, orders, or supplier operations.

### Persistence

- **Current FastAPI demo:** SQLite for immediate local use.
- **Current Strapi demo:** PostgreSQL through Docker/local configuration.
- **Target application:** PostgreSQL-compatible domain and migrations for operational persistence.
- Redis is optional later for jobs/rate limiting/contractually permitted short-lived caching, not required for the current prototype.

### External boundaries

| System | Intended responsibility |
|---|---|
| Primavera/Cegid | Stock, prices, customers, orders, invoices |
| TecDoc/TecAlliance | Future licensed vehicle/catalogue/product/fitment linkages |
| partslink24 | Manual OEM/genuine-parts validation unless integration rights are obtained |
| GLS | Shipping quotation/label/tracking after credentials and workflow agreement |
| Payment provider | Payment intents, webhooks, settlement; provider not yet selected |
| Supplier feeds | Supplier offers, virtual stock, cost, lead time, later purchase routing |

---

## 11. Strapi CMS

Strapi was introduced so Fahad's team can eventually edit customer-facing content without code changes.

### Intended CMS ownership

- product editorial content;
- brands and category presentation;
- homepage copy and sections;
- banners and promotions;
- FAQs;
- SEO fields;
- generic pages;
- navigation and footer;
- images/media;
- page-builder components;
- editorial roles and publishing workflow.

### Explicitly not CMS-owned

- live stock;
- live prices;
- fitment verdicts;
- vehicle identity/K-Type resolution;
- orders and payment truth;
- supplier synchronization;
- Primavera synchronization;
- shipping labels/tracking truth.

### What works today

- **VERIFIED:** Strapi runs against PostgreSQL.
- **VERIFIED:** homepage hero can be edited as draft, published, and refreshed into the storefront.
- **VERIFIED:** product editorial content can be edited/published and appears on product pages.
- **VERIFIED:** public content endpoints use allowlisted population and remove admin/audit credentials.
- **VERIFIED:** draft content does not leak into public output.
- **MODELLED, NOT RENDERED:** generic pages, navigation, footer, FAQs, SEO, banners, and promotions.
- **NOT BUILT:** production editorial permissions, client users, media workflow, full page routing, and deployment configuration.

---

## 12. Current prototype

### Real implemented functionality

- Next.js Portuguese storefront shell.
- FastAPI API and typed schemas.
- provider-independent interfaces and environment-based provider selection.
- plate and VIN normalization.
- free vPIC as the first VIN stage.
- zero/one/multiple/partial candidate states.
- generic multiple-candidate confirmation UI.
- manual make → model → generation → year → engine selector using clearly marked demo data.
- saved vehicle garage and deduplication.
- catalogue and product routes.
- OEM/reference/SKU/EAN search mechanics.
- cart quantity/update/remove behavior.
- server-side order-price calculation.
- authenticated customer/admin boundaries through a Next.js server BFF.
- signed, versioned, eight-hour sessions that fail closed without a strong `SESSION_SECRET`.
- provider status administration view.
- architecture view.
- Strapi homepage/product editorial publish flow.
- automated Python/frontend/session/CMS security regression tests.

### Demo-only functionality/data

- product records and images/visuals;
- stock quantities;
- prices and IVA examples;
- delivery estimates;
- payment step;
- order fulfilment;
- GLS estimates;
- manual vehicle taxonomy;
- canned conflict walkthrough;
- local user/admin credentials;
- local SQLite orders.

### Waiting for provider/client access

- arbitrary Portuguese matrícula result;
- exact EU/PT VIN result beyond vPIC's basic output;
- validated K-Type mapping;
- production catalogue and fitment;
- Primavera data/sync;
- supplier feeds;
- GLS API;
- payment provider;
- final client brand/domain/content.

### Useful routes

- `/` — vehicle discovery and CMS hero.
- `/catalogo` — catalogue/product filtering.
- `/produto/[id]` — product details and editorial merge.
- `/garagem` — saved vehicles.
- `/carrinho` — cart.
- `/checkout` — demo checkout.
- `/admin/providers` — provider evidence/status.
- `/admin/*` — mostly labelled placeholders.
- `/architecture` — system boundaries.

---

## 13. Security and quality work

The prototype was independently red-teamed and revised. Problems were documented rather than hidden.

| Problem discovered | Resolution |
|---|---|
| Public CMS endpoint exposed admin/audit fields including password hash | Explicit populate allowlist and recursive sanitisation; payload regression test added; local editor credential rotated |
| CMS capabilities were overstated | Architecture and demo now distinguish rendered surfaces from modelled-only content |
| Browser bundle contained API credentials | Replaced with server-side Next.js session/BFF boundary |
| Public default session secret allowed forged cookie | Removed every fallback; application refuses to start without strong `SESSION_SECRET` |
| Session lacked enforced expiry/schema version | Signed v1 payload with issued/expiry timestamps and eight-hour server validation |
| Garage created duplicate saved vehicles | Upsert/deduplication added for VIN/plate and manual identity fields |
| Auto Ways was falsely attributed to research data | Removed; research result attributed only to Autofrance and excluded from customer flow |
| Provider statuses implied untested services were live | Split into tested, documented, research-only, waiting, and not-configured states |
| Static demo fitment labels implied compatibility | All demo products now require compatibility confirmation |
| Real-looking but wrong OE references appeared in demo | Replaced with explicit `SAMPLE-*` references |
| Client-submitted item price could affect order total | Server resolves product IDs and computes authoritative price |
| One provider returning several variants looked like source conflict | `MULTIPLE` separated from cross-provider `CONFLICT` |
| Unvalidated detailed result could show `EXACT_VARIANT` | Display precision capped at `ENGINE` without validated evidence |

Latest recorded checks:

- Python `pytest`: 79 passed.
- Repository `unittest`: 62 passed.
- Frontend/session tests: 11 passed.
- Next.js production build: passed.
- CMS payload/publish regression: passed.
- Missing/forged/tampered/expired session behavior: passed.

### Demo verdict

`collaboration/READY_TO_SHOW_DAVID` exists. The exact verdict is:

> **READY TO SHOW DAVID**, provided it is described as an implementation and safety demo with no live Portuguese plate provider, no live fitment source, and demo products/prices/stock/payment/shipping.

One non-blocking label improvement remains before connecting a live provider: replace `REAL_TESTED` for a live-but-unvalidated provider response with a clearer label such as `LIVE_UNVALIDATED`. vPIC's tested label is accurate.

---

## 14. What does not work yet

- Arbitrary Portuguese matrícula lookup: no real provider credential is connected.
- Exact Portuguese/EU VIN identity: vPIC is insufficient; richer providers remain untested or research-only.
- Production fitment: no licensed authoritative source is connected.
- Production catalogue: only demo data exists.
- Primavera: no live inspection or integration.
- Supplier feeds: none integrated.
- GLS: no live credentials, quotes, labels, or tracking.
- Payments: demo only; provider not selected.
- Customer identity: prototype session/auth only, not a production account system.
- CMS: only homepage hero and product editorial are rendered.
- Admin: provider status works; other modules are placeholders.
- Search: demo catalogue mechanics, not production search infrastructure.
- Provider caching: disabled/avoided where rights are unknown.
- GDPR/retention: policy and DPA requirements are not final.
- Marketing/distribution: strategy and commercial engagement remain separate.
- TecDoc: no direct or reseller contract/access is available.

---

## 15. Phase 1 — launch foundation

### Commercial context

David is considering a working model of approximately **€10,000 per month for three months**. This is not agreed pricing and must not appear as a final quote until scope, dependencies, staffing, exclusions, and third-party costs are confirmed.

### Goal

A Portuguese customer can identify or confirm their vehicle, find an appropriate product in the launch catalogue, understand compatibility status, and complete an order without staff manually performing the entire journey.

### Workstream 1 — product and UX

- final PeçasAuto/new-brand design implementation once name is chosen;
- Portuguese-first copy and Portugal terminology;
- responsive/mobile-first storefront;
- homepage and navigation;
- categories and brand discovery;
- vehicle-first search prominence;
- product listing and detail experience;
- vehicle garage;
- customer-support entry points;
- accessible loading/error/empty states;
- honest demo/provider/verification labelling removed or adapted for production.

### Workstream 2 — vehicle identification

- Portuguese matrícula route;
- VIN route;
- manual vehicle selector;
- one/multiple/partial/no-result handling;
- customer confirmation and audit trail;
- provider adapters and fallback policy;
- K-Type/catalogue-vehicle bridge;
- per-field provenance and precision;
- timeout, rate-limit, malformed-response, and provider-unavailable behavior;
- controlled storage/caching only where rights allow;
- benchmark with client-supplied verified PT vehicles.

### Workstream 3 — catalogue

- filters, brake pads, and brake discs;
- agreed initial brands, up to the proposed 83 only where data exists;
- product, brand, category, manufacturer reference, EAN, OE references;
- technical attributes and restrictions;
- product images under valid rights;
- alternative brands/products;
- catalogue import and validation pipeline;
- reference/OE/SKU/EAN search;
- catalogue vehicle mapping.

### Workstream 4 — fitment safety

- `MATCH`, `NO_MATCH`, `UNKNOWN`, `CONFLICT` internal verdicts;
- customer states such as compatible, confirmation required, and verification required;
- never infer fitment from text, OE search, or vehicle identity alone;
- restrictions and exception handling;
- manual staff review queue;
- logging of source/date/verification status;
- false-confident-result monitoring;
- no positive compatibility until trusted licensed evidence exists.

### Workstream 5 — CMS

- production Strapi deployment;
- homepage/page components;
- product editorial content;
- brands/categories;
- SEO fields;
- banners/promotions;
- navigation/footer;
- FAQs and support pages;
- media management;
- editorial roles, draft/publish, and audit expectations;
- explicit boundary preventing CMS from controlling operational truth.

### Workstream 6 — commerce

- customer account and session/identity solution;
- addresses;
- cart and quantity rules;
- server-side price and stock verification;
- checkout;
- IVA-inclusive presentation and invoice-related requirements;
- selected Portuguese payment methods/provider;
- idempotent payment/order flow;
- order confirmation and notifications;
- order history;
- support and cancellation states.

### Workstream 7 — shipping

- GLS credentials and API evaluation;
- shipping methods and prices;
- delivery estimate rules;
- address/service validation;
- shipment creation/labels;
- tracking architecture;
- failure/retry/manual fallback;
- returns boundary.

### Workstream 8 — admin and operations

- product/catalogue view;
- orders and customers;
- prices and stock view;
- imports with validation/errors;
- provider configuration/status/health;
- vehicle lookup issues;
- ambiguous identity queue;
- fitment review queue;
- audit log;
- operational roles and permissions.

### Workstream 9 — SEO

- server-rendered category, brand, product, and editorial pages;
- Portuguese titles/descriptions/canonical URLs;
- stable slugs and URL structure;
- product/category structured data where accurate;
- XML sitemap and robots rules;
- performance/Core Web Vitals;
- reference/OE search landing strategy without thin/duplicate pages;
- no indexing of demo or unresolved content.

### Workstream 10 — infrastructure

- development, staging, production separation;
- managed PostgreSQL;
- object storage/CDN for permitted media;
- secret management;
- database migrations and backups;
- structured logs and redaction;
- monitoring/error tracking/uptime;
- CI/CD and rollback;
- rate limiting and abuse protection;
- optional job worker/Redis only if justified;
- security headers, dependency updates, and admin audit.

### Workstream 11 — testing

- normalization/unit tests;
- stored provider-response contract tests;
- live provider smoke command;
- Portuguese vehicle benchmark;
- catalogue import validation;
- fitment safety/regression;
- cart/checkout/order pricing;
- payment and GLS webhook/idempotency;
- permissions/session/security;
- CMS public-payload and draft/publish;
- responsive/browser/accessibility;
- load/failure testing;
- launch runbook and rollback rehearsal.

### Phase 1 acceptance criteria

1. A customer can use matrícula, VIN, manual selection, or reference search.
2. Ambiguous vehicles require confirmation and never silently become exact.
3. Saved vehicle context persists with source and verification status.
4. Launch products and content come from licensed/client-approved sources.
5. Positive compatibility appears only from the agreed authoritative fitment path.
6. Live server-side stock and price are checked before order confirmation, or any manual boundary is explicit.
7. Payment and GLS flows work in staging and production with idempotency/retry behavior.
8. Client staff can manage the agreed editorial/catalogue surfaces.
9. Security, logging, backup, monitoring, privacy, and operational runbooks are reviewed.
10. A launch decision is supported by a Portuguese benchmark and signed client acceptance.

### Phase 1 dependencies

- final brand/domain;
- production vehicle identity provider or agreed manual fallback;
- licensed catalogue/fitment route;
- initial product/brand data;
- payment provider onboarding;
- GLS access;
- operational rules and support ownership;
- client feedback and content;
- legal/privacy decisions;
- decision on Primavera depth at launch.

### Phase 1 risks

- provider access delays;
- catalogue/licensing terms;
- wrong-part risk;
- 83-brand scope expanding data work;
- CMS/catalogue ownership confusion;
- payment/GLS onboarding;
- client-content delay;
- attempting deep ERP/supplier automation inside launch scope.

### Client inputs required for Phase 1

- brand name, domain, identity assets, and legal company details;
- launch categories/brands/SKUs;
- product exports, prices, stock, images, technical data, and rights;
- 10–20 verified Portuguese vehicle cases initially;
- partslink24/manual output for disputed cases;
- provider/TecDoc quotes and access;
- GLS and payment account details;
- support hours, shipping, returns, pricing, and fulfilment policies;
- named client decision makers and content owners.

---

## 16. Phase 2 — operations and automation

### Goal

Integrate PeçasAuto into Fahad's actual operation so online sales do not create duplicated manual work.

### Primavera/Cegid

- inspect version, modules, hosting, database, licensing, and API;
- define system of record by entity;
- stock synchronization by warehouse;
- retail and professional price-list synchronization;
- customer synchronization;
- order creation and state updates;
- invoice/credit-note workflow;
- refunds/returns interaction;
- retry, reconciliation, idempotency, and audit;
- manual fallback for unsupported ERP operations.

### Supplier integrations

- prioritised supplier list;
- API/CSV/XML/Excel/SFTP discovery;
- SKU/brand/EAN/OE normalization;
- supplier stock, cost, and lead-time imports;
- supplier offer ranking;
- catalogue/media/specification ingestion where licensed;
- stale-feed detection and import error handling;
- virtual stock with truthful delivery promises;
- supplier data-quality dashboard.

### B2B/workshop experience

- company/VAT account;
- staff users and permissions;
- workshop/professional price lists;
- customer-specific discounts;
- credit terms subject to ERP rules;
- saved vehicles/fleets;
- fast OE search and reorder;
- order/invoice history;
- quote request and account-manager workflow;
- bulk ordering.

### Returns and operations

- RMA/returns workflow;
- reason codes including fitment error;
- warehouse/customer-service states;
- supplier return linkage;
- compatibility dispute evidence;
- refund/credit-note synchronization;
- performance and return-rate analytics.

### Catalogue quality and fitment operations

- missing-image/reference/attribute queues;
- source conflicts and stale data;
- manual vehicle/product verification;
- provider disagreement review;
- correction provenance;
- high-return SKU review;
- supplier normalization tools;
- import schedules and exception reporting.

### Phase 2 acceptance criteria

1. Agreed stock/prices/orders/customer records synchronize without uncontrolled duplication.
2. Failed syncs are visible, retryable, and reconcilable.
3. At least the priority supplier feeds update stock/prices/catalogue on an agreed schedule.
4. Professional accounts receive correct authorised pricing and permissions.
5. Returns and compatibility exceptions are operationally traceable.
6. Staff can identify data-quality and integration failures without engineering database access.

### Phase 2 dependencies

- Primavera technical access and vendor/licence permission;
- real workflow demonstration and sample exports;
- supplier cooperation and contracts;
- stable product identifiers;
- final B2B pricing/credit rules;
- operations ownership and staff training.

### Phase 2 risks

- old/custom Primavera implementation;
- undocumented business rules;
- inconsistent supplier feeds;
- stock timing and overselling;
- customer-specific pricing complexity;
- invoice/legal requirements;
- automation built before current manual process is understood.

---

## 17. Phase 3 — scale

### Goal

Evolve from a focused online shop into scalable Portuguese automotive-commerce infrastructure.

### Scope candidates

- expand categories and brands;
- add suppliers and larger virtual catalogue;
- supplier selection by cost, stock, delivery, quality, and contract;
- purchase-order automation with approval rules;
- multiple warehouses and stock allocation;
- Portugal-wide logistics optimisation;
- advanced B2B/workshop/fleet tooling;
- saved-fleet servicing and reorder workflows;
- customer retention, reminders, email/SMS, and lifecycle automation;
- native applications only if justified by customer behaviour;
- stronger search, synonyms, typo tolerance, reference search, and ranking;
- responsible recommendations and alternatives;
- analytics for search gaps, conversion, returns, margin, supplier performance, and fitment failures;
- marketing integrations kept commercially separate from core development;
- Spain only after Portugal demand and operating model are proven;
- provider redundancy and failover;
- legally permitted internal accumulation of verified corrections/mappings;
- reduced single-provider dependency without unauthorised copying;
- scaling, queues, cache strategy, CDN, observability, disaster recovery, and security maturity.

### Phase 3 acceptance criteria

1. Catalogue, search, orders, and integrations meet agreed production volumes and availability.
2. Multi-supplier/warehouse allocation remains auditable and margin-aware.
3. B2B and fleet workflows are operationally adopted.
4. Provider failure does not require rewriting customer applications.
5. Internal verified data has explicit provenance and legal storage rights.
6. Expansion decisions are based on measured Portuguese demand and unit economics.

---

## 18. Three-month delivery model

The proposed three-month engagement is not the same as completing all three strategic phases.

### Illustrative Month 1 — foundation, data, storefront

- final scope and dependency register;
- environments, CI/CD, security baseline;
- production data model and PostgreSQL migrations;
- brand/storefront design implementation;
- CMS deployment and priority editorial surfaces;
- provider credential integration and real-response tests;
- vehicle/manual/confirmation/garage flows;
- initial catalogue import pipeline and data audit.

### Illustrative Month 2 — commerce, CMS, integrations, operations

- product listing/detail/search;
- fitment provider and safety states if licence is available;
- accounts, cart, checkout, payment sandbox;
- GLS sandbox/contract integration;
- admin/import/review workflows;
- CMS pages/navigation/SEO completion;
- initial Primavera investigation and controlled order handoff;
- client review cycles and mobile QA.

### Illustrative Month 3 — hardening and launch readiness

- production payment/GLS activation;
- provider/fitment benchmark and defect resolution;
- security, performance, accessibility, SEO, analytics;
- monitoring, backups, alerts, operational runbooks;
- staff training and content/catalogue completion;
- selected ERP/supplier work only where access and complexity permit;
- staged launch, observation, rollback plan, and acceptance.

### Reality check

- Provider contracting, TecDoc onboarding, supplier feeds, and ERP complexity can extend beyond three months.
- A full Phase 2 and Phase 3 are not automatically included in the initial engagement.
- If all Phase 1 features plus deep Primavera and multiple supplier integrations are required, scope/time must expand.
- The working engineering estimate in `reports/PHASE1_DEVELOPMENT_PLAN.md` is 73–125 engineering days before contingency for the broad Phase 1 list. Two engineers can parallelise work, but external dependencies remain on the critical path.
- Any fixed launch date must include explicit assumptions and client-response deadlines.

---

## 19. Known client dependencies

We need Fahad/Ayaz to provide or demonstrate:

- partslink24 account/package and permitted screenshots/exports;
- written API, integration, display, caching, and storage rights for partslink24 if programmatic use is desired;
- Primavera/Cegid version, modules, API/licensing, hosting, and database arrangement;
- product, stock, price, customer, order, and invoice examples/exports;
- current vehicle-identification software name/version and live workflow;
- current TecDoc/reseller proposal and contract scope;
- final 83-brand list and initial SKU estimate;
- supplier list and sample API/CSV/XML/Excel/SFTP feeds;
- supplier data rights, identifiers, stock, prices, images, specs, OE references, and fitment fields;
- GLS contract, account, credentials, services, labels, rates, and tracking flow;
- payment preferences and legal merchant onboarding;
- new brand/legal company name, registration number, VAT/billing information, address, and contacts;
- domain and brand decision;
- launch geography and delivery promises;
- product/pricing/return/support policies;
- operational users and responsibilities;
- support owner and compatibility-dispute owner;
- 10–20 verified Portuguese vehicles for first benchmark, expanding to 100–500 before strong production trust.

Enterprise/fleet/data-provider accounts may require the legal company name, company registration number, business address, intended use, volume, and billing details. Access is blocked where the new entity/details are not available; nobody should invent these during onboarding.

---

## 20. Open decisions for David

- [ ] Do we agree on Next.js + FastAPI + Strapi + PostgreSQL as the production direction?
- [ ] Does Strapi remain separate, or should editorial admin be simplified for Phase 1?
- [ ] What exact Phase 1 fits inside the first three months?
- [ ] Is the commercial model fixed scope, monthly engineering engagement, or staged milestones?
- [ ] Is approximately €10,000/month × three months the framing David wants to explore?
- [ ] What staffing allocation is assumed for Komail and David?
- [ ] What is the launch definition: soft launch, public paid orders, or operational integration?
- [ ] Which vehicle lookup method is mandatory on launch day?
- [ ] Can matrícula launch with partial identity plus customer confirmation if no K-Type provider is ready?
- [ ] Which provider benchmark threshold is acceptable?
- [ ] Which source is authoritative for fitment?
- [ ] Are TecDoc/API licences expressly client-paid and excluded from development fees?
- [ ] Is TecDoc direct, reseller, or TIPS4Y the preferred negotiation path?
- [ ] Is partslink24 manual validation enough as a launch support fallback?
- [ ] Is Primavera included in the first three months as discovery/manual handoff, or deep automation?
- [ ] Are supplier feeds in the first engagement? If yes, how many and which formats?
- [ ] Which payment methods/providers are required?
- [ ] What GLS scope is mandatory at launch?
- [ ] What CMS surfaces are required at launch?
- [ ] What admin/operations features are genuinely needed versus placeholders?
- [ ] What warranty/defect period follows launch?
- [ ] What maintenance, incident response, and support model follows launch?
- [ ] Is marketing/growth explicitly a separate agreement?
- [ ] Who owns product/copy/catalogue quality on the client side?
- [ ] What assumptions trigger change control or timeline movement?

---

## 21. Commercial boundaries

Development/engineering fees should be separate from:

- TecAlliance/TecDoc licences;
- matrícula/VIN API calls and subscriptions;
- partslink24 or other catalogue subscriptions;
- supplier API/data fees;
- Primavera/Cegid licences, vendor services, and connector costs;
- GLS contract, shipment, label, and related fees;
- payment processing and chargeback fees;
- hosting, database, object storage, CDN, monitoring, email, and SMS;
- domain and email services;
- third-party SaaS;
- app-store fees if native applications are later approved;
- marketing media spend, SEO content production, ads, and ongoing acquisition management.

The proposal must identify:

1. client-paid third-party costs;
2. estimated usage assumptions;
3. exclusions;
4. change-control triggers;
5. what happens if a provider refuses rights or misses onboarding dates.

Do not absorb unknown recurring data/licence costs into a fixed development price.

---

## 22. What to tell Fahad

Suggested concise narrative:

> We tested the idea of using free vehicle data first. That was worth doing because it lets us reduce paid calls and keep the platform independent. On the real VIN, free vPIC only identified Peugeot; it did not give the exact engine or version needed for safe parts matching.
>
> A separate research source produced a detailed 3008 result and K-Type, while the expected vehicle was supplied as a 5008. That conflict is useful: it proves why we should never trust one detailed-looking result or show a false compatibility tick.
>
> We have therefore changed from “free-only” to “free-first plus licensed fitment.” The customer can use matrícula, VIN, manual selection, or OE reference. When several versions are possible, the customer confirms one. The platform normalizes that vehicle and then uses a licensed catalogue/fitment source to decide which parts fit.
>
> We can continue building the commerce engine before full TecDoc access because the provider layer is replaceable. TecDoc can later supply the strongest catalogue and fitment data without forcing us to rebuild the storefront.
>
> Primavera remains valuable for stock, prices, customers, orders, and invoices. It is not the vehicle-identification system. partslink24 remains valuable for staff/OE validation while we confirm whether any backend integration is legally available.
>
> Before final scope, we need to inspect your Primavera setup, current lookup software, partslink24 package, supplier feeds, TecDoc quote, GLS process, and initial catalogue.

---

## 23. Risks

| Risk | Level | Control |
|---|---|---|
| Wrong vehicle identification | High | Portuguese benchmark, provenance, multiple candidates, user/staff confirmation, second source |
| Wrong fitment / returns | High | Licensed fitment provider, restriction handling, no positive claim from identity alone, review workflow |
| TecDoc access/onboarding time | High | Provider abstraction, free/cheap identity routes, manual fallback, early commercial request |
| Data licensing/cache/storage | High | Written rights register, no unapproved persistence, client-paid licences |
| Supplier data quality | High | Normalization, validation, stale-feed detection, exception dashboard |
| Primavera integration uncertainty | High | Technical inspection before fixed automation scope; phased/manual boundary |
| Scope expansion toward “AUTODOC in v1” | High | Launch categories, written acceptance criteria, phase/change control |
| Client catalogue/content delays | Medium–High | delivery checklist, owners, deadlines, fallback scope |
| Provider false confidence | High | precision caps, independent verification, `FALSE_CONFIDENT_RESULT`, disagreement handling |
| Provider outage/lock-in | Medium | replaceable adapters, fallback cascade, monitoring, later redundancy |
| GDPR/privacy for plate/VIN | High | lawful basis, minimisation, retention, DPA, access controls, redacted logs |
| Payment/shipping onboarding | Medium–High | start early, sandbox, manual fallback, idempotency |
| Performance/search scale | Medium | measured PostgreSQL search first, search index only when justified, caching within rights |
| SEO migration/duplicate content | Medium | stable URLs, canonical policy, server rendering, no index of demo/thin pages |
| Operations not ready for online volume | High | map order-to-delivery/returns, training, staged launch, operational owner |
| Security regression | High | CI tests, secrets manager, dependency management, least privilege, audits |

---

## 24. Repository map

| Path | Purpose / what David's agent should inspect |
|---|---|
| `DAVID.md` | This handoff; current decision/evidence index. |
| `README.md` | Local installation, run commands, demo routes, tests. |
| `apps/web/` | Next.js/React/TypeScript storefront, BFF session routes, garage/catalogue/cart/checkout/admin/architecture UI. |
| `apps/api/` | FastAPI/SQLAlchemy application API, schemas, auth, provider status, demo catalogue/orders. |
| `apps/cms/` | Strapi schemas, editorial public boundary, content-flow/security checks. |
| `app/` | Provider-independent domain models, normalization, orchestration, fitment safety, bridge, garage/ERP contracts, benchmark logic. |
| `providers/` | Replaceable adapters for vPIC, Auto Ways, Matricula.co.pt, TIPS4Y, TelePeças, TecAlliance, partslink24 boundary, Primavera stub, mocks. |
| `tools/test_vehicle.py` | One-command arbitrary VIN/plate test by provider or cascade. |
| `tools/test_provider.py` | Lower-level provider test and optional raw-evidence persistence. |
| `tests/` and `apps/api/tests/` | Provider, normalization, cascade, bridge, fitment, garage/ERP, CLI, and API regression tests. |
| `config/providers.example.env` / `.env.example` | Credential names and runtime provider switches; no live secrets. |
| `reports/PEÇASAUTO_DEMO_REVIEW.md` | Independent demo/red-team history and final approval. |
| `collaboration/READY_TO_SHOW_DAVID` | Current demo approval marker and known non-blocking items. |
| `reports/FINAL_PRE_TECDOC_DATA_STRATEGY.md` | Evidence-based provider/data conclusion. |
| `reports/PROVIDER_COMMERCIAL_COMPARISON.md` | Provider price/access comparison; check dates before proposal. |
| `reports/PHASE1_DEVELOPMENT_PLAN.md` | Architecture, modules, indicative engineering-day ranges, dependencies. |
| `reports/VEHICLE_LOOKUP_IMPLEMENTATION_STATUS.md` | Current arbitrary plate/VIN behavior and credential-ready integration. |
| `reports/client_ground_truth_research.md` | Field-by-field disputed client vehicle evidence. |
| `docs/vehicle-to-catalogue-bridge.md` | K-Type/catalogue mapping problem and safe rules. |
| `docs/provider_landscape.md` | Provider shortlist and evidence status. |
| `docs/data_rights_register.md` | Rights/caching/storage assumptions. |
| `docs/partslink24_role.md` | Manual/OE/programmatic boundaries. |
| `docs/primavera_integration_contract.md` | Intended ERP contract and non-responsibilities. |
| `reports/raw_evidence/` | Original saved provider/research payloads; do not reinterpret without source/status. |
| `reports/DAVID_DEMO_SCRIPT.md` | Five-minute walkthrough. |
| `reports/DAVID_QA_PREP.md` | Likely questions and concise technical answers; some counts/statements may be older than this handoff. |
| `collaboration/` | Historical review/decision trail. Newer approval/evidence files supersede stale drafts. |

### Known stale/inconsistent historical documents

- `collaboration/JOINT_VALIDATION_DRAFT.md` claims a live Auto Ways VIN result. The latest evidence register and final demo review say no verified Auto Ways call/raw evidence exists. Treat that claim as stale and **do not repeat it**.
- Earlier demo reviews contain issues that were later fixed. Read the final verdict at the top of `reports/PEÇASAUTO_DEMO_REVIEW.md` first.
- Some older test counts in QA/report files predate the final security pass. Current recorded counts are in `collaboration/SESSION_SECURITY_FIXED`.
- Provider public pricing must always be rechecked at proposal time.

---

## 25. Current status checklist

| Component | Status | Evidence / next move |
|---|---|---|
| Product/business concept | **DONE** | Separate Portugal-first brand and phased platform direction established |
| Provider-independent architecture | **DONE** | Interfaces, cascade, config, normalization, bridge/fitment boundaries implemented |
| Next.js customer prototype | **DONE** | Clickable end-to-end demo |
| FastAPI prototype | **DONE** | Vehicle, garage, catalogue, order, admin/provider endpoints |
| Strapi prototype | **DONE** | Homepage/product editorial live; broader models exist |
| Demo security remediation | **DONE** | Final tests and approval marker |
| Portuguese plate production lookup | **WAITING FOR PROVIDER** | Need authorised key and real response |
| VIN free stage | **DONE** | vPIC works but is only BASIC on client case |
| Rich EU/PT VIN provider | **WAITING FOR PROVIDER** | Auto Ways/Vincario/One Auto/TecAlliance benchmark |
| Manual vehicle fallback | **DONE (DEMO DATA)** | Needs licensed/production taxonomy |
| Multiple candidate flow | **DONE** | One-provider variants vs provider conflict separated |
| Client 3008/5008 resolution | **WAITING FOR CLIENT** | partslink24/registration/plate-provider evidence |
| Vehicle benchmark | **IN PROGRESS** | Architecture ready; verified Portuguese sample is too small |
| K-Type bridge | **IN PROGRESS** | Contract and safety logic exist; production mapping unverified |
| Production fitment | **WAITING FOR PROVIDER** | Licensed source required |
| Production catalogue | **WAITING FOR CLIENT/PROVIDER** | Data, rights, 83 brands, images, SKUs |
| Product/reference search | **DONE (DEMO)** | Production index/data not connected |
| Garage | **DONE (PROTOTYPE)** | Production accounts/privacy/migrations remain |
| Cart/order totals | **DONE (PROTOTYPE)** | Server pricing verified; no live stock/payment |
| Payment | **NOT STARTED** | Provider/client decision required |
| GLS | **NOT STARTED** | Credentials/workflow required |
| Primavera discovery | **WAITING FOR CLIENT** | Confirmed system, exact setup unknown |
| Primavera integration | **NOT STARTED** | After discovery |
| Supplier feeds | **NOT STARTED** | Samples/rights/priorities required |
| B2B/workshop portal | **NOT STARTED** | Phase 2 |
| Returns/RMA | **NOT STARTED** | Phase 2 |
| Production hosting/CI/CD | **NOT STARTED** | Local prototype only |
| GDPR/data retention/DPA | **IN PROGRESS** | Safety defaults exist; legal/business policy needed |
| Final brand/domain | **WAITING FOR CLIENT** | Required for launch implementation |
| TecAlliance/direct quote | **WAITING FOR PROVIDER** | Request minimum Portugal scope |
| Existing reseller quote | **WAITING FOR CLIENT** | Fahad must supply document/scope |
| Final commercial proposal | **NOT STARTED** | David/Komail decisions and dependencies first |

---

## 26. Friday meeting preparation

### David should review before Friday

- [ ] This entire `DAVID.md`.
- [ ] `reports/DAVID_DEMO_SCRIPT.md` and run the five-minute demo.
- [ ] `reports/PEÇASAUTO_DEMO_REVIEW.md` final verdict and non-blocking items.
- [ ] `reports/PHASE1_DEVELOPMENT_PLAN.md` engineering-day ranges.
- [ ] `reports/PROVIDER_COMMERCIAL_COMPARISON.md` plus the updated prices in this file.
- [ ] `reports/client_ground_truth_research.md` and the 3008/5008 distinction.
- [ ] Decide proposed engagement model, staffing, exclusions, and launch definition.
- [ ] Decide how much Primavera/supplier work can honestly fit in the first three months.

### Komail should obtain before Friday where possible

- [ ] Fahad's TecDoc/reseller quote and scope.
- [ ] partslink24 screenshot/output for the client VIN or registration document.
- [ ] Primavera version/modules/API details or meeting access.
- [ ] current vehicle-identification software name and demo.
- [ ] top supplier list and one representative feed.
- [ ] final/priority launch brands and approximate SKU volume.
- [ ] GLS account/API details.
- [ ] payment preferences.
- [ ] company/legal details or clarity on whether the new entity exists.
- [ ] client view on €10k/month × three months versus fixed scope—without presenting it as agreed.

### What to show Fahad

- [ ] Four search routes.
- [ ] One/multiple/partial/no-result states.
- [ ] Manual confirmation and saved garage.
- [ ] Catalogue/product/cart/checkout flow clearly labelled demo.
- [ ] Provider status page.
- [ ] Architecture page showing provider independence.
- [ ] Strapi edit/publish for the surfaces that actually render.
- [ ] Why fitment is separate from identity.
- [ ] Phase 1 versus later automation.

### What not to promise

- [ ] 100% vehicle or fitment accuracy.
- [ ] A free TecDoc replacement.
- [ ] Automatic compatibility before licensed data is connected and benchmarked.
- [ ] Full AUTODOC-scale catalogue in version 1.
- [ ] Deep Primavera integration before inspection.
- [ ] Supplier APIs/stock before suppliers provide access and usable data.
- [ ] Fixed launch date before provider, payment, GLS, and catalogue dependencies are confirmed.
- [ ] Native apps or Spain at launch.
- [ ] Marketing outcomes as part of the engineering scope.
- [ ] Rights to store/cache/display third-party data without written terms.

### Questions to ask Fahad

1. Can you show one real customer request from matrícula/VIN through part selection, stock, order, invoice, and delivery?
2. What software currently resolves Portuguese plates and VINs?
3. Can you show the disputed vehicle in partslink24 and the registration document?
4. What exact partslink24 package and rights do you have?
5. What is the exact Primavera/Cegid version, modules, hosting, and API availability?
6. What is in the TecDoc/reseller quotation, and may we compare it directly with TecAlliance/TIPS4Y?
7. Which products/brands/SKUs are essential for launch?
8. Own stock only, or supplier stock at launch?
9. Which suppliers can deliver API/CSV/XML/Excel/SFTP data?
10. How are B2C and professional prices determined?
11. Which payment methods are required?
12. How does GLS work today?
13. Who owns catalogue quality, disputed compatibility, support, fulfilment, and returns?
14. What exactly counts as a successful first three months?
15. Is the new legal entity ready for provider/payment/domain contracts?

### Commercial decisions to obtain internally

- [ ] Three-month monthly engagement versus fixed scope/milestones.
- [ ] Working commercial level and staffing assumptions.
- [ ] Exact Phase 1 inclusions/exclusions.
- [ ] Third-party costs paid directly by client.
- [ ] TecDoc/identity-provider procurement responsibility.
- [ ] Primavera and supplier integration position.
- [ ] Post-launch warranty, support, hosting, and maintenance.
- [ ] Separate marketing/growth agreement.
- [ ] Change-control and client-delay clauses.

---

## Final position

The opportunity is credible because the client already has operational automotive experience, suppliers, stock/premises, partslink24, Primavera/Cegid, and a real understanding of the trade. The software opportunity is larger than a website: it is a controlled orchestration layer across vehicle identity, catalogue/fitment, commerce, inventory, ERP, suppliers, payments, and delivery.

The prototype proves that the customer and architecture flows can be built without locking the frontend to TecDoc or another provider. It does **not** prove that free data is fitment-grade, that a Portuguese plate provider works for the client vehicle, or that production operations are integrated.

The safest position for the proposal is:

> Build the focused commerce foundation first. Use free data where it is reliable, low-cost Portuguese identity services where they pass the benchmark, and licensed premium data where wrong compatibility would cost more than the licence. Automate Primavera and suppliers only after the actual operation is inspected.
