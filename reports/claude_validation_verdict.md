# Claude Validation Verdict — Portuguese Vehicles Only

Date: 2026-10-05. Scope: PT-registered / PT-market vehicles only. Raw evidence: `reports/claude_raw_evidence/`.

**Evidence caveat.** The files this campaign brief told me to read do not exist in the repo: `reports/real_validation_matrix.csv`, `client_vehicle_comparison.html`, `reports/cost_model.md`, `reports/raw_evidence/`, `docs/portugal-official-data-route.md`. `collaboration/CODEX_STATUS.md` says external providers are NOT VERIFIED and test providers are MOCK ONLY. So there is no Codex campaign evidence to verify yet; if it lives elsewhere, send it. Everything below marked TESTED is my own request.

## REAL CLIENT TEST RESULT

Case `client_001`: CG-17-GC / VF3MCYHZUPS034433, client-supplied expectation Peugeot 5008 II 1.5 BlueHDi 130 (CLIENT_PROVIDED, PT).

### VIN
- Providers tested: **public NHTSA vPIC only** (live, `DecodeVinValues` + `DecodeVin`, HTTP 200).
- Result: `Make=PEUGEOT`, `Manufacturer=AUTOMOBILES PEUGEOT`, `ModelYear=2023`, `VehicleType=PASSENGER CAR`. **Empty:** Model, Trim, Series, Body, Displacement, Engine model, HP/kW, Fuel, Drive, Transmission. Errors returned: `1` check digit fails, `8` no detailed data, `400` invalid char `9:U`.
- Best precision: **BASIC** (make). Not even MODEL: no model returned, so "5008" is not identified. ModelYear 2023 is vPIC's pos-10 guess and is unreliable for EU VINs; do not trust it without a second source.
- Verdict for Portuguese vehicles: **NOT FIT FOR PURPOSE** as an identifier (on n=1; the pattern matches how vPIC is built, US-centric, so I'd expect the same on other EU VINs, but that needs more PT VINs to claim).
- Cost: €0. Latency ~0.47 s.
- Failure mode is the good kind: it returned thin data plus explicit error codes, not a wrong confident car. Any adapter must map error 8 to BASIC and never infer a model.
- Offline decoders built on vPIC data (Corgi etc.) share this ceiling, so they add no PT capability.

### MATRÍCULA
- Providers tested: **none.** No free API exists that I could lawfully call. Matricula.co.pt needs a registered account (10 free test searches); TelePeças has no public API docs.
- Not done deliberately: creating an account in Komail's/Fahad's name is outward-facing, so I did not.
- Best precision: **NOT TESTED**. Claimed (unverified) by vendors: brand, model, colour, engine size / variant-engine.
- Cost: €0 spent.

## FREE OPTIONS
- **Viable (narrow role):** local VIN structure parse (length, charset, WMI → make) as a router; vPIC as an optional BASIC cross-check.
- **Insufficient:** vPIC and vPIC-derived offline decoders for model/engine/variant on PT vehicles. Tested on the client VIN: make only.
- **None found** for free PT plate → vehicle. The "Qual veículo é" app is free but consumer-only, no API, undisclosed source, shows brand/model/version and itself warns data may be wrong.

## CHEAP PAID OPTIONS

| Candidate | Evidence | Status |
|---|---|---|
| **Matricula.co.pt** | Vendor page: €0.20/query (min 100-pack, −10% above 1000), 10 free test searches, SOAP/JSON, "20 fields", sourced from government data | **First candidate to test, free tier.** Fields (power kW? engine code? version?) unverified. Terms for caching and commercial resale unseen. |
| **TelePeças** | Plate or VIN, fields year/brand/model/variant, "/api/" listed, no public docs/pricing | Contact for API access and terms; may be best value if Fahad already trades with them. |
| EU VIN aggregators (Zylalabs, Apify VINdata) | Marketplace listings only | Not evaluated; low priority; check whether they actually return engine/variant for PT VINs. |

### Free vs cheap vs premium (cost gate)
| Tier | Result on client_001 | Cost |
|---|---|---|
| FREE (vPIC) | BASIC: make only | €0 |
| CHEAP (Matricula.co.pt) | **UNKNOWN. Not tested.** | free for 10 lookups, then ~€0.20 |
| PREMIUM (TecAlliance / partslink24) | **UNKNOWN. Not tested.** | quote needed |

The paid jump materially improving accuracy is **plausible but not proven.** Do not recommend spending beyond the free 10 lookups until those results exist.

## OFFICIAL PORTUGUESE DATA ROUTE
- IMT/IRN offer a **per-vehicle certificate of technical characteristics** (owner-driven, online) and an inspection report by plate. These are documents for a vehicle's owner, not a lookup API for a shop. Useful only as **independent ground truth for a customer's own car**, e.g. to verify a benchmark vehicle.
- IMT publishes **aggregate** fleet statistics only; I found no per-vehicle open dataset on dados.gov.pt.
- No official B2B plate-lookup route found in this pass. Vendors like Matricula.co.pt claim to use official government sources, so the legitimate path to IMT data appears to be via licensed intermediaries. **Open question for Komail:** ask Fahad's existing plate software vendor what their source is; that is the most likely official-data route.
- Not exhaustively searched: IRN/AT access for accredited businesses. Worth one phone call to IMT.

## PARTSLINK24
- Solves (manual use): VIN/OE lookup and catalogue browsing by Fahad's staff, so it is the best **ground-truth source** for the Stage-1 benchmark.
- Needs written confirmation: package, VIN depth, API availability, export, programmatic access, ecommerce display, caching. Manual use ≠ backend integration.

## FITMENT
**NOT SOLVED.** Even a perfect matrícula result gives vehicle identity only. Bridging needs: **vehicle identity → catalogue vehicle ID (TecDoc ktype / partslink24 vehicle key) → product fitment links.** Missing providers: a licensed catalogue (TecDoc or partslink24 with rights) and a mapping layer from plate-vendor fields (make/model/engine size) to those catalogue IDs. Mapping from fuzzy text to a ktype is itself an ambiguity risk; it must produce `CONFIRM_COMPATIBILITY` when multiple ktypes remain.

## WHAT WE CAN BUILD TODAY
Interfaces, precision/verdict model, PT plate and VIN normalisation, manual selector shell, part-number search (labelled search-only), Primavera boundary, a `MatriculaCoPtProvider` adapter against its documented SOAP/JSON API once the test account exists.

## WHAT REQUIRES TECDOC LATER
Catalogue vehicle IDs, product fitment, OE cross-references at scale, exact-variant selection.

## MONEY NEEDED FOR NEXT TEST
**€0** for the next step: 10 free Matricula.co.pt lookups, which need registration by Komail/Fahad. If those are good, a 100-pack is ≈ €20 (at €0.20, vendor-stated) and needs Komail's approval, though it is within the €5 cap only for ≤25 lookups. Nothing spent so far.

## PROVISIONAL STACK (not validated)
Local VIN parse → Matricula.co.pt and/or TelePeças for plate identity (to be tested) → Fahad's existing source if it is better → catalogue ID mapping → partslink24/TecDoc for fitment (rights pending) → manual selector fallback. vPIC optional BASIC cross-check only.

## WHAT TO TELL FAHAD
1. We tested the free VIN route on your car (CG-17-GC): it only returned "Peugeot". Free VIN data cannot be the customer's identity step.
2. Plate lookup is the realistic route; a candidate costs about €0.20 per lookup (vendor-stated, untested).
3. Please send 10–20 real Portuguese vehicles (plate + VIN + the engine/power as shown in partslink24).
4. Please tell us which plate software you already use and where it gets its data.
5. Please confirm in writing whether your partslink24 subscription allows API or programmatic use.

## NEXT 5 ACTIONS
1. **Komail/Fahad:** register the Matricula.co.pt test account; run `CG-17-GC` plus 9 more PT plates; save raw JSON in `reports/claude_raw_evidence/`.
2. **Komail:** request TelePeças API docs and pricing; ask Fahad which plate source his current software uses.
3. **Fahad:** supply 10–20 PT vehicles with partslink24 screenshots (engine code, kW, first registration).
4. **Codex:** retest items below, add `country` and `portuguese_market_verified` to fixtures; write a Matricula.co.pt adapter against real responses.
5. **Komail:** get partslink24 rights answers in writing.

## DEPTH NOT REACHED (honest limits)
Auto Delta / Oscaro / Mister-Auto comparison was not done: they need a plate or vehicle chosen in their UI, and I did not scrape. It should be done manually once a provider returns a vehicle. Matrícula and TecAlliance were not tested.
