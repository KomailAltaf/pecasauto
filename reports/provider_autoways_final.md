# Autoways (Auto Ways Network, "AUTO-NOW"): commercial position

Basis: vendor's public OpenAPI specs (SwaggerHub registry, saved in `reports/claude_raw_evidence/autoways/`), website, FAQ and CGV (terms of sale) read 2026-10-05. **No call to the API has been made** (no token). Tags: DOCUMENTED (vendor says so), UNVERIFIED (not tested), QUOTE REQUIRED.

## Verdict
**Best documented single-vendor route to plate/VIN → K-Type + engine code + kW for Portugal. Not tested; price unknown; K-Type/TecDoc reuse rights unknown.** Worth a demo token immediately (free, ≈24 h). Not a production dependency until the six open questions below are answered in writing.

## Capability checklist
| Question | Answer | Tag |
|---|---|---|
| Portuguese matrícula | Yes: `GET https://app.auto-ways.net/api/v1/pt?plaque=<plate>&token=<token>&output_lang=en\|fr`; "80M license plates in Portugal" | DOCUMENTED (spec) |
| VIN | Yes: `GET /api/v1/vin/?vin=<VIN>&country=PT&token=<token>`; spec lists Germany, Austria, Belgium, Spain, France, Italy, Portugal | DOCUMENTED (spec) |
| K-Type | Yes: field `AWN_k_type` in both responses; also `AWN_TID`, `AWN_libelle` (TecDoc-style label). Their SDK page says results come from "matching algorithms between registration data and the SRA / TECDOC / NATCODE reference databases": **K-Type is derived by matching, not supplied by TecAlliance** | DOCUMENTED; accuracy UNVERIFIED |
| Fields returned (vendor examples, not our vehicle) | PT plate example: `AWN_VIN, AWN_marque, AWN_modele, AWN_modele_etude, AWN_k_type, AWN_puissance_chevaux, AWN_puissance_KW, AWN_code_moteur, AWN_energie, AWN_nbr_cylindre_energie, AWN_date_mise_en_circulation, AWN_numero_de_serie, AWN_TID, AWN_libelle`, many unknowns returned as `0`/`Inconnue`. VIN example adds `AWN_version`, `AWN_type_mine`, dimensions, weight, CO2. Site claims 100+ fields | DOCUMENTED; real PT completeness UNVERIFIED (the PT example has several zero/unknown fields) |
| Free test | Demo form `https://app.auto-ways.net/demo`: full name/company, WhatsApp (+351 available), optional website; 3 steps (info, verification, password); FAQ says demo account within 24 h. CGV says **20 free credits for new users**. The credit amount in the demo flow itself was not visible | DOCUMENTED (CGV/FAQ) |
| Price model | **Credits**: "1 API credit = 1 request"; monthly credit plans (PayPal/card) or pay-per-request; only HTTP 200 responses consume credits (FAQ); cancel any time; no refunds except proven API error; RapidAPI resale has separate plans/terms. **Price table is loaded by JavaScript and was not retrievable** | per-lookup price: **QUOTE REQUIRED** |
| Commercial usage (e-commerce) | Marketed for parts e-commerce, insurance, garages. The CGV does not restrict or grant ecommerce use explicitly | DOCUMENTED marketing; contractual right UNVERIFIED |
| Caching / storage | **CGV and FAQ are silent.** Cannot cache or store results until written confirmation | QUOTE/WRITTEN ANSWER REQUIRED |
| Separate TecDoc licence needed? | **Not stated anywhere.** Autoways references TecDoc as a reference database; whether using the K-Type identifier in our own catalogue requires our own TecAlliance licence is unanswered | UNKNOWN; ask Autoways and TecAlliance |
| K-Type legal use in our system | K-Type is TecAlliance's vehicle identifier. A number being returned by a third party does not by itself grant rights to TecDoc *data* (parts links); we would still need a licensed catalogue to use it for fitment. Using it as an internal key is likely low-risk but **not confirmed**. Not legal advice | UNKNOWN |

## Red flags / diligence
1. **Counterparty and jurisdiction unclear:** contact is a web form, an obfuscated email, and a WhatsApp number with a Moroccan country code (+212). Site claims EU hosting and GDPR compliance, with no company registration details found in the pages read. Ask for legal entity, registered address, DPA.
2. **Data origin undisclosed:** "official database in real time" without naming the source (for Portuguese plates likely IMT-derived via an intermediary). We cannot assess lawfulness of onward use. Ask for the source and a written statement of rights.
3. **Public credential leakage:** a public GitHub gist from the vendor contains an API token in clear text and the swagger spec pre-fills a default token. I did not use either. Tell them; also a hygiene signal about their operational security.
4. **Derived K-Type:** matching algorithm output, not TecAlliance-issued: must be validated against a licensed catalogue and cross-checked (see `reports/ktype_crosscheck.csv`) before use. Unknown behaviour on 3008-vs-5008 style ambiguity (client_001).
5. **Single-source risk:** one small vendor, credits model, no stated SLA/uptime for PT.

## What to ask (also in `reports/provider_contact_drafts.md`)
Portugal legal entity and data source; per-lookup price at 1k/10k/50k/100k and monthly plans; commercial e-commerce use in a Portuguese B2C shop; caching/storage of plate, VIN, K-Type and engine data (and duration); whether a TecDoc licence is required to use K-Type/TID; sample real PT response (vehicle supplied by us); ambiguity handling (returns several candidates?); SLA; GDPR DPA.

## Test to run once a token exists (HUMAN ACTION: get token at the demo URL)
1. `…/api/v1/pt?plaque=CG17GC&token=<ours>&output_lang=en`
2. `…/api/v1/vin/?vin=VF3MCYHZUPS034433&country=PT&token=<ours>`
3. Compare: `AWN_modele`, `AWN_k_type` (130708 = 3008 SUV, 130738 = 5008 II), `AWN_code_moteur` (YHZ/DV5RC expected), `AWN_puissance_KW` (96 expected), plate-vs-VIN agreement. Store raw JSON in `reports/claude_raw_evidence/autoways/`.
Decision rule: both calls agree on the K-Type and a licensed catalogue/partslink24 confirms it → promote to PARTIALLY VERIFIED. Plate and VIN disagree → CONFLICT, no auto-selection.

**Status: WAITING FOR ACCESS.**
