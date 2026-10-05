# JOINT VALIDATION: Claude's DRAFT position (NOT the completed joint file)

`collaboration/JOINT_VALIDATION_COMPLETE.md` does **not** exist yet. It requires Codex's agreement and the minimum evidence below. This draft is Claude's side only; Codex must review, challenge and sign.

## Minimum-evidence checklist (2026-10-05)
| Requirement | Status |
|---|---|
| Real PT VIN tested | DONE (vPIC BASIC; Autofrance ENGINE + K-Type) |
| Real PT matrícula tested | **NOT DONE**: credential-blocked (Matricula.co.pt, TelePeças auth errors; Openapi/Autoways need signup) |
| ≥2 independent vehicle-data sources compared | PARTIAL: vPIC (make) + Autofrance (retailer, TecDoc-style) + VIN-structure analysis; neither independent of TecDoc for model |
| Returned K-Type independently cross-checked | DONE for K-Type identity (Autodoc + Schaeffler); VIN→K-Type mapping PARTIAL |
| Provider costs documented | DONE (see price tables) |
| Licensing uncertainty documented | DONE |
| partslink24 role documented | DONE (ToS bars backend integration; manual validation) |
| Direct TecDoc route documented | DONE (`reports/tecdoc_direct_access_strategy.md`) |
| Client vehicle conflict resolved or marked unresolved | LIKELY RESOLVED toward 3008 (2 independent lines); pending partslink24/plate/certificate |
| Raw evidence saved | DONE |

## Claude's proposed positions (for Codex to accept/contest)
- **Best matrícula route:** UNDETERMINED (nothing tested live). Best *documented* PT plate → K-Type + kW + engine code + VIN: **Autoways** (vendor's OpenAPI spec, free token) and **Tips4y** (TecDoc Vehicle ID, ≈€0.10/lookup, bundled with its TecDoc catalogue). Cheap identity-only: Openapi / Matricula.co.pt.
- **Best VIN route:** UNDETERMINED for production. Autofrance proves VIN→ENGINE+K-Type is achievable and is cross-checked for the client VIN (3008 likely) but is a storefront backend (research only; answers fake VINs confidently). Lawful candidates: **Autoways VIN-DECODER (country=PT)**, Vincario, TecAlliance.
- **Best K-Type bridge:** user-confirmed vehicle now; provider K-Type only after cross-check; TecDoc VRM/VIN later.
- **Fitment status:** NOT SOLVED.
- **Pre-TecDoc architecture:** `reports/pre_tecdoc_decision_tree.md` + `docs/vehicle-to-catalogue-bridge.md`, with MODEL_CONFLICT handling.
- **Known pricing:** see `reports/DIRECT_TECDOC_AND_RESELLER_COMPARISON.md`.
- **Blockers:** plate-provider credentials; partslink24 VIN result; second K-Type source; TecAlliance quote.
- **Fahad must provide:** partslink24 VIN result + original screenshot/registration certificate for client_001; 10–20 PT cars; plate-software name; TecDoc quote; partslink24 rights.
- **David can start:** interfaces, precision/verdict model, MODEL_CONFLICT confirm flow, garage store, search-by-reference, Primavera boundary.

Codex sign-off: ______ (pending)
