# Executive Findings — Portugal-only evidence round

Generated: 2026-10-05

## Scope

The provider-independent safety foundation is implemented and tested. Public and self-hosted vPIC plus a research-only European storefront endpoint were called with the Portuguese client VIN. Commercial plate/VIN, TecDoc, partslink24, supplier and Primavera APIs were not available. No provider is production-verified.

## VERIFIED

- The repository now contains executable models, provider boundaries, orchestration, fixtures, tests, benchmark tooling and generated reports.
- The local git baseline exists.
- Synthetic fixtures are excluded from accuracy metrics by code and test.
- The client VIN `VF3MCYHZUPS034433` passes structural EU validation even though its North-American checksum signal is false.
- Test catalogue records are labelled `MOCK ONLY` and `SEARCH MECHANICS ONLY`.

## PARTIALLY VERIFIED

- Precision levels and fitment hard gates behave as specified in unit tests.
- Portuguese plate normalization covers the four specified historical/current patterns.
- Provider swapping, error isolation, circuit threshold and provider-scoped cache work in local tests.
- The local VIN parser validates structure only. It does not identify make/model/engine/variant.
- Public vPIC returned Peugeot only for the client VIN; self-hosted vPIC reproduced the same BASIC-only result.
- The research-only Autofrance endpoint returned ENGINE-level data and KType 130708. Public catalogue references cross-check the KType identity as a 3008; the VIN→KType assignment remains partial and conflicts with the client-provided 5008.
- Autofrance is excluded from the production cascade because commercial rights are unknown and the endpoint does not verify VIN existence.

## NOT VERIFIED

- Portuguese-market accuracy of any free, commercial or client vehicle-identification provider.
- Manual vehicle taxonomy backed by real fitment data.
- OEM search against a licensed production catalogue.
- Vehicle-product fitment for any real product.
- Primavera integration depth and supplier-feed quality.

## WAITING FOR CREDENTIALS

- TelePeças API.
- Matricula.co.pt API/terms.
- TecAlliance/TecDoc services and licence.
- partslink24 programmatic/API/export rights (manual client access is confirmed).
- Existing client vehicle software identification and export/API details.
- Primavera/Cegid version, modules and API credentials.

## MOCK ONLY

- `MockIdentityProvider` output.
- `fixtures/test_catalogue.json`.
- Stored mock raw identity response.
- Generated mock plumbing counts. These are excluded from provider accuracy.

## Benchmark state

- Eligible non-synthetic fixture rows: 0.
- Portuguese campaign inputs (including client-provided): 1.
- Independently verified Portuguese fixture rows: 0.
- Stage-1 requirement: 10-20 real, independently verifiable vehicles plus at least one VIN and one plate provider.
- Current benchmark therefore validates mechanics only, not provider fitness.

## Cost state

Cost scenarios exist for 1k/10k/50k/100k lookups and both cache policies. Known free request costs are recorded; commercial costs remain unknown or vendor-advertised. Cost-per-correct-engine and cost-per-exact-variant cannot be calculated until verified PT ground truth and benchmark evidence exist.

## Next evidence gate

Obtain written rights/credentials and a 10-20 vehicle ground-truth set. Rerun the same commands without changing the customer-facing architecture.
