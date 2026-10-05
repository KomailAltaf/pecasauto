# Portuguese official vehicle-data route

Checked 2026-10-05. Scope: lawful, production-suitable lookup for Portuguese vehicles. Absence of a public API in this review is not proof that a private B2B agreement cannot exist.

| Agency / route | Service found | Public vehicle-identity API? | B2B access? | Pricing | Known restrictions | Contact / next action |
|---|---|---:|---|---|---|---|
| IMT | Homologation, vehicle documents, inspections and administrative services | **No public ecommerce lookup API identified** | TO VERIFY | Unknown | Public services appear document/owner/administrative oriented | Ask IMT whether licensed bulk or B2B plate→technical-vehicle access exists and who may qualify |
| IRN / Justiça | Automotive registration and permanent registration certificate | **No** public catalogue/fitment API identified | TO VERIFY | Per-certificate/manual services exist | Legal/ownership registration information is not a low-latency ecommerce identity feed | Ask whether accredited companies can obtain machine-readable technical fields; do not treat legal registration certificate as catalogue data |
| Autoridade Tributária | SFA2/EFAPI for vehicle-tax and registration processes | Not an ecommerce read API | Restricted economic/operator workflows exist | Unknown | The documented web service supports fiscal/registration submissions, not arbitrary plate lookup | Ask whether any read-only vehicle-technical service is available to automotive distributors; expect access restrictions |
| dados.gov.pt / INE | Aggregate fleet and vehicle-registration statistics | No per-vehicle dataset found | Open-data API is catalogue-level | Free | Aggregate data cannot identify a vehicle | No production identity role; retain for market analysis only |
| Licensed intermediary | Matricula.co.pt / Openapi PT-car / TelePeças / Tips4y | Yes, documented commercial APIs | Yes, provider-specific | Public or quote | Rights, caching and field depth vary | Benchmark with real PT vehicles and obtain written terms |

## Finding

**PARTIALLY VERIFIED:** no obvious free public IMT/IRN/AT endpoint was found that accepts a Portuguese plate and returns fitment-grade technical identity for ecommerce. Official services found are administrative, fiscal, certificate, or aggregate-data services. A direct B2B route remains **TO VERIFY** by contact.

Sources reviewed: official IMT/IRN/AT/dados.gov.pt pages. No restricted system was accessed.

