# Portugal Auto Validation Lab

Local workspace for validating Portuguese vehicle-identification providers, automotive catalogue sources, and fitment accuracy before the platform architecture is finalised.

## Structure

- `app/` — local validation interface and orchestration
- `providers/` — replaceable VIN, matrícula, catalogue, fitment, inventory, and supplier adapters
- `benchmarks/` — benchmark runners and scoring logic
- `fixtures/` — sanitised test vehicles and expected results
- `reports/` — generated comparison reports
- `docs/` — research and technical documentation
- `tests/` — automated tests
- `collaboration/` — Komail, Codex, Claude, and David hand-off documents

No production integrations, credentials, or client data should be committed here.
