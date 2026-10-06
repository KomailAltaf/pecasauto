from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from app.models import LookupStatus, as_dict
from app.settings import PlatformSettings
from app.vehicle_resolution import resolve_vehicle
from providers.configured import ConfiguredVehicleProvider
from providers.registry import VEHICLE_FACTORIES, catalogue_vehicle_provider, vehicle_provider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run one lawful configured vehicle-provider request.")
    parser.add_argument("--provider", choices=sorted(VEHICLE_FACTORIES), required=True)
    route = parser.add_mutually_exclusive_group(required=True)
    route.add_argument("--plate", help="Portuguese matrícula, e.g. CG-17-GC")
    route.add_argument("--vin", help="VIN/chassis number")
    parser.add_argument("--catalogue-provider", default=None, help="Override CATALOGUE_VEHICLE_PROVIDER")
    parser.add_argument("--save-raw", type=Path, help="Explicitly persist the raw response; verify provider storage rights first")
    return parser


def run(args: argparse.Namespace) -> tuple[dict, int]:
    provider = vehicle_provider(args.provider)
    input_type = "registration" if args.plate else "vin"
    input_value = args.plate or args.vin
    result = provider.identify_by_registration(input_value) if args.plate else provider.identify_by_vin(input_value)
    settings = PlatformSettings.from_env()
    catalogue_name = args.catalogue_provider or settings.catalogue_vehicle_provider
    resolution = resolve_vehicle(result, catalogue_vehicle_provider(catalogue_name))
    candidate = result.candidates[0] if result.candidates else None
    raw: object = getattr(provider, "last_raw", None)
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            pass
    output = {
        "provider": provider.name,
        "input_type": input_type,
        "input_value": input_value,
        "status": result.status.value,
        "evidence_status": result.evidence_status.value,
        "error": result.error_code,
        "raw_result": raw,
        "normalized_vehicle": as_dict(candidate) if candidate else None,
        "precision_level": candidate.precision.name if candidate else None,
        "ktype": candidate.provider_vehicle_ids.get("ktype") if candidate else None,
        "engine": candidate.engine_family if candidate else None,
        "engine_code": candidate.engine_code if candidate else None,
        "power_kw": candidate.power_kw if candidate else None,
        "power_hp": candidate.power_hp if candidate else None,
        "latency_ms": result.latency_ms,
        "estimated_cost_eur": result.cost,
        "catalogue_resolution": as_dict(resolution),
        "tested_at": datetime.now(timezone.utc).isoformat(),
        "notice": "A provider response is not fitment proof. COMPATIBLE requires a trusted configured fitment source.",
    }
    if args.save_raw and getattr(provider, "last_raw", None) is not None:
        args.save_raw.parent.mkdir(parents=True, exist_ok=True)
        args.save_raw.write_text(str(getattr(provider, "last_raw")), encoding="utf-8")
        output["raw_saved_to"] = str(args.save_raw)
        output["storage_warning"] = "Operator explicitly requested storage; contractual rights still require verification."
    return output, 2 if result.status is LookupStatus.NOT_CONFIGURED else 0


def main() -> int:
    output, code = run(build_parser().parse_args())
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
