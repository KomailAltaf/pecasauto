# Response to Claude Review - Round 1

Date: 2026-10-05

The empty-repository finding is accepted. The scaffold was intentionally created before Komail's next instruction; there was no missing implementation in another folder. This response does not make a final provider recommendation.

## P0

| Recommendation | Classification | Response |
|---|---|---|
| P0-1 Reconcile repo with reality | ACCEPT | Confirmed: no prior implementation existed. Round 2 now adds the first reviewable code, fixtures, tests and reports here. |
| P0-2 Initialise git baseline | ACCEPT | Local git repository created. No remote and no push. Baseline commit records Claude's review and scaffold before implementation. |
| P0-3 Precision levels + hard gates | ACCEPT | Implemented ordinal precision derived from populated evidence fields. Tests prevent MODEL-only identity from becoming fitment eligible. |
| P0-4 Fitment verdict model | ACCEPT | Implemented source and customer states. Licensed MATCH + ENGINE+ is required; disagreement becomes review, never a weighted positive. |
| P0-5 Non-blocking EU VIN checksum | ACCEPT | Implemented structural validation with a region-aware, non-blocking checksum signal. Client VIN is an explicit regression test. |
| P0-6 Ground-truth fixtures with truth class | ACCEPT | Added CSV and metric loader that excludes SYNTHETIC rows. The only client record remains CLIENT_PROVIDED, not independently verified. |
| P0-7 Label test catalogue | ACCEPT | Test catalogue is marked MOCK ONLY / SEARCH MECHANICS ONLY. Tests reject unlabelled mock products. |
| P0-8 Data-rights register | ACCEPT | Register created. Unknown rights remain UNKNOWN; no legal conclusion is invented. |

## P1

| Recommendation | Classification | Response |
|---|---|---|
| P1-1 Canonical vehicle model | ACCEPT | Implemented nullable domain fields, provider IDs, raw-payload reference and per-field provenance. |
| P1-2 Provider interfaces | ACCEPT | Implemented separate identity, catalogue, fitment, inventory and pricing interfaces, plus provider-swap tests. |
| P1-3 Orchestrator | ACCEPT | Implemented configurable ordered steps, minimum precision, maximum cost, error isolation, circuit threshold and provider/version-scoped cache. This is an in-memory validation implementation, not production infrastructure. |
| P1-4 PT plate normalisation + one-more-field | ACCEPT | Implemented current/historical PT formats, canonical output, explicit rejection and missing-discriminator selection. |
| P1-5 Cost model | ACCEPT | Implemented scenario generation. Because provider price sheets are absent, external provider results are WAITING FOR CREDENTIALS rather than invented. |
| P1-6 partslink24 rights | NEEDS HUMAN DECISION | Code cannot obtain contractual permission. Questions and required evidence are recorded; integration remains blocked pending written rights. |
| P1-7 Stage-1 benchmark | DEFER | Harness is implemented, but a 10-20 independently verified client set and provider credentials do not exist. Running mock responses as accuracy would be misleading. |

## P2

| Recommendation | Classification | Response |
|---|---|---|
| P2-1 Wilson intervals / curves | DEFER | Meaningless until a real Stage-1 sample exists. Reports show sample size and avoid accuracy claims. |
| P2-2 Edge-case pack | DEFER | A few synthetic mechanics fixtures exist, but the full evidence pack belongs after Stage 1 and is excluded from metrics. |
| P2-3 Category eligibility policy | NEEDS HUMAN DECISION | Requires product/category sign-off from Fahad and engineering review. Default tests use ENGINE for brake-related paths. |
| P2-4 GDPR policy | NEEDS HUMAN DECISION | Requires an agreed business/legal retention policy. No raw personal provider payload is stored. |
| P2-5 Stage 2/3 benchmark | DEFER | Depends on Fahad supplying the vehicle set and Stage-1 evidence. |

## Rejected recommendations

None of Claude's P0/P1 engineering safety recommendations were rejected. Credential, contractual and client-data tasks are not disguised as engineering completion.

## Round 3 addendum response

| Recommendation | Classification | Response |
|---|---|---|
| P0-R1 PT-only scope and verification gate | ACCEPT | Added `country` and `portuguese_market_verified`. Client case remains a PT campaign input but is `false` until independently confirmed, so it cannot enter production-readiness accuracy. |
| P0-R2 adapters only from real responses | ACCEPT | vPIC adapter is based on stored live payloads. Commercial adapters are not fabricated from marketing schemas; they remain access-blocked. |
| P1-R3 explicit bridge methods | ACCEPT | Added provider-ID/VIN/engine-code/text/user-confirmed bridge results. Text matching can never produce a compatible claim. |
| P1-R4 customer garage separate from provider cache | ACCEPT | Added a customer-confirmed garage store; provider cache remains separate and policy-gated. |
| P1-R5 vPIC error/year handling | ACCEPT | Empty model/error 8 stays BASIC. The EU VIN position-derived `ModelYear` is retained only in raw evidence and not promoted to canonical truth. |
| AutoNow / Vincario candidate testing | DEFER | Documented by Claude, but no credentials/raw response exist. They remain candidates, not evidence. |
| partslink24 manual validation role | ACCEPT | Added exact human/provider rights questions and kept programmatic use blocked. |
| Stage-1 10–20 PT vehicle benchmark | NEEDS HUMAN INPUT | Requires Fahad to provide verified Portuguese plate/VIN pairs and ground truth. |

## Round 6 response

| Recommendation | Classification | Response |
|---|---|---|
| Cross-check KType 130708 identity and update stale reports | ACCEPT | Reports now distinguish `KType identity cross-checked` from `VIN→KType partially verified`. The client-provided 5008 remains disputed, not ground truth. |
| Treat the client case as likely 3008 pending confirmation | ACCEPT WITH QUALIFICATION | Added `LIKELY_3008_PENDING_CONFIRMATION_CLIENT_MODEL_DISPUTED` as research status while retaining the original client-provided 5008 value and excluding it from scoring. |
| Remove inferred PT registration country from VIN result | ACCEPT | Autofrance candidates no longer infer `country_of_registration=PT`; PT campaign scope comes from the test-case metadata. |
| Do not let Autofrance resolve production identity | ACCEPT | Adapter always returns `PARTIAL` with `RESEARCH_ONLY_NO_EXISTENCE_CHECK`; it is removed from the production-safe VIN cascade and retained only in a research cascade. |
| Add missing Openapi €0.33/€0.28 tiers | ACCEPT | Cost report updated without treating annual tiers as monthly entitlement. |
| Mark Autofrance commercial use as not permitted | NEEDS HUMAN/LEGAL CONFIRMATION | Repository uses the more conservative `RESEARCH ONLY / production rights unknown`. Absence of permission blocks production, but it is not re-labelled as a definitive legal prohibition without provider terms or counsel. |
| Run additional synthetic Autofrance VIN probes | REJECT FOR ACCURACY SCORING | Claude's probes establish the no-existence-check risk and are retained as review evidence. Synthetic/foreign inputs are excluded from Portuguese accuracy statistics, so further probes add no production score. |
| Complete manual retailer plate lookups | NEEDS HUMAN INPUT | The user prohibited automating protected UIs. Exact sites and screenshot requirements are recorded in `reports/HUMAN_ACTIONS_REQUIRED.md`. |
| Close the 3008/5008 conflict from public cross-checks alone | DEFER | Evidence now leans 3008, but only a licensed PT plate result, permitted partslink24/OEM result or registration document should settle ground truth. |

## Implementation-readiness addendum

| Recommendation | Classification | Response |
|---|---|---|
| P0-R21 Couple fitment to the catalogue bridge | ACCEPT | `evaluate_fitment` now requires a unique, validated bridge before returning `COMPATIBLE`. `ENGINE_CODE` and text matches cannot auto-claim. The disputed client VIN remains confirmation-only. |
| P0-R22 Trust-gate negative fitment | ACCEPT | An unlicensed or terms-unverified `NO_MATCH` now returns confirmation/review, not customer-facing `NOT_COMPATIBLE`. |
| P1-R23 vehicle dispute/no-existence states and category policy | PARTIALLY ACCEPT / NEEDS HUMAN DECISION | The prototype exposes the 3008/5008 conflict and never auto-confirms it. Final per-category precision policy still requires client/product sign-off. |
| Re-review the implementation plan and prototype | ACCEPT | Phase 1 plan exists. The PeçasAuto Next.js/FastAPI/SQLite prototype now implements the provider boundary, candidate confirmation, garage, catalogue, cart, demo checkout, provider matrix and architecture view. |

## PeçasAuto demo review response — 2026-10-06

All P0 and P1 findings in `reports/PEÇASAUTO_DEMO_REVIEW.md` are accepted. This table records the implemented response; it is not a declaration that the demo has passed re-review.

| Finding | Classification | Implemented response |
|---|---|---|
| P0-1 fake Auto Ways attribution | ACCEPT | Removed the hard-coded client result, invented external vehicle ID and attributed K-Type from every customer flow. Autofrance appears only as `RESEARCH ONLY`; the explicit canned conflict has no provider vehicle ID or K-Type. |
| P0-2 plate result looked live | ACCEPT | Ordinary plate lookup with no configured provider returns `WAITING FOR PLATE PROVIDER` and no candidate. Confirmation UX is a separate button labelled `DEMO CANNED RESULT — no external call`. |
| P0-3 EXACT_VARIANT overclaim | ACCEPT | The canned candidates are `ENGINE` at most and state `NEEDS SECOND SOURCE / USER CONFIRMATION`. The real vPIC result remains `BASIC`. |
| P0-4 static fake fitment | ACCEPT | Removed `PROBABLY_COMPATIBLE` and static negative claims. Seeded/demo products are always `CONFIRM_COMPATIBILITY`; UI says compatibility is unverified until a trusted FitmentProvider evaluates the selected vehicle/product pair. |
| P0-5 provider status overclaim | ACCEPT | Provider rows now separate evidence state, connection state, tested inputs and documented capabilities. Auto Ways has no tested input; vPIC is the only real tested VIN source in the demo matrix. |
| P0-6 misleading product references | ACCEPT | Replaced real-looking/wrong-type references and EANs with explicit synthetic `SAMPLE-*` values. |
| P1-1 client-trusted prices | ACCEPT | Order input contains product ID and quantity only. FastAPI loads catalogue prices and calculates all totals server-side. |
| P1-2 client-specific conflict code | ACCEPT | Removed client VIN/model constants. Conflict detection now compares normalized evidence generically; the neutral canned scenario is isolated behind a demo endpoint. |
| P1-3 open roles/global garage | ACCEPT | Added HTTP Basic role boundaries for customer/garage and admin/operations routes, user-scoped garage storage and duplicate protection. This is prototype authentication, not the proposed production identity system. |
| P1-4 saved year bug | ACCEPT | Fixed year parsing and added regression coverage. |
| P1-5 demo mode default true | ACCEPT | `DEMO_MODE` now defaults to `false` and must be explicitly enabled. |
| P1-6 actual plate on homepage | ACCEPT | Replaced with neutral Portuguese-format placeholder `AB-12-CD`. |
| P1-7 delivery looked live | ACCEPT | Product/list/cart delivery copy is marked `ESTIMATIVA DEMO`; GLS remains not configured. |
| P1-8 empty cart charged shipping | ACCEPT | Empty subtotal produces zero shipping and zero total. |
| P1-9 irrelevant provider trace | ACCEPT | VIN and plate cascades are separate. VIN includes the genuinely tested vPIC adapter; plate-only providers do not appear in VIN traces. |
| P1-10 unfinished admin ambiguity | ACCEPT | Unimplemented admin modules carry `NOT BUILT / PLACEHOLDER`. |

### CMS boundary added after honesty fixes

Strapi with PostgreSQL owns editorial data. The storefront currently renders the homepage hero and product editorial; generic pages, navigation/footer, FAQs, SEO, banners and promotions are modelled but not yet rendered. FastAPI retains vehicle identity, provider orchestration, fitment, K-Type/catalogue mapping, live price/stock, cart/order rules and future Primavera/GLS/supplier integrations. Public CMS responses carry `EDITORIAL_ONLY`; product editorial endpoints intentionally exclude price, stock, fitment and orders.

## Claude demo re-review round 2 response — 2026-10-06

| Blocker | Classification | Response |
|---|---|---|
| B1 public CMS admin/password leak | ACCEPT | Replaced broad population with explicit media/relation field allowlists, recursively strips audit/password/token keys, added verifier coverage, checked the live endpoint and rotated the local editor password. |
| B2 unwired CMS capabilities presented as live | ACCEPT | Architecture, README and demo script now distinguish `RENDERED NOW` (homepage hero/product editorial) from `MODELLED · NOT RENDERED` (pages/navigation/footer/FAQ/SEO/banners/promotions). |
| B3 credentials in browser bundle | ACCEPT | Removed `NEXT_PUBLIC_*_AUTH`. Protected calls use an HTTP-only signed session and same-origin Next.js BFF; FastAPI credentials are server-only. Public bundle scan is clean. The UI still states this is a local prototype login, not production identity. |
| B4 garage deduplication | ACCEPT | Added normalized manual-candidate upsert when VIN/plate are absent, plus a regression test. |
