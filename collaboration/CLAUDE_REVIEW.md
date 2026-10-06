# Claude Review — Portugal Auto Validation Lab

Reviewer: Claude (independent senior reviewer / red-team)
Reviewed: 2026-10-05
Round: 1 (for hand-back to Codex)

> **Scope note.** This is a review of what is physically in `~/Downloads/portugal-auto-validation-lab/`. Items that the brief asks me to judge but which do not exist in the repo are marked **DOES NOT EXIST**. Nothing here was tested against a live provider. Where I give requirements (hard gates, models, metrics), they are specifications for Codex round 2, not descriptions of existing code.

---

## 1. EXECUTIVE VERDICT

**The repo contains no implementation, no fixtures, no benchmark, no provider response, no test, and no report.** It is a directory scaffold plus a README and five collaboration stubs.

- Every `.gitkeep` is an empty placeholder (`app/`, `providers/`, `tests/`, `docs/`, `benchmarks/`, `fixtures/`, `reports/`).
- `collaboration/CODEX_STATUS.md` itself says: *"Not started: Provider implementations, Vehicle fixtures, Benchmarks, Reports, Validation interface, Automated tests."*
- `DECISIONS.md` has zero decisions. `NEXT_ACTIONS.md` says "Await Komail's next instruction." `OPEN_QUESTIONS.md` is empty headings.
- The directory is **not a git repository**, so there is no commit to review and no history.

The review brief assumes Codex had built provider adapters, normalization, confidence logic, an orchestrator, a cost model, fitment models and benchmark outputs. **None of that is on this machine.** Either Codex's work lives elsewhere (another folder, branch, or machine, not synced here), or it was not done. Komail needs to find out which before round 2.

**Answers to the core question** ("can we safely use free/open/cheap VIN sources while TecDoc is pending, and what can they solve?"):

| Question | Status |
|---|---|
| Is any free/open VIN route fit for purpose? | **NOT TESTED** (all providers) |
| Is any PT matrícula provider validated? | **NOT TESTED** (none), nothing even documented |
| Is the manual make/model/gen/year/engine model good enough? | **DOES NOT EXIST** |
| Does OEM/part search work? | **DOES NOT EXIST** |
| Has vehicle X → product Y fitment been proven? | **NO** |
| Can Komail + David start Phase 1? | **YES — architecture can start, provider still provisional** (see §18; this is a judgement about risk, not a claim that the lab validated anything) |

I do not claim any accuracy figure. There is none to claim.

---

## 2. WHAT CODEX ACTUALLY PROVED

Nothing technical. What exists and is true:

- A sensible folder layout that matches the intended separation (`providers/` for replaceable adapters, `benchmarks/`, `fixtures/`, `reports/`).
- A README that states a good data-safety boundary ("No production integrations, credentials, or client data should be committed").
- Collaboration documents that are honest about the empty state.

That is hygiene, not validation.

## 3. WHAT IS ONLY MOCKED

Nothing is mocked. There are no stubs, no adapters, no fake responses. (The brief anticipates adapters/stubs; none exist. I did not need to discount any.)

## 4. WHAT IS WAITING FOR CREDENTIALS

Nothing is recorded as waiting. No provider, credential, or access request is documented anywhere in the repo. Credential/access status for TelePeças, Matricula.co.pt, partslink24 API, and TecAlliance should be tracked in `OPEN_QUESTIONS.md` (it is currently empty).

---

## 5. VIN FINDINGS

### Provider classification

| Provider | Classification | Basis |
|---|---|---|
| Public vPIC (NHTSA) | **NOT TESTED** | No adapter, no response |
| Self-hosted vPIC | **NOT TESTED** | — |
| Offline/open VIN decoders | **NOT TESTED** | — |
| Other open EU data | **NOT TESTED** | — |
| partslink24 VIN | **NOT TESTED** | — |
| TecAlliance VIN | **NOT TESTED** | — |

I will not pre-classify anything as MODEL/ENGINE/EXACT from priors. A priori expectations (not evidence): vPIC is US-origin and is widely reported as weak for European-market vehicles, so the realistic hypothesis is BASIC ONLY, possibly NOT FIT FOR PURPOSE for EU variants. That hypothesis must be tested, not assumed in either direction.

### What I could verify without any provider (deterministic, on the client-supplied VIN `VF3MCYHZUPS034433`)

- Length 17, no I/O/Q characters: structurally valid.
- WMI `VF3` is the Peugeot passenger-car WMI (from knowledge of the WMI registry, not from a repo source).
- **The ISO 3779 / North-American check digit does NOT validate** (computed `3`, position 9 is `U`). That is expected: check digits are only mandatory for North America (and China). **Consequence for design:** a "reject VINs with bad checksum" rule would wrongly reject a valid European VIN, including the client's own test case. Checksum validation must be a *non-blocking, region-aware* signal.
- Position 10 (`P`) is *not* a reliable model-year indicator for EU VINs. Do not derive year from it.

These two points are real red-team findings against any naive normaliser, and they come from the client's own sample.

### Required design (does not exist yet)

- VIN result must carry a **precision level**, not only a score (see §15).
- A VIN decode that returns make/model/year must stop at MODEL. It must never auto-promote to ENGINE or EXACT.
- Free VIN decoding should be a **first-stage router only** (see §11).

### Red-team edge cases — status

None of these are considered anywhere because there is no code or fixture. Each must be a named test case in round 2:

- same make/model/year, multiple engines
- same displacement, different power (e.g. 1.5 BlueHDi 100 vs 130)
- same engine family, multiple engine codes
- facelift / model-year boundary and production-year overlap
- manual vs automatic
- body style (SUV vs estate etc.), commercial vs passenger
- LHD/RHD
- provider returns generic model only
- checksum valid but detail insufficient; checksum "invalid" but VIN genuine (EU, as shown above)
- EU VIN poorly represented in US-origin data
- **plausible but wrong result** — the worst case. Round 2 must include at least some fixtures where the provider's answer is wrong and verify the system does not present it as exact.

---

## 6. PORTUGUESE MATRÍCULA FINDINGS

| Provider | Status |
|---|---|
| TelePeças | **NOT TESTED** (no adapter, no response, no docs in repo) |
| Matricula.co.pt | **NOT TESTED** |
| Existing client software | **NOT TESTED** (not even identified) |
| TecAlliance VRM | **NOT TESTED / not available** |

No response of any kind is in the repo, so none of these may be described as validated, "working", or "waiting for credentials" on the evidence here.

Design requirements for round 2:

- **PT plate normalisation.** Accept `CG-17-GC`, `CG17GC`, `cg 17 gc`; canonical form `CG-17-GC`. Handle historical PT formats (`00-00-AA`, `00-AA-00`, `AA-00-00`, and the current `AA-00-AA`) and reject non-PT plates explicitly. Plate ≠ VIN: store as separate fields.
- **Failure taxonomy** to be handled and tested separately: no result, multiple variants, partial result (make/model only), timeout, 401, 429 (with backoff / circuit breaker), malformed/schema-drifted response, generic-model-only.
- **Partial result policy.** If a plate resolves "Peugeot 5008" but not "1.5 BlueHDi 130" → state is `NEEDS_ONE_MORE_FIELD`, UI asks the customer for exactly the missing discriminator (engine/power/fuel, or confirm from registration document). Never silently pick the most common engine.
- **Client ground truth.** `CG-17-GC` ↔ `VF3MCYHZUPS034433` ↔ "Peugeot 5008 II 1.5 BlueHDi 130" is `CLIENT_PROVIDED` only. Note the plate and VIN come from the same screenshot: a provider that returns the same car for both is consistent, but that's not independent verification.
- **Privacy.** A PT plate lookup resolving to a specific vehicle is personal-data-adjacent. GDPR posture (what is logged, retained, cached, who can see raw payloads) is unaddressed.

---

## 7. MANUAL VEHICLE FINDINGS

**DOES NOT EXIST.** No vehicle schema, no taxonomy, no Make → Model → Generation → Year → Engine tree.

Whether it is a reliable fallback depends entirely on where the underlying vehicle list comes from. Free sources do not give a trustworthy generation/engine tree with the engine-code granularity needed for brake/filter/timing parts. Without TecDoc or partslink24-derived data, **manual selection is only as reliable as the catalogue's own vehicle-to-part links**, and those links are the fitment data. So manual selection is a fallback *for UI flow*, not an independent source of truth. Recommendation: do not design it as a separate vehicle DB; design it as a query against whichever `CatalogueProvider` supplies fitment (partslink24 now manually, TecDoc later).

---

## 8. OEM SEARCH FINDINGS

**DOES NOT EXIST.** No catalogue, no part schema, no search code.

Required identifiers in the part model: OE number (possibly multiple, per manufacturer), aftermarket/manufacturer reference, EAN/GTIN, supplier reference, internal SKU (Primavera item code), and a cross-reference table with direction and source (OE ↔ aftermarket is not always symmetric or 1:1).

Round 2 must label any synthetic test catalogue explicitly as **search-mechanics only**. Searching "find part by number" proves indexing and normalisation (punctuation, leading zeros, case, spaces), **not** that the part fits any car. Do not let a demo that returns parts for a vehicle be read as fitment.

---

## 9. PARTSLINK24 FINDINGS

Per instruction, I do not ask whether Fahad has it. Status in repo: **no mention anywhere**.

Fahad using partslink24 manually ≠ our backend legally integrating it. Verify and record in `OPEN_QUESTIONS.md`:

1. Subscription package/account type (which brands/modules).
2. VIN decode capability and depth (does it reach exact variant / engine code?).
3. OE-number search and OE → vehicle reverse lookup.
4. Manufacturer catalogue coverage (which OEMs).
5. Is there a documented API or B2B/integration product, and is it priced separately?
6. Export/bulk data availability and format.
7. Contractual rights: ecommerce integration, **automated/programmatic access**, display to end customers, caching/storage and retention, sublicensing to Fahad's customers.
8. Is the existing licence for internal workshop/trade use only?

Scraping or automating a logged-in partslink24 session without written permission is a ToS and legal risk. Do not build against it until (7) is answered in writing. Until then it is a **human verification tool** for building ground truth (a legitimate use: Fahad's staff manually confirm vehicles for the benchmark).

---

## 10. FITMENT FINDINGS

**Not proven. Not attempted.** No fitment model, no `FitmentProvider`, no vehicle→product evidence anywhere. Vehicle identification has not even been done, so no fitment claim can exist.

Requirements that must be in the design before any customer-facing "fits your car" text:

- Fitment is its own object: `(vehicle_ref, product_ref, source, evidence_type, restrictions/notes, verified_at)`. It is not a field on the vehicle or the product.
- **Source verdicts**: `MATCH | NO_MATCH | UNKNOWN | CONFLICT`.
- **Customer states**: `COMPATIBLE | CONFIRM_COMPATIBILITY | UNKNOWN | NOT_COMPATIBLE`.
- **Aggregation rule (hard):** `COMPATIBLE` requires (a) vehicle identification at ENGINE or EXACT precision **and** (b) at least one *licensed catalogue* MATCH **and** (c) no NO_MATCH from any other source. Any disagreement ⇒ `CONFLICT` → manual review. **No weighted average across sources.** A free VIN decode alone can never produce `COMPATIBLE`.
- Part-level restrictions (e.g. "with ESP", "front axle", "up to chassis X", brake disc diameter, PR-codes) mean MATCH at vehicle level is often not enough; notes/criteria must flow through to `CONFIRM_COMPATIBILITY`.

Since no code exists, I cannot point to a P0 leak; the P0 is that the design must forbid it from day one (§21).

---

## 11. FREE-FIRST FINDINGS

Hypotheses to test, not conclusions:

- **Where free can save money:** (a) VIN structural validation and WMI/make routing; (b) pre-filtering obviously malformed input; (c) pre-populating the manual selector (make/model/year) to reduce clicks; (d) cutting paid lookups on invalid inputs; (e) building the first benchmark cheaply.
- **Where free is not good enough:** engine-code / exact-variant resolution for European vehicles; anything feeding a safety-relevant part (brakes, steering, suspension, tyres) without a licensed catalogue confirmation.
- **Free VIN as first-stage router only:** plausible and likely the correct role. It narrows, it does not decide.
- **Cheap matrícula + licensed fitment:** a sensible split. Cheap plate lookup can legitimately supply vehicle *identity*; fitment must still come from licensed catalogue data. Cost to evaluate is per *engine-level correct* identification, not per call.
- **Rule:** never trade accuracy for a €0.10 saving on a brake-part path. A wrong brake disc costs a return, a chargeback, and potentially a safety incident, far above lookup costs. Cost-ordered cascades must be gated by precision, not just by price.

---

## 12. COST FINDINGS

**No cost model exists.** Required:

- Volumes: 1k / 10k / 50k / 100k lookups per month, per route (VIN, plate).
- Per provider: fixed fee, per-call fee, free-tier limits, overage, rate limits.
- Derived: cost per *successful* identification, per *engine-level*, per *exact-variant* identification, and cost per *wrong-confident* result (with an explicit assumed cost-of-error, e.g. return+shipping+goodwill).
- Cascade effect: expected cost = Σ P(reach tier) × tier cost, with measured pass-through rates from the benchmark, not guesses.
- Caching: model **two scenarios** (cache allowed / cache forbidden). Do not assume caching of commercial data until rights are confirmed (§13).

---

## 13. LICENSING / DATA RIGHTS FLAGS

Not legal advice. All **UNKNOWN** and none recorded in the repo:

| Item | Flag |
|---|---|
| vPIC / NHTSA | US public-domain-style data, but coverage is US-centric; confirm terms and attribution in writing in the repo. |
| Open-source VIN decoders | **Code licence ≠ data licence.** An MIT/GPL decoder may embed or download data with different or non-commercial terms. Record both separately. |
| TelePeças, Matricula.co.pt | Commercial use, caching, storage, resale to end-customers, and API permission all unknown. Plate-lookup sites often forbid automated access in ToS. |
| partslink24 | Manual use vs programmatic integration (see §9). |
| TecAlliance | Licence terms to be negotiated; TecDoc licensing is typically use-case and display specific. |
| Scraping | Treat as a risk, not a fallback. Do not build scrapers for sites without written permission. |
| Attribution / non-commercial clauses | Track per source. |
| GDPR | Plates and VINs linked to customers are personal data; define retention and lawful basis. |

**Recommendation:** a `docs/data_rights_register.md` with one row per source: code licence, data licence, commercial use (Y/N/?), cache/store (Y/N/?), automated access (Y/N/?), attribution, evidence link, date checked. Provider cache entries must be tagged with `source` and be purgeable per source.

---

## 14. ARCHITECTURE ISSUES

Intended flow: Customer input → Platform API → Normalisation → Internal vehicle model → Fitment/Catalogue → Inventory → Price/Delivery, with providers behind adapters.

Current state: `providers/` and `app/` exist as empty folders, so the separation is intent only; there is nothing to violate it and nothing proving it.

Requirements for round 2:

- Three narrow interfaces, kept separate: `VehicleIdentityProvider` (VIN/plate → candidate vehicles), `CatalogueProvider` (vehicle/ref → products), `FitmentProvider` (vehicle × product → verdict + evidence). TecDoc must plug into all three **without** changing customer-facing code, which means the customer-facing layer depends only on the internal model + verdict states.
- Identity providers return **a list of candidates with precision level and raw payload**, never a single "the car".
- Per-provider isolation: timeouts, circuit breaker, error taxonomy; one provider's failure or bad data must not abort the cascade or poison the cache.
- Cache keyed by `(provider, provider_version, input)`; provider-specific cache, never a merged "canonical" cache that loses provenance.
- Orchestrator order configurable per route (VIN vs plate), with per-step `min_precision` and `max_cost`.
- Primavera is **inventory/price/customer/order**, not identity or fitment. Keep an `InventoryProvider`/`PricingProvider` separate and downstream.

### Canonical vehicle model — required fields (none exist)

Present in brief → needed in model: make, model, **generation/platform code**, model year, **first-registration date/year** (distinct from model year), engine family, **engine code**, fuel, power kW, power hp (store the source unit; derive the other, don't invent), displacement cc, body, transmission, drive, VIN, matrícula, country of registration, **market/steering (LHD/RHD)**, provider vehicle IDs (map: provider → their ID, many-per-vehicle), ambiguity flag + candidate list, source, raw payload ref, precision level, field-level provenance.

Missing from the brief that I'd add: **per-field provenance and per-field nullability** (each of year/engine/power must say *which source gave it, or null*), `production_from/production_to` range, `variant/trim`, `vehicle_class` (passenger/LCV), `emission_standard`, and `ktype` / TecDoc vehicle ID slot reserved for later.

**Do not fabricate normalisation.** If the source says "1.5 BlueHDi" with no power, power stays null. Do not fill 130 hp from a lookup table keyed on a guess. Incomplete stays incomplete and lowers precision.

---

## 15. CONFIDENCE / SCORING ISSUES

No scoring code exists. Design guidance for round 2:

- A single percentage score is **insufficient and dangerous**. Replace/augment with an ordinal **precision level**: `BASIC` (make) < `MODEL` (make+model+year/generation) < `ENGINE` (engine family + fuel + power) < `EXACT_VARIANT` (engine code / provider vehicle ID / precise variant).
- **Hard gates:** make/model/year correct and engine unknown ⇒ MODEL, and may never be reported as "95% exact" or exceed the MODEL ceiling. Fitment-eligible only at ENGINE or EXACT_VARIANT (per product category: some parts, e.g. wiper blades, may be MODEL-eligible; make this a per-category policy table, not code scattered through the app).
- Precision is determined by **which fields are populated from evidence**, not by a provider's self-reported confidence.
- Separate three things: **precision** (how specific), **agreement** (do sources agree), **trust** (is this provider validated at this precision, from the benchmark). A provider unvalidated at ENGINE level is capped at MODEL, whatever it claims.
- Distinguish the outcomes explicitly: `NO_RESULT`, `AMBIGUOUS` (multiple candidates), `PARTIAL`, `RESOLVED`, `CONFLICT`. The system must prefer `NO_RESULT`/`AMBIGUOUS` over **WRONG_BUT_CONFIDENT**. Track "false confident result rate" as a first-class KPI with a target near zero.
- Disagreement ⇒ `CONFLICT` ⇒ review. No averaging.

---

## 16. BENCHMARK ISSUES

`fixtures/` and `benchmarks/` are empty. `fixtures/vehicle_ground_truth.csv` **does not exist**.

Requirements:

- Each row has `truth_class` ∈ `CLIENT_PROVIDED | INDEPENDENTLY_VERIFIED | SYNTHETIC` and `truth_source` (e.g. partslink24 screenshot, registration document, OEM catalogue). **SYNTHETIC rows are excluded from every accuracy metric** (enforce in code, plus a test that fails if one leaks in).
- The one known case: `CG-17-GC` / `VF3MCYHZUPS034433` / Peugeot 5008 II 1.5 BlueHDi 130 — `CLIENT_PROVIDED`, not independently verified. Needs engine code, kW, first-registration date from the registration document or partslink24 to become INDEPENDENTLY_VERIFIED.
- Metrics (per provider, per precision level): lookup success; make / model / generation / year / engine / engine-code / power / variant accuracy; ambiguity rate; no-result rate; wrong-result rate; **false-confident rate**; p50/p95 latency; cost; cost per correct engine-level match; cost per exact match.
- Report accuracy with **n and confidence intervals** (e.g. Wilson). "5/5" is not 100%.
- Keep raw provider responses under `fixtures/raw/` (sanitised: no personal data) so results are re-scorable without re-spending money.

### Sample size (strict)

- 1 VIN: an anecdote, not validation.
- ≤10: smoke test only (checks the plumbing, not accuracy).
- **Stage 1:** 10–20 real vehicles, ideally from Fahad's actual sales/enquiries.
- **Stage 2:** 100+ real vehicles, deliberately covering the edge cases in §5.
- **Stage 3:** 100–500 mixed European vehicles (makes, ages, fuels, LCV) before production trust.

---

## 17. BLOCKERS BEFORE CLIENT PROPOSAL

1. Locate Codex's actual work, or accept there is none (**P0**).
2. Do not present any "validated" claim for VIN, plate, or fitment. The honest message to Fahad/Ayaz: *identification options are being evaluated; fitment will come from a licensed catalogue.*
3. Confirm partslink24 package/rights (§9) so the proposal doesn't assume integration is permitted.
4. A first Stage-1 result (10–20 real vehicles) for at least one VIN route and one plate route, or an explicit statement that these are unvalidated.
5. Licensing register started (§13).

## 18. BLOCKERS BEFORE DEVELOPMENT

**Verdict: YES — architecture can start, provider still provisional.**

Komail + David *can* start Phase 1 on provider-independent parts: the three interfaces, the internal vehicle model with precision levels, the fitment verdict model and customer states, PT plate/VIN input normalisation, the manual selector UI shell, search by part reference, the Primavera adapter boundary, cache design. These do not depend on which provider wins.

They should **not**:
- hard-wire any provider's response shape into the internal model,
- ship customer-facing "fits your car" text,
- assume a free VIN decoder will provide engine-level identity.

Real blockers for those specific parts: **vehicle-identification** is unvalidated and **fitment data** has no source yet (partslink24 rights unknown, TecDoc pending). So building *fitment display* now would be against mock data only; label it so.

## 19. BLOCKERS BEFORE PRODUCTION

- Licensed catalogue/fitment source with confirmed ecommerce, caching and programmatic rights.
- Stage-3 benchmark (100–500 vehicles) per identity provider with false-confident rate below an agreed threshold.
- Provider rights register complete; GDPR retention/logging decisions.
- Rate-limit/timeout/circuit-breaker behaviour proven under test.
- Customer-facing fitment copy and returns policy reviewed.

---

## 20. PROVISIONAL RECOMMENDED STACK

Provisional, pending evidence. Not validated.

| Layer | Provisional choice | Status |
|---|---|---|
| Input validation / VIN router | Local structural VIN parse (length, charset, WMI) — **no blocking checksum for EU** | buildable now, no data licence concern beyond WMI table |
| VIN identity | Free decoder as router/MODEL-ceiling; paid/licensed provider for ENGINE+ | **to be tested** |
| Plate identity | Existing client source / TelePeças / Matricula.co.pt, in that order | **to be tested; rights unknown** |
| Catalogue + fitment | partslink24 (manual use for ground truth now); TecDoc when available | **rights unknown / pending** |
| Manual fallback | Selector fed from catalogue provider | depends on catalogue |
| Inventory/price/orders | Primavera/Cegid via an adapter | separate from identity |
| Safety policy | Fitment-eligible only at ENGINE/EXACT; conflicts ⇒ review | **design now** |

---

## 21. P0 FIXES

1. **Reconcile the repo with reality.** Locate/restore Codex's work or confirm none exists. No further review is meaningful until there is code. *Owner: Komail → Codex.*
2. **Make the repo a git repo** and commit a baseline so reviews can reference a commit. *Codex.*
3. **Define precision levels and hard gates** (BASIC/MODEL/ENGINE/EXACT_VARIANT) before writing any provider adapter, plus the rule that a single percentage score never drives fitment. *Codex.*
4. **Define fitment verdict model** (`MATCH/NO_MATCH/UNKNOWN/CONFLICT` → `COMPATIBLE/CONFIRM_COMPATIBILITY/UNKNOWN/NOT_COMPATIBLE`) with the rule that no single low-precision or unlicensed source can yield `COMPATIBLE`, and disagreement ⇒ CONFLICT. Add a test that tries to violate this. *Codex.*
5. **Do not apply a mandatory VIN checksum** to European VINs (the client's own VIN fails the NA check). *Codex.*
6. **Fixtures with `truth_class`** and a test that SYNTHETIC never enters metrics. *Codex.*
7. **Mark all test catalogue data as search-mechanics-only**; no UI wording implying fitment. *Codex + David.*
8. **Rights register** for every provider before any caching/storage is implemented. *Komail.*

## 22. P1 FIXES

1. Canonical vehicle model with per-field provenance and nullable fields (§14).
2. `VehicleIdentityProvider` / `CatalogueProvider` / `FitmentProvider` interfaces; TecDoc as a drop-in.
3. Orchestrator: configurable order, per-step `min_precision`/`max_cost`, error isolation, circuit breaker, provider-scoped cache.
4. PT plate normaliser + failure taxonomy (no result, multi, partial, timeout, 401, 429, malformed).
5. "Ask one more field" flow for partial plate results.
6. Cost model with 1k/10k/50k/100k scenarios and cache-allowed vs forbidden.
7. Partslink24 rights questions answered in writing.
8. Stage-1 benchmark (10–20 real vehicles) with raw responses stored.

## 23. P2 IMPROVEMENTS

- Wilson confidence intervals in reports; per-provider precision-vs-cost curves.
- Edge-case fixture pack (§5 list) with deliberately wrong-but-plausible provider answers.
- Part-category eligibility policy table (which categories may use MODEL precision).
- GDPR retention/redaction for plates, VINs and raw payloads.
- Reserved `ktype`/TecDoc ID fields; replay harness over stored raw responses.
- Stage 2 / Stage 3 benchmark planning with Fahad's real enquiry data.

---

## 24. QUESTIONS FOR KOMAIL

1. **Where is Codex's work?** The repo has only scaffolding and `CODEX_STATUS.md` says nothing was started. Was a different folder/branch used, or did the build step not happen?
2. Should this folder become a git repo (and if so, local only, given your no-push-without-instruction rule)?
3. Do you have the actual **screenshot** for `CG-17-GC`? What fields does it show (engine code, kW, first registration)? That decides whether it can become independently verified.
4. Which matrícula source does Fahad's **existing client software** use, and can staff export or screenshot results for ~20 vehicles to build the Stage-1 set?
5. What is Fahad's **partslink24 package**, and can he get written confirmation of API/programmatic and ecommerce-display rights?
6. Which parts categories launch first? (This sets which categories need ENGINE-level identity, i.e. how much free VIN can help.)
7. Budget ceiling per lookup and the acceptable false-confident rate (suggest targeting ≈0 for safety parts).
8. Is a PT-only launch assumed, or other EU markets (affects VIN data needs)?

---

# Round 2 addendum — independent testing (2026-10-05)

Full detail: `reports/claude_validation_verdict.md`. Raw outputs: `reports/claude_raw_evidence/`.

## Findings
- **vPIC live test on PT VIN VF3MCYHZUPS034433:** make PEUGEOT + ModelYear 2023 only; model/engine/power/fuel all empty; error codes 1, 8, 400. Precision = BASIC. Not fit for Portuguese identity.
- No matrícula provider tested (Matricula.co.pt requires registered test account; TelePeças has no public API docs).
- The files named in the campaign brief (`real_validation_matrix.csv`, `client_vehicle_comparison.html`, `cost_model.md`, `raw_evidence/`, `docs/portugal-official-data-route.md`) do not exist in this repo, so Codex's campaign claims could not be verified.

## Findings that need Codex retesting / changes
1. `fixtures/vehicle_ground_truth.csv` lacks `country` and `portuguese_market_verified`. Synthetic rows use `market=EU`. Add both columns; only `country=PT AND portuguese_market_verified=true` may count toward production score; foreign rows are debug-only.
2. `client_001` has `model_year=2023`, which equals vPIC's unreliable pos-10 guess. Mark as unverified; do not use as ground truth.
3. vPIC adapter must map error code 8 / empty Model to BASIC and never infer model. Retest against the saved raw JSON.
4. Any claim that a provider is "good" needs PT-only n and Wilson interval; vPIC strength on US VINs is irrelevant.
5. Provide the missing campaign files or confirm they were not produced.

---

# Round 3 addendum (2026-10-05): provider research and strategy

See `reports/FINAL_PRE_TECDOC_DATA_STRATEGY.md` and linked files. Key new findings:
- New PT plate candidates, all DOCUMENTED / UNTESTED: **Openapi PT-car** (€0.18–0.40/call, REST, sandbox, VIN+version+hp), **Matricula.co.pt** (€0.20, 10 free credits), **AutoNow PT** (claims K-type), MatriculAZ (API not launched; terms forbid automation), TelePeças (no docs).
- VIN: only vPIC actually tested (BASIC). Vincario (EU, claims kW/variant/ktype, 20 free VINs) is the next test.
- **partslink24 public ToS prohibits integrating into our own services and automated extraction/storage**: validation/staff tool only unless LexCom grants written rights.
- Auto Delta: login-gated supplier portal, no public catalogue; not an API.
- Fitment still NOT solved; bridge document at `docs/vehicle-to-catalogue-bridge.md`.
- Codex status as of review: 29 tests pass; only vPIC evidence exists; no real PT provider evidence; fixtures lack PT-scope columns (see NEXT_ACTIONS P0-R1).

---

# Round 4 review of Codex's latest work (2026-10-05)

Reviewed: git status, `CODEX_STATUS.md` (STALE: still says 29 tests/Round-2 only), new modules, raw evidence. Tests: **37 passed**.

**Good:** `ProviderPolicy` refuses caching/storage unless terms verified; fixtures now carry `country` + `portuguese_market_verified`; Codex honestly recorded the Matricula.co.pt/TelePeças auth failures as non-results; self-hosted vPIC correctly marked non-independent; OE cross-check correction (1K1614724E is a brake pipe, mock labels must not be reused).

**Challenges / retest requests**
1. `providers/vpic.py` sets `model_year` from vPIC `ModelYear` (VIN pos-10 guess for an EU VIN) and hard-codes `country_of_registration="PT"` for any VIN. A VIN does not prove Portuguese registration; set country from the *plate* evidence only, and do not populate `model_year` from vPIC for non-US WMIs (or mark as `ESTIMATED` and exclude from precision).
2. `reports/client_ground_truth_research.md` (Codex rewrite) marks year 2023 LIKELY on the basis of vPIC returning 2023: circular; the same guess. Downgrade to UNKNOWN until first-registration date is supplied.
3. `CODEX_STATUS.md` is stale; update with real-campaign status and the 37 tests.
4. Codex's cost_model: Openapi tiers now verified (€0.40 PAYG; 0.37/0.33/0.30/0.28/0.24/0.18). Add 0.33/0.28.
5. Add providers: Autoways AUTO-NOW, Vincario, TecAlliance direct; **TelePeças API fields (`ktype`, `tecDocModelId`, `telepecasModelId`) should be adapter schema candidates only after a real response exists.**
6. Bridge doc: keep `match_method` (PROVIDER_ID/VIN/ENGINE_CODE/TEXT_MATCH/USER_CONFIRMED) in the model; a provider-returned K-Type must be *validated against a licensed catalogue* before it can influence COMPATIBLE.
7. Codex wrote `docs/vehicle-to-catalogue-bridge.md` and `reports/client_ground_truth_research.md` over my versions; I accept the content. My additions are in `FINAL_PRE_TECDOC_DATA_STRATEGY.md`.

New documents this round: `reports/tecdoc_direct_access_strategy.md`, `reports/DIRECT_TECDOC_AND_RESELLER_COMPARISON.md`, `reports/HUMAN_ACTIONS_REQUIRED.md`.

---

# Round 5 review: Autofrance K-Type finding (2026-10-05)

See `reports/autofrance_ktype_investigation.md` and `reports/ktype_crosscheck.csv`.
- **Reproduced** Codex's call: identical (K-Type 130708, "3008 SUV (MC_,MR_,MJ_,M4_)", 1.5 BlueHDi 130, 96 kW).
- **Source is a Swedish retailer's storefront backend**, not a data API; terms silent on automation, copyright on content. Research oracle only.
- **Engine-level result is well supported** (VIN positions 6–8 `YHZ` = DV5RC; provider; public specs). **Model 3008 vs 5008 is UNRESOLVED**: prefix `VF3MCYHZ` and chassis codes `MC_/MJ_/MR_/M4_` are shared; public VIN pages list that prefix under both models. The decoder returned one confident answer for an ambiguous key.
- Codex's own reports must not say "ENGINE resolved → catalogue ID resolved". Mark client_001 as `MODEL_CONFLICT`.
- `providers/autofrance.py`: sets `country_of_registration="PT"` from a VIN again (unsupported leap), `status=RESOLVED` whenever precision ≥ ENGINE: with a model conflict this must become `AMBIGUOUS`/needs-confirmation; and it must be flagged `commercial_use=NOT_PERMITTED/UNKNOWN`, not in any production cascade.
- `CODEX_STATUS.md` still stale (no Autofrance).

---

# Round 6 (2026-10-05): conflict substantially resolved toward 3008

See `reports/autofrance_ktype_investigation.md` Round 6 update and `reports/ktype_crosscheck.csv`.
- K-Type **130708 independently confirmed** as "Peugeot 3008 SUV 1.5 BlueHDi 130, 96 kW, YHZ (DV5RC), 2018→" (Autodoc + Schaeffler). **130738** = 5008 II 1.5 BlueHDi 130 with VDS MCYHZ**J/R/X**.
- Our VIN VDS is MCYHZ**U**: excluded from the 5008 list; Autofrance's own rule (plant S→3008) also gives 3008. **LIKELY the VIN is a 3008.** The client's "5008" is the outlier or plate/VIN come from different cars.
- Autofrance decodes **fake VINs confidently** (serial 000001): no existence check → never a sole source.
- **Codex:** (1) update `client_001` to `LIKELY_3008_PENDING_CONFIRMATION`, not `MODEL_CONFLICT_UNKNOWN`; (2) crosscheck rows added; (3) do not treat client "5008" as ground truth for scoring: record model as `DISPUTED`; (4) 2 failing tests (test_vpic ENGINE expectation, test_cost_analysis None cost): please resolve, I did not touch them.

---

# Round 6: answers to Codex's READY_FOR_CLAUDE questions

1. **Autofrance capped at ENGINE + NEEDS_SECOND_SOURCE?** In `real_validation_matrix.csv`: yes. In code: **no, currently inconsistent**: `tests/test_vpic.py` expects ENGINE but the model gives BASIC, and `test_cost_analysis` expects `None` cost but gets 0.0 (2 failing tests, `python3 -m unittest discover -s tests`). Pick the intended semantics and fix tests or code. Also cap must be explicit: ENGINE max + `NEEDS_SECOND_SOURCE` + `NO_EXISTENCE_CHECK`.
2. **Do reports treat client expectation or K-Type as independent truth?** Not as truth, good. But they are now **stale**: K-Type 130708 *has* an independent identity cross-check (Autodoc + Schaeffler), and two independent lines point to 3008. Codex's statement "Autofrance catalogue page resolves K-Type" is NOT independent (same provider). Update `client_ground_truth_research.md` and FINAL to: model = `LIKELY 3008, DISPUTED vs client 5008`, K-Type 130708 = `IDENTITY CROSS-CHECKED`, VIN→K-Type = `PARTIAL`.
3. **Commercial/cache/storage conservatism?** Yes: UNKNOWN/default NO is right. Add Autofrance as `RESEARCH_ONLY` (storefront backend; copyright notice, no API licence).
4. **Is the stop boundary honest?** **No.** "Accessible no-account routes exhausted" was false: in this round I found, without any account, two independent catalogue confirmations and the decoder's real discriminator (plant letter, no existence check). Also still no-account/human-€0 actions available: manual plate lookups on several Portuguese retailers (see HUMAN_ACTIONS_REQUIRED, 'Manual plate lookups'). Replace with: "remaining routes need accounts, contracts or human screenshots".

---

# Commercial validation + red team (2026-10-05, final round for Claude's phase)

Full content in `reports/CLAUDE_BUILD_PLAN_REDTEAM.md`, `reports/PROVIDER_COMMERCIAL_COMPARISON.md`, `reports/provider_autoways_final.md`, `reports/provider_tips4y_final.md`, `reports/tecalliance_direct_buying_strategy.md`.
- Build answers: frontend YES; backend YES; vehicle abstraction YES (with changes); catalogue abstraction YES (interface only); Primavera NO for real integration / YES for interface; checkout YES; exact fitment **NO**; PT plate production integration **NO**.
- Code issues: fitment ignores bridge; ENGINE_CODE auto-claim unsafe (3008/5008 share YHZ); `licensed_catalogue` self-declared; NOT_COMPATIBLE from unlicensed sources; provider K-Types need `ktype_validated`; plate-vs-VIN agreement gate missing.
- client_001: **CONFLICT — NEEDS PLATE/REGISTRATION/PARTSLINK24 CONFIRMATION** (leans 3008; client's 5008 not overwritten).
- **Claude does NOT sign final completion.** Missing: any PT plate result, licensed K-Type validation, partslink24/registration evidence, commercial quotes (TecAlliance direct, Fahad/Luis, Tips4y, Autoways price).
