# Claude Executive Review (for Komail and David)

Date: 2026-10-05. Full detail: `collaboration/CLAUDE_REVIEW.md`.

## CURRENT ANSWER

**Have we established if the APIs are fit for purpose? No.**

The repo currently holds only an empty folder structure, a README, and placeholder notes. There is no code, no test vehicles, no provider response, no benchmark. `CODEX_STATUS.md` confirms nothing was started. If Codex built something elsewhere, it isn't in this folder.

**VIN:** Nothing tested. vPIC, offline decoders, partslink24 and TecAlliance are all NOT TESTED. A free decoder is likely useful only as a first-stage router, but that is a hypothesis.

**Matrícula:** Nothing tested. TelePeças, Matricula.co.pt and the client's existing software are all NOT TESTED. There are no responses, and no documentation of credentials or access.

**Fitment:** Not proven, not attempted. Identifying a car is not the same as knowing a part fits it.

## WHAT CAN WE USE TODAY

- partslink24 (Fahad's existing subscription) as a *manual* tool for building ground truth. This is not the same as being allowed to integrate it into our backend.
- Local VIN structure checks (length, characters, make code).
- Note: the client's own VIN `VF3MCYHZUPS034433` fails the North-American check digit. That is normal for a European VIN, so checksum must never block a VIN.

## WHAT STILL NEEDS ACCESS

- partslink24: written answers on API, export, programmatic and ecommerce rights, and caching.
- TelePeças / Matricula.co.pt: accounts, pricing, terms of use, API access.
- The client's existing plate software: what it is and whether results can be exported.
- TecAlliance / TecDoc: pending.

## WHAT WE SHOULD TEST NEXT

1. Find out where Codex's work is, or whether it was never built.
2. A Stage-1 smoke test: 10–20 real vehicles from Fahad's business, at least one VIN route and one plate route, with raw responses saved.
3. For each result, record how specific it got: make only, model, engine, or exact variant. Record wrong-but-confident results separately.
4. Add deliberately tricky cases: same model with different engines or power, facelifts, manual vs automatic.

## WHAT CAN START BEING BUILT NOW

**Yes: architecture can start, provider still provisional.** Provider-independent parts only:

- Internal vehicle model with a precision level (basic, model, engine, exact variant)
- The three interfaces: identity, catalogue, fitment
- Fitment verdicts and customer states (Compatible / Confirm / Unknown / Not compatible)
- PT plate and VIN input cleaning
- Manual make/model/year/engine selector shell
- Part-number search (labelled as search only)
- Primavera adapter boundary (stock, price, orders)

Do not ship "fits your car" wording yet.

## PROVISIONAL DATA STACK

- Free VIN decode: router and make/model only (to be tested)
- Plate lookup: existing client source, then TelePeças, then Matricula.co.pt (to be tested; rights unknown)
- Fitment: licensed catalogue only, partslink24 if rights allow, TecDoc later
- Manual selector: fed from the catalogue
- Primavera: stock, price, customers, orders. Not vehicle identity.

None of this is validated.

## BIGGEST RISKS

1. **Wrong but confident** brake or suspension parts. This is worse than "no result".
2. A single percentage score hiding that the engine is unknown.
3. Open-source code mistaken for open data. Rights to cache or store provider data are unknown.
4. partslink24 used by our backend without permission.
5. A demo catalogue being read as proof of fitment.

## NEXT 5 ACTIONS

1. Komail: confirm where Codex's work is; set up a local git baseline (no push).
2. Codex: precision levels, hard gates, and fitment verdict rules, with tests that try to break them.
3. Komail and Fahad: get the real vehicle list (10–20, with screenshots including engine code and power) and the partslink24 package and rights answers.
4. Komail: start the data-rights register (code licence vs data licence, commercial use, caching, automated access).
5. Codex: build the fixture file with CLIENT_PROVIDED / INDEPENDENTLY_VERIFIED / SYNTHETIC labels and run the Stage-1 benchmark once providers are accessible.
