# Direct TecDoc vs partner/reseller vs alternatives

Prices are public list figures ex-VAT where available; otherwise **QUOTE REQUIRED**. No provider below has been tested on `CG-17-GC` (Codex's Matricula.co.pt and TelePeças calls without credentials returned auth errors only).

## Price/access table
| Provider | Role | Setup fee | Monthly | Per call | Included | Vehicle identity | K-Type | Fitment | Catalogue | Commercial rights | Status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Fahad/Luis quote | unknown | QUOTE REQUIRED | | | | | | | | | Not in repo; Komail to attach |
| **TecAlliance direct** | catalogue + VRM/VIN + KType | QUOTE REQUIRED | QUOTE REQUIRED (turnover % + annual minimum reported, unverified) | QUOTE REQUIRED | | VIN, VRM (PT unconfirmed) | **Yes** (native) | **Yes** | **Yes** | Licence defines | Contact |
| **Tips4y (tips4y.pt)** | PT plate API → TecDoc Vehicle ID + TecDoc WebService/B2B webshop | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED (API integrable) | | PT plate; claims 99.3 % of post-1989 vehicles | **Yes (TecDoc Vehicle ID, documented)** | **Yes via TecDoc** | **Yes** | Partner terms: QUOTE REQUIRED | **Contact P0** |
| **Autoways AUTO-NOW** | plate/VIN → KType | €0 (demo) | plans via RapidAPI; **pricing page shows none** | QUOTE REQUIRED | | plate, VIN; 100+ fields; **PT documented in vendor spec** | **Claimed** | No | No | Unknown | Demo signup |
| **Matricula.co.pt** | plate identity | €0 | pay-as-you-go | **€0.20** (−10% on ≥1000-block) | 10 free tests | brand, model, engine size, fuel, VIN (RegCheck std); **kW/version/ktype not documented** | No | No | No | Unknown | Credential-blocked |
| **Openapi PT-car** | plate identity | €0 | annual plans | **€0.40 PAYG; €0.37 @1k/yr, 0.33 @5k, 0.30 @10k, 0.28 @25k, 0.24 @50k, 0.18 @200k** | sandbox | 30+ fields incl. version, hp, VIN, ABI | **No** (docs don't mention) | No | No | Unknown | Sandbox signup |
| **TelePeças** | plate/VIN + marketplace + parts | integrator terms: QUOTE REQUIRED | seller plans €150–1,200 | decode €0.25 → €0.123; tech data €1.93–8.00; verification €0.16–0.25 | | plate/VIN | **Documented (`ktype`, `tecDocModelId`)** | "Serve no meu carro?" check, OEM/IAM compatibility | stock marketplace | Unknown; **it is a competing marketplace** | Credential-blocked |
| **Vincario** | VIN decode | €0 trial | volume plans | €0.49 @100 → €0.22 @5k | 20 free | VIN only; EU/PT claimed | Claimed | No | No | Enterprise caching tier | Signup |
| partslink24 | OEM catalogue (staff) | Fahad has it | already paid | n/a | | VIN | OEM IDs | OEM fitment | OEM | **Public ToS prohibits own-service integration/automation** | Manual only |
| NHTSA vPIC | VIN | €0 | | €0 | | make only (**VERIFIED**) | No | No | No | public | Done: BASIC |

## What each actually provides
- **TecAlliance direct / partner:** the only route that is a *licensed fitment* source. Everything else is identity.
- **Autoways, TelePeças:** the only candidates that *claim* a catalogue vehicle ID (K-Type) from a plate or VIN. Either could remove the fuzzy text→K-Type step if the claim holds for Portugal. Neither is verified.
- **Matricula.co.pt, Openapi:** cheap plate identity; documents do not mention K-Type or engine code. Would need our own mapping + customer confirmation.
- **Vincario:** VIN fallback.

## Cheapest workable combinations (ratings are my judgement from documentation, UNVERIFIED)
| Option | Accuracy | Fitment readiness | Cost | Complexity | Licensing risk | Launch suitability |
|---|---|---|---|---|---|---|
| **A** Matricula/Openapi + TecDoc direct | medium (engine needs confirmation) | **High once TecDoc live** | plate €0.18–0.40 + TecDoc quote | medium (own text→KType mapping) | low–medium | Good after TecDoc |
| **B** AutoNow K-Type + TecDoc | potentially highest (if PT K-Type real) | High | low per call; TecDoc still needed | low | **medium: K-Type reuse/licence unclear** | Best if verified |
| **C** TelePeças identity/catalogue + Primavera | unknown | **Partial** (their catalogue only) | seller plan + decode credits | medium | **high** (competing marketplace, terms unknown) | Possible temporary launch if terms allow |
| **D** cheap plate + manual engine confirmation + TecDoc later | medium; user-confirmed | Low until TecDoc; staff-curated list for top SKUs | lowest | low | low | **Best realistic launch path** |
| **E** partslink24 manual + temporary provider + TecDoc | high for staff-verified cases only | manual only, doesn't scale | lowest cash | high labour | **ToS limits to real customer orders** | Customer-service fallback only |

## Expected next commercial action
1. Send the TecAlliance/partner question list this week (long lead time, unlocks fitment).
2. In parallel run the €0 trials (Autoways, Matricula.co.pt, Openapi sandbox, Vincario) on `CG-17-GC` / the VIN to see which returns K-Type/engine/kW.
3. Ask TelePeças for integrator terms and *explicitly whether a competing webshop may use their data*.
4. Decide Option D as launch plan, upgrade to A or B when evidence arrives.

## Round 6 additions
| Provider | Role | Setup | Monthly | Per call | Notes |
|---|---|---|---|---|---|
| **Tips4y plate pack (Pack 300)** | PT plate → TecDoc Vehicle ID | n/a | n/a | **€0.10 + VAT** (300 for €30) | Only for Tips4y TecDoc catalogue clients (cash terms), **not for resale**, API terms QUOTE REQUIRED |
| **Solutions4yb** | PT TecDoc WS 3.0 webshop plugin + Autodata + ERP (PHC, Inforap, ActiveX, Artsoft) | QUOTE REQUIRED | QUOTE REQUIRED | QUOTE REQUIRED | Primavera not listed; plate source unstated |

**Cheapest known plate lookup (DOCUMENTED): Tips4y ≈ €0.10**, then Openapi €0.18 (200k/yr), Matricula.co.pt €0.18–0.20, TelePeças ≈ €0.12–0.25 per decode. **Cheapest K-Type-capable and Portuguese: Tips4y** (TecDoc Vehicle ID). Updated ranking of next commercial action: (1) Tips4y: bundle TecDoc catalogue + plate; (2) TecAlliance direct quote as the price anchor; (3) Solutions4yb as a second integrator quote.
