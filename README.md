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
- `apps/api/` — FastAPI + SQLAlchemy prototype API
- `apps/web/` — Next.js + React customer and admin prototype
- `apps/cms/` — Strapi editorial CMS (PostgreSQL)

No production integrations, credentials, or client data should be committed here.

## Credential-ready provider test

Copy the variable names from `config/providers.example.env` into your shell or secret manager, then run:

```bash
python3 -m tools.test_provider --provider autoways --plate CG-17-GC
python3 -m tools.test_provider --provider autoways --vin VF3MCYHZUPS034433
```

Missing credentials return `NOT_CONFIGURED`. Raw responses print to the terminal and are not stored unless `--save-raw` is explicitly supplied.

## PeçasAuto full-stack prototype

The prototype runs beside the validation work. It never imports research evidence into customer data and distinguishes `REAL_TESTED`, `DEMO`, `DOCUMENTED_CAPABILITY`, `WAITING_FOR_ACCESS`, `NOT_CONFIGURED`, `RESEARCH_ONLY`, and `MOCK`.

### Install

```bash
cd ~/Downloads/portugal-auto-validation-lab
uv sync --python 3.12
cd apps/web && pnpm install
cd ../cms && pnpm install
```

### Run the API

```bash
cd ~/Downloads/portugal-auto-validation-lab
DEMO_MODE=true \
CUSTOMER_USERNAME=demo-customer CUSTOMER_PASSWORD=customer-secret \
ADMIN_USERNAME=demo-admin ADMIN_PASSWORD=admin-secret \
uv run uvicorn apps.api.pecasauto_api.main:app --reload --port 8000
```

API docs: `http://localhost:8000/docs`

### Run the frontend

```bash
cd ~/Downloads/portugal-auto-validation-lab/apps/web
NEXT_PUBLIC_API_URL=http://localhost:8000 \
NEXT_PUBLIC_STRAPI_URL=http://localhost:1337 \
FASTAPI_API_URL=http://127.0.0.1:8000 \
FASTAPI_CUSTOMER_AUTH=demo-customer:customer-secret \
FASTAPI_ADMIN_AUTH=demo-admin:admin-secret \
DEMO_CUSTOMER_LOGIN=demo-customer:customer-secret \
DEMO_ADMIN_LOGIN=demo-admin:admin-secret \
SESSION_SECRET="$(openssl rand -base64 48)" \
pnpm dev
```

Open `http://localhost:3000`.

`SESSION_SECRET` is required and must contain at least 32 bytes of random data. The web application refuses to start without it. Keep it server-side and reuse the same securely stored value across restarts when existing sessions should remain valid.

### Real provider configuration

Copy `.env.example` to `.env` and add a provider credential, or export it in the shell. Provider secrets belong in `.env`/a secret manager, never in committed source:

```bash
export VEHICLE_PROVIDER=autoways
export AUTOWAYS_API_KEY=...
```

No frontend change is required after switching a provider. Restart FastAPI and run:

```bash
python -m tools.test_vehicle --plate "CG-17-GC" --country PT --provider cascade
python -m tools.test_vehicle --vin "VF3MCYHZUPS034433" --country PT --provider cascade
```

`DEMO_MODE` defaults to `false`. Enabling it adds a separate canned conflict walkthrough. Ordinary matrícula/VIN searches never turn into a canned provider result: when no useful live result exists the search outcome is `WAITING_FOR_PROVIDER`, while each trace step remains honestly `NOT_CONFIGURED`/access-blocked.

Protected browser calls use a same-origin Next.js session/BFF. FastAPI credentials are server-only (`FASTAPI_*_AUTH`) and must never use a `NEXT_PUBLIC_` prefix. The local login is a prototype boundary, not the final customer identity system.

### Run Strapi + PostgreSQL

```bash
cd ~/Downloads/portugal-auto-validation-lab
docker compose up -d postgres

cd apps/cms
APP_KEYS='local-key-1,local-key-2,local-key-3,local-key-4' \
API_TOKEN_SALT='local-api-token-salt' \
ADMIN_JWT_SECRET='local-admin-jwt-secret' \
TRANSFER_TOKEN_SALT='local-transfer-token-salt' \
JWT_SECRET='local-users-jwt-secret' \
ENCRYPTION_KEY='local-encryption-key' \
DATABASE_HOST=127.0.0.1 DATABASE_NAME=pecasauto_cms \
DATABASE_USERNAME=pecasauto DATABASE_PASSWORD=pecasauto_local \
pnpm start
```

CMS admin: `http://localhost:1337/admin`. The current local Docker volume contains the rotated demo editor `admin@pecasauto.local` / `LocalDemo!2026-Rotated`. These are local-only credentials and must never be deployed.

Strapi owns editorial content. **Rendered now:** homepage hero and product editorial. **Modelled but not rendered yet:** generic pages, navigation/footer, FAQs, SEO, banners and promotions. FastAPI remains the source of operational truth for vehicle identity, fitment, price, stock, cart/order rules and integrations.

Verify draft isolation, publish/refresh, the page builder and product editorial:

```bash
cd apps/cms
# use the same environment variables as the start command
pnpm build
pnpm verify:content
```

### Database

The default database is `apps/api/data/pecasauto.db` (ignored by git). Set a PostgreSQL SQLAlchemy URL later without changing the models:

```bash
export DATABASE_URL=postgresql+psycopg://user:password@localhost/pecasauto
```

### Tests and build

```bash
cd ~/Downloads/portugal-auto-validation-lab
uv run pytest -q
uv run python -m unittest discover -s tests -v

cd apps/web
SESSION_SECRET="$(openssl rand -base64 48)" pnpm test
SESSION_SECRET="$(openssl rand -base64 48)" pnpm build

cd ../cms
pnpm build
pnpm verify:content
```

Do not run `pnpm build` in `apps/web` while `pnpm dev` is serving the same `.next` directory. Stop the development server for the production build, then restart `pnpm dev`; otherwise the live browser can temporarily request mismatched CSS/build assets.

### Five-minute demo

Follow [`reports/DAVID_DEMO_SCRIPT.md`](reports/DAVID_DEMO_SCRIPT.md). The useful routes are:

- `/` — vehicle discovery
- `/catalogo` — catalogue and filters
- `/garagem` — saved vehicles
- `/carrinho` and `/checkout` — demo commerce flow
- `/admin/providers` — provider capability/status matrix
- `/architecture` — system boundaries
