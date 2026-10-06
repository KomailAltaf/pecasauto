# Provider commercial comparison

Only numbers published by the vendor itself are shown (ex-VAT unless stated). **Unknown = QUOTE REQUIRED.** Nothing was negotiated; nothing was tested on a Portuguese plate. Date 2026-10-05.

| Provider | Role | Plate | VIN | K-Type | Catalogue | Fitment | Setup fee | Monthly | Per lookup | Minimum spend | Commercial rights | TecDoc licence required? | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **Luis / Fahad existing quote** | Reseller (scope unknown) | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | n/a (is the TecDoc route) | **Not in repo; Komail to attach** |
| **TecAlliance direct** | Catalogue + VRM/VIN + K-Type + fitment (source of truth) | Yes (Portugal listed; module/fee unknown) | Yes | Native | Yes | Yes | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED (reported: turnover % + annual minimum, unverified) | By licence | n/a (is TecDoc) | DOCUMENTED; no quote |
| **Tips4y** | PT plate → TecDoc vehicle number + TecDoc WebService/webshop (probable reseller) | Yes (99.3 % post-1989, claim) | Documented in marketing (K-Type via VIN) per Codex notes; UNVERIFIED | Yes (TecDoc vehicle number) | Yes (TecDoc) | Yes (via TecDoc) | QUOTE REQUIRED | QUOTE REQUIRED | **€0.10 + VAT** (Pack 300 = €30 + VAT) | Pack of €30 | Not stated; pack "not for resale" | Pack sold only to Tips4y TecDoc customers; standalone: UNKNOWN | DOCUMENTED; quote needed |
| **Autoways** | Plate/VIN → K-Type + engine code + kW (identity/bridge only) | Yes (PT spec) | Yes (`country=PT`) | Yes (`AWN_k_type`, derived by matching) | No | No | QUOTE REQUIRED | Credit plans (amounts not retrievable) | QUOTE REQUIRED (20 free credits) | QUOTE REQUIRED | Not stated; caching silent | Not stated: UNKNOWN | DOCUMENTED; waiting for demo token |
| **TelePeças** | Marketplace + plate/VIN decode + parts | Yes | Yes | Documented in API docs (`ktype`, `tecDocModelId`) | Own stock/marketplace; OEM/IAM compatibility check | Partial ("Serve no meu carro?") | QUOTE REQUIRED (integrator account) | Seller plans €150 / €300 / €700 / €1,200 (API listed on the €1,200 plan) | VIN/plate decoding **€25 per 100 → €615 per 5,000 (€0.25 → €0.123)**; technical data €1.93–8.00; vehicle check €1.99 single, €0.16–0.25 volume | QUOTE REQUIRED | Unknown; **competing marketplace**; terms silent on API | UNKNOWN | DOCUMENTED; credentials needed |
| **Matricula.co.pt** (RegCheck) | PT plate identity only | Yes | No | **Not documented** | No | No | None | None (pay as you go) | **€0.20** (−10% on ≥1,000 packs, min. pack 100) | Pack of 100 = €20 | Not stated; says official government data | No (not a TecDoc product) | DOCUMENTED; 10 free test credits; endpoint live, untested |

Additional reference (not requested): **Openapi PT-car**: plate identity, 30+ fields, no K-Type documented: €0.40 PAYG, €0.37 (1k/yr), 0.33 (5k), 0.30 (10k), 0.28 (25k), 0.24 (50k), 0.18 (200k) per call.

## Reading the table
- **Cheapest published plate lookup:** Tips4y ≈ €0.10 (restricted eligibility), then TelePeças ≈ €0.12 at 5,000-decode volume, Matricula.co.pt €0.18–0.20.
- **Only K-Type-capable plate options:** Tips4y, Autoways, TelePeças (documented, none tested). Matricula.co.pt does not document K-Type.
- **Only fitment-capable:** TecAlliance (directly or through Tips4y/Fahad's reseller).
- **Biggest unknown:** the TecDoc licence price (Fahad's quote vs direct vs Tips4y). This outweighs any per-lookup difference of cents.
- A per-lookup price is only meaningful with a tested hit-rate for engine-level and K-Type results on Portuguese vehicles.
