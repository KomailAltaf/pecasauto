# Phase 1 development plan — Portuguese automotive ecommerce

Status: implementation-readiness draft. Provider choice and fitment licence remain provisional. Engineering-day ranges are planning estimates, not commitments; they assume two experienced engineers, prompt client feedback and usable third-party credentials.

## Objective

A Portuguese customer identifies a vehicle, selects a compatible launch-category product and completes an order without staff manually performing the whole lookup. The storefront never consumes TecDoc, Autoways, TIPS4Y, Matricula.co.pt or TelePeças payloads directly.

## Architecture

```text
Next.js / React storefront + admin
              ↓ HTTPS
FastAPI application API
  ├─ identity orchestration
  ├─ catalogue/search
  ├─ fitment safety
  ├─ cart/checkout/orders
  └─ customer garage
              ↓
PostgreSQL — platform records and provenance
Redis — optional short-lived jobs/rate limits/cache only when provider terms allow
              ↓
Provider adapters
  ├─ vehicle lookup: Autoways / TIPS4Y / Matricula / TelePeças / TecAlliance
  ├─ catalogue + fitment: licensed provider, TecDoc later
  ├─ operations: Primavera/Cegid
  ├─ logistics: GLS
  └─ payments: provider to be selected
```

Redis is justified only for background-job coordination, rate limiting and legally permitted short-lived caching. PostgreSQL remains the system of record for the platform.

## Services

- `web-storefront`: Portuguese-first Next.js/React customer application.
- `web-admin`: catalogue, import, order, customer and exception-review UI; may share the Next.js application initially.
- `api`: FastAPI business/API layer.
- `worker`: imports, notifications, provider retries and synchronization jobs.
- `postgres`: users, vehicles, products, fitments, inventory snapshots, carts, orders and provenance.
- `redis` optional: job queue/rate-limit state, never unapproved permanent provider-data storage.
- object storage: licensed product images/import files/log exports.

## Database

Core entities:

- `vehicles`: canonical nullable vehicle identity and internal ID.
- `vehicle_external_ids`: provider, external ID type, KType/provider ID, provenance.
- `vehicle_identity_observations`: raw-field references, precision, status, timestamps; retention policy required.
- `saved_vehicles`: customer-confirmed garage profile and verification status/source.
- `brands`, `categories`, `products`, `oe_references`.
- `fitments`: product↔vehicle/catalogue-ID relationship, source, verdict, restrictions and verification date.
- `inventory`, `prices`, `supplier_offers`.
- `customers`, `addresses`, `carts`, `cart_lines`, `orders`, `order_lines`, `payments`, `shipments`, `returns`.
- `import_jobs`, `integration_runs`, `provider_health`, `audit_log`.

VIN and matrícula access must be restricted and retained only under an agreed GDPR policy. Provider payloads are not persisted when storage rights are unknown.

## API endpoints

Indicative internal API, subject to final domain review:

```text
POST /v1/vehicles/identify/registration
POST /v1/vehicles/identify/vin
GET  /v1/vehicles/manual/makes
GET  /v1/vehicles/manual/models
GET  /v1/vehicles/manual/engines
POST /v1/vehicles/confirm
POST /v1/garage/vehicles
GET  /v1/garage/vehicles
DELETE /v1/garage/vehicles/{id}

GET  /v1/catalogue/categories
GET  /v1/catalogue/products
GET  /v1/catalogue/products/{slug}
GET  /v1/catalogue/search?q=
POST /v1/fitment/check

POST /v1/cart/items
GET  /v1/cart
POST /v1/checkout
GET  /v1/orders/{id}
GET  /v1/orders/{id}/tracking

POST /v1/admin/imports
GET  /v1/admin/integration-runs
GET  /v1/admin/compatibility-review
```

Provider names and credentials never appear in public API contracts.

## Customer vehicle flow

1. Customer supplies matrícula, VIN, manual selection or OE/reference.
2. Identity provider returns one or more candidates.
3. Platform normalizes fields and records provenance.
4. Existing unresolved conflict produces a confirmation step, not an automatic vehicle.
5. KType/provider catalogue ID is used when present.
6. Without KType, canonical make/model/generation/year/engine/code/power is mapped through `CatalogueVehicleProvider`.
7. Ambiguity asks exactly one useful question.
8. Customer-confirmed profile is stored in the garage, subject to provider-data rights.
9. Products receive a fitment verdict only from `FitmentProvider`.

## Search and catalogue

- Search by description, internal SKU, EAN, manufacturer reference and OE reference.
- Initial categories: filters, brake pads and brake discs.
- Initial 83 brands only where licensed catalogue/product data is available.
- Product result includes brand, reference, IVA-inclusive price, stock/delivery and compatibility state.
- Search index starts with PostgreSQL full-text/trigram if adequate; OpenSearch/Typesense/Meilisearch remains a measured later decision.

## Fitment

Internal source verdicts: `MATCH`, `NO_MATCH`, `UNKNOWN`, `CONFLICT`.

- `Compatível com o seu veículo` requires a trusted licensed `MATCH`, sufficient vehicle precision, no contradiction and no unresolved restrictions.
- Non-authoritative or restricted results show `Confirmar compatibilidade`.
- Missing evidence shows `Compatibilidade precisa de verificação`.
- The platform does not infer fitment from OE search, text similarity or vehicle identity alone.

## Vehicle garage

Saved profile includes internal vehicle ID, matrícula, VIN, make, model, generation, year, engine, engine code, power, fuel, KType, provider, verification status/source and timestamp.

Customer-confirmed profiles are separate from provider caches. Provider-derived profiles are reusable only when verified contractual storage rights allow it.

## Admin

- product/category/brand management;
- stock and price view;
- orders/customers;
- imports and row-level errors;
- provider health and integration runs;
- disputed vehicle/fitment queue;
- catalogue gaps and missing images;
- manual validation evidence references;
- audit log.

## Checkout, payment and GLS

- IVA-inclusive pricing and address validation.
- Payment intent created server-side; webhook is authoritative.
- Idempotent order creation prevents duplicate payment/order records.
- GLS label/tracking integration after credentials and service contract.
- Order state transitions are explicit and audited.
- Primavera order/invoice synchronization may remain manual in early Phase 1 if its API is not ready.

## Logging and monitoring

- structured request/job logs without secrets;
- correlation ID across lookup, checkout and ERP/shipping calls;
- provider latency, error, ambiguity and precision metrics;
- false-confident/conflict rate;
- integration health and circuit-breaker state;
- checkout/payment/GLS/ERP alerts;
- raw vehicle identifiers redacted or access-controlled.

## Testing

- unit tests for normalization, provider parsing, precision, fitment and rights policies;
- stored-response contract tests for each credentialed provider;
- provider sandbox/live smoke command using the real PT case;
- 10–20 independently verified PT vehicles before provider choice;
- 100–500 PT vehicles before production trust in automatic identification;
- payment/GLS webhook and idempotency tests;
- import rollback/data-quality tests;
- responsive/browser/accessibility testing;
- load and failure testing for search, provider timeouts and checkout.

## Deployment

- separate development, staging and production environments;
- managed PostgreSQL; Redis only if the worker/rate-limit design needs it;
- secrets in platform secret manager, never source control;
- migrations run through CI/CD with backup/rollback;
- provider and payment sandbox in staging;
- CDN/object storage for permitted images;
- monitoring, error tracking, uptime checks and audited admin access.

## Engineering effort

Ranges include implementation and direct tests, not provider contracting, client delays or full data cleansing.

| Module | Size | Indicative engineering days | Dependencies |
|---|---|---:|---|
| Architecture, environments, CI/CD, security baseline | Medium | 4–7 | hosting choices |
| Design system and responsive storefront shell | Medium | 5–8 | brand/name/content |
| Vehicle identity API and provider orchestration | Large | 6–10 | one real provider credential/schema |
| Manual selector and confirmation UX | Medium | 3–5 | licensed vehicle taxonomy/catalogue |
| Vehicle garage and verification/provenance | Medium | 3–5 | GDPR/storage policy |
| Catalogue/product/brand/category model | Large | 6–10 | catalogue data and rights |
| Search and OE/reference lookup | Medium | 4–7 | product/reference imports |
| Fitment service and customer states | Large | 5–9 | licensed fitment source |
| Product listings/detail/alternatives | Medium | 5–8 | catalogue/images/prices |
| Cart, checkout and customer accounts | Large | 6–10 | payment and business rules |
| Payment integration | Medium | 3–5 | provider onboarding/credentials |
| GLS shipping and tracking | Medium | 3–6 | GLS API/service credentials |
| Admin and import tooling | Large | 7–12 | sample real imports |
| Primavera Phase 1 boundary/manual handoff | Small–Medium | 2–4 | version/workflow inspection |
| Deeper Primavera automation | Large / Phase 2 | 6–12+ | API/modules/data mapping |
| Logging, monitoring, analytics and SEO | Medium | 4–7 | deployment environment |
| End-to-end QA, mobile QA and launch hardening | Large | 7–12 | stable integrations/data |

The combined Phase 1 is approximately **73–125 engineering days** before contingency if every listed customer/admin/commerce function is included. With two engineers and strict scope, parallel work may fit an approximately eight-week programme, but provider onboarding, catalogue readiness and client decisions are external critical-path dependencies. A reduced launch must reduce modules rather than compress validation.

## Development sequence

1. Foundation: FastAPI/Next.js/PostgreSQL, auth, CI/CD, canonical data model.
2. Identity: credentialed provider adapter, manual fallback, garage and conflict workflow.
3. Catalogue: initial imports, search, categories/products and catalogue vehicle mapping.
4. Fitment: licensed source, restrictions, admin review and customer messaging.
5. Commerce: cart, checkout, payment, orders, notifications.
6. Operations: GLS, controlled Primavera handoff, admin/imports.
7. Hardening: PT benchmark, mobile/E2E/security/load testing, monitoring and launch preparation.

## Blocking decisions

- production matrícula/VIN provider and contractual rights;
- licensed catalogue/fitment source;
- authoritative resolution of `CG-17-GC` / `VF3MCYHZUPS034433`;
- catalogue files/83-brand availability;
- payment provider and Portuguese methods;
- GLS credentials/service rules;
- Primavera version/modules/workflow;
- GDPR retention and support/returns processes.
