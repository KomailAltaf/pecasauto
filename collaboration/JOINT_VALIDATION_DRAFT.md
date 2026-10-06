# Joint validation draft — implementation readiness

Date: 2026-10-05. Status: **DRAFT — NOT FINAL COMPLETION**.

## Prototype implementation update

The PeçasAuto local prototype is runnable and demonstrates the customer and technical boundaries without changing the evidence status below. It is not a final provider recommendation and does not resolve the client vehicle conflict.

- Next.js / React / TypeScript frontend
- FastAPI / SQLAlchemy / SQLite demo backend
- visible provider trace, source labels and candidate confirmation
- saved garage, catalogue, product, cart and demo checkout
- provider matrix and architecture view
- Primavera, partslink24, TecDoc and GLS kept behind their intended boundaries

## Proven

- Provider-independent vehicle, catalogue-vehicle, fitment, inventory, supplier and ERP interfaces exist.
- Five candidate vehicle adapters return `NOT_CONFIGURED` when required credentials/contracts are absent.
- Autoways VIN was tested live with the client VIN and returned 3008, 1.5 BlueHDi 130, engine code `YHZ_DV5RC`, 96 kW and K-Type `130708`. This remains disputed against the client-provided 5008 expectation. The documented Portuguese plate route returned HTTP 404 for this account/product.
- One-command provider testing prints raw and normalized output without persisting it by default.
- Runtime provider selection is environment-driven.
- KType and canonical-field catalogue-bridge paths exist.
- Manual one-more-detail state and customer-confirmed garage models exist.
- Fitment cannot display `Compatible` without a trusted licensed match.
- Primavera is isolated to stock, prices, customers, orders and invoices.
- partslink24 has no scraping/programmatic implementation.
- The Portugal-only benchmark gate and evidence status remain intact.

## Provisional

- Autoways is now partially tested: the VIN route works and is technically rich; the matrícula route/account remains unresolved and production/data rights still need confirmation.
- TIPS4Y may offer the cleanest PT plate→TecDoc vehicle bridge, but its contracted API shape and price must be supplied.
- Matricula.co.pt is a low-cost identity candidate; it may not return a KType or fitment-grade engine variant.
- TelePeças may supply identity plus catalogue identifiers, but endpoint/package rights remain unknown.
- TecAlliance/TecDoc remains the premium catalogue/fitment baseline.

## Blocked

- No real Portuguese matrícula provider response exists for `CG-17-GC`.
- The 3008/5008 conflict for `VF3MCYHZUPS034433` is unresolved by authoritative Portuguese/OEM evidence.
- Production fitment is not configured.
- Primavera version/API/modules are uninspected.
- GLS/payment credentials and final providers are absent.
- Provider caching/storage rights and GDPR retention policy are not finalized.

## Access Komail needs

1. One credential or free-trial account for Autoways, TIPS4Y, Matricula.co.pt or TelePeças.
2. Permitted partslink24 screenshot/output or registration document for the client vehicle.
3. Ten to twenty independently verified Portuguese vehicle cases.
4. TecAlliance/TecDoc and TIPS4Y commercial/API responses.
5. Primavera version/modules/API demonstration.
6. GLS and selected payment-provider onboarding details.

## Can start now

- Next.js/FastAPI/PostgreSQL project foundation.
- Canonical vehicle/product/catalogue/provenance schema.
- Public API contracts independent of providers.
- Manual vehicle selector shell and conflict/confirmation workflow.
- Customer garage, authentication and accounts.
- Product/category/brand/admin foundations using clearly labelled development data.
- Cart/order domain, logging, monitoring, CI/CD and test harnesses.

## Must wait for credentials or decisions

- Selecting the production vehicle provider.
- Real plate/VIN adapter contract tests.
- Automatic KType mapping confidence.
- Licensed product fitment and customer compatibility claims.
- Production catalogue import and images.
- Automated Primavera, GLS and payment workflows.
- Final delivery commitment tied to external onboarding.

## Immediate credential test

```bash
python3 -m tools.test_provider --provider autoways --plate CG-17-GC
python3 -m tools.test_provider --provider autoways --vin VF3MCYHZUPS034433
```

Replace `autoways` with `tips4y`, `matriculapt`, `telepecas` or `tecalliance` after adding the corresponding environment variables. A provider response is evidence, not automatic fitment proof.
