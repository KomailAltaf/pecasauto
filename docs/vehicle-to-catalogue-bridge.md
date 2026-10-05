# Vehicle → catalogue bridge

## Current client-case evidence

KType `130708` has been cross-checked in independent public catalogue references as the identity for a Peugeot 3008 SUV 1.5 BlueHDi 130. The separate claim that VIN `VF3MCYHZUPS034433` maps to `130708` is only **PARTIALLY VERIFIED**: it comes from a research-only storefront endpoint that does not validate VIN existence and conflicts with the client's 5008 label. KType identity and VIN→KType mapping are different claims and remain separately tracked.

## Why this is the critical boundary

Plate/VIN services answer **what vehicle is this?** Catalogue services answer **which part links to which catalogue vehicle?** A textual result such as `Peugeot 5008 II / 1.5 BlueHDi 130` is not itself a fitment key.

```text
PT matrícula / VIN
        ↓
provider result + provider vehicle ID
        ↓
canonical PT vehicle candidate
        ↓
bridge candidates (never silently pick)
        ↓
TecDoc KType / NType OR OEM catalogue vehicle ID
        ↓
licensed product linkage + restrictions
        ↓
MATCH / NO_MATCH / REVIEW
```

## Candidate bridge identifiers

| Identifier | Potential role | Evidence / limitation | Status |
|---|---|---|---|
| TecDoc KType / NType | Direct aftermarket catalogue key | TecAlliance documents harmonised vehicle IDs. TelePeças docs expose optional `ktype` and `tecDocModelId`. | DOCUMENTED CAPABILITY; access required |
| Autofrance KType | Research VIN→KType bridge | Actual client VIN returned KType `130708`; public catalogues cross-check the KType identity, but the VIN mapping conflicts with the client label, the endpoint has no existence check, and production rights are unknown. | PARTIALLY VERIFIED; research only |
| TelePeças vehicle/model ID | Provider-local bridge | Official API docs expose `telepecasModelId`, `ktype`, `tecDocModelId`, years and fuel fields. Whether the decoding endpoint returns them for PT plates must be tested. | DOCUMENTED CAPABILITY; credentials required |
| ABI code | Plate-data classification key | Matricula/Openapi schemas document ABI code. No mapping from ABI to KType has been proven. | UNVERIFIED bridge |
| Engine code + power + production date | Candidate narrowing | Useful discriminator but not always unique; chassis/PR-code restrictions can remain. | PARTIALLY VERIFIED concept; not sufficient alone |
| VIN | OEM catalogue entry | partslink24 documents VIN-based genuine-parts identification, but integration rights are unknown. | MANUAL capability documented |
| partslink24 vehicle context | OEM validation | Can establish genuine OE references manually. No programmatic identifier/export is confirmed. | WAITING FOR HUMAN OUTPUT / RIGHTS |
| Type approval / national type | Possible identity bridge | Availability in commercial PT plate responses not proven. | TO TEST |
| Text matching | Last-resort candidate generation | Must return candidates and ambiguity; never automatic exact mapping. | Safe only with confirmation |

## Safe matching rule

1. Accept a direct licensed provider vehicle ID mapping when returned by the same provider/catalogue contract.
2. Otherwise create candidate catalogue IDs using make/model/generation/year/engine/fuel/power.
3. If one exact candidate remains, still preserve provenance and catalogue restrictions.
4. If multiple candidates remain, ask for one discriminator or route to support.
5. Only a licensed fitment linkage can produce `COMPATIBLE`; identity alone cannot.

## Best pre-TecDoc bridge candidates

- **TelePeças → KType/TecDoc model ID:** strongest documented local candidate, but actual decoder response and rights are untested.
- **Autofrance research VIN → KType:** strongest actual no-account evidence result so far; useful only as a prototype/benchmark oracle and excluded from production until conflict, existence validation, coverage and rights are resolved.
- **Tips4y matrícula → VIN/KType → TecDoc:** explicit documented bridge, contract and exact data depth unknown.
- **partslink24 manual VIN → OE catalogue:** workable human validation route, not a proven backend integration.
- **Plate provider → canonical fields → manual engine confirmation → manually curated initial-category mapping:** buildable now for a narrow launch, but requires human-reviewed catalogue mappings and must show `CONFIRMAR COMPATIBILIDADE` where restrictions remain.
