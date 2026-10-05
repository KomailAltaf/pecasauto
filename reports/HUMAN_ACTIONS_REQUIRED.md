# Human actions required

I did not create any account: each needs Komail's or Fahad's real name, email or WhatsApp, and I will not invent or substitute details. Priority P0 = unblocks the client-car test.

### Autoways (AUTO-NOW): plate/VIN → K-Type  [P0, now the highest-value test]
ACTION: Create free demo account (form: full name/company, WhatsApp number with +351, optional website; 3 steps: info → verification → password; they say the demo account arrives within 24 h).
URL: https://app.auto-ways.net/demo
COST: €0
WHY: only provider with a documented *plate/VIN → TecDoc K-Type* API; tests CG-17-GC and the VIN. **Portugal plate and VIN→K-Type are documented in the vendor's OpenAPI spec (SwaggerHub, round 6)**. Ask in the form/WhatsApp: "Do you support Portuguese plates and return K-Type for Portugal?"
WHAT TO SEND BACK: API key/token, or the JSON for CG-17-GC and VF3MCYHZUPS034433 (redact nothing in the vehicle fields).
PRIORITY: P0

### Matricula.co.pt
ACTION: Register a test account and verify email; they advertise 10 free lookups.
URL: https://www.matricula.co.pt (Register form on the home page)
COST: €0
WHY: Codex's call with no valid username returned `Your username is incorrect`, so the endpoint is live but untested. Need the real Portuguese response fields (kW, version, engine code?, ktype?).
WHAT TO SEND BACK: username (not password), the raw XML/JSON for CG-17-GC.
PRIORITY: P0

### Openapi.com (Portuguese Car Check)
ACTION: Create free console account, generate a sandbox OAuth token, call `GET https://test.automotive.openapi.com/PT-car/CG-17-GC`.
URL: https://console.openapi.com
COST: €0 for sandbox. Production pay-as-you-go €0.40+VAT/call: **do not run production without approval**.
WHY: Documented 30+ fields incl. version, hp, VIN, ABI code; sandbox may return sample data only, so also ask whether sandbox returns real plates.
WHAT TO SEND BACK: sandbox JSON, plus their answer on storing results.
PRIORITY: P0

### TelePeças
ACTION: Request API credentials via the contact form (subject "api"); ask about plate/VIN decoding access without a seller subscription.
URL: https://www.telepecas.com/contactos/?assunto=api (pricing: https://www.telepecas.com/precos/)
COST: €0 to ask. Public price list: VIN/plate decoding **€25 per 100 → €615 per 5,000 accesses (€0.25 → €0.123)**; technical data €1.93–8.00 per access; "Serve no meu carro?" €1.99 single / €0.16–0.25 volume; seller plans €150–1,200/month (API access listed on the €1,200 Ultra plan). Buying through an integrator account: QUOTE REQUIRED.
WHY: its API docs list `ktype`, `tecDocModelId`, `telepecasModelId`, engine, kW, version. Also asks: is a competing webshop allowed to use it (TelePeças is itself a marketplace).
WHAT TO SEND BACK: client id/secret (privately), response for CG-17-GC, and written terms.
PRIORITY: P0

### Vincario (VIN)
ACTION: Create a free trial account (20 free VIN lookups).
URL: https://vincario.com
COST: €0
WHY: only EU-focused VIN decoder claiming variant/kW/ktype; test `VF3MCYHZUPS034433` and 19 more PT VINs.
WHAT TO SEND BACK: API key (privately) or raw JSON.
PRIORITY: P1

### TecAlliance (direct) and one Portuguese partner
ACTION: Send the questions in `reports/tecdoc_direct_access_strategy.md` via the TecDoc "Contact us" page, stating Portugal; same email to one partner.
URL: https://www.tecalliance.net/solutions/tecdoc
COST: €0
WHY: needed to get a priced path to fitment and the earliest start date.
WHAT TO SEND BACK: written quotes, scope, start date.
PRIORITY: P0 (long lead time)

### Fahad
ACTION: (a) Send the Luis/partner TecDoc quote and any contract; (b) Portuguese registration certificate **or** a partslink24 VIN screenshot for CG-17-GC (engine code, kW, first registration, gearbox); (c) 10–20 more Portuguese vehicles the same way; (d) name of the plate-lookup software already in use and its data source; (e) partslink24 contract: written answer from LexCom on API/integration; (f) Primavera version/modules; (g) Auto Delta customer login if any.
COST: €0
WHY: ground truth for scoring; stops us paying for what he already owns.
PRIORITY: P0 for (a), (b), (d); P1 rest

### Tips4y (only if you want a PT integrator quote)
ACTION: Use **tips4y.pt** (not tips4y.webcomum.com), then request a quote (see Tips4y section above).
COST: €0
PRIORITY: P2

### Manual plate lookups on public Portuguese parts sites (NEW, fastest free test)
ACTION: A human types `CG-17-GC` into the plate/matrícula box (no signup, no purchase) on several Portuguese parts shops, and screenshots the "your vehicle" box, **including the page URL** (Autodoc-style URLs contain the TecDoc K-Type, e.g. `…/130708-1-5-bluehdi-130`). Suggested: auto-doc.pt, motointegrator.pt, expertautopecas.pt, norauto.pt, sofrapa (loja.sofrapa.pt), autopartslogistic.com. Do not automate; their terms generally forbid it, a person typing one plate is normal use.
COST: €0 (≈10 minutes)
WHY: gives several independent plate→vehicle(+K-Type) answers for the client car without any API account. Decides 3008 vs 5008 from the plate side.
WHAT TO SEND BACK: screenshots with URL for each site.
PRIORITY: P0

### Tips4y (Portuguese: plate → TecDoc Vehicle ID + TecDoc web service) NEW P0
ACTION: Contact via https://www.tips4y.pt/en/plate-number-search or the contact page. Ask for a demo/trial of the plate API using `CG-17-GC` and VIN `VF3MCYHZUPS034433`, and a quote for plate API + TecDoc WebService for a B2C shop in Portugal. Questions in `reports/provider_contact_shortlist.md` (#1).
URL: https://www.tips4y.pt/en/plate-number-search
COST: €0 to ask
WHY: only PT vendor documenting both plate→TecDoc ID and the TecDoc catalogue service; could replace the plate-provider + TecDoc-direct combination.
WHAT TO SEND BACK: demo result for the client car, quote, terms.
PRIORITY: P0

NOTE (round 6): after getting the Autoways token, run exactly: `GET https://app.auto-ways.net/api/v1/pt?plaque=CG17GC&token=<yours>&output_lang=en` and `GET https://app.auto-ways.net/api/v1/vin/?vin=VF3MCYHZUPS034433&country=PT&token=<yours>`; send back the two JSON bodies. Expect fields `AWN_modele`, `AWN_k_type`, `AWN_code_moteur`, `AWN_puissance_KW` (per vendor spec). If the plate returns `AWN_k_type=130708` the plate and VIN agree on a 3008; if it returns a 5008 K-Type (130738 family) the screenshot's plate and VIN are inconsistent.
