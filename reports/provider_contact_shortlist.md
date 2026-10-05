# Provider contact shortlist (max 5)

> **Round 6 update: two PT-documented plate→TecDoc-ID routes: Autoways (OpenAPI spec confirms PT plate + PT VIN→K-Type, kW, engine code; free demo token) and Tips4y (TecDoc Vehicle ID + TecDoc web service; ≈€0.10/lookup pack). Start both in parallel.** Tips4y (tips4y.pt) below: Portuguese vendor documenting *plate → TecDoc Vehicle ID via API* **and** a TecDoc web service/B2B webshop. Ask: price for plate API + TecDoc WebService/B2C licence (are they a TecAlliance reseller?), coverage of K-Type for client car (CG-17-GC / VIN VF3MCYHZUPS034433), data source, caching/storage rights, Primavera integration, trial/sandbox, contract term. Known price: none. Target: plate API ≤ €0.15/call or bundled; ramp pricing on TecDoc. Autoways, Openapi, Vincario, TecAlliance follow; Matricula.co.pt is the cheap test.


Prices are vendor-published figures (DOCUMENTED, ex-VAT unless stated). None negotiated.

## 1. Autoways "AutoNow PT" (plate/VIN → K-type)
- **Why:** only candidate claiming Portuguese plate **and VIN → TecDoc K-type**, i.e. the bridge. Scoped for e-commerce.
- **Role:** identity + bridge key.
- **Ask:** free demo; response sample for CG-17-GC; fields (engine code, kW, ktype, type-approval); is K-type licensed for use without our own TecDoc licence?; data source; caching/storing rights; price per call and monthly plans; SLA.
- **Known price:** none. **Target:** ≤ €0.15/call at 10k+/month, caching of customer-confirmed vehicles allowed.

## 2. Openapi.com, Portuguese Car Check
- **Why:** documented REST + OAuth, free signup + sandbox, public price list, VIN + version + hp in response.
- **Role:** primary cheap plate identity candidate.
- **Ask:** full sample response for CG-17-GC (sandbox), whether kW / engine code / type approval exist, data source, whether results may be stored for the customer's garage, enterprise price at 50–100k/yr, uptime.
- **Known price:** €0.18+VAT base; €0.40 @1k/yr down to €0.18 @200k/yr. **Target:** ≤ €0.18 at ≤50k calls/yr; storage allowed.

## 3. Matricula.co.pt (RegCheck)
- **Why:** confirmed 10 free test credits; €0.20 per call; cheap to test now.
- **Role:** alternate / cross-check plate source.
- **Ask:** field list incl. kW and version; source; terms for caching; volume price beyond 1000-blocks.
- **Known price:** €0.20 (−10% >1000-blocks). **Target:** ≤ €0.15 at volume.

## 4. Vincario (vindecoder.eu)
- **Why:** EU-focused VIN decoder claiming PT coverage, kW, variant, TecDoc/ktype mapping, 20 free test VINs, published tiers.
- **Role:** VIN route and K-type bridge cross-check.
- **Ask:** run 20 PT VINs incl. VF3MCYHZUPS034433; fields returned; ktype accuracy; enterprise caching tier terms.
- **Known price:** €0.49/100, €0.298/500, €0.249/1k, €0.22/5k; invalid VINs free. **Target:** ≤ €0.15 at 10k+.

## 5. TecAlliance Portugal / reseller (TecDoc Catalogue Reseller or Data Integrator partner)
- **Why:** the actual fitment source; also provides VRM later; we need the earliest realistic date and cost.
- **Role:** catalogue + fitment + vehicle IDs (future/premium).
- **Ask:** timeline; licence cost model (volume/users/distribution); is there a reseller or lighter web-service tier for a new webshop; PT plate (VRM) module; sandbox access.
- **Known price:** none public (negotiated annually). **Target:** written quote and start date.

*Also, but not for an outside vendor:* ask Fahad which plate software he uses and its data source (could be the best, cheapest route); and ask partslink24/LexCom in writing about API/integration rights (public ToS says no).

*Not on the list:* TelePeças (call only if Fahad already deals with them), MatriculAZ (API not launched; terms forbid automation), free consumer sites (terms forbid commercial/automated use), Auto Delta (supplier, not a data API).
