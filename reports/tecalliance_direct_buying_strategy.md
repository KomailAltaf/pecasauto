# TecAlliance direct buying strategy

Basis: TecAlliance's public pages and trade press read earlier today; secondary commentary on licensing. **No quote exists in the repo and no TecAlliance figure is public.** Anything unknown below is **QUOTE REQUIRED**. I stopped additional web research on request.

## Is direct cheaper than Fahad's reseller quote?
**Cannot be answered: Fahad/Luis's quote is not in the repo (QUOTE REQUIRED: Komail to attach it) and TecAlliance has not been asked.** What can be said:
- TecAlliance states TecDoc is available by **direct licence or through partners/resellers**. A direct licence removes a reseller margin but usually adds integration work and minimum commitments; a reseller may bundle the webshop/integration and lighter terms.
- Reported (secondary, UNVERIFIED) pricing logic for TecDoc web-service licences: **percentage of shop turnover with an annual minimum**, plus data-package factors (article groups, vehicle types, languages, refresh rate, web service vs database export). Treat as a negotiating hypothesis, not a number.
- Compare **same scope on both quotes**, in a table: Portugal-only, plate (VRM) + VIN + K-Type, filters/brakes first, web service (not full export), B2C public shop, 12–36 month term.

## Facts gathered
| Item | Finding | Tag |
|---|---|---|
| Web Service | TecDoc Catalogue / Web Service lets own shops integrate TecDoc data via API (B2B and B2C) | DOCUMENTED |
| Vehicle identification | TecDoc page lists **VIN decoder, VRM matching, KType, direct vehicle search**; "vehicle identification in Germany, Austria, Belgium, Spain, France, Italy and Portugal" | DOCUMENTED |
| Portugal VRM | Portugal listed; whether PT VRM is in the base package or a paid module, and its per-lookup fee: unknown | QUOTE REQUIRED |
| VIN → K-Type | Documented in TecAlliance API documentation (OneDB / vehicle search "VIN to kType") | DOCUMENTED |
| Catalogue & fitment | Vehicle → article links with criteria, OE and cross-references, images, attributes | DOCUMENTED |
| Portugal-only package | Not published; ask explicitly | QUOTE REQUIRED |
| Direct licensing | Page: "direct licensing or partner channels"; contact through the TecDoc "Contact us" form | DOCUMENTED |
| Setup fee / minimum annual commitment / usage pricing | Not public | QUOTE REQUIRED |
| Iberia commercial contact | A 2021 trade-press article named **José Antonio Tercero** as TecDoc commercial owner for Spain and Portugal (previously Valeo Service Spain, Brembo Spain). May be outdated; **verify before use**. No direct email/phone found. Online shop: `shop.tecalliance.net`; solutions: `solutions.tecalliance.net` | PARTIALLY DOCUMENTED |
| Official Portugal partner | Partner programme tiers (Gold/Silver/Partner/Consultant) with roles "TecDoc Catalogue Reseller", "TecDoc Data Integrator". **No authorised Portuguese partner list obtained.** Candidates that sell TecDoc locally: Tips4y, Solutions4yb (status as authorised partners unverified) | UNVERIFIED |
| Cheaper entry tiers | TecAlliance and third parties sell online catalogue subscriptions (12-month); whether a web-service entry tier for new webshops exists: unknown | QUOTE REQUIRED |

## What we need (minimum scope)
PT plate (VRM) and VIN → K-Type; vehicle → article links with restrictions; OE/cross-reference numbers; article basics; web service; Portugal-only; **filters and brakes first** (add groups later).

## What we do not need
Other countries' data and languages; TecRMI repair/labour data; truck/moto/commercial modules at launch; TecCom ordering; B2B webshop product; valuation/insurance modules.

## Negotiation angles
1. Scope: Portugal-only, API-only, two product groups at launch, add groups on ramp.
2. Ramp pricing: low year-1 minimum (new brand, no turnover history); step up with sales.
3. Competing quotes: Fahad's reseller, Tips4y, TecAlliance direct, same scope sheet.
4. Bundle VRM/VIN lookups in the licence instead of per-call third-party fees.
5. Pilot term with sandbox before minimum commitment starts.
6. Rights: written permission to store K-Types and vehicle selections in our garage database; clarity on caching article data for performance.
7. Reference value: Fahad's existing distribution relationship.

## Questions to put in writing (see `reports/provider_contact_drafts.md`)
Package options and price for the scope above; setup fee; minimum annual commitment; usage fees for web-service calls, VRM and VIN; term; included updates; sandbox; whether a partner/reseller price is lower or higher for the same scope; caching/storage rights; whether K-Types obtained elsewhere can be used with our licence; implementation timeline.

## Next commercial action
1. Komail attaches Fahad/Luis's quote and scope. 2. Send TecAlliance direct request (draft #1). 3. Request Tips4y's bundled quote (draft #2). 4. Fill `reports/PROVIDER_COMMERCIAL_COMPARISON.md` with real numbers when they arrive.

**Status: QUOTE REQUIRED. Direct-vs-reseller question OPEN.**
