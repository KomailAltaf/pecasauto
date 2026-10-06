# Codex status — Portugal-only real validation campaign

Date: 2026-10-06. Total money spent: **€0**. Production-score sample: **n=0 independently verified Portuguese vehicles**. Campaign inputs: one client-provided PT case. Automated test suite: **76 Python tests + 3 frontend tests passing**.

| Provider | Actual test | Raw evidence | Result | Precision | Spend | Blocker |
|---|---|---|---|---|---:|---|
| Local VIN parser | Yes, client VIN | Deterministic code/tests | Structure valid; EU checksum non-blocking | No identity | €0 | Not a data source |
| NHTSA vPIC public | Yes, client VIN | `reports/raw_evidence/vpic_public_*.json` | Peugeot only; model/engine empty; errors 1,8,400 | BASIC_ONLY | €0 | US-intended dataset; not PT fit for purpose |
| Self-hosted vPIC | Yes, official NHTSA DB locally | `reports/raw_evidence/vpic_self_hosted_*.json` | Same result as public vPIC | BASIC_ONLY | €0 API | Same dataset, no coverage gain |
| Autoways VIN | No verified provider call/evidence | No raw provider response | Public schema/documentation only; no vehicle result may be attributed to Auto Ways | NOT TESTED | €0 | Valid credential and permitted test required |
| Autoways matrícula | No verified provider call/evidence | No raw provider response | Public schema/documentation only; no Portuguese plate result exists | NOT TESTED | €0 | Confirm contracted Portugal endpoint and test with access |
| Autofrance research VIN | Yes, client VIN | `reports/raw_evidence/autofrance_*` | Peugeot 3008 SUV, 1.5 BlueHDi 130, 96 kW, KType 130708 | ENGINE_LEVEL / PARTIAL | €0 | Research-only, no existence check, client model disputed; excluded from production cascade |
| Matricula.co.pt | Access test only | `matriculapt_CG-17-GC_access_response.xml` | Username required; no vehicle result | NOT_TESTED | €0 | Free test account required |
| TelePeças | OAuth access test only | `telepecas_auth_access_response.json` | Client credentials required | NOT_TESTED | €0 | Seller/integrator OAuth + contract |
| Openapi PT-car | Documentation | — | PT plate fields/pricing documented | NOT_TESTED | €0 | Account/token and terms |
| Tips4y | Documentation | — | PT plate/VIN→KType/TecDoc bridge documented | NOT_TESTED | €0 | Commercial access |
| partslink24 | Client access confirmed, no output supplied | — | Manual VIN/OE role only | NOT_TESTED | €0 | Fahad output + written integration rights |
| TecAlliance | Documentation | — | Premium VIN/VRM→KType/NType + catalogue route | NOT_TESTED | €0 | Quote, contract, credentials |

## Implemented

- Portugal-only scoring gate: `country=PT` and `portuguese_market_verified=true`; client expectation remains outside production score.
- Real vPIC and Autofrance adapters based on stored responses.
- Configurable VIN and plate cascades that continue past access blockers.
- Free vPIC now runs first for VIN; commercial providers follow when its result is below ENGINE precision.
- `.env`-driven Auto Ways/TIPS4Y/Matricula.co.pt/TelePeças adapters and `tools.test_vehicle` CLI are ready for credentials.
- Provider terms/cache policy; unknown terms disable caching.
- Manual one-more-field fallback, disagreement review, false-confident status.
- Vehicle→catalogue bridge methods; text match can never claim compatibility.
- Research-only evidence previously associated K-Type `130708` with a 3008, but this is not attributed to Auto Ways, is not exposed in the customer flow and does not settle the client vehicle.
- Customer-confirmed garage separate from provider cache.
- Real matrix, comparison, cost model, ground-truth research, official-route research, provider contacts and final strategy.
- 76 unit/provider/API/normalization/fitment/cost/CLI tests passing.

## Full-stack PeçasAuto prototype

- Next.js / React / TypeScript customer application in `apps/web`.
- FastAPI / Pydantic / SQLAlchemy API in `apps/api`.
- SQLite prototype persistence for FastAPI; Strapi runs on PostgreSQL. SQLAlchemy remains PostgreSQL compatible.
- Clickable journey: four search routes, explicit provider-unavailable behavior, a separate neutral canned conflict, manual confirmation, saved garage, catalogue, product, cart and demo checkout.
- Strapi CMS owns editorial content; FastAPI owns operational truth. Draft/publish/refresh, product editorial and page-builder behavior are verified against PostgreSQL.
- Public Strapi responses use explicit allowlists and do not expose admin audit/password/token fields.
- Protected browser calls use an HTTP-only signed local session and server-side BFF; FastAPI credentials are absent from public bundles.
- Garage upsert covers confirmed candidates with and without VIN/registration.
- Internal provider matrix and architecture pages.
- `REAL_TESTED`, `DEMO`, `MOCK`, `DOCUMENTED_CAPABILITY`, `WAITING_FOR_ACCESS`, `NOT_CONFIGURED` and `RESEARCH_ONLY` are explicit evidence states.
- Fitment now requires a validated catalogue bridge plus licensed, terms-verified evidence before `COMPATIBLE`.
- All 12 frontend routes compile in the production build; the seven primary demo routes return HTTP 200 locally.
- Demo guide: `reports/DAVID_DEMO_SCRIPT.md`.

## Remaining human/external blockers

- Resolve 3008-vs-5008 using permitted partslink24/OEM/registration-document evidence.
- Matricula.co.pt free account and real plate payload.
- TelePeças/Tips4y/Openapi/Vincario credentials or trials.
- 10–20 independently verified PT vehicles, then 100–500 PT-only benchmark.
- Written production/caching/reuse rights for Autofrance and commercial providers.
- Licensed fitment source before automatic compatibility.
