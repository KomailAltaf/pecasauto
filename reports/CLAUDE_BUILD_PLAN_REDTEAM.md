# Claude red-team review of Codex's build state and Phase 1 plan

Date 2026-10-05. **`reports/PHASE1_DEVELOPMENT_PLAN.md` and `collaboration/JOINT_VALIDATION_DRAFT.md` do not exist yet**, so this reviews the code present (`app/fitment.py`, `app/bridge.py`, `app/cascades.py`, `app/fallback.py`, adapters; 46 tests passing) and answers the build questions. Re-review the plan when it lands.

## Can we safely build…
| Item | Answer | Why |
|---|---|---|
| **Frontend** | **YES** | No dependency on a provider. Build against the interfaces and verdict states. Rules: no "fits your car ✓" copy tied to mock/unlicensed data; show `CONFIRMAR COMPATIBILIDADE`; vehicle-confirmation step must be able to show 2+ candidates (e.g. 3008/5008) with images. |
| **Backend (platform)** | **YES** | Accounts, cart, search, garage, orders, admin, logging, config-driven provider cascade. All provider data is optional input. |
| **Vehicle abstraction** | **YES, with changes** | Model + precision + provenance exist. Add: `MODEL_CONFLICT`/`DISPUTED` state, `NO_EXISTENCE_CHECK` flag, plate/VIN agreement check, `ktype_validated` flag, per-field source. |
| **Catalogue abstraction** | **YES (interface), NO (real implementation)** | No licensed catalogue exists. Build the interface and a staff-curated stub only. |
| **Primavera integration** | **NO (real integration); YES (interface only)** | Version, modules and API access are unknown. Define an `InventoryProvider`/`PricingProvider` boundary and mocks; do not code against Primavera until Fahad confirms version/API. |
| **Checkout** | **YES** | Independent of vehicle data (payments, GLS shipping, VAT). Condition: product pages and returns copy must not promise compatibility; consider a "compatibility confirmed on order" flag for unconfirmed vehicles. |
| **Exact fitment** | **NO** | No licensed fitment source; Autofrance is research-only; K-Types are unverified. Only `CONFIRM_COMPATIBILITY`/`UNKNOWN`. |
| **Portuguese matrícula production integration** | **NO** | No PT plate provider returned a vehicle; rights unknown for all. Adapters may be written the moment a real response exists (Autoways spec example can seed schema tests, labelled SPEC_EXAMPLE). |

## Findings on the existing code (unsafe/unsupported items)
1. **`evaluate_fitment` ignores the bridge** (`app/fitment.py` vs `app/bridge.py`): COMPATIBLE needs ENGINE precision + a licensed MATCH, but nothing requires `CatalogueBridgeResult.may_claim_compatible`. A TEXT_MATCH or multi-candidate bridge could still reach COMPATIBLE. **Fix: pass the bridge result in; COMPATIBLE only if `may_claim_compatible`.**
2. **`MatchMethod.ENGINE_CODE` can claim compatible with one candidate** (`bridge.py`). Engine code does **not** distinguish 3008 from 5008 (both YHZ/DV5RC): exactly the client case. Remove ENGINE_CODE from the auto-claim set or require model/body confirmation.
3. **`licensed_catalogue` is a self-declared boolean** on `FitmentEvidence`. Nothing ties it to a verified provider policy. Tie it to `ProviderPolicy.terms_verified` and a registered licensed source.
4. **NOT_COMPATIBLE from any source:** `verdicts == {NO_MATCH}` returns NOT_COMPATIBLE even from an unlicensed or low-precision source: a false negative hides valid products. Require a licensed catalogue NO_MATCH; otherwise UNKNOWN/CONFIRM.
5. **K-Type trust:** `MatchMethod.PROVIDER_ID` may claim compatible with one candidate. A provider K-Type derived by matching (Autoways) or from an unlicensed storefront must not qualify until validated (second independent source or licensed catalogue). Add `ktype_validated`.
6. **Minimum precision is global (ENGINE).** Needs a per-category policy table (brakes/filters ENGINE+, wipers MODEL).
7. **Cascade composition:** plate cascade lacks Autoways/Tips4y/Openapi steps and has no **plate-vs-VIN agreement** gate. If plate and VIN resolve to different models (client_001 possibility), result must be CONFLICT.
8. **Autofrance adapter:** correctly out of the production cascade; confirm it can never feed the garage/cache and that status is capped (ENGINE + NEEDS_SECOND_SOURCE + NO_EXISTENCE_CHECK). Network errors in `identify_by_vin` use bare `urlopen`: ensure the orchestrator wraps it (error isolation test with a timeout).
9. **Garage store:** confirm it stores only user-confirmed vehicles with `match_method=USER_CONFIRMED` and the *set of candidates shown*; never provider-returned K-Types without rights.
10. **Positives:** unknown terms disable caching; Autofrance excluded from production; text matches cannot claim compatible; PT-only scoring gate; source disagreement → CONFLICT.

## client_001 status (unchanged)
**CONFLICT — NEEDS PLATE/REGISTRATION/PARTSLINK24 CONFIRMATION.** Evidence leans 3008 (K-Type 130708 cross-checked; VDS MCYHZ**U** not in the 5008 II list; Autofrance rule S→3008), but no authoritative Portuguese source. The client's "5008" expectation is not overwritten.

## Claude sign-off
**Not signed.** Material evidence missing: no PT plate result, no K-Type validation in a licensed catalogue, no partslink24/registration-document result, no commercial quotes. Acceptable to start Phase 1 on the YES items above.
