from __future__ import annotations

import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from app.models import EvidenceStatus, IdentityResult, LookupStatus, Provenance, VehicleCandidate
from app.normalization import normalize_vin
from providers.base import VehicleIdentityProvider


def candidate_from_autofrance(payload: dict, raw_ref: str | None = None) -> VehicleCandidate:
    vehicle = payload.get("vehicle") or {}
    ktype = vehicle.get("ktype") or payload.get("ktype")
    model = vehicle.get("model")
    # Autofrance returns the TecDoc model/platform codes in parentheses. Keep the
    # source model verbatim, while exposing those returned codes as generation
    # evidence. Do not promote `from_year` to the individual vehicle's model year.
    platform_match = re.search(r"\(([^)]+)\)", model or "")
    generation = platform_match.group(1).strip() if platform_match else None
    return VehicleCandidate(
        make=vehicle.get("manufacturer"), model=model, generation=generation,
        production_from=str(vehicle.get("from_year")) if vehicle.get("from_year") else None,
        production_to=str(vehicle.get("to_year")) if vehicle.get("to_year") else None,
        engine_family=vehicle.get("cartype"), fuel=vehicle.get("fueltype"),
        power_kw=float(vehicle["kw"]) if vehicle.get("kw") is not None else None,
        power_hp=float(vehicle["hp"]) if vehicle.get("hp") is not None else None,
        displacement_cc=int(vehicle["ccm"]) if vehicle.get("ccm") is not None else None,
        body=vehicle.get("bodytype"), vin=payload.get("vin"), country_of_registration=None,
        provider_vehicle_ids={"autofrance_ktype": str(ktype)} if ktype else {},
        field_provenance={field: Provenance("autofrance_public") for field in ("make", "model", "engine_family", "fuel", "power_kw") if vehicle.get({"make":"manufacturer", "model":"model", "engine_family":"cartype", "fuel":"fueltype", "power_kw":"kw"}[field]) is not None},
        raw_payload_ref=raw_ref,
    )


class AutofranceProvider(VehicleIdentityProvider):
    name = "autofrance_public"
    version = "2026-10"

    def __init__(self, evidence_dir: Path | None = None):
        self.evidence_dir = evidence_dir

    def identify_by_vin(self, vin: str) -> IdentityResult:
        parsed = normalize_vin(vin)
        if not parsed.structurally_valid:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.PARTIALLY_VERIFIED)
        url = "https://api.autofrance.se/api/regnum/vin?vin=" + urllib.parse.quote(parsed.normalized)
        started = time.perf_counter()
        with urllib.request.urlopen(url, timeout=20) as response:
            raw = response.read()
        latency_ms = (time.perf_counter() - started) * 1000
        payload = json.loads(raw)
        raw_ref = None
        if self.evidence_dir:
            self.evidence_dir.mkdir(parents=True, exist_ok=True)
            path = self.evidence_dir / f"autofrance_{parsed.normalized}.json"
            path.write_bytes(raw)
            raw_ref = str(path)
        candidate = candidate_from_autofrance(payload, raw_ref)
        # Research-only endpoint: it has no documented production/reuse licence
        # and does not prove that a VIN exists. Even an ENGINE-level payload is
        # therefore never a resolved production identity on its own.
        return IdentityResult(
            self.name,
            LookupStatus.PARTIAL,
            [candidate],
            EvidenceStatus.PARTIALLY_VERIFIED,
            latency_ms,
            0.0,
            error_code="RESEARCH_ONLY_NO_EXISTENCE_CHECK",
            raw_payload_ref=raw_ref,
        )

    def identify_by_registration(self, registration: str) -> IdentityResult:
        return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.PARTIALLY_VERIFIED, error_code="UNSUPPORTED_ROUTE")
