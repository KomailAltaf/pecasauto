# PeçasAuto — five-minute David demo

Status: implementation prototype submitted for independent re-review. The customer journey and system boundaries are implemented. Catalogue, inventory, fitment, shipping, payment and the explicit conflict scenario are demonstrative data unless a screen says otherwise.

## Before the demo

Run PostgreSQL, Strapi, FastAPI and Next.js using the commands in `README.md`. Set `DEMO_MODE=true` deliberately for this session; it defaults to `false`.

Open:

- storefront: `http://localhost:3000`
- CMS: `http://localhost:1337/admin`
- API docs: `http://localhost:8000/docs`

## 0:00–0:40 — Start with the customer journey

Open the homepage. Point out the four routes customers understand:

- matrícula
- VIN
- manual vehicle selection
- OE / part reference

The browser calls FastAPI only. No customer-facing code calls Auto Ways, TecDoc or another provider directly.

Also point out the labels. The prototype distinguishes `REAL TESTED DATA`, `DEMO DATA`, `DOCUMENTED CAPABILITY`, `WAITING FOR ACCESS`, `MOCK` and `UNVERIFIED RESEARCH`.

## 0:40–1:25 — Show honest lookup behaviour

In the matrícula tab, enter the neutral example `AB-12-CD`.

Expected result: `WAITING FOR PLATE PROVIDER`. No vehicle candidate should appear because no configured provider returned one.

In the VIN tab, the client test VIN may be entered if needed. The actual vPIC response is labelled `REAL TESTED DATA` and `BASIC`; it does not identify an engine, exact variant or K-Type. The UI asks for manual completion instead of pretending the vehicle is resolved.

Open the validation panel and show that the trace contains only providers relevant to the selected input. Auto Ways is `NOT CONFIGURED`; vPIC is the tested VIN source.

## 1:25–2:05 — Demonstrate the candidate-confirmation UX

Click `Carregar exemplo de conflito`.

State clearly: this is a `DEMO CANNED RESULT`; it is not a plate lookup and no external provider was called. It exists only to demonstrate multiple candidates and user confirmation.

The candidates are limited to `ENGINE` precision, require a second source/user confirmation, and contain no invented external vehicle ID or K-Type.

Choose a candidate and save it to `Meu Carro`. The saved record retains its demo provenance and confirmation method.

## 2:05–3:00 — Browse the demonstrative catalogue

Open the catalogue and a product page. Show:

- synthetic `SAMPLE-*` product and OE references
- IVA-inclusive demonstrative prices
- `ESTIMATIVA DEMO` delivery timing
- no positive compatibility claim
- `CONFIRMAR COMPATIBILIDADE` / `COMPATIBILIDADE POR VERIFICAR`

Explain that vehicle identity and product fitment are separate. A saved vehicle does not make a product compatible. Only a trusted `FitmentProvider` may eventually return that result.

Add an item to the cart and change its quantity. Empty carts have zero shipping and zero total. During checkout, the browser submits product IDs and quantities; FastAPI calculates prices from the server-side catalogue. Payment and shipping remain demo-only.

## 3:00–3:40 — Show the provider evidence matrix

Open `/admin/providers` through the local prototype login. The FastAPI role boundary is real; this is still a local demonstration identity system, not production authentication.

Show the distinct evidence states:

- vPIC: `TESTED`, VIN only, BASIC result
- Auto Ways: `NOT CONFIGURED`; documented fields are not test evidence
- TIPS4Y, TelePeças and TecDoc: documented capability / waiting for access
- Autofrance: research only, not a production integration
- partslink24: manual validation / OE source only
- Primavera: future operational ERP boundary
- GLS: not configured

Unknown prices and rights remain unknown.

## 3:40–4:30 — Edit published content in Strapi

Open Strapi. Show that it owns editorial content only:

- homepage and page-builder sections
- product copy
- brands and categories
- homepage hero and product editorial (rendered now)
- pages, navigation, footer, FAQ, SEO, banners and promotions (modelled in Strapi, not yet rendered)

Edit a harmless homepage or product editorial field, save as a draft, confirm the published storefront does not change, then publish and refresh the storefront. Revert the demonstration edit afterward.

FastAPI still owns price, stock, vehicle identity, fitment, carts, orders and integrations. Strapi cannot publish operational truth.

## 4:30–5:00 — Architecture and close

Open `/architecture` and explain:

```text
Customer → Next.js → FastAPI → vehicle/provider adapters → normalized vehicle
                  ↘ Strapi published editorial content
FastAPI → catalogue bridge → fitment → live inventory/price → order rules
        → future Primavera / GLS / payment integrations
```

TecDoc can later enter through the provider interfaces without rebuilding the storefront. Product editorial remains separate from live operational data.

## What the prototype proves

- the click-through customer journey
- the Next.js / FastAPI / Strapi ownership boundary
- provider-independent identity orchestration
- honest waiting, partial and multiple-candidate states
- manual confirmation and saved-vehicle state
- demonstrative catalogue, cart and checkout mechanics
- server-side order pricing
- compatibility safety defaults
- provider evidence/status presentation
- replaceable TecDoc, Primavera, partslink24 and GLS boundaries

## What it does not prove

- a working Portuguese matrícula provider
- the disputed client vehicle's exact model, engine, variant or K-Type
- licensed production fitment
- production product, stock, price or delivery data
- live Primavera, payment or GLS integrations
- that documented provider capability has been tested
- production security, operations or scale

The correct closing line is: **the implemented flow and safety boundaries are real; provider access and operational automotive data remain evidence-gated.**
