from __future__ import annotations

import csv
import html
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "reports"
RAW = REPORTS / "raw_evidence"

FIELDS = [
    "test_case", "input_type", "input_value", "provider", "tested_or_documented", "success",
    "make", "model", "generation", "year", "engine", "engine_code", "fuel", "power_kw",
    "variant", "precision_level", "ambiguous", "wrong", "latency_ms", "cost",
    "commercial_use_status", "cache_allowed", "storage_allowed", "fitment_available", "notes",
    "raw_evidence", "decision", "can_support_auto_fitment", "blocker", "country",
    "portuguese_market_verified",
]


def empty(provider: str, input_type: str, input_value: str, **extra: object) -> dict[str, object]:
    row: dict[str, object] = {field: "" for field in FIELDS}
    row.update({
        "test_case": "client_001",
        "input_type": input_type,
        "input_value": input_value,
        "provider": provider,
        "success": "false",
        "ambiguous": "false",
        "wrong": "false",
        "commercial_use_status": "UNKNOWN",
        "cache_allowed": "UNKNOWN",
        "storage_allowed": "UNKNOWN",
        "fitment_available": "false",
        "decision": "NOT_TESTED",
        "can_support_auto_fitment": "NO",
        "country": "PT",
        "portuguese_market_verified": "false",
    })
    row.update(extra)
    return row


def vpic_row(provider: str, evidence_file: str, latency_ms: float) -> dict[str, object]:
    payload = json.loads((RAW / evidence_file).read_text(encoding="utf-8"))
    result = payload["Results"][0]
    return empty(
        provider,
        "VIN",
        "VF3MCYHZUPS034433",
        tested_or_documented="ACTUAL_TEST",
        success="true",
        make=result.get("Make", ""),
        model=result.get("Model", ""),
        year=result.get("ModelYear", ""),
        engine=result.get("EngineModel", ""),
        fuel=result.get("FuelTypePrimary", ""),
        power_kw=result.get("EngineKW", ""),
        variant=result.get("Trim") or result.get("Series") or "",
        precision_level="BASIC_ONLY",
        latency_ms=round(latency_ms, 1),
        cost="€0",
        commercial_use_status="PUBLIC API; NHTSA states free public use",
        cache_allowed="DOCUMENTED PUBLIC DATA; local policy review still required",
        storage_allowed="DOCUMENTED PUBLIC DATA; local policy review still required",
        notes=f"ErrorCode {result.get('ErrorCode')}. Model, engine, fuel, power and variant absent. EU model year is not independently trusted.",
        raw_evidence=f"reports/raw_evidence/{evidence_file}",
        decision="BASIC_ONLY",
        can_support_auto_fitment="NO",
    )


def rows() -> list[dict[str, object]]:
    result = [
        empty(
            "Autofrance public VIN", "VIN", "VF3MCYHZUPS034433",
            tested_or_documented="ACTUAL_TEST", success="true", make="PEUGEOT",
            model="3008 SUV (MC_, MR_, MJ_, M4_)", year="2018+ production range",
            engine="1.5 BlueHDi 130", fuel="Diesel", power_kw="96",
            variant="KType 130708", precision_level="ENGINE_LEVEL", ambiguous="true",
            latency_ms=3916.2, cost="€0", commercial_use_status="RESEARCH ONLY; PRODUCTION/REUSE RIGHTS UNKNOWN",
            cache_allowed="UNKNOWN", storage_allowed="UNKNOWN", fitment_available="PUBLIC CATALOGUE PAGE CLAIMS TECDOC-LINKED PARTS",
            notes="Research-only endpoint with no existence check. KType 130708 identity was cross-checked as 3008; VIN→KType remains partial and conflicts with the client-provided 5008.",
            raw_evidence="reports/raw_evidence/autofrance_VF3MCYHZUPS034433.json; reports/raw_evidence/autofrance_ktype_130708_catalogue.html",
            decision="ENGINE_LEVEL", can_support_auto_fitment="NEEDS_SECOND_SOURCE",
            blocker="No existence check; client-model conflict; production rights and 83-brand/Portugal coverage unverified",
        ),
        vpic_row("NHTSA vPIC public", "vpic_public_VF3MCYHZUPS034433.json", 874.3),
        vpic_row("Self-hosted vPIC", "vpic_self_hosted_VF3MCYHZUPS034433.json", 162.8),
        empty(
            "Local VIN structural parser", "VIN", "VF3MCYHZUPS034433",
            tested_or_documented="ACTUAL_TEST", success="true", precision_level="NONE",
            cost="€0", commercial_use_status="INTERNAL CODE", cache_allowed="true",
            storage_allowed="true", notes="Validates length/charset and treats EU checksum as non-blocking; provides no vehicle identity.",
            raw_evidence="app/normalization.py; tests/test_normalization.py",
            decision="NOT_FIT_FOR_PURPOSE", blocker="No vehicle data by design",
        ),
        empty(
            "Matricula.co.pt", "MATRICULA", "CG-17-GC",
            tested_or_documented="ACCESS_TEST + DOCUMENTED_CAPABILITY", latency_ms=337.7,
            cost="€0 (access test); advertised €0.20/request after 10 free tests",
            commercial_use_status="REQUIRES LICENCE CONFIRMATION", fitment_available="false",
            notes="Official endpoint returned 'Your username is incorrect'. Public documentation advertises make/model/engine-size plus other fields; response depth is unverified.",
            raw_evidence="reports/raw_evidence/matriculapt_CG-17-GC_access_response.xml",
            decision="NOT_TESTED", blocker="Free test account credentials required",
        ),
        empty(
            "TelePeças", "MATRICULA / VIN", "CG-17-GC / VF3MCYHZUPS034433",
            tested_or_documented="ACCESS_TEST + DOCUMENTED_CAPABILITY", latency_ms=80.3,
            cost="€0 access test; production price unknown", commercial_use_status="REQUIRES CONTRACT",
            notes="OAuth endpoint returned invalid_client. Official pages document PT plate/VIN decoding, technical data, OEM compatibility and KType-capable catalogue fields.",
            raw_evidence="reports/raw_evidence/telepecas_auth_access_response.json",
            decision="NOT_TESTED", can_support_auto_fitment="NEEDS_SECOND_SOURCE",
            blocker="Seller/integrator account and API credentials required",
        ),
        empty(
            "Openapi PT-car", "MATRICULA", "CG-17-GC",
            tested_or_documented="DOCUMENTED_ONLY", cost="Advertised €0.40 PAYG; €0.18-€0.37 volume",
            commercial_use_status="DOCUMENTED B2B API; TERMS TO VERIFY", notes="Official page documents make, model, version, fuel, displacement, horsepower, VIN and ABI code for Portuguese plates.",
            decision="NOT_TESTED", can_support_auto_fitment="NEEDS_SECOND_SOURCE", blocker="Account/token and paid wallet or trial access required",
        ),
        empty(
            "Tips4y matrícula", "MATRICULA", "CG-17-GC", tested_or_documented="DOCUMENTED_ONLY",
            cost="Quote required", commercial_use_status="DOCUMENTED B2B API; CONTRACT REQUIRED",
            fitment_available="DOCUMENTED VIA TECDOC", notes="Provider advertises PT plate lookup connected to VIN and TecDoc KType. No live response or commercial terms obtained.",
            decision="NOT_TESTED", can_support_auto_fitment="NEEDS_SECOND_SOURCE", blocker="Commercial contact and credentials required",
        ),
        empty(
            "TecAlliance Vehicle Identification", "MATRICULA / VIN", "CG-17-GC / VF3MCYHZUPS034433",
            tested_or_documented="DOCUMENTED_ONLY", cost="Quote required", commercial_use_status="LICENSE REQUIRED",
            fitment_available="DOCUMENTED WITH TECDOC SERVICES", notes="Official product documentation states VIN/VRM to harmonised TecDoc KType/NType data.",
            decision="NOT_TESTED", can_support_auto_fitment="NEEDS_SECOND_SOURCE", blocker="Contract, Portugal coverage confirmation and credentials required",
        ),
        empty(
            "partslink24 manual", "VIN", "VF3MCYHZUPS034433", tested_or_documented="CLIENT ACCESS CONFIRMED; TEST NOT PROVIDED",
            cost="Existing client subscription; integration cost unknown", commercial_use_status="MANUAL USE CONFIRMED; PROGRAMMATIC RIGHTS UNKNOWN",
            fitment_available="OEM CATALOGUE MANUAL", notes="Useful for human OE/VIN validation. No output for this VIN is stored yet.",
            decision="NOT_TESTED", can_support_auto_fitment="NO", blocker="Fahad must provide permitted manual output; API/export rights need written confirmation",
        ),
    ]
    return result


def render_comparison(data: list[dict[str, object]]) -> None:
    providers = ["Client expectation", "vPIC", "self-hosted VIN", "TelePeças", "Matricula.co.pt", "TecAlliance", "partslink/manual reference", "other tested providers"]
    values = {
        "Client expectation": {"Make":"Peugeot", "Model":"5008", "Generation":"II", "Year":"2023 (client context)", "Engine":"1.5 BlueHDi", "Engine code":"UNKNOWN", "Fuel":"Diesel", "Power":"130 hp", "Variant":"UNKNOWN", "Vehicle ID":"UNKNOWN", "Result precision":"CLIENT_PROVIDED", "Cost":"—"},
        "vPIC": {"Make":"PEUGEOT · PASS", "Model":"— · FAIL", "Generation":"— · FAIL", "Year":"2023 · PARTIAL", "Engine":"— · FAIL", "Engine code":"— · FAIL", "Fuel":"— · FAIL", "Power":"— · FAIL", "Variant":"— · FAIL", "Vehicle ID":"— · FAIL", "Result precision":"BASIC_ONLY", "Cost":"€0"},
        "self-hosted VIN": {"Make":"PEUGEOT · PASS", "Model":"— · FAIL", "Generation":"— · FAIL", "Year":"2023 · PARTIAL", "Engine":"— · FAIL", "Engine code":"— · FAIL", "Fuel":"— · FAIL", "Power":"— · FAIL", "Variant":"— · FAIL", "Vehicle ID":"— · FAIL", "Result precision":"BASIC_ONLY", "Cost":"€0 API"},
        "TelePeças": {key:"WAITING FOR ACCESS" for key in ["Make","Model","Generation","Year","Engine","Engine code","Fuel","Power","Variant","Vehicle ID","Result precision","Cost"]},
        "Matricula.co.pt": {key:"WAITING FOR ACCESS" for key in ["Make","Model","Generation","Year","Engine","Engine code","Fuel","Power","Variant","Vehicle ID","Result precision","Cost"]},
        "TecAlliance": {key:"WAITING FOR ACCESS" for key in ["Make","Model","Generation","Year","Engine","Engine code","Fuel","Power","Variant","Vehicle ID","Result precision","Cost"]},
        "partslink/manual reference": {key:"NOT TESTED" for key in ["Make","Model","Generation","Year","Engine","Engine code","Fuel","Power","Variant","Vehicle ID","Result precision","Cost"]},
        "other tested providers": {"Make":"PEUGEOT · PASS", "Model":"3008 SUV · LIKELY / DISPUTED", "Generation":"MC/MR/MJ/M4 · PARTIAL", "Year":"2018+ production range only", "Engine":"1.5 BlueHDi 130 · CROSS-SUPPORTED", "Engine code":"YHZ/DV5RC · PUBLIC CROSS-CHECK", "Fuel":"Diesel · PASS", "Power":"96 kW / 131 hp · PARTIAL", "Variant":"not exact", "Vehicle ID":"KType 130708 · IDENTITY CROSS-CHECKED", "Result precision":"ENGINE_LEVEL / RESEARCH ONLY / REVIEW", "Cost":"€0"},
    }
    fields = ["Make","Model","Generation","Year","Engine","Engine code","Fuel","Power","Variant","Vehicle ID","Result precision","Cost"]
    head = "".join(f"<th>{html.escape(p)}</th>" for p in providers)
    body = "".join("<tr><th>"+html.escape(field)+"</th>"+"".join(f"<td>{html.escape(values[p][field])}</td>" for p in providers)+"</tr>" for field in fields)
    (REPORTS / "client_vehicle_comparison.html").write_text(f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width'><title>PT client vehicle comparison</title><style>body{{font:14px/1.45 system-ui;margin:0;background:#f3f1eb;color:#15231e}}header{{background:#102d25;color:white;padding:42px 5vw}}main{{padding:32px 5vw}}.notice{{border-left:5px solid #a9463f;background:#f7e8e4;padding:16px;margin:20px 0}}.table{{overflow:auto;background:white;border:1px solid #ccd3cf}}table{{border-collapse:collapse;min-width:1700px}}th,td{{text-align:left;vertical-align:top;padding:12px;border:1px solid #dfe3e0}}thead th{{background:#1f493c;color:white}}tbody th{{background:#e8ebe8;position:sticky;left:0}}</style></head><body><header><small>PORTUGAL-ONLY · CLIENT CASE</small><h1>CG-17-GC / VF3MCYHZUPS034433</h1><p>Client expectation is context, not independent ground truth.</p></header><main><div class='notice'><b>Current result:</b> vPIC identifies only the make. Research cross-checks support the engine and KType identity, and point toward a 3008, but the client supplied 5008. No licensed PT plate/OEM source has confirmed the full vehicle or exact variant.</div><div class='table'><table><thead><tr><th>Field</th>{head}</tr></thead><tbody>{body}</tbody></table></div></main></body></html>""", encoding="utf-8")


def main() -> None:
    data = rows()
    with (REPORTS / "real_validation_matrix.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)
    render_comparison(data)
    print(json.dumps({"rows": len(data), "actual_tests": 4, "provider_vehicle_payloads": 3, "spend_eur": 0}, indent=2))


if __name__ == "__main__":
    main()
