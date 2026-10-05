# Portugal Provider Landscape (2026-10-05)

Evidence tags: **DOCUMENTED** = read on the vendor's public page/docs (a claim, not tested). **TESTED** = I made a real request. Only vPIC has been TESTED. Nothing below was bought or registered.

## Matrícula → vehicle (Portugal-specific)

| Provider | Matrícula / VIN | Fields claimed | API / trial / price | Rights & terms | Status |
|---|---|---|---|---|---|
| **Openapi.com "Portuguese Car Check"** `GET automotive.openapi.com/PT-car/{plate}` (sandbox `test.automotive.openapi.com`) | plate (formats `AA-00-AA`, `9027QL`…) | 20+: ABI code, make, model, **version**, fuel, engine size, **horsepower**, **VIN**, registration date, colour, indicative value. No engine code / kW / ktype documented | REST + OAuth token, free signup + sandbox; **PAYG €0.40+VAT; annual plans 1k/yr €0.37, 5k €0.33, 10k €0.30, 25k €0.28, 50k €0.24, 200k €0.18 per call** (verified on vendor page 2026-10-05; correction of my earlier range). Fields now listed as 30+, still no ktype/engine code/kW; 10,000 req/min | Says "official sources". Commercial/caching terms NOT seen | DOCUMENTED. **Best testable.** Sandbox response schema not published; test needed. |
| **Matricula.co.pt** (RegCheck family, Infinite Loop Development Ltd, Ireland) | plate | "20 fields": make, model, colour, engine size (standard fields: description, year, make, model, engine size, fuel, VIN) | SOAP/ASMX XML+JSON; **€0.20/query, 100-min packs, −10% >1000**; **10 free test credits after email verification** | Says real-time official government data. Terms for caching/resale NOT seen | DOCUMENTED. Cheapest testable with confirmed free test. Thin on power/engine code. |
| **Autoways "AutoNow PT"** (RapidAPI "VIN decoder support TecDoc catalog"; swaggerhub `salesautowaysnet`) | plate **or VIN**, "80M PT plates" | Car info **+ K-type for TecDoc compatibility** (claimed) | `GET /pt`; no public price; "request a free demo"; e-commerce scoped | Unknown | DOCUMENTED. Vendor = **Autoways / Auto Ways Network (auto-ways.net)**; REST/JSON, 100+ fields incl. K-Type, KBA, SRA, engine code, kW, VIN; free demo (24h) at app.auto-ways.net/demo; pay via RapidAPI credits; **Portugal plate + VIN K-Type documented in the vendor's own OpenAPI spec (round 6)**; TecDoc licence needs unstated. Contact. |
| **TelePeças** | plate or VIN, many EU formats | year, brand, model, variant/engine, class | site lists `/api/`; no public docs/price | Unknown | DOCUMENTED only. Contact. |
| **MatriculAZ** | plate | API doc lists 18 fields: VIN, make, model, version, year, fuel, power kW/CV, displacement, traction, gearbox, category… | REST `POST api.matriculaz.pt/v1/lookup`; **API "in preparation", not available**; price TBD | **Terms: commercial access only by specific agreement; automation/bulk prohibited; data source undisclosed; informational only** | DOCUMENTED. Not usable yet; watch. |
| **CheckViatura** | plate (free web) | make, model, version, year, fuel, cc, power, insurance | no API | **Terms forbid bots/scraping and commercialising content** | NOT USABLE for production; human spot-check only. |
| InfoMatricula / AutoMatrícula | plate (free web) | make/model/power/VIN/insurance/IUC | no API seen | users report wrong fuel/cc/year/power | NOT USABLE; low trust. |
| "Qual veículo é" app | plate | make, model, version | none | self-warns data may be wrong | NOT USABLE. |
| Fahad's existing plate software | unknown | unknown | unknown | unknown | **UNKNOWN: ask. Possibly the best direct route.** |
| IMT / IRN (official) | owner-driven certificate; inspection report by plate | per-vehicle technical certificate | no B2B lookup API found | official | Ground-truth tool only; no lookup API found. Not exhaustively checked (accredited-business access untested). |

## VIN → vehicle (EU)
| Provider | Evidence | Status |
|---|---|---|
| NHTSA vPIC (public) | **TESTED** on `VF3MCYHZUPS034433`: make + year only → **BASIC** | free; insufficient |
| Corgi / vin-lite / universal-vin-decoder | vPIC-derived or ~1–1.5k WMI codes | same ceiling; no gain |
| **Vincario (vindecoder.eu)** | claims EU/Portugal coverage, ~40 fields, kW, variant, body, transmission, **TecDoc/ktype mapping**; 20 free test VINs; **€0.49/100, €0.298/500, €0.249/1k, €0.22/5k per VIN; invalid VINs free**; enterprise caching tier | DOCUMENTED. **Best testable VIN route.** Needs signup. |
| Zylalabs "Europe Vehicle Decoder" / Apify VINdata | marketplace listings; 7-day trial on Zylalabs | Low priority; unverified depth |
| Autoways VIN→TecDoc (RapidAPI) | listing only | Check with AutoNow |

## Catalogue / fitment (pre-TecDoc)
| Provider | Role | Evidence | Rank |
|---|---|---|---|
| **TecAlliance via reseller/Data Integrator** | The real fitment source; Partner Program has "TecDoc Catalogue Reseller" and "Data Integrator" roles; web service licence; price negotiated, volume/users/model | DOCUMENTED | Future (premium). Ask whether a reseller can give a lighter, sooner licence. |
| **Infopro Digital Automotive (ETAI Ibérica, ISI Condal, HaynesPro)** | Iberian catalogues/technical data, B2B web services | DOCUMENTED (vague) | Temporary launch candidate to enquire; unclear if fitment API for webshops |
| Auto Delta (Leiria wholesaler) | **Supplier / client area, login-gated; no public catalogue or plate search** | DOCUMENTED | Not an API; a supplier + manual reference once Fahad has an account |
| partslink24 | OEM catalogues, VIN | **ToS prohibits integration into own services and automated extraction** | Validation / staff tool only (see FINAL §PARTSLINK24) |
| Apify/RapidAPI "TecDoc alternative" scrapers | repackaged TecDoc data | **Licensing very doubtful** | UNSUITABLE for production (rights risk) |
| Autodata, Webcat | UK-centric workshop data | no PT evidence | Unsuitable (no PT evidence) |

Excluded: random providers with no Portugal evidence.

## Update 2026-10-05 (round 4)
- **TelePeças** API docs (`api.telepecas.com/v1`, Bearer token, seller/integrator account needed) list `ktype`, `tecDocModelId`, `telepecasModelId`, engine, kW, version. Public prices: VIN/plate decoding €25/100 → €615/5,000; technical data €1.93–8.00; seller plans €150–1,200/mo. Unauthenticated call returned OAuth `invalid_client` (Codex raw evidence): endpoint alive, NOT a vehicle result.
- **Matricula.co.pt**: endpoint alive (Codex call returned 'Your username is incorrect'). Portuguese field list NOT published in the docs I could read (PDF covers UK).
- **Tips4y** (PT TecDoc webshop integrator): use the genuine domain tips4y.pt (the webcomum.com host has a mismatched certificate).

## Round 6 NEW LEAD: Tips4y (Portuguese), plate → TecDoc Vehicle ID + TecDoc web service
- Source: tips4y.pt pages as summarised by search (direct fetch blocked: server omits intermediate certificate; I did not bypass verification). Page: `https://www.tips4y.pt/en/plate-number-search`.
- **DOCUMENTED CAPABILITY:** "Pesquisa por Matrícula" returns detailed vehicle data **including the TecDoc Vehicle ID**; claims **99.3 % of vehicles in circulation after 1989** (incl. imported); **integrable via API**; also sells a **TecDoc WebService** (own B2B/B2C shop), a **TecDoc B2B webshop** integrated with the customer's own stock/prices, and TecRMI portal.
- **Why it matters:** the only Portuguese vendor found that covers *both* halves (PT plate → TecDoc vehicle ID, and TecDoc catalogue/fitment web service) from one contact. Fits Option B/A in the comparison; may be a TecDoc partner route that avoids buying plate and catalogue separately.
- **Unknown (QUOTE REQUIRED):** price, whether they are a TecAlliance reseller (licence passes through them), API terms, caching/storage, data source of the plate lookup, whether the K-Type is returned for all fuels/models, Primavera integration.
- **Status:** DOCUMENTED, UNTESTED. Contact is now **P0**.

### Tips4y pricing evidence (round 6, fetched 2026-10-05)
- **"Pack 300": €30 + VAT for 300 plate searches (≈ €0.10 per lookup)** at `tips4y.odoo.com/compra-pack-300`. Purchase inside the customer's reserved area; **exclusive to TecDoc-catalogue customers with cash payment terms; "NÃO DISPONÍVEL PARA REVENDA".** Validity not stated; other packs not shown on that page.
- Claims: 99.3 % of post-1989 vehicles identified; 98 % unique-coding rate; >8 million plate queries per year (trade press: Jornal das Oficinas, Revista Pós-Venda; marketing claims, UNVERIFIED).
- Implication: plate lookup is cheapest known (≈€0.10) **but bundled to being a Tips4y TecDoc client**. So Tips4y is probably a TecAlliance reseller/partner; plate price and TecDoc licence are one commercial conversation.
- Another PT integrator: **Solutions4yb** (Lisbon, founded 2014): TecDoc Web Services 3.0 WordPress plugin ("s4yb Parts TecDoc"), Autodata, ERP integration (PHC, Inforap, ActiveX, Artsoft: **Primavera not listed**), search by plate/VIN/engine/reference. Plate data source not stated. DOCUMENTED, UNTESTED; secondary contact.

## Round 6 UPDATE: Autoways spec (DOCUMENTED, vendor's own OpenAPI)
- **PT plate:** `GET https://app.auto-ways.net/api/v1/pt?plaque=…&token=…`; vendor example for a PT-format plate returns **VIN, make, model, K-Type (`AWN_k_type`), kW, hp, engine code (`AWN_code_moteur`), first-registration date, fuel, `AWN_TID`, `AWN_libelle`** (TecDoc-style label with chassis codes).
- **VIN:** `GET /api/v1/vin/?vin=…&country=PT`, "Germany, Austria, Belgium, Spain, France, Italy and Portugal"; adds `AWN_version`, `AWN_type_mine`.
- **This is the strongest documented single-vendor route to ENGINE/EXACT + K-Type for both plate and VIN in Portugal.** Free token via https://auto-ways.net/demo (24 h). Still UNTESTED; pricing unknown (credits via RapidAPI); TecDoc licence implications unknown; data origin "official database" unspecified.
- Raw spec: `reports/claude_raw_evidence/autoways/`. I did not use the default token in the spec or the token leaked in their public gist.

### Autoways terms (CGV, fetched 2026-10-05)
Credit-based ("1 credit = 1 API request"); monthly plans via PayPal/card or pay-per-request; **20 free credits for new users**; cancel anytime; no refunds except proven API error; RapidAPI resale has separate plans/terms. **Silent on data reuse, caching/storage, resale, and TecDoc/K-Type licence compliance** → must be asked in writing before storing K-Types. Price table is JS-loaded (not retrievable): QUOTE/ACCOUNT REQUIRED.
