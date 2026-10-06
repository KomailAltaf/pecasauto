# FINAL VERDICT (2026-10-06): READY TO SHOW DAVID

All original security/CMS blockers are resolved and the 15 final approval checks pass. The approval covers the demo **as it will be shown today** (no live provider connected). Honest framing for David: the flow and safety rules are real; provider data, products, prices, stock, fitment and payments are demo or waiting for access.

## Final approval checks (independently re-run)
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | No default/fallback session secret | PASS | Repo-wide search for the old defaults (`local-development-session-secret…`, `replace-this-local-session-secret`, `APP_SESSION_SECRET`) finds nothing outside tests/forbidden-list; `.env.example` has an empty `SESSION_SECRET=`. |
| 2 | Missing secret prevents startup | PASS | `next info` (loads `next.config.ts`) exits 1 for missing, short (<32 bytes) and placeholder secrets; exit 0 with a strong secret. |
| 3 | Forged cookie fails | PASS | Valid-looking v1 admin payload signed with each old public default → 401; role-escalated customer cookie (payload edited, original signature) → 401. |
| 4 | Expired session fails | PASS | Independent vitest run (10 tests, then deleted): 9h-old, exactly-at-expiry and future-dated sessions all rejected. |
| 5 | Tampered session fails | PASS | Live: altered payload → 401; altered signature → 401; unit: empty/extra segments, wrong secret rejected. |
| 6 | Secret not in browser bundle | PASS | No `SESSION_SECRET`, `FASTAPI_*`, demo credentials in `.next/static`, page HTML, or served JS chunks. |
| 7 | Cookie flags | PASS | `HttpOnly; SameSite=Lax; Path=/; Max-Age=28800`; `Secure` off only in local development (production policy covered by a unit test). |
| 8 | Login works after restart | PASS | Wrong password 401; admin and customer login 200; admin cookie → dashboard/providers 200; customer cookie → garage 200; customer → admin 401; no cookie 401. |
| 9 | CMS public payload regression | PASS | `check-public-payload.cjs` passes on homepage and a published product editorial; no `createdBy/updatedBy/password/email/token` keys. |
| 10 | Garage dedupe | PASS | Same vehicle twice → same row; different engine → new row (live). |
| 11 | Provider test generic | PASS | Fresh API instance + spec-shaped fake provider (synthetic vehicles), env vars only; 8 arbitrary plates/VINs processed; no input literals in the lookup path. |
| 12 | One provider, several variants | PASS | Two variants from one provider → `MULTIPLE` / "Encontrámos várias versões possíveis"; `CONFLICT` ("Conflito entre fornecedores") only for vPIC vs provider disagreement. |
| 13 | Connected provider not "waiting for access" | PASS | Live provider result shows `source_type` REAL_TESTED, trace `RESOLVED`; `WAITING_FOR_ACCESS` only when nothing answered. (See P1 note.) |
| 14 | No EXACT_VARIANT for unverified results | PASS | All unvalidated provider candidates display `ENGINE`. |
| 15 | `VEHICLE_LOOKUP_IMPLEMENTATION_STATUS.md` exists and is accurate | PASS | Matches observed behaviour (waiting state, BASIC vPIC, config-only provider connection, MULTIPLE/CONFLICT rules, precision cap, security/CMS status); CLI runs and reports `NOT_CONFIGURED` without credentials. |

Tests: `pytest` 79 passed; repo `unittest` OK; web `vitest` 11 passed. Cleanup: temporary test files removed, test servers on :8010/:9911 stopped, garage rows from my tests deleted.

## Non-blocking items to fix before the first real provider credential is connected
- **P1: `REAL_TESTED` label on unvalidated provider results.** A live Autoways/Tips4y response currently gets `source_type: REAL_TESTED` (the chip text in the UI) while the same response says "Resultado de fornecedor não verificado" and K-Type `UNVERIFIED`. "Tested" reads as validated. Use a distinct value such as `LIVE_UNVALIDATED`, and reserve `REAL_TESTED` for providers validated on the Portuguese benchmark. Not visible in today's demo (no provider connected; vPIC's REAL_TESTED is accurate).
- **P2:** CMS pages/navigation/SEO remain modelled but not rendered (labelled honestly); admin modules other than Providers are placeholders (labelled); demo orders remain in local SQLite; stock is not enforced at order time (demo).

---

# PeçasAuto demo review (acting as David): ROUND 2

Re-reviewed from scratch on 2026-10-06 against the running stack: Next.js :3000, FastAPI :8000, Strapi :1337, PostgreSQL :5432. Method: browser walkthrough, direct API calls, Strapi admin API edits (local editor account from the project README), code inspection. Evidence: `reports/claude_raw_evidence/demo_review2/`. Tests re-run: 71 passed (`.venv/bin/python -m pytest -q`).

# VERDICT: NOT READY

Round 1's honesty problems are fixed and verified live. Four new blockers appeared in the CMS and auth layers. They are small, but each one lets David believe something that is not true (a security boundary, CMS capabilities, "role protected", "deduplicated").

## Round 1 items, verified against the running app
| Round 1 issue | Result | How verified |
|---|---|---|
| P0-1 fake "Auto Ways" provenance / invented ID 4607 | **FIXED** | Plate and VIN responses and garage rows contain no Auto Ways attribution, no external ID, no K-Type. |
| P0-2 plate lookup returned canned result | **FIXED** | `AB-12-CD` and `CG-17-GC` → `PROVIDER_UNAVAILABLE / WAITING_FOR_ACCESS`, zero candidates (UI shows "WAITING FOR PLATE PROVIDER"). Canned data only via a separate button and endpoint, banner states "no external call"; candidates are generic VW Golf, ENGINE level, null K-Type. |
| P0-3 EXACT_VARIANT overclaim | **FIXED** | Highest precision shown anywhere in the demo is ENGINE (canned) / BASIC (vPIC). |
| P0-4 static fitment labels | **FIXED** | All 10 products `CONFIRM_COMPATIBILITY`; product page says "COMPATIBILIDADE POR VERIFICAR… nunca apresentado como compatível ou incompatível"; no "provavelmente" / "não compatível". |
| P0-5 providers page overstated | **FIXED** | Evidence / connection / tested-inputs / documented-capability columns; Auto Ways "NOT CONFIGURED, tested NONE"; Autofrance RESEARCH ONLY; `/api/providers` is `MIXED_EVIDENCE`. |
| P0-6 wrong OE references | **FIXED** | `SAMPLE-*`, `DEMO-EAN-*` everywhere; real-looking OE search returns nothing. |
| P1 client-price tampering | **FIXED** | Order with injected `price: 0.01` totalled the server price (€168.60 both times). |
| P1 hard-coded client conflict logic | **FIXED** | No client VIN/plate/3008 literals in the API (only the generic manual-selection list). |
| P1 `_first_year` bug | **FIXED** | Saved rows show year 2017 / 2023. |
| P1 DEMO_MODE default | **FIXED** | `config.py` default false (the running instance has demo mode explicitly on). |
| P1 homepage prefilled plate | **FIXED** | Neutral `AB-12-CD` placeholder only. |
| P1 delivery claims | **FIXED** | "ESTIMATIVA DEMO · …" on cards, product page, checkout. |
| P1 empty cart total | **FIXED** | `shippingCost` returns 0 for empty subtotal. |
| P1 trace shows vPIC / hides irrelevant steps | **FIXED** | VIN trace includes vPIC (REAL_TESTED, BASIC); plate trace lists plate providers + manual only. |
| P1 admin placeholders | **FIXED** | Products / Orders / Vehicles / Inventory / Integrations all "NOT BUILT · PLACEHOLDER". |
| P1 API role boundaries | **FIXED at the API** (see B3 for the browser) | `/api/providers`, `/api/admin/*`: 401 without credentials, 401 for the customer, 200 for admin; garage is user-scoped (admin user sees 0 rows). |
| P1 garage deduplicated | **NOT FIXED** (see B4) | |

## Verified working in the new CMS layer
- Strapi native REST (`/api/pages`, `/api/homepage`, …) returns 404, so only the custom boundary routes are public; their payloads carry `ownership: EDITORIAL_ONLY`.
- Homepage edit: save as draft → public API and storefront unchanged; publish → public API and storefront show the new hero heading; unpublish → public endpoint returns `null` and the storefront falls back to built-in copy without the "STRAPI · PUBLISHED EDITORIAL" badge; original restored and republished.
- Product editorial: draft invisible; published → shown on the product page with "STRAPI · PUBLISHED EDITORIAL"; price, stock, fitment, delivery still come from FastAPI; unpublish hides it. Editorial schema has no price/stock/fitment fields.
- Vehicle lookup, candidate confirmation, catalogue, product page, cart, checkout, provider status and architecture pages all render honest labels (DEMO / WAITING / NOT CONFIGURED / TESTED / DOCUMENTED).
- Strapi rate-limits repeated admin logins (HTTP 429 after rapid attempts).

# REMAINING BLOCKERS

**B1. The public CMS product endpoint leaks the CMS admin user record, including the password hash.**
`GET /api/pecasauto/products/:externalId` (no authentication) returns `createdBy` and `updatedBy` with the editor's email, bcrypt `password` hash and token fields, because the controller uses `populate: "*"` (`apps/cms/src/api/public-content/controllers/public-content.ts`). Appears whenever any product editorial is published. Fix: explicit populate allowlist (brand, category, images, seo), strip `createdBy/updatedBy`, add a test that the public payload never contains those keys. Also rotate the local editor password afterwards.

**B2. The architecture page and demo script present CMS capabilities that are not wired.**
Architecture page and `reports/DAVID_DEMO_SCRIPT.md` say Strapi edits "pages, navigation, footer, FAQs, SEO, banners, promotions". Tested: a created and published `Page` is unreachable (Strapi public boundary 404; storefront has no page route). Navigation is hard-coded in the header; the Site-settings entry is empty (admin API 404) and unused. SEO fields (homepage `noIndex`, metadata) are ignored: `layout.tsx` uses static metadata. Only the homepage hero and the product editorial are rendered from Strapi (the feature-grid copy in Strapi differs from what the page shows). Fix: either wire pages, navigation and SEO, or label them "MODELLED IN CMS · NOT YET RENDERED" on the architecture page and in the script, and do not demo page creation, navigation or SEO.

**B3. "Role protected" is not true end to end: admin and customer credentials ship in the public browser bundle.**
`NEXT_PUBLIC_ADMIN_AUTH=demo-admin:admin-secret` and the customer credential are inlined into the static JS (found in `app/page.js`, `app/admin/page.js`, `app/garagem/page.js`). `/admin` and `/admin/providers` have no login: anyone who opens the storefront can see admin data and read the admin password. The API boundary is real, the browser path bypasses it. Fix: server-side session/BFF (credentials never in `NEXT_PUBLIC_*`), or at minimum a visible banner "DEMO: no real authentication; credentials are public in this build" and remove the claim of role protection from the demo script and README.

**B4. Garage deduplication does not work.**
Saving the same confirmed vehicle twice via `POST /api/garage` creates two rows (distinct database ids; I removed the two I added). The earlier P1 listed dedupe as fixed. Fix: unique key on (user, make, model, engine, year, registration/VIN), or upsert.

## Housekeeping from my testing
- My test content in Strapi is removed (test editorial for `PA-BRK-001` deleted, test page deleted, homepage restored to the original heading and republished). One earlier cleanup attempt was blocked by Strapi's login rate limit (caused by my own rapid login attempts) and succeeded once the window passed. A pre-existing editorial entry for `PA-DIS-001` (Codex's) remains.
- My demo orders remain in the local SQLite (the dashboard shows 4 orders); the extra garage rows I created were deleted.

## When these are fixed
Re-run: B1 curl on a published editorial; B2 page/nav/SEO walkthrough or labels; B3 `grep NEXT_PUBLIC_.*AUTH .next/static`; B4 save-twice test. If all pass, this is READY TO SHOW DAVID and I will create `collaboration/READY_TO_SHOW_DAVID`. It does not exist now.

---

# ROUND 3 STATUS (2026-10-06): still NOT READY

| Blocker | Status | Verified |
|---|---|---|
| B1 CMS endpoint leaks admin user + password hash | **FIXED by Claude** | Explicit populate allowlist + `sanitize()` removing `createdBy/updatedBy/localizations`; Strapi rebuilt and restarted; live check on published editorial `PA-DIS-001`: no audit/credential keys; `apps/cms/scripts/check-public-payload.cjs` PASS (homepage and product). |
| B2 CMS capabilities overstated | **FIXED by Codex (labels)** | Architecture page now shows "RENDERED NOW: homepage hero · product editorial" and "MODELLED, NOT RENDERED: pages · navigation · footer · FAQ · SEO · promotions"; README and demo script match. Not wired, but honestly labelled. |
| B3 credentials in public bundle / no login | **MOSTLY FIXED by Codex; one new P0 remains** | Bundle no longer contains `demo-admin`/`admin-secret`/`FASTAPI_ADMIN_AUTH`; unauthenticated `/api/platform/*` → 401; session is HMAC-signed, httpOnly. **P0-S1:** the session secret falls back to a public default (`local-development-session-secret-change-me`); a cookie forged with it passed the session check on the running instance (request then failed 503 only because upstream credentials were not loaded in that process). Also no server-side expiry. The running web process predates the new env, so demo logins currently return 401 until restarted. |
| B4 garage duplicates | **FIXED by Claude** | `POST /api/garage` twice with the same vehicle without plate/VIN returns the same row (live, after API restart); a different engine creates a distinct row; regression test added (API tests 10 pass, repo 76 pass). |

**Remaining blocker before approval: P0-S1 (session secret must fail closed, expiry enforced), then a re-run of the login flow with the web process restarted with the documented env.** The demo is not approved.

## Lookup architecture review (arbitrary plates/VINs)
`reports/VEHICLE_LOOKUP_IMPLEMENTATION_STATUS.md` does not exist yet; reviewed the code and ran a config-only test (spec-shaped fake Autoways server with synthetic vehicles, second API instance with only `VEHICLE_PROVIDER`, `AUTOWAYS_API_TOKEN`, `AUTOWAYS_BASE_URL` set; raw results in `reports/claude_raw_evidence/lookup_config_test/`).
- **Arbitrary inputs: YES.** Eight different plates/VINs all went through normalisation → cascade → candidates; no input literals in the lookup path.
- **Adding a provider = configuration only: YES.** Env vars select and configure the adapter; the frontend and response schema were untouched. (Spec-shaped fake only; not a real vendor response.)
- **Free VIN cannot pass as exact: YES.** vPIC results are BASIC / `NEEDS_SECOND_SOURCE_OR_USER_CONFIRMATION`; `may_claim_compatibility` is always false; all products stay `CONFIRM_COMPATIBILITY`; vPIC vs a different provider's make → `CONFLICT`.
- **Multiple candidates normal and selectable: PARTLY.** The UI lists and confirms N candidates, but one provider returning two variants is mislabelled `CONFLICT` instead of `MULTIPLE` (P1-L1). Two further labelling issues: live-but-unvalidated results show `WAITING_FOR_ACCESS` (P1-L2) and `EXACT_VARIANT` precision for unvalidated results (P1-L3). All logged in `collaboration/NEXT_ACTIONS.md`.
