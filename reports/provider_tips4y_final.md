# Tips4y: commercial position

Basis: tips4y.pt pages (as returned by search/fetch summaries; direct fetch fails TLS verification because the server omits its intermediate certificate, which I did not bypass), `tips4y.odoo.com` purchase page, trade-press articles (Jornal das Oficinas, Revista Pós-Venda) read 2026-10-05. **Nothing tested.** The brief asked for a direct contact person: **none found publicly; I will not guess one.**

## Verdict
**Commercially the most interesting Portuguese option: one vendor that documents plate → TecDoc vehicle number *and* a TecDoc web-service/webshop, with the cheapest published plate price (≈€0.10).** But the cheap plate pack is restricted to its own TecDoc customers, so the real question is the bundled TecDoc quote, not the €30 pack. Contact now; compare against Fahad's reseller quote and TecAlliance direct.

## Checklist
| Question | Finding | Tag |
|---|---|---|
| Portugal presence | Portuguese-language site, `.pt` domain, Portuguese trade press, Portugal-specific plate service; "Especialistas em Dados para o Ecossistema Automóvel". Company registration/address not captured | DOCUMENTED |
| TecDoc relationship | Sells **TecDoc catalogue solutions, a TecDoc B2B WebShop, a TecDoc WebService** (for your own B2B/B2C shop) and a TecRMI portal. The plate pack is "exclusive to TecDoc-catalogue customers". Strongly suggests reseller/partner status. **Whether Tips4y is an authorised TecAlliance partner/reseller is not stated in the pages read** (TecAlliance's partner programme has "TecDoc Catalogue Reseller" and "Data Integrator" roles) | LIKELY; UNVERIFIED; ask both Tips4y and TecAlliance |
| Portuguese matrícula lookup | Yes. "Pesquisa por Matrícula": 99.3 % of vehicles in circulation after 1989 incl. imported; 98 % unique-coding rate; >8 million queries/year (marketing claims) | DOCUMENTED; UNVERIFIED |
| TecDoc vehicle number / K-Type | Yes: service "provides detailed vehicle data and the corresponding TecDoc vehicle number". Exact JSON field names unknown | DOCUMENTED |
| €30 + VAT / 300 lookups pack | **Confirmed on the purchase page:** "Pack 300" = €30 + VAT for 300 plate searches (≈€0.10 each); bought online in the customer's reserved area; "exclusive to TecDoc catalogue customers with cash payment terms"; **"NOT AVAILABLE FOR RESALE"**; validity period not stated; no other pack tiers shown | DOCUMENTED |
| API / web service | Plate search "can be integrated via API"; TecDoc WebService offered for own shops. API docs, auth, limits not public | DOCUMENTED; terms QUOTE REQUIRED |
| Ecommerce commercial rights | Not stated. The "no resale" clause needs interpretation: showing a looked-up vehicle to our own shop customers is probably in scope, passing lookups to third parties is not. **Written confirmation required** that a public B2C webshop may use the plate API | QUOTE/WRITTEN ANSWER REQUIRED |
| Plate lookup needs separate TecDoc licence? | **Effectively yes in the sense that the pack is only sold to TecDoc customers of Tips4y.** Whether the API plate service can be bought standalone: unknown | UNKNOWN: ask |
| Caching/storage | Not stated. Assume forbidden until confirmed | QUOTE REQUIRED |
| Setup / monthly / minimum | Not published | QUOTE REQUIRED |

## Why it matters commercially
- If Tips4y is a TecAlliance reseller, **one conversation could cover:** plate lookup → TecDoc vehicle number, catalogue/fitment web service, and a webshop module: the exact bridge the project lacks (identity → catalogue ID → fitment).
- Plate price (≈€0.10) is below every other published price (Openapi €0.18 at 200k/yr, Matricula.co.pt €0.18–0.20, TelePeças ≈€0.12–0.25 per decode).
- Risks: dependence on a reseller margin on TecDoc; lock-in to their webshop; "no resale" and customer-eligibility conditions; unverified accuracy claims; site TLS misconfiguration (minor, but ask them to fix it).

## Test / questions
HUMAN ACTION: request a demo or trial of the plate API with a test plate (use a vehicle for which we hold the client's permission; see drafts) and a quote for TecDoc WebService for a Portugal-only B2C shop. Draft in `reports/provider_contact_drafts.md`. Decide before sending whether to include the client's real plate/VIN.

**Status: DOCUMENTED, NOT TESTED, QUOTE REQUIRED.**
