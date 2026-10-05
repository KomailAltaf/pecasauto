# Pre-TecDoc decision tree (Portugal)

Built from evidence in `reports/portugal_provider_landscape.md`; provider names are the *candidates*, none validated.

```
MATRÍCULA ENTERED
 ├─ normalise (CG-17-GC); invalid format? ──► ask again (free, no paid call)
 ├─ our verified-vehicle store hit?  [only if licence permits storing provider data;
 │                                     customer-confirmed vehicles are ours to store]
 │      YES ─► load vehicle (+ confirmed engine) ─► BRIDGE
 │      NO  ▼
 ├─ PT plate provider (Openapi / Matricula.co.pt / AutoNow / TelePeças)
 │      error / timeout / 429 ─► next provider, or ─► MANUAL SELECTOR
 │      no result ─► ask for VIN or manual selector
 │      returns catalogue ID (ktype)? ─► BRIDGE: PROVIDER_ID
 │      returns make+model+cc+hp+fuel+year ▼
 ├─ Can text uniquely narrow to ONE catalogue vehicle? (needs the catalogue)
 │      YES ─► show "Is this your car? Peugeot 5008 1.5 BlueHDi 130" ─► customer confirms ─► USER_CONFIRMED
 │      NO  ─► show the 2–5 engine/version options from the catalogue ─► customer picks (check engine code on registration doc)
 └─ Provider returns make/model only ─► same, plus "enter VIN" shortcut

VIN ENTERED (alternative / fallback)
 ├─ structural check (no mandatory EU checksum) ─► WMI → make
 ├─ VIN provider (Vincario / AutoNow; not vPIC, it returned make only)
 │      ENGINE-level result ─► BRIDGE
 │      otherwise ─► manual engine confirmation

BRIDGE → catalogue vehicle ID
 ├─ no catalogue source yet (pre-TecDoc) ─► STOP at identity: show parts by reference/OE search only; no "fits your car"
 ├─ licensed catalogue MATCH + identity ENGINE+ ─► COMPATIBLE
 ├─ MATCH but partial restrictions / TEXT_MATCH ─► CONFIRM_COMPATIBILITY
 ├─ sources disagree ─► CONFLICT ─► staff review
 └─ nothing known ─► UNKNOWN (offer staff contact / WhatsApp)

AFTER CONFIRMATION: save vehicle to customer garage (our data, GDPR-governed) ─► skip paid lookup on return visits.
```

Minimum data to reach "Confirm your engine" safely: make, model/generation, year range, fuel; catalogue list of engine options for that model (that list itself needs a licensed catalogue).
