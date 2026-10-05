# Portugal-only provider landscape

Checked 2026-10-05. `DOCUMENTED` means a provider page describes the capability; it does not mean the client case was successfully returned.

| Provider | PT plate | VIN | Engine/power/variant | Catalogue ID / fitment | Access / price | Rights state | Campaign status |
|---|---|---|---|---|---|---|---|
| Existing client software | Possible | Possible | Unknown | Unknown | Client access, not local | Export/API unknown | WAITING FOR HUMAN ACCESS |
| TelePeças | Documented | Documented | Technical fields claimed; exact depth untested | Docs expose TelePeças ID, TecDoc model ID, optional KType and OEM/compatibility | OAuth seller/integrator credentials; quote | Contract required | ACCESS TESTED; DATA UNTESTED |
| Matricula.co.pt | Yes | VIN advertised among fields | Make/model/engine size + 20 fields; engine code unknown | ABI code, no KType mapping proven | 10 free; €0.20/call advertised | Terms/cache/storage unknown | ENDPOINT ACCESS TESTED; CREDENTIAL BLOCKED |
| Openapi PT-car | Yes | VIN documented in response | Model/version/fuel/displacement/CV | ABI code; no KType mapping proven | €0.40 PAYG; €0.18/0.24/0.28/0.30/0.33/0.37 published annual tiers | B2B API documented; reuse terms to verify | DOCUMENTED ONLY |
| Tips4y | Yes | Connected | Vehicle characteristics advertised | Explicit VIN + TecDoc KType / TecDoc webservice | Quote | Contract required | DOCUMENTED ONLY |
| Autofrance | No PT plate | Reachable VIN endpoint | Actual engine/fuel/kW/hp result | Actual KType; identity cross-checked publicly | No request fee observed; 10/min documented | RESEARCH ONLY; production reuse/brand coverage unknown; no existence check | ACTUAL TEST; ENGINE-level / disputed model |
| NHTSA vPIC | No | Yes | Client case returned none | None | Free | Public/open data | ACTUAL TEST; BASIC_ONLY |
| Self-hosted vPIC | No | Yes | Same as public vPIC | None | Infra only | MIT code/NHTSA data | ACTUAL TEST; BASIC_ONLY |
| Vincario | No PT plate proved | Global/EU marketed | Detailed engine/variant fields documented | KBA/type-approval fields; KType not proven in our test | 20 B2B tests advertised; published paid tiers | Terms required | ACCESS REQUIRED / UNTESTED |
| Vehicle Databases EU VIN | No | EU-specific documented | Detailed EU specs documented | No KType shown | API key required | Terms required | UNTESTED |
| Munic/Ekko | No PT plate proved | Europe region documented | Rich vehicle description | GraphQL schema includes KType | Credentials likely required | Terms required | UNTESTED |
| TecAlliance Vehicle Identification | VIN + VRM documented | Yes | Harmonised TecDoc vehicle data | Direct KType/NType and catalogue ecosystem | Quote/contract | Licensed | DOCUMENTED PREMIUM BASELINE |
| partslink24 | No production plate API proved | Manual VIN functions documented | OEM catalogue context | OEM/genuine-parts validation | Existing client subscription | Automated reuse blocked until written permission | MANUAL RESOURCE; NO PROGRAMMATIC ASSUMPTION |

## Exhaustion boundary

Accessible automated no-account routes were exercised: local parser, public vPIC, self-hosted vPIC and the Autofrance research endpoint. Catalogue identity cross-checks were also recorded. The remaining decisive Portugal-specific routes require an account/token, contract/client access, or human screenshots from normal manual use. No signup was completed in Komail/Fahad's name and no paid credit was purchased.
