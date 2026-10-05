# Public-page claims (NOT verified by testing)
| Candidate | URL | Claims (as read 2026-10-05) |
|---|---|---|
| Matricula.co.pt | https://www.matricula.co.pt | PT plate API, "20 fields" (brand, model, colour, engine size); EUR 0.20/query, min block 100, 10% off >1000; 10 free test searches on registration; SOAP ASMX (XML/JSON); says data real-time from official government sources; 11+ countries. Terms for caching/resale/ecommerce NOT seen. |
| TelePeças | https://www.telepecas.com | Plate or VIN lookup, many EU plate formats; fields year/brand/model/variant-engine/class; lists an /api/ endpoint, no public docs/pricing seen. |
| "Qual veiculo e" app | https://pplware.sapo.pt/?p=1029378 | Free consumer app, shows brand/model/version only; data source undisclosed; article warns data may be wrong/incomplete. No API. |
| IMT certidao de caracteristicas | https://www2.gov.pt/pt/servicos/obter-uma-certidao-de-caracteristicas-tecnicas-do-veiculo | Official paper/online certificate, per vehicle, owner-driven. Not a lookup API. |
| IMT inspection report by plate | https://www2.gov.pt/pt/servicos/obter-relatorio-de-resultados-das-inspecoes-tecnicas-de-veiculo | Inspection history by plate; not a variant source. |
| IMT monthly stats bulletin | https://www.imt-ip.pt/?p=5787 | Aggregate fleet stats only; no per-vehicle open data found on dados.gov.pt. |
| Corgi / universal-vin-decoder / vin-lite | npm / github | Offline decoders built on vPIC or ~1-1.5k WMI codes: same data ceiling as vPIC for EU. Full SAE WMI DB is paid. |
| Zylalabs European VIN Decoder, Apify VINdata | zylalabs.com, apify.com | Commercial/aggregator EU VIN decoders; not evaluated, pricing and variant depth unknown. |
