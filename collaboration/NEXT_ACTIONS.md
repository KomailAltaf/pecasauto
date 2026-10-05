# Next Actions

Updated by Claude review round 1 (2026-10-05). Source: `collaboration/CLAUDE_REVIEW.md`.

## Round 2 implementation status

Codex response: `collaboration/REVIEW_RESPONSE.md`.

- Accepted P0/P1 engineering items are implemented and tested.
- P1-6 partslink24 rights requires written human/provider evidence.
- P1-7 Stage-1 benchmark is deferred until 10-20 real vehicles and provider access exist.
- P2 work remains deferred or requires human policy decisions as classified in the response.
- No final provider recommendation has been made.

## P0

### P0-1 Reconcile repo with reality
- **Action:** Find Codex's prior work (other folder/branch/machine) or confirm none exists; copy it into this folder.
- **Why:** Repo contains only scaffolding; `CODEX_STATUS.md` says nothing was started. Nothing reviewable.
- **Owner:** Komail → Codex
- **Evidence needed:** Files in `app/`, `providers/`, `fixtures/`, `benchmarks/`, `tests/`.
- **Done when:** Real code exists here and a review can cite files/commit.

### P0-2 Initialise git baseline
- **Action:** `git init` (local only), commit baseline.
- **Why:** No commit to review; no history.
- **Owner:** Codex (Komail approves; no push)
- **Evidence needed:** `git log` shows a commit.
- **Done when:** Review can state "commit reviewed: <hash>".

### P0-3 Precision levels + hard gates
- **Action:** Implement BASIC / MODEL / ENGINE / EXACT_VARIANT, derived from populated evidence fields, not provider self-confidence. Per-part-category minimum precision.
- **Why:** Make/model/year with unknown engine must never read as "95% exact".
- **Owner:** Codex
- **Evidence needed:** Unit tests: MODEL-only result cannot become fitment-eligible for engine-dependent parts.
- **Done when:** Tests pass and a single % score never drives a fitment verdict.

### P0-4 Fitment verdict model
- **Action:** Source verdicts MATCH/NO_MATCH/UNKNOWN/CONFLICT → customer states COMPATIBLE/CONFIRM_COMPATIBILITY/UNKNOWN/NOT_COMPATIBLE. COMPATIBLE needs ENGINE+ identity AND licensed catalogue MATCH AND no NO_MATCH.
- **Why:** Prevent a low-confidence source producing "Compatible ✓"; disagreement must not average positive.
- **Owner:** Codex
- **Evidence needed:** Tests: A=MATCH,B=NO_MATCH → CONFLICT; free-VIN-only → never COMPATIBLE.
- **Done when:** Tests pass.

### P0-5 No mandatory VIN checksum for EU VINs
- **Action:** Make checksum a non-blocking, region-aware signal.
- **Why:** Client VIN `VF3MCYHZUPS034433` fails the NA check digit (computed 3, pos 9 = U) yet is a normal EU VIN.
- **Owner:** Codex
- **Evidence needed:** Test using that VIN is accepted.
- **Done when:** Test passes.

### P0-6 Ground-truth fixtures with `truth_class`
- **Action:** Create `fixtures/vehicle_ground_truth.csv` with CLIENT_PROVIDED / INDEPENDENTLY_VERIFIED / SYNTHETIC; seed with CG-17-GC / VF3MCYHZUPS034433 as CLIENT_PROVIDED.
- **Why:** Synthetic data must never inflate accuracy.
- **Owner:** Codex, Komail supplies real vehicles
- **Evidence needed:** Test that fails if a SYNTHETIC row reaches metrics.
- **Done when:** Test passes.

### P0-7 Label test catalogue as search-mechanics only
- **Action:** Any demo catalogue is tagged non-fitment; no UI wording implying "fits your car".
- **Why:** Search mechanics ≠ fitment.
- **Owner:** Codex + David
- **Evidence needed:** Visible label in data and UI.
- **Done when:** Review finds no fitment-implying copy tied to mock data.

### P0-8 Data-rights register
- **Action:** `docs/data_rights_register.md`: per source code licence, data licence, commercial use, caching/storage, automated access, attribution, evidence, date.
- **Why:** Open-source code ≠ reusable data; caching rights unknown.
- **Owner:** Komail (with David)
- **Evidence needed:** Written ToS/contract links per source.
- **Done when:** Every candidate source has a row; unknowns marked UNKNOWN.

## P1

### P1-1 Canonical vehicle model
- **Action:** Fields per review §14 incl. per-field provenance, nullable fields, first-registration vs model year, engine code, kW/hp, provider IDs map, raw payload ref.
- **Why:** Avoid fake normalisation; keep provenance.
- **Owner:** Codex
- **Evidence needed:** Schema + tests with missing fields staying null.
- **Done when:** Schema reviewed by Claude round 2.

### P1-2 Provider interfaces
- **Action:** `VehicleIdentityProvider`, `CatalogueProvider`, `FitmentProvider`, plus separate Inventory/Pricing boundary.
- **Why:** TecDoc must plug in without customer-facing changes.
- **Owner:** Codex
- **Evidence needed:** A fake TecDoc-like provider swapped in by config in a test.
- **Done when:** Swap works with no customer-layer change.

### P1-3 Orchestrator
- **Action:** Configurable order, per-step min_precision/max_cost, error isolation, circuit breaker, provider-scoped cache.
- **Why:** One provider must not poison results or cache.
- **Owner:** Codex
- **Evidence needed:** Tests for timeout/401/429/malformed isolation.
- **Done when:** Tests pass.

### P1-4 PT plate normalisation + "ask one more field"
- **Action:** Normalise CG-17-GC / CG17GC / lowercase; handle all PT formats; partial result → request one discriminator.
- **Why:** Never guess engine from a generic model.
- **Owner:** Codex
- **Evidence needed:** Tests incl. partial "Peugeot 5008" case.
- **Done when:** Tests pass.

### P1-5 Cost model
- **Action:** 1k/10k/50k/100k scenarios, cost per successful / engine-level / exact identification, cache-allowed vs forbidden.
- **Why:** Cost must be gated by accuracy.
- **Owner:** Codex, Komail supplies provider pricing
- **Evidence needed:** Provider price sheets.
- **Done when:** Report generated from real prices, unknowns flagged.

### P1-6 partslink24 rights
- **Action:** Get written answers on package, VIN depth, OE search, API, export, ecommerce/programmatic/caching rights.
- **Why:** Manual use ≠ backend integration.
- **Owner:** Komail ↔ Fahad
- **Evidence needed:** Email/contract from partslink24.
- **Done when:** §9 questions all answered or marked refused.

### P1-7 Stage-1 benchmark
- **Action:** 10–20 real vehicles from Fahad's business; run at least one VIN route and one plate route; store sanitised raw responses.
- **Why:** First real evidence; still only a smoke test.
- **Owner:** Komail + Fahad, Codex runs
- **Evidence needed:** Ground-truth CSV + raw responses + report with n.
- **Done when:** Report shows per-provider precision-level accuracy and false-confident count.

## P2

### P2-1 Statistics
- **Action:** Wilson intervals, precision-vs-cost curves.
- **Why:** "5/5" is not 100%.
- **Owner:** Codex
- **Evidence needed:** Report output.
- **Done when:** Reports include n and intervals.

### P2-2 Edge-case fixture pack
- **Action:** Fixtures for multi-engine, same displacement/different power, facelift, manual/auto, body, LCV, LHD/RHD, plausible-but-wrong provider answers.
- **Why:** Worst failure is wrong-but-confident.
- **Owner:** Codex
- **Evidence needed:** Fixtures + tests.
- **Done when:** Each edge case has a passing test.

### P2-3 Part-category eligibility policy
- **Action:** Table of minimum precision per category.
- **Why:** Brakes need ENGINE+; wipers may not.
- **Owner:** Komail + Fahad + Codex
- **Evidence needed:** Signed-off table.
- **Done when:** Policy loaded from config.

### P2-4 GDPR handling
- **Action:** Retention/redaction for plates, VINs, raw payloads.
- **Why:** Personal-data-adjacent.
- **Owner:** Komail
- **Evidence needed:** Written policy.
- **Done when:** Implemented in storage layer.

### P2-5 Stage 2/3 benchmark plan
- **Action:** 100+ then 100–500 mixed European vehicles.
- **Why:** Needed before production trust.
- **Owner:** Komail + Fahad
- **Evidence needed:** Vehicle list.
- **Done when:** Stage 2 executed.

---

## Claude round 3 additions (2026-10-05) — retests / requests for Codex

### P0-R1 PT-only scope fields
- **Action:** add `country` and `portuguese_market_verified` to `fixtures/vehicle_ground_truth.csv`; only `country=PT AND portuguese_market_verified=true` counts toward production score; synthetic/foreign rows debug-only. Mark client_001 `portuguese_market_verified=false` until the registration certificate / partslink24 check exists.
- **Why:** client_001 `model_year=2023` is only vPIC's pos-10 guess; first-registration date unknown.
- **Owner:** Codex. **Evidence:** test failing if non-PT or unverified rows reach metrics. **Done when:** passes.

### P0-R2 Real adapters from real responses only
- **Action:** once Komail saves sandbox/test JSON from Openapi `PT-car`, Matricula.co.pt, Vincario into `reports/claude_raw_evidence/plate/` and `/vin/`, build adapters against them and re-score. Do not write adapters from vendor marketing pages.
- **Why:** response schemas unpublished (Openapi, AutoNow) or thin (Matricula.co.pt).
- **Done when:** each provider has a precision class on client_001 from a real raw file.

### P1-R3 Bridge model
- **Action:** implement `match_method` ∈ PROVIDER_ID | VIN | ENGINE_CODE | TEXT_MATCH | USER_CONFIRMED + `candidates_count` per `docs/vehicle-to-catalogue-bridge.md`; TEXT_MATCH can never produce COMPATIBLE.
- **Done when:** tests enforce it.

### P1-R4 Customer garage store
- **Action:** store customer-confirmed vehicles (our data) separately from provider cache; provider cache purgeable per source.

### P1-R5 vPIC adapter
- **Action:** error code 8 / empty Model → BASIC; ModelYear from VIN pos 10 must not populate `model_year` for EU VINs. Retest on `reports/raw_evidence/vpic_*.json` (identical to my copy).

### Retest note
Codex raw evidence for vPIC matches mine byte-for-byte (detailed file). 29 tests pass as of this review. No Codex provider evidence beyond vPIC exists yet.

---

## Claude round 4 additions (2026-10-05)

### P0-R6 Fix vPIC adapter leaps
- **Action:** don't derive `model_year` from EU VIN pos-10; don't set `country_of_registration="PT"` from a VIN.
- **Owner:** Codex. **Evidence:** test using `raw_evidence/vpic_public_VF3MCYHZUPS034433.json` expects `model_year=None`, country None. **Done when:** passes.

### P0-R7 Update CODEX_STATUS.md to current reality (37 tests, real-campaign results, access blockers).

### P0-R8 Human access (Komail/Fahad): see `reports/HUMAN_ACTIONS_REQUIRED.md`. Done when raw JSON for CG-17-GC from ≥2 PT plate providers is in `reports/raw_evidence/`.

### P1-R9 Provider schemas: build Autoways, TelePeças, Matricula.co.pt, Openapi adapters **only from real responses**; record whether ktype/engine code/kW were returned and score precision.

### P1-R10 K-Type validation harness: when a provider returns a K-Type, require confirmation by a second source (licensed catalogue/partslink24 manual) before use; log disagreement as CONFLICT.

### P1-R11 Quote tracker: add `docs/quotes.md` (TecAlliance direct, PT partner, Fahad/Luis quote, TelePeças integrator) with date, scope, price, terms.

---

## Claude round 5 additions (2026-10-05): Autofrance / K-Type

### P0-R12 Model-conflict state
- **Action:** add `MODEL_CONFLICT`/`AMBIGUOUS_PLATFORM_SIBLINGS` handling: when provider model ≠ user-stated model, or VDS prefix is known to be shared by sibling models (3008/5008), result is CONFIRM, never RESOLVED/COMPATIBLE. Client_001 must be recorded as `MODEL_CONFLICT`.
- **Owner:** Codex. **Evidence:** test with raw Autofrance payload + stated model 5008 → CONFIRM. **Done when:** passes.

### P0-R13 Autofrance provider policy
- **Action:** register `autofrance_public` in `docs/data_rights_register.md` as `RESEARCH_ONLY / NOT_FOR_PRODUCTION` (retailer storefront backend, no API licence); exclude from production cascades in `app/cascades.py`; no `country_of_registration="PT"` from a VIN.
- **Owner:** Codex.

### P1-R14 K-Type validation
- **Action:** `reports/ktype_crosscheck.csv` is the register; add rows whenever any provider returns a K-Type. A K-Type needs a second *independent* source before use.

### P1-R15 Discriminator data
- **Action:** add `platform_siblings` knowledge (VDS→candidate models) as data we learn from licensed sources, not hardcoded guesses.

### HUMAN: Fahad runs VF3MCYHZUPS034433 in partslink24 (screenshot: model, engine code, build date, OE ref list for e.g. oil filter and a rear brake part) AND sends the original client screenshot / registration certificate. Resolves 3008 vs 5008.

### P0-R16 (Claude round 6) Decide client_001 model
- **Action:** run `CG-17-GC` through ≥1 PT plate provider (HUMAN: see HUMAN_ACTIONS_REQUIRED) AND Fahad's partslink24 VIN lookup. If plate says 5008 and VIN says 3008 → plate/VIN mismatch in the screenshot; get the original screenshot.
- **Owner:** Komail/Fahad (access), Codex (scoring). **Done when:** one licensed/OEM source states the model.

### P1-R17 Decoder-existence guard
- **Action:** any VIN decoder result that is identical for synthetic/non-existent serials must be flagged `NO_EXISTENCE_CHECK` and capped at CONFIRM. Add a regression test using the stored synthetic_debug payloads.

### P0-R18 Sync reports with Round 6 (Codex)
- **Action:** update `client_ground_truth_research.md`, `real_validation_matrix.csv` (Autofrance row: add `independent_ktype_identity=CONFIRMED`, `model_status=LIKELY_3008_DISPUTED`), FINAL §K-Type, `READY_FOR_CLAUDE`; fix the 2 failing tests; reword the stop boundary (see CLAUDE_REVIEW Round 6 Q4).
- **Done when:** unittest green and no report says the K-Type is unverified or that the conflict is unknown.

### P0-R19 Tips4y (Claude round 6)
- **Action:** add Tips4y to `docs/provider_landscape.md`, rights register and matrix as DOCUMENTED (plate→TecDoc Vehicle ID via API, TecDoc WebService). Codex's earlier note about "Tips4y matrícula → VIN/KType" is consistent; I corrected my TLS remark (genuine domain tips4y.pt; chain incomplete).
- **Done when:** listed with status WAITING FOR ACCESS and contact action.

### P0-R20 Autoways adapter schema (Claude round 6)
- **Action:** the vendor's public OpenAPI spec (stored in `reports/claude_raw_evidence/autoways/`) defines the response fields. Write the adapter/mapping against the **spec's example shape** with unit tests on that example only (label `SPEC_EXAMPLE`, not accuracy evidence); keep status NOT_TESTED until a real token response exists. Map: `AWN_k_type`→`provider_vehicle_ids["autoways_ktype"]`, `AWN_code_moteur`→engine_code, `AWN_puissance_KW`→power_kw, `AWN_date_mise_en_circulation`→first_registration (PT plate route only), `AWN_VIN`→vin (from plate route = provenance PLATE_PROVIDER).
- **Done when:** adapter + tests pass; no network call without a token.
