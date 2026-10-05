from __future__ import annotations

import csv
import html
import json
from pathlib import Path

from benchmarks.core import cost_scenarios, is_production_score_eligible, load_campaign_inputs, load_ground_truth, provider_summaries


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"


def format_value(value):
    return "—" if value is None else value


def generate() -> dict[str, object]:
    REPORTS.mkdir(exist_ok=True)
    fixture_path = ROOT / "fixtures" / "vehicle_ground_truth.csv"
    eligible_truth = load_ground_truth(fixture_path)
    campaign_inputs = load_campaign_inputs(fixture_path)
    all_truth = load_ground_truth(fixture_path, include_synthetic=True)
    providers = provider_summaries()

    csv_path = REPORTS / "provider_comparison.csv"
    fields = list(providers[0].__dataclass_fields__)
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows([item.__dict__ for item in providers])

    cost_path = REPORTS / "cost_analysis.json"
    cost_path.write_text(json.dumps(cost_scenarios(), indent=2), encoding="utf-8")

    rows = "".join(
        "<tr>" + "".join(f"<td>{html.escape(str(format_value(getattr(item, field))))}</td>" for field in fields) + "</tr>"
        for item in providers
    )
    html_path = REPORTS / "provider_comparison.html"
    html_path.write_text(f"""<!doctype html><html><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\"><title>Provider Comparison</title><style>
body{{margin:0;background:#f2f0ea;color:#17201c;font:15px/1.5 system-ui,sans-serif}}header{{padding:48px 5vw;background:#132f27;color:white}}main{{padding:36px 5vw}}h1{{font-size:42px;margin:8px 0}}.legend{{display:flex;gap:8px;flex-wrap:wrap;margin:20px 0}}.badge{{padding:7px 9px;border:1px solid #88958e;font-size:11px;font-weight:800}}.warning{{padding:18px;border-left:5px solid #a53c36;background:#f5e2df;margin:20px 0}}.table{{overflow:auto;background:white;border:1px solid #d5d9d4}}table{{border-collapse:collapse;min-width:1500px;width:100%}}th,td{{padding:11px;border-bottom:1px solid #d5d9d4;text-align:left;vertical-align:top}}th{{background:#e5e9e6;font-size:11px;text-transform:uppercase}}section{{margin:32px 0}}code{{background:#e7ebe8;padding:2px 5px}}</style></head><body><header><small>PORTUGAL-ONLY · INTERNAL VALIDATION</small><h1>Automotive Provider Comparison</h1><p>Generated from executable benchmark/report code and stored raw evidence.</p></header><main><div class=\"warning\"><b>No provider is production-verified.</b> vPIC returned make only. A research-only endpoint returned an engine and KType, but is excluded from production and conflicts with the client label. Commercial providers remain untested or access-blocked.</div><div class=\"legend\"><span class=\"badge\">VERIFIED</span><span class=\"badge\">PARTIALLY VERIFIED</span><span class=\"badge\">NOT VERIFIED</span><span class=\"badge\">WAITING FOR CREDENTIALS</span><span class=\"badge\">MOCK ONLY</span></div><section><h2>Evidence inventory</h2><p>Production-score rows: <b>{len(eligible_truth)}</b>. Portuguese campaign inputs: <b>{len(campaign_inputs)}</b>. Total fixture rows including debug-only foreign/synthetic: {len(all_truth)}.</p></section><section><h2>Provider status</h2><div class=\"table\"><table><thead><tr>{''.join(f'<th>{html.escape(field.replace("_"," "))}</th>' for field in fields)}</tr></thead><tbody>{rows}</tbody></table></div></section><section><h2>Cost analysis</h2><p>Scenarios for 1k, 10k, 50k and 100k monthly calls were generated. Cost per correct engine remains undefined because no provider returned an independently verified PT engine-level result.</p></section></main></body></html>""", encoding="utf-8")

    executive = REPORTS / "executive_findings.md"
    production_eligible = [row for row in eligible_truth if is_production_score_eligible(row)]
    executive.write_text(f"""# Executive Findings — Portugal-only evidence round

Generated: 2026-10-05

## Scope

The provider-independent safety foundation is implemented and tested. Public and self-hosted vPIC plus a research-only European storefront endpoint were called with the Portuguese client VIN. Commercial plate/VIN, TecDoc, partslink24, supplier and Primavera APIs were not available. No provider is production-verified.

## VERIFIED

- The repository now contains executable models, provider boundaries, orchestration, fixtures, tests, benchmark tooling and generated reports.
- The local git baseline exists.
- Synthetic fixtures are excluded from accuracy metrics by code and test.
- The client VIN `VF3MCYHZUPS034433` passes structural EU validation even though its North-American checksum signal is false.
- Test catalogue records are labelled `MOCK ONLY` and `SEARCH MECHANICS ONLY`.

## PARTIALLY VERIFIED

- Precision levels and fitment hard gates behave as specified in unit tests.
- Portuguese plate normalization covers the four specified historical/current patterns.
- Provider swapping, error isolation, circuit threshold and provider-scoped cache work in local tests.
- The local VIN parser validates structure only. It does not identify make/model/engine/variant.
- Public vPIC returned Peugeot only for the client VIN; self-hosted vPIC reproduced the same BASIC-only result.
- The research-only Autofrance endpoint returned ENGINE-level data and KType 130708. Public catalogue references cross-check the KType identity as a 3008; the VIN→KType assignment remains partial and conflicts with the client-provided 5008.
- Autofrance is excluded from the production cascade because commercial rights are unknown and the endpoint does not verify VIN existence.

## NOT VERIFIED

- Portuguese-market accuracy of any free, commercial or client vehicle-identification provider.
- Manual vehicle taxonomy backed by real fitment data.
- OEM search against a licensed production catalogue.
- Vehicle-product fitment for any real product.
- Primavera integration depth and supplier-feed quality.

## WAITING FOR CREDENTIALS

- TelePeças API.
- Matricula.co.pt API/terms.
- TecAlliance/TecDoc services and licence.
- partslink24 programmatic/API/export rights (manual client access is confirmed).
- Existing client vehicle software identification and export/API details.
- Primavera/Cegid version, modules and API credentials.

## MOCK ONLY

- `MockIdentityProvider` output.
- `fixtures/test_catalogue.json`.
- Stored mock raw identity response.
- Generated mock plumbing counts. These are excluded from provider accuracy.

## Benchmark state

- Eligible non-synthetic fixture rows: {len(eligible_truth)}.
- Portuguese campaign inputs (including client-provided): {len(campaign_inputs)}.
- Independently verified Portuguese fixture rows: {len(production_eligible)}.
- Stage-1 requirement: 10-20 real, independently verifiable vehicles plus at least one VIN and one plate provider.
- Current benchmark therefore validates mechanics only, not provider fitness.

## Cost state

Cost scenarios exist for 1k/10k/50k/100k lookups and both cache policies. Known free request costs are recorded; commercial costs remain unknown or vendor-advertised. Cost-per-correct-engine and cost-per-exact-variant cannot be calculated until verified PT ground truth and benchmark evidence exist.

## Next evidence gate

Obtain written rights/credentials and a 10-20 vehicle ground-truth set. Rerun the same commands without changing the customer-facing architecture.
""", encoding="utf-8")

    result = {
        "eligible_truth_rows": len(eligible_truth),
        "independently_verified_rows": len(production_eligible),
        "provider_rows": len(providers),
        "status": "NOT VERIFIED",
    }
    (REPORTS / "benchmark_summary.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    print(json.dumps(generate(), indent=2))
