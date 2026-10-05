# Provider-independent architecture

## Boundaries

1. `VehicleIdentityProvider`: VIN or registration to candidate vehicles.
2. `CatalogueProvider`: product/reference search.
3. `FitmentProvider`: vehicle-product evidence.
4. `InventoryProvider` and `PricingProvider`: downstream commercial state, including Primavera.

Customer code consumes only the canonical model and customer fitment state. It does not consume a provider response directly.

## Safety gates

- Precision is ordinal: `BASIC < MODEL < ENGINE < EXACT_VARIANT`.
- Missing fields remain null. Normalisation does not fabricate values.
- Identity and fitment are separate decisions.
- `COMPATIBLE` requires ENGINE+ identity, a licensed catalogue MATCH, no NO_MATCH, and no unresolved restriction.
- EU VIN checksum mismatch is a warning, not a rejection.
- Provider cache keys include provider name, provider version, route and input.

## Current implementation status

- Core models and safety gates: **PARTIALLY VERIFIED** through unit tests.
- Provider interfaces and mock swap: **PARTIALLY VERIFIED**.
- External providers: **WAITING FOR CREDENTIALS** or **NOT VERIFIED**.
- Test catalogue: **MOCK ONLY** and search-mechanics-only.

