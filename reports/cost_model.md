# Pre-TecDoc lookup cost model

Date: 2026-10-05. Prices are provider-advertised and exclude VAT unless stated. Success-rate economics remain unknown until 10–20 independently verified Portuguese vehicles are tested.

## Direct request cost

| Route | € / request used | 1,000 | 10,000 | 50,000 | 100,000 |
|---|---:|---:|---:|---:|---:|
| Local structural VIN | 0 | 0 | 0 | 0 | 0 |
| Public vPIC | 0 | 0 | 0 | 0 | 0 |
| Self-hosted vPIC | 0 API fee | infra only | infra only | infra only | infra only |
| Autofrance public VIN | 0 published API fee at documented 10/min limit | 0 API fee* | 0 API fee* | 0 API fee* | 0 API fee* |
| Matricula.co.pt public rate | 0.20 | 200 | 2,000 | 10,000 | 20,000 |
| Openapi PT-car PAYG | 0.40 | 400 | 4,000 | 20,000 | 40,000 |
| Openapi PT-car published volume tiers | 0.37 / 0.33 / 0.30 / 0.28 / 0.24 / 0.18 by annual package | requires matching annual plan | requires matching annual plan | requires matching annual plan | requires matching annual plan |
| TelePeças | unknown | quote | quote | quote | quote |
| Tips4y | unknown | quote | quote | quote | quote |
| TecAlliance | unknown | quote | quote | quote | quote |

## Cost per successful ENGINE result

Formula: `total provider spend / number of independently correct ENGINE-or-better results`.

| Provider | Correct ENGINE results in PT campaign | Cost / successful ENGINE result |
|---|---:|---:|
| Public vPIC | 0 / 1 | Undefined — no ENGINE result |
| Self-hosted vPIC | 0 / 1 | Undefined — no ENGINE result |
| Local parser | 0 / 1 | Undefined — no identity result |
| Autofrance | Unknown correctness / 1 ENGINE-level response | €0 request cost, but cost per **correct** engine cannot be claimed until the 3008-vs-5008 conflict is resolved |
| Plate providers | Not tested | Cannot calculate |

## Routing scenarios

1. **FREE FIRST:** local validation → licensed free VIN provider. vPIC observed ENGINE success is 0/1. Autofrance returned ENGINE-level data but is research-only, has no existence check and cannot be counted as a production success.
2. **CHEAP MATRÍCULA + MANUAL CONFIRMATION:** `€0.20 × paid plate calls`; engine completion rate and catalogue mapping rate are unknown. At 10k calls the request ceiling is €2,000 before cache; it is not yet a fitment cost.
3. **CACHE FIRST:** disabled for commercial providers until written terms confirm caching/storage. No saving is claimed.
4. **MULTI-PROVIDER FALLBACK:** expected cost is `Σ(reach probability × tier call price)`. Reach probabilities are not yet measured, so a numeric total would be fabricated.
5. **PREMIUM LOOKUP:** TecAlliance quote and Portugal benchmark required.

\* Autofrance commercial reuse, sustained-volume permission and brand coverage are unverified. A zero public endpoint fee is not a production contract.

## Decision rule

Optimize cost only after measuring: correct engine rate, exact variant rate, ambiguity, false-confident rate, and bridge-to-catalogue rate. A cheaper plate response that cannot reach a catalogue ID may have a higher real cost per successful purchase.
