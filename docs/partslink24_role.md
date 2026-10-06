# partslink24 role

The implementation boundary is `Partslink24Boundary`. It exposes no HTTP calls and performs no browser automation.

Three roles remain separate:

1. **Manual validation:** Fahad/staff use the existing account to confirm a VIN/vehicle or disputed result.
2. **OE reference source:** staff use genuine manufacturer catalogues to validate OE references.
3. **Future programmatic integration:** disabled until written API, integration, display, caching and storage rights are granted.

## 1. Manual validation source — usable now within the existing account

- Run VIN manually.
- Confirm model, production context, engine code/power and genuine catalogue path.
- Capture permitted screenshots/exports as benchmark ground truth.
- Cross-check OE references and chassis restrictions.

Status: **DOCUMENTED CAPABILITY / HUMAN OUTPUT REQUIRED**.

## 2. OE / genuine-part reference source

Useful for validating genuine manufacturer references and the OEM side of cross-reference mappings. It does not automatically provide an aftermarket multi-brand fitment licence.

Status: **DOCUMENTED CAPABILITY; PACKAGE-SPECIFIC**.

## 3. Programmatic backend source

Do not implement without written confirmation covering API/webservice, account package, automated access, ecommerce display, export, caching, storage and retention. Browser automation or scraping is not a substitute for permission.

Status: **WAITING FOR WRITTEN RIGHTS**.

Exact questions are in `docs/provider_contact_templates/partslink24_questions.md`.
