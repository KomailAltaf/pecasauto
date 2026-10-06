# David: technical brief (Portuguese parts platform, pre-TecDoc)

**Evidence status:** every provider is DOCUMENTED, NOT TESTED on a Portuguese plate, except vPIC and the Autofrance research oracle. Repo: `~/Downloads/portugal-auto-validation-lab/` (46 tests green). Details: `reports/CLAUDE_BUILD_PLAN_REDTEAM.md`.

## What we proved
- **vPIC (free VIN)**: client VIN → make only (BASIC). Useless for PT variants.
- **Autofrance** (a Swedish shop's backend, research only): VIN → K-Type 130708, "3008 SUV 1.5 BlueHDi 130, 96 kW". K-Type identity cross-checked by Autodoc + Schaeffler. It also answers **fake VINs confidently**, so never a sole source.
- **client_001 (`CG-17-GC` / `VF3MCYHZUPS034433`)**: client says 5008 II; evidence leans 3008. Status **CONFLICT — NEEDS PLATE/REGISTRATION/PARTSLINK24 CONFIRMATION.** Engine YHZ/DV5RC is consistent. VIN descriptor `MC` is shared by 3008 and 5008, so VIN alone is ambiguous.
- Identity ≠ fitment. Fitment is **not solved**.

## Architecture
```
Customer input (plate | VIN | manual | OE/part no.)
 → normalisation (PT plate formats; VIN structure only, no EU checksum)
 → IdentityProvider cascade (configurable; per-step min precision, cost cap, isolation)
 → canonical Vehicle (precision BASIC/MODEL/ENGINE/EXACT, per-field provenance, DISPUTED)
 → Bridge → catalogue vehicle ID (match_method + candidates_count)
 → CatalogueProvider / FitmentProvider (licensed only)
 → InventoryProvider (Primavera) → pricing/GLS → checkout
Customer garage = our own store of user-confirmed vehicles (separate from provider cache)
```
Customer-facing states: COMPATIBLE / CONFIRM_COMPATIBILITY / UNKNOWN / NOT_COMPATIBLE. COMPATIBLE only if: ENGINE+ identity, unique bridge, licensed MATCH, no restrictions, no conflict.

## Provider strategy (candidates, none validated)
| Layer | Candidates |
|---|---|
| Plate → vehicle | Tips4y (≈€0.10, TecDoc vehicle number, bundled to its TecDoc customers); Autoways (PT spec: K-Type, kW, engine code, VIN; free token); TelePeças (ktype fields documented); Matricula.co.pt €0.20 and Openapi €0.18–0.40 (identity only) |
| VIN | Autoways VIN-DECODER (`country=PT`), Vincario; vPIC as BASIC cross-check only |
| Catalogue/fitment | TecDoc (direct, via Tips4y, or via Fahad's reseller): **QUOTE REQUIRED** |
| Stock/price | Primavera (version/API unknown) |
| partslink24 | Staff/validation tool only: public ToS prohibits integrating it into our own services or automated extraction |

## What can start now (YES)
Frontend; backend platform; vehicle abstraction; catalogue interface + curated stub; checkout/GLS; garage store; search by OE/EAN/SKU (search-only); MODEL_CONFLICT confirm flow (show 3008/5008 with images).
## Blocked (NO)
Exact fitment; PT plate production integration; real Primavera integration; any provider-data caching until rights are written; production trust (need PT benchmark of 20 → 100+ → 500).

## Fixes before relying on the fitment code
1. Pass the bridge result into `evaluate_fitment`; COMPATIBLE needs `may_claim_compatible`.
2. Remove ENGINE_CODE from auto-claim (YHZ is shared by 3008/5008).
3. NOT_COMPATIBLE only from a licensed source.
4. Add `ktype_validated`, `NO_EXISTENCE_CHECK`, `DISPUTED`, plate-vs-VIN agreement gate.
5. Per-category minimum precision.

## TecDoc role
Source of truth for catalogue vehicle ID, vehicle→article links with criteria, OE/cross-references, and (via VRM/VIN) identification. Plug in behind `CatalogueProvider`/`FitmentProvider`; customer code unchanged. Licence route (direct vs reseller vs Tips4y): open commercial decision.

## Phases
P1 (now): platform, interfaces, garage, manual selector, search, checkout, mocks labelled MOCK. P2: PT plate adapter from a real response; VIN adapter; Stage-1 benchmark (10–20 PT cars verified via partslink24/registration docs). P3: licensed catalogue + fitment, bridge validation, narrow launch (filters + brakes). P4: Stage 2/3 benchmark (100–500), expand groups, Primavera live.

## Major risks
Wrong-but-confident decoders (Autofrance behaviour); K-Type derived by matching; 3008/5008-type platform siblings; unknown caching/licence rights; GDPR for plates/VINs; single small vendors (Autoways); TecDoc price/lock-in; Primavera API unknown.
