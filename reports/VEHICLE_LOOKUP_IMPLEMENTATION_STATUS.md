# Vehicle lookup implementation status

Date: 2026-10-06
Scope: Portugal-only pre-TecDoc implementation readiness.

## Short answer

The lookup architecture is ready for a real provider credential. Arbitrary Portuguese plates do not identify a vehicle today because no live Portuguese plate provider is configured. Arbitrary VINs run through free vPIC first; European VINs often return only BASIC or MODEL data, so the platform asks for more information instead of claiming an exact vehicle.

No arbitrary plate or VIN automatically receives canned client data. The neutral canned conflict remains a separate, explicitly labelled demo action only.

## What works now?

- Provider-independent FastAPI vehicle search endpoint.
- Separate VIN and Portuguese matrícula cascades.
- Free/public vPIC is the first VIN step.
- Auto Ways, TIPS4Y, Matricula.co.pt, TelePeças and TecAlliance adapters return `NOT_CONFIGURED` without required credentials/contract paths.
- `.env` loading and a documented `.env.example`.
- One, multiple, partial and no-result provider outcomes.
- Candidate normalization with make/model/generation/year/engine/engine code/fuel/power/variant/provider IDs/K-Type where actually returned.
- Customer confirmation and saved normalized vehicle.
- Garage upsert/deduplication for VIN/plate and manual candidates without either identifier.
- CLI testing for individual providers or the cascade.
- Admin evidence/configuration view with `CONNECTED`, `NOT CONFIGURED`, `TESTED`, `DOCUMENTED ONLY` and `RESEARCH ONLY` distinctions.
- A later catalogue vehicle ID and fitment boundary. Identity never becomes a compatibility claim by itself.

## Why arbitrary Portuguese plate lookup currently does not work

There is no configured live Portuguese plate credential in the environment. The current plate cascade attempts configured, Portugal-capable adapters and receives `NOT_CONFIGURED` from each. The API therefore returns:

```text
WAITING_FOR_PROVIDER
```

with zero candidates and a manual-selection fallback. It does not fabricate a result.

## Why arbitrary VIN lookup may return partial data

vPIC is public and free, but NHTSA focuses on vehicles intended for the US market. For the Portuguese client VIN it returned Peugeot/manufacturer-level data only. It did not return model, engine, engine code, power, variant or K-Type. The normalized precision is therefore `BASIC`, and the UI asks the customer to complete/confirm the vehicle.

The system continues to configured commercial VIN providers after a BASIC/MODEL result. If none are connected, the partial vPIC candidate remains visible with its actual missing fields.

## What credential/API is needed next?

The most useful next credential is one Portugal-capable provider that accepts both matrícula and VIN and returns engine/variant plus a catalogue bridge ID where possible.

Adapters are prepared for:

- Auto Ways: `AUTOWAYS_API_KEY` (or legacy `AUTOWAYS_API_TOKEN`). Public endpoint assumptions still require a permitted live test.
- TIPS4Y: `TIPS4Y_API_KEY`, base URL and contracted VIN/plate paths.
- Matricula.co.pt: `MATRICULAPT_USERNAME` for plate only.
- TelePeças: access token or OAuth credentials plus contracted VIN/plate paths.
- TecAlliance: key, base URL and contracted paths when available.

Secrets belong in local `.env` or a secret manager and are ignored by Git.

## What changes after a credential is connected?

Nothing in the frontend architecture changes.

1. Add the environment values.
2. Select the provider with `VEHICLE_PROVIDER` or `FALLBACK_PROVIDER`.
3. Restart FastAPI.
4. Run the CLI against a real Portuguese plate/VIN.
5. The same provider trace, normalization, candidate confirmation and garage flow appear in the UI.

The provider result is still not trusted as fitment. A returned K-Type stays unverified until catalogue/independent validation policy permits it.

## Multiple vehicle candidates

Multiple results are a normal outcome, not an error:

```text
provider result
→ normalize every candidate
→ display make/model/generation/year/engine/power/fuel/variant
→ customer selects one
→ store selected normalized vehicle plus candidate set and confirmation method
→ resolve catalogue vehicle ID
→ ask trusted fitment provider
```

Partial results ask for the missing engine or variant. No-result falls back to manual vehicle selection.

Several variants returned by one provider are labelled `MULTIPLE` / “Encontrámos várias versões possíveis”; this is not described as provider disagreement. `CONFLICT` is reserved for incompatible results returned by two or more providers. A live result with candidates is shown as real provider evidence, never as “waiting for access”. Unless the provider evidence has been validated, displayed precision is capped at `ENGINE` even when a payload contains fields that could otherwise calculate as `EXACT_VARIANT`.

## CLI commands

```bash
python -m tools.test_vehicle --plate "CG-17-GC" --country PT --provider cascade
python -m tools.test_vehicle --vin "VF3MCYHZUPS034433" --country PT --provider cascade

python -m tools.test_vehicle --provider autoways --plate "CG-17-GC" --country PT
python -m tools.test_vehicle --provider tips4y --vin "VF3MCYHZUPS034433" --country PT
python -m tools.test_vehicle --provider matriculapt --plate "CG-17-GC" --country PT
python -m tools.test_vehicle --provider telepecas --plate "CG-17-GC" --country PT
```

The output includes provider attempted, HTTP status, raw response, normalized candidates, precision, engine, engine code, power, K-Type, latency, known per-call cost and next action. A missing credential exits non-zero and says `WAITING_FOR_PROVIDER`.

## How much can remain free?

Free/open components can cover:

- VIN structure validation.
- vPIC BASIC routing where it returns data.
- manual vehicle selection.
- normalization, candidate handling, confirmation and garage storage.
- provider orchestration and the internal vehicle model.

Free vPIC cannot currently provide fitment-grade Portuguese identity for the real test VIN.

## What is paid?

Likely paid/licensed areas are:

- reliable Portuguese matrícula lookup.
- stronger European VIN engine/variant resolution.
- catalogue vehicle IDs such as K-Type.
- aftermarket catalogue and fitment data.
- commercial caching/storage/reuse rights.
- supplier, ERP and logistics integrations where contracts require them.

Exact provider prices remain unknown unless backed by a quote/contract. The application does not invent them.

## What happens when TecDoc is connected later?

TecDoc/TecAlliance enters through the existing provider interfaces:

```text
free/open identity
→ low-cost identity provider
→ customer confirmation
→ TecDoc catalogue vehicle ID
→ TecDoc fitment/catalogue
→ FastAPI price/stock/order truth
```

The Next.js customer flow does not need to be rebuilt. TecDoc can become a catalogue/fitment provider while another service continues to handle Portuguese matrícula.

## P0 security/CMS status

- Strapi public product queries now use explicit relation/media allowlists and recursively strip audit/admin secret fields.
- Live public endpoint checked: no `createdBy`, `updatedBy`, email, password hash or token fields.
- CMS verifier tests this boundary.
- Architecture/demo copy now distinguishes rendered CMS surfaces from models not yet rendered.
- Browser credentials moved out of `NEXT_PUBLIC_*`. Protected calls use an HTTP-only Next.js session and server-side FastAPI BFF credentials.
- Next.js now requires a server-only `SESSION_SECRET` with at least 32 bytes and refuses to start without it. There is no default/fallback secret. Sessions carry a signed schema version plus issued/expiry timestamps and expire after eight hours; invalid, expired or tampered cookies receive `401`.
- Session cookies are `HttpOnly`, `SameSite=Lax`, and `Secure` in production (disabled only in explicit local development).
- Public bundle scan contains no demo API credentials.
- Garage deduplication now covers manual candidates with no VIN or plate.
- Local Strapi editor password was rotated after the leak review.

## Current evidence status

| Route | Current result | Status |
|---|---|---|
| Arbitrary PT plate | No connected provider; zero candidates | `WAITING_FOR_PROVIDER` |
| Client Portuguese-market VIN via vPIC | Peugeot only; no model/engine/variant | `BASIC / PARTIAL` |
| Auto Ways | Adapter/config ready; no verified live response | `NOT CONFIGURED` |
| TIPS4Y | Adapter/config ready; contract paths required | `DOCUMENTED ONLY` |
| Matricula.co.pt | Plate adapter ready; username required | `NOT CONFIGURED` |
| TelePeças | Adapter/config ready; OAuth/paths required | `DOCUMENTED ONLY` |
| TecAlliance | Interfaces ready; contract/key/paths required | `WAITING FOR ACCESS` |

## Next action tomorrow

Add one real provider credential and any contract-specific endpoint paths to `.env`, restart FastAPI, run both CLI commands, preserve permitted raw evidence, and compare the normalized result to independently known Portuguese vehicle data before enabling customer-facing confidence.
