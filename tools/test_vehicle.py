from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from app.models import EvidenceStatus, IdentityResult, LookupStatus, PrecisionLevel, as_dict
from app.settings import PlatformSettings
from providers.registry import vehicle_provider


PROVIDERS = ("autoways", "tips4y", "matriculapt", "telepecas")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description="Test a Portugal vehicle lookup through one provider or the configured cascade.")
    lookup = command.add_mutually_exclusive_group(required=True)
    lookup.add_argument("--plate", help="Portuguese matrícula")
    lookup.add_argument("--vin", help="VIN from a Portuguese-market vehicle")
    command.add_argument("--country", default="PT", choices=["PT"], help="This lab scores Portugal only")
    command.add_argument("--provider", default="cascade", choices=(*PROVIDERS, "cascade"))
    return command


def _provider_names(route: str, selected: str) -> list[str]:
    if selected != "cascade":
        return [selected]
    settings = PlatformSettings.from_env()
    configured = [settings.vehicle_provider, settings.fallback_provider]
    if route == "vin":
        ordered = ["vpic", *configured, "tips4y", "telepecas", "tecalliance"]
        allowed = {"vpic", "autoways", "tips4y", "telepecas", "tecalliance"}
    else:
        ordered = [*configured, "tips4y", "matriculapt", "telepecas", "tecalliance"]
        allowed = {"autoways", "tips4y", "matriculapt", "telepecas", "tecalliance"}
    return list(dict.fromkeys(name for name in ordered if name in allowed))


def _raw(provider: Any) -> Any:
    value = getattr(provider, "last_raw", None)
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value


def _attempt(provider: Any, result: IdentityResult) -> dict[str, Any]:
    candidates = [as_dict(candidate) for candidate in result.candidates]
    return {
        "provider_attempted": result.provider,
        "http_result": getattr(provider, "last_http_status", None),
        "status": result.status.value,
        "error": result.error_code,
        "raw_data": _raw(provider),
        "normalized_candidates": candidates,
        "precision": result.best_precision.name if candidates else None,
        "engine": [candidate.engine_family for candidate in result.candidates],
        "engine_code": [candidate.engine_code for candidate in result.candidates],
        "power_kw": [candidate.power_kw for candidate in result.candidates],
        "k_type": [candidate.provider_vehicle_ids.get("ktype") or candidate.provider_vehicle_ids.get("autoways_ktype") for candidate in result.candidates],
        "latency_ms": result.latency_ms,
        "cost_eur": result.cost,
    }


def _next_action(attempts: list[dict[str, Any]]) -> str:
    if any(item["normalized_candidates"] and item["precision"] in {"ENGINE", "EXACT_VARIANT"} for item in attempts):
        return "DISPLAY_CANDIDATES_FOR_CUSTOMER_CONFIRMATION; then resolve catalogue vehicle ID and ask the fitment source."
    if any(item["normalized_candidates"] for item in attempts):
        return "PARTIAL_RESULT; ask for missing engine/variant or continue to manual selection."
    if all(item["status"] == "NOT_CONFIGURED" for item in attempts):
        return "WAITING_FOR_PROVIDER; add a credential to .env and restart."
    return "NO_RESULT; continue to the next lawful provider or manual vehicle selection."


def run(args: argparse.Namespace) -> tuple[dict[str, Any], int]:
    route = "registration" if args.plate else "vin"
    value = args.plate or args.vin
    attempts: list[dict[str, Any]] = []
    for name in _provider_names(route, args.provider):
        provider = vehicle_provider(name)
        try:
            result = provider.identify_by_registration(value) if route == "registration" else provider.identify_by_vin(value)
        except Exception as exc:
            result = IdentityResult(name, LookupStatus.ERROR, evidence_status=EvidenceStatus.NOT_VERIFIED, error_code=f"NETWORK_OR_PROVIDER_ERROR:{type(exc).__name__}")
        attempts.append(_attempt(provider, result))
        if result.status is LookupStatus.RESOLVED and result.best_precision >= PrecisionLevel.ENGINE:
            break
    output = {
        "country": "PT",
        "input_type": route,
        "input_value": value,
        "provider_mode": args.provider,
        "attempts": attempts,
        "next_action": _next_action(attempts),
        "fitment_warning": "Vehicle identity is not compatibility. Never claim fitment without a trusted FitmentProvider result.",
    }
    waiting = not any(item["normalized_candidates"] for item in attempts)
    return output, 2 if waiting else 0


def main() -> int:
    output, code = run(parser().parse_args())
    print(json.dumps(output, indent=2, ensure_ascii=False))
    return code


if __name__ == "__main__":
    sys.exit(main())
