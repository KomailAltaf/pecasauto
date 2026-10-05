# Autofrance K-Type 130708 investigation

Timestamps 2026-10-05. Tags: VERIFIED (I reproduced), DOCUMENTED, LIKELY, UNRESOLVED.

## 1. The result (VERIFIED, reproduced independently)
`GET https://api.autofrance.se/api/regnum/vin?vin=VF3MCYHZUPS034433` → HTTP 200, 1.96 s, byte-identical payload to Codex's: `ktype 130708`, `PEUGEOT`, model string **"3008 SUV (MC_, MR_, MJ_, M4_)"**, cartype "1.5 BlueHDi 130", from 2018, 131 hp / 96 kW, 1499 cc, Diesel, SUV. Raw: `reports/claude_raw_evidence/autofrance/vin_VF3MCYHZUPS034433.json` (+ ts file). Catalogue page `autofrance.se/fordon/130708` (Codex raw HTML) adds **engine code "YHZ (DV5RC)"**, chassis "MC_, MR_, MJ_, M4_", 1,867 matching parts.

## 2. What Autofrance is (DOCUMENTED)
A **Swedish retailer** (Autofrance, Helsingborg warehouse, since 1988; `autofrance.se`, Swedish UI). `api.autofrance.se/api/regnum/vin` is the backend of its own storefront, **not a published data product**. Its purchase terms (köpvillkor) protect site content by copyright and forbid copying without written permission; they say nothing about API/automation. **Not a lawful basis for production use.** Treat as a *reference oracle for research* only. Do not build the product on it. Throttle any further use; do not bulk query.

## 3. Is it TecDoc-derived? (LIKELY, not proven)
Yes in form: the `ktype` integer, the model string with chassis codes in brackets ("3008 SUV (MC_, MR_, MJ_, M4_)"), `cartype`, `ccm`, `kw/hp` are TecDoc vehicle-table conventions. The retailer almost certainly holds a TecDoc/partner licence and a VIN→K-Type decoder. I cannot name the upstream.

## 4. The 3008 vs 5008 conflict: findings
**a) The VIN does not discriminate 3008 from 5008 in positions 4–8.**
- `VF3` Peugeot; `MC` = body/platform code shared by both; **`YHZ` = engine code (DV5RC 1.5 BlueHDi 130)**: the VIN itself encodes the engine, and Autofrance's page names the same code. Strong, independent structural support for ENGINE level.
- Public VIN-report listings (search snippets; those sites block automated fetches with 403, so I did not retrieve them) show VINs with the **identical prefix `VF3MCYHZ…` labelled both "Peugeot 3008" (e.g. …UPS049790, …UPS032824) and "Peugeot 5008" (e.g. …UNS111323)**. Aggregators disagree with each other: they are low-quality evidence, but they show the prefix is not a safe 3008/5008 key.
- Parts catalogues label the **5008 II with the same chassis-code set**: "PEUGEOT 5008 II (MC_, MJ_, MR_, M4_)" (Schaeffler listings), and Autofrance labels the 3008 with "(MC_, MR_, MJ_, M4_)". Chassis codes are shared across both models, so chassis text cannot settle it.
- Same plant (Sochaux, position 11 `S`), same EMP2 platform. A 5008 II is longer (extra row/wheelbase), so rear-body and some chassis parts differ; engine-bay parts largely match.

**b) So the conflict is most plausibly platform-sharing ambiguity resolved arbitrarily by the decoder, not proof that the car is a 3008.** Equally unproven: the client's "5008" (we have only a "roughly" description of the screenshot). Possible causes ranked: (1) decoder picked one of two valid candidates [most plausible]; (2) decoder error; (3) client/screenshot mistake; (4) K-Type table alias. **Status: UNRESOLVED.**

**c) Engine/power match.** Autofrance 96 kW / 131 hp vs client 130 hp, and public spec sites list the 5008 II 1.5 BlueHDi 130 at 96 kW, DV5RC: consistent. Production: Autofrance "2018→"; 5008 II launched 2017, 3008 II 2016/2017; both span the 2023 car. Engine-level result: **LIKELY correct (VIN structure + provider + public specs agree).** Model-level: **CONFLICT.**

## 5. Is VIN→K-Type reliable? 
Not demonstrated. n=1, one provider, one claimed vehicle that conflicts with the client. The decoder returned a single confident answer for an ambiguous platform code: **this is exactly the WRONG-BUT-CONFIDENT risk.** Rule: a provider K-Type may never reach COMPATIBLE on its own; it must be cross-checked in a licensed catalogue or by partslink24, and a model-name disagreement with the user's own input must force CONFIRM.

## 6. Independent confirmation of K-Type 130708 (NOT achieved)
Searches for "KTYPE 130708" found no independent catalogue page. Autofrance's own catalogue page agrees with its own API (same source, not independent). Needed: TecDoc catalogue/partner, a second retailer's `ktype=130708` page, or Fahad's partslink24 VIN result. Also needed: the K-Type(s) TecDoc assigns to **5008 II 1.5 BlueHDi 130** for comparison (not found publicly).

## 7. What resolves it (ordered)
1. **Fahad runs the VIN in partslink24 (Peugeot catalogue)**: the OEM answer is definitive for 3008 vs 5008; screenshot model, engine code, build date.
2. **Portuguese registration certificate** (D.2 type/variant/version + commercial name) or the Portuguese plate API: `CG-17-GC` should return model.
3. The original client screenshot (what exactly does it say: 5008 or 3008?).
4. Any plate/VIN provider that returns *model* from the plate (Openapi/Matricula.co.pt/TelePeças/Autoways): an independent plate-based model, since the VIN doesn't discriminate.
5. A TecDoc-licensed VIN decode returning candidate list.

## 8. Product rule derived
If provider model ≠ user-stated model, or multiple candidates share a VDS: show both candidates and ask "Peugeot 3008 or 5008?" (one tap), with images. Never auto-select.

---

# ROUND 6 UPDATE (2026-10-05, later): supersedes §4b, §6, §7 where they conflict

## A. K-Type 130708 IS independently confirmed as an identity (VERIFIED by 2 independent public TecDoc-style sources)
- **Autodoc** (UK/DE storefront URLs, via search results; the pages themselves return HTTP 403 to automated fetch, so I did not retrieve them): `…/peugeot/3008/3008-suv/130708-1-5-bluehdi-130`, titled "Peugeot 3008 SUV 1.5 BlueHDi 131 PS Diesel 96 kW 2018–2025 **YHZ (DV5RC)**".
- **Schaeffler catalogue listing (rolling.hu)**: "PEUGEOT 3008 SUV (MC_, MR_, MJ_, M4_) 1.5 BlueHDi 130".
- Both match Autofrance's K-Type → vehicle mapping exactly. So **130708 = Peugeot 3008 SUV 1.5 BlueHDi 130, 96 kW, YHZ/DV5RC, from 02.2018**. 
- **130738 = Peugeot 5008 II 1.5 BlueHDi 130** (Autodoc `…/5008/5008-ii/130738-1-5-bluehdi-130-mcyhzj-mcyhzr-mcyhzx`; Schaeffler "5008 II … 1.5 BlueHDi 130 (MCYHZJ, MCYHZR, MCYHZX)"; same K-Type Autofrance returns for `VF3MCYHZJJL092080`).

## B. What decides 3008 vs 5008 (new, tested)
1. **Catalogue VDS lists.** TecDoc-derived listings tie the 5008 II 1.5 BlueHDi 130 to VIN descriptors **MCYHZ + J / R / X**. Our VIN's descriptor is **MCYHZ + U**: **not in the 5008 list.** (The 3008 listing shows no suffix list, so this is evidence of exclusion from the 5008, not an explicit inclusion in the 3008.)
2. **Autofrance decoder behaviour (my probes, raw in `reports/claude_raw_evidence/autofrance/`):** 5 real-looking `VF3MCYHZ?PS/NS` VINs → 130708 (3008). `VF3MCYHZJJL092080` → 130738 (5008). **Synthetic debug VINs (not accuracy data):** changing position 9 (J/R/X/U) never changed the result; changing **position 11** did: `S` → 130708 (3008), `L` → 130738 (5008). So its rule is plant-letter based, applied to any serial, including the fake `000001` ones: **it does not check that a VIN exists** and always answers confidently.
3. Two *different* discriminators (catalogue: position 9 ∉ {J,R,X}; Autofrance: plant S) **both point to 3008 for our VIN.** Aggregator sites that label some `…NS…` VINs as 5008 are inconsistent and lower quality.
4. My earlier suggestion that plant letter "can't discriminate" was untested; tested now: it is Autofrance's rule, but its real-world validity is unproven (plant letters S/L are not documented as model-specific, and secondary sources disagree about which plant builds the 5008 II).

## C. Revised conclusion
- **LIKELY: VIN `VF3MCYHZUPS034433` is a Peugeot 3008 (II) 1.5 BlueHDi 130 (K-Type 130708), not a 5008.** Evidence: engine from the VIN itself (YHZ) + two independent catalogue identities + two different discriminators. Confidence: moderate, not confirmed: no OEM or registration-document output.
- **Client's "5008" expectation is therefore the likely outlier**, or the plate and VIN in the screenshot belong to different cars (or the VIN was mistyped). **Next decisive test:** what does `CG-17-GC` resolve to? If a plate provider returns "5008", the pair is inconsistent: STOP and verify the screenshot.
- Status: **K-Type 130708 cross-checked (identity); VIN→K-Type mapping for this VIN PARTIALLY VERIFIED; client conflict LIKELY RESOLVED IN FAVOUR OF 3008 but pending partslink24 / plate / certificate.**
- **Product consequence:** the existing rule stands (provider model ≠ user model ⇒ CONFIRM). Plus: a decoder that never rejects non-existent VINs cannot be trusted as sole source.

## D. Autofrance (storefront) legality: unchanged
Research oracle only. My total calls this session: ~16 requests at ≥2 s spacing; no bulk queries.
