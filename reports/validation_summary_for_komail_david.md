# Validation summary for Komail + David

## 1. What worked for VIN?

**PARTIALLY VERIFIED:** Autofrance returned ENGINE-level data and KType 130708; independent public catalogue references cross-check the KType identity as a 3008. The VIN→KType assignment remains partial and research-only. vPIC returned make only. Local parsing safely validates structure but identifies no vehicle.

## 2. What worked for Portuguese matrícula?

**NOT VERIFIED:** no vehicle data was returned without credentials. Matricula.co.pt and TelePeças access requirements were confirmed by their actual error responses.

## 3. Which provider got exact engine/variant?

None reached independently verified EXACT_VARIANT. Autofrance reached ENGINE level and returned a catalogue ID, but no engine code and a model conflict.

## 4. Which free routes are useful?

Autofrance is useful as a research oracle proving that VIN→KType is technically achievable, but it is excluded from the production cascade. vPIC/local parsing are useful only for validation/routing. No free route is production-proven on Portuguese vehicles.

## 5. Which cheap paid route is best?

Matricula.co.pt is the cheapest first benchmark candidate (€0.20 advertised after 10 free tests); Openapi PT-car has a richer documented schema. Neither can be selected before real PT responses.

## 6. What money is needed next?

€0 for Matricula.co.pt's advertised free tests and provider outreach. No spend was made. A later 100-call Matricula pack would be about €20 and exceeds the current €5 approval cap, so stop before purchase.

## 7. What can be built now?

The provider-independent platform, manual fallback, KType bridge contract, evidence replay, safe states and commercial provider adapters once raw responses arrive.

## 8. What must wait for TecDoc?

Not architecture. Production-scale licensed aftermarket product linkages may use TecDoc or another licensed fitment source. Automatic `COMPATIBLE` claims must wait for one.

## 9. What should we tell Fahad?

Research evidence now leans toward a 3008, not the client-provided 5008, but only a plate/OEM/registration result can settle the pairing. We need Fahad's partslink24/manual ground truth and 10–20 real PT cases before promising accuracy.

## 10. What still needs testing?

The real plate on TelePeças, Matricula.co.pt, Openapi and Tips4y; the VIN on Vincario/other EU providers; partslink24 manual truth; Portugal coverage/rights; and product fitment for the launch categories.
