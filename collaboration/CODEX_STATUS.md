# Codex status — Portugal-only real validation campaign

Date: 2026-10-05. Total money spent: **€0**. Production-score sample: **n=0 independently verified Portuguese vehicles**. Campaign inputs: one client-provided PT case. Automated test suite: **46 passing**.

| Provider | Actual test | Raw evidence | Result | Precision | Spend | Blocker |
|---|---|---|---|---|---:|---|
| Local VIN parser | Yes, client VIN | Deterministic code/tests | Structure valid; EU checksum non-blocking | No identity | €0 | Not a data source |
| NHTSA vPIC public | Yes, client VIN | `reports/raw_evidence/vpic_public_*.json` | Peugeot only; model/engine empty; errors 1,8,400 | BASIC_ONLY | €0 | US-intended dataset; not PT fit for purpose |
| Self-hosted vPIC | Yes, official NHTSA DB locally | `reports/raw_evidence/vpic_self_hosted_*.json` | Same result as public vPIC | BASIC_ONLY | €0 API | Same dataset, no coverage gain |
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
- Provider terms/cache policy; unknown terms disable caching.
- Manual one-more-field fallback, disagreement review, false-confident status.
- Vehicle→catalogue bridge methods; text match can never claim compatibility.
- KType `130708` identity cross-checked as 3008; VIN→KType remains partial and the original 5008 label remains disputed.
- Customer-confirmed garage separate from provider cache.
- Real matrix, comparison, cost model, ground-truth research, official-route research, provider contacts and final strategy.
- 46 unit/provider/normalization/fitment/cost tests passing.

## Remaining human/external blockers

- Resolve 3008-vs-5008 using permitted partslink24/OEM/registration-document evidence.
- Matricula.co.pt free account and real plate payload.
- TelePeças/Tips4y/Openapi/Vincario credentials or trials.
- 10–20 independently verified PT vehicles, then 100–500 PT-only benchmark.
- Written production/caching/reuse rights for Autofrance and commercial providers.
- Licensed fitment source before automatic compatibility.
