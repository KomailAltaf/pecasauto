# VIN results, `VF3MCYHZUPS034433` (PT vehicle, client_001)

| Provider | Raw file | Class | Notes |
|---|---|---|---|
| NHTSA vPIC `DecodeVinValues` | vpic_decodevinvalues.json | **BASIC** | PEUGEOT, ModelYear 2023 (guess), model empty, errors 1/8/400 |
| NHTSA vPIC `DecodeVin` | vpic_decodevin.json | **BASIC** | same, long form (identical to Codex's `reports/raw_evidence/vpic_public_detailed_*.json`, byte-for-byte) |
| Corgi / vin-lite / other offline vPIC-based decoders | not run | NOT_USEFUL (expected) | same data source; no EU variant data |
| Vincario / Zylalabs / AutoNow | not run | NOT TESTED | need account/key: HUMAN ACTION REQUIRED, see FINAL file |

No other genuinely free, keyless EU VIN decoder was found.
