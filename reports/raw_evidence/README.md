# Raw evidence

Payloads in this directory are stored exactly as returned by the tested endpoint.
They are not normalized or edited. Test scope is the Portuguese client case only:
`CG-17-GC` / `VF3MCYHZUPS034433`.

Observed on 2026-10-05:

- `vpic_public_VF3MCYHZUPS034433.json`: HTTP 200, 874 ms, €0.
- `vpic_public_detailed_VF3MCYHZUPS034433.json`: HTTP 200, 346 ms, €0.
- `vpic_self_hosted_VF3MCYHZUPS034433.json`: HTTP 200, 163 ms, €0 marginal API cost. It uses the same NHTSA dataset and therefore is not an independent source.
- `autofrance_VF3MCYHZUPS034433.json`: HTTP 200, 3,916 ms, €0. Research-only storefront endpoint; returns Peugeot 3008 SUV, 1.5 BlueHDi 130, 96 kW and KType 130708; conflicts with client-provided model 5008 and does not prove VIN existence.
- `autofrance_ktype_130708_catalogue.html`: HTTP 200 public catalogue page for KType 130708; page states TecDoc-linked compatible parts. Production reuse rights remain unknown.
- `autofrance_products_ktype_130708.json`: exploratory product-search response. The query did not visibly prove KType filtering, so it is not used as fitment evidence.
- `matriculapt_CG-17-GC_access_response.xml`: HTTP 500, 338 ms; exact response was `Your username is incorrect`. No vehicle data returned.
- `telepecas_auth_access_response.json`: HTTP 400, 80 ms; exact OAuth response confirms client credentials are required.
- `telepecas_api_unauthenticated_response.txt`: HTTP 404 against a marketing-page example route; not a vehicle test and not used for provider accuracy.

No paid request was made. Total campaign spend: **€0**.
