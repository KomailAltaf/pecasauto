# Next Actions

Updated by Claude review round 1 (2026-10-05). Source: `collaboration/CLAUDE_REVIEW.md`.

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
