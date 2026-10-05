# Client vehicle ground-truth research

Case: Portuguese matrícula `CG-17-GC`; VIN `VF3MCYHZUPS034433`.

The plate/VIN pairing and vehicle description were provided by the client. No independent official or licensed catalogue output has yet been supplied.

| Field | Value | Classification | Evidence |
|---|---|---|---|
| Portuguese market context | PT registration `CG-17-GC` | CONFIRMED | Plate format + client case |
| VIN | `VF3MCYHZUPS034433` | CLIENT_PROVIDED | Client case |
| Manufacturer | Peugeot / Automobiles Peugeot | CONFIRMED | Client + live public vPIC + self-hosted vPIC |
| Model | likely 3008 SUV; client supplied 5008 II | LIKELY / DISPUTED | Autofrance returned 3008/KType 130708. Independent public catalogue references cross-check 130708 as 3008 and 130738 as the comparable 5008. The VIN→KType assignment is still not confirmed by an OEM/registration source. |
| Generation | MC/MR/MJ/M4 family codes | LIKELY / INCOMPLETE | Returned platform codes are consistent with the 3008 KType identity, but shared PSA platform notation does not independently prove the exact model. |
| Year | unknown exact year; production range 2018+ | UNKNOWN / INCOMPLETE | vPIC raw says 2023 from a VIN-position inference that is not promoted. Autofrance gives a production range, not this vehicle's registration/model year. |
| Engine family | 1.5 BlueHDi 130 | LIKELY | Client and live Autofrance agree on engine family/output label |
| Power | 130 hp client / 131 hp and 96 kW provider | LIKELY | Difference is consistent with rounding conventions, but independent source is still needed |
| Fuel | Diesel | LIKELY | Client and live Autofrance agree; vPIC returned no fuel |
| Engine code | YHZ / DV5RC | LIKELY | Public KType catalogue cross-checks associate this code with 130708 and the returned engine; OEM/partslink24 confirmation is still required. |
| Exact variant | — | UNKNOWN | Needs licensed vehicle identity/catalogue output |
| Catalogue vehicle ID / KType | 130708 | IDENTITY CROSS-CHECKED; VIN MAPPING PARTIAL | Independent public catalogue references identify KType 130708 as 3008 1.5 BlueHDi 130. The research endpoint's assignment of this VIN to that KType remains unlicensed and only partially verified. |

## What would upgrade this to independent ground truth

One permitted partslink24 VIN result or manufacturer/OEM output, plus the vehicle registration document or a second licensed PT identity provider response. Fields must be recorded individually; agreement on make does not validate engine or variant.
