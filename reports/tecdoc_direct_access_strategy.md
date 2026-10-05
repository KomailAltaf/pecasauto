# TecDoc direct access strategy (Portugal)

Date 2026-10-05. Tags: DOCUMENTED = public page; QUOTE REQUIRED = no public figure. Nothing here was negotiated or tested.

## DIRECT TECALLIANCE ROUTE
- TecAlliance's own TecDoc page lists **VIN decoder, VRM (plate) matching, KType and vehicle-detail search** under both **direct licensing** and **partner/reseller channels** (DOCUMENTED).
- The licence "can only be provided by TecAlliance directly or through authorised partners" (secondary source; consistent with TecAlliance's page).
- **Pricing is not public.** Secondary sources describe a model of *percentage of shop turnover with an annual minimum*, plus the data package (article groups, vehicle types, languages, refresh rate, web service vs database export). Treat as UNVERIFIED hearsay; QUOTE REQUIRED.
- Public contact path: TecDoc product page "Contact us" and TecAlliance online shop (`solutions.tecalliance.net`, `shop.tecalliance.net`). **Not found:** a Portugal/Iberia email or phone.
- Whether a small startup tier exists: **not published.** QUOTE REQUIRED.
- Whether Portuguese VRM is included in the base web service or a separate module: **not published**; must be asked explicitly.

## PORTUGAL PARTNER ROUTE
- TecAlliance has dedicated Spain+Portugal commercial leadership: the TecDoc commercial owner for Spain and Portugal was named as **José Antonio Tercero** (Jornal das Oficinas, 25 Sep 2021; may be out of date; verify before use). The article gives no contact details.
- Partner programme tiers (Gold/Silver/Partner/Consultant) with specialisations incl. **TecDoc Catalogue Reseller** and **TecDoc Data Integrator** (DOCUMENTED, Brazil page; confirm equivalents for Portugal).
- The contact on the page found is TecAlliance Brazil's; **do not use it for Portugal.** Use the TecDoc "Contact us" form and state "Portugal".
- A Portuguese partner I found: **Tips4y** (TecDoc webshop/B2B integrator). **Correction (round 6):** the genuine domain is **tips4y.pt** (valid GlobalSign wildcard certificate for `*.tips4y.pt`; the server just omits the intermediate certificate, so some tools report 'unable to verify'). The earlier problem was on a different host, `tips4y.webcomum.com`, whose certificate belongs to another server: use tips4y.pt only.

## RESELLER ROUTE
- Resellers/integrators add margin and bundle development; benefits: faster start, sometimes a lighter licence, Portuguese support. Risks: markup, lock-in, unclear whether K-Type/VRM data may be reused outside their platform.
- Fahad/Luis quote: **not in the repo, unknown. QUOTE REQUIRED** (Komail to attach it).

## WHAT TO ASK (send to TecAlliance and one PT partner, same questions)
1. Direct licence for a **Portugal-only B2C/B2B webshop**: model (turnover %, minimum, per-user), setup fee, term, minimum commitment.
2. Is a web-service licence available without the full database? Smallest package that gives: **vehicle search by Portuguese plate (VRM), VIN, KType, vehicle → articles, OE ↔ aftermarket cross-references, article images/attributes**.
3. Is **Portuguese VRM** included? Source of the PT plate data? Per-lookup fee? Caching/storage rights for vehicle IDs the customer confirms?
4. Is a **sandbox/trial** available, and how long until credentials?
5. Time from signature to production data.
6. Direct vs partner price difference for the same scope.
7. Can the licence cover **Primavera-linked stock display** and our own search UX (no restriction on how stock is shown)?
8. Data refresh frequency; SLA; terms on reusing KType in our own database.

## WHAT WE ACTUALLY NEED (minimum viable)
- Vehicle identification by **PT plate + VIN → KType**.
- **Vehicle → article links** with restrictions/criteria (the real fitment).
- **OE and cross-reference numbers**, EAN where available.
- Article basics (brand, group, attributes, images). Portugal-market data only.
- Web service (API), not a full data dump (unless cheaper).

## WHAT WE DO NOT NEED
- Other-country vehicle data and languages beyond PT/EN.
- Workshop data (TecRMI repair/labour), truck/motorcycle/commercial modules at launch (unless Fahad sells them).
- Their B2B webshop product (we are building our own UX).
- TecCom ordering (Primavera + supplier feeds cover stock/orders).
- Vehicle valuation, insurance data, or registration-fee modules.

## LIKELY NEGOTIATION ANGLES
- **Scope reduction:** Portugal-only, API-only, limited article groups at launch (add later).
- **Ramp pricing:** low minimum in year 1; step up with turnover (new brand, zero sales history).
- **Reference customer:** a new Portuguese brand with an existing distributor (Fahad) as anchor.
- **Competitive tension:** PT partner quote vs direct quote vs Autoways/TelePeças combined stack (shows we have a pre-TecDoc alternative, so we are not desperate).
- **Bundle VRM:** ask for plate lookups included instead of paying per-call to a third party.
- **Term:** ask for a pilot period with sandbox before the minimum commitment starts.
