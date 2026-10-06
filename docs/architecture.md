# Provider-independent architecture

## Boundaries

1. `VehicleIdentityProvider`: VIN or registration to candidate vehicles.
2. `CatalogueVehicleProvider`: canonical vehicle to catalogue vehicle ID/KType candidates.
3. `CatalogueProvider`: product/reference search.
4. `FitmentProvider`: vehicle-product evidence.
5. `InventoryProvider` and `SupplierProvider`: internal/supplier availability.
6. `ERPProvider`: stock, prices, customers, orders and invoices only.

Customer code consumes only the canonical model and customer fitment state. It does not consume a provider response directly.

## Safety gates

- Precision is ordinal: `BASIC < MODEL < ENGINE < EXACT_VARIANT`.
- Missing fields remain null. Normalisation does not fabricate values.
- Identity and fitment are separate decisions.
- `COMPATIBLE` requires ENGINE+ identity, a licensed catalogue MATCH, no NO_MATCH, and no unresolved restriction.
- EU VIN checksum mismatch is a warning, not a rejection.
- Provider cache keys include provider name, provider version, route and input.
- Missing credentials return `NOT_CONFIGURED`; no adapter fabricates a response.
- Provider selection comes from environment configuration, not customer-facing logic.

## Current implementation status

- Core models and safety gates: **PARTIALLY VERIFIED** through unit tests.
- Provider interfaces and mock swap: **PARTIALLY VERIFIED**.
- External providers: **WAITING FOR CREDENTIALS** or **NOT VERIFIED**.
- Test catalogue: **MOCK ONLY** and search-mechanics-only.
