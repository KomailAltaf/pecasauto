# Provider runtime and credential testing

The application depends on internal interfaces, never vendor response objects:

```text
Customer/API
  → VehicleIdentityProvider
  → canonical VehicleCandidate
  → CatalogueVehicleProvider
  → catalogue vehicle ID / KType candidate
  → FitmentProvider
  → MATCH / NO_MATCH / UNKNOWN / CONFLICT
```

Provider selection is environment-driven. Copy `config/providers.example.env` into the deployment secret manager; do not commit populated values.

Autoways routes are also configuration values because vendor accounts and API products may expose different contracted paths:

```text
AUTOWAYS_PLATE_PATH=/pt
AUTOWAYS_VIN_PATH=/vin/
```

The defaults match the stored vendor OpenAPI documents. Override them only with an official account-specific path.

## One-command tests

```bash
python3 -m tools.test_provider --provider autoways --plate CG-17-GC
python3 -m tools.test_provider --provider autoways --vin VF3MCYHZUPS034433
python3 -m tools.test_provider --provider tips4y --plate CG-17-GC
python3 -m tools.test_provider --provider matriculapt --plate CG-17-GC
python3 -m tools.test_provider --provider telepecas --plate CG-17-GC
python3 -m tools.test_provider --provider tecalliance --vin VF3MCYHZUPS034433
```

Without required credentials/contracts each command returns `NOT_CONFIGURED`. This is expected and is not provider testing.

The CLI prints the raw response, canonical vehicle, precision, engine, engine code, power, KType, latency, estimated request cost and catalogue-resolution state. Raw responses are not persisted by default. `--save-raw PATH` is an explicit operator action and must only be used when storage rights allow it.

## Contract-dependent adapters

- Autoways paths and field names come from the stored public OpenAPI specification; only the token is missing.
- Matricula.co.pt uses the documented `CheckPortugal` endpoint and username.
- TIPS4Y, TelePeças and TecAlliance paths vary with the purchased package. Their adapter requires contracted base URLs/paths rather than inventing endpoints.
- TelePeças supports either a supplied access token or OAuth client credentials.

## Safety

- A KType is a catalogue identity, not product fitment evidence.
- `VF3MCYHZUPS034433` remains in the conflict registry until Portuguese plate, registration-document, OEM or permitted partslink24 evidence resolves it.
- Unknown provider storage terms disable persistent provider caching.
- Customer-confirmed garage data is stored separately from provider caches.
