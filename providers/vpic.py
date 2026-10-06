from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from app.models import EvidenceStatus, IdentityResult, LookupStatus, Provenance, VehicleCandidate
from app.normalization import normalize_vin
from providers.base import VehicleIdentityProvider


def candidate_from_vpic_row(row: dict, vin: str, raw_ref: str | None = None) -> VehicleCandidate:
    def text_value(key: str) -> str | None:
        value = row.get(key)
        return str(value).strip() if value not in (None, "") else None

    def number(key: str) -> float | None:
        value = text_value(key)
        try:
            return float(value) if value else None
        except ValueError:
            return None

    # NHTSA explicitly scopes vPIC detail to vehicles intended for the US. For
    # this PT-only campaign, a year inferred from an EU VIN position is retained
    # only in raw evidence and not promoted into the canonical vehicle.
    trusted_model_year = None
    displacement = number("DisplacementCC")
    return VehicleCandidate(
        make=text_value("Make"), model=text_value("Model"), model_year=trusted_model_year,
        engine_family=text_value("EngineModel"), fuel=text_value("FuelTypePrimary"),
        power_kw=number("EngineKW"), power_hp=number("EngineHP"),
        displacement_cc=int(displacement) if displacement else None,
        variant=text_value("Trim") or text_value("Series"), body=text_value("BodyClass"),
        vehicle_class=text_value("VehicleType"), vin=vin, country_of_registration=None,
        field_provenance={key: Provenance("vpic_public") for key in ("make", "model") if text_value({"make":"Make", "model":"Model"}[key])},
        raw_payload_ref=raw_ref,
    )


class VpicProvider(VehicleIdentityProvider):
    """NHTSA vPIC adapter.

    vPIC is tested only as a free, basic routing source. NHTSA states its data
    represents vehicles intended for sale/import into the United States, so an
    EU result is never promoted beyond what the returned fields actually prove.
    """

    name = "vpic_public"
    version = "4"

    def __init__(self, base_url: str = "https://vpic.nhtsa.dot.gov/api", evidence_dir: Path | None = None):
        self.base_url = base_url.rstrip("/")
        self.evidence_dir = evidence_dir
        self.last_raw: str | None = None
        self.last_http_status: int | None = None

    def identify_by_vin(self, vin: str) -> IdentityResult:
        parsed = normalize_vin(vin)
        if not parsed.structurally_valid:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.VERIFIED)
        encoded = urllib.parse.quote(parsed.normalized)
        url = f"{self.base_url}/vehicles/DecodeVinValues/{encoded}?format=json"
        started = time.perf_counter()
        with urllib.request.urlopen(url, timeout=20) as response:
            raw = response.read()
            self.last_http_status = response.status
        self.last_raw = raw.decode("utf-8", errors="replace")
        latency_ms = (time.perf_counter() - started) * 1000
        payload = json.loads(raw)
        row = (payload.get("Results") or [{}])[0]
        raw_ref = None
        if self.evidence_dir:
            self.evidence_dir.mkdir(parents=True, exist_ok=True)
            target = self.evidence_dir / f"{self.name}_{parsed.normalized}.json"
            target.write_bytes(raw)
            raw_ref = str(target)

        candidate = candidate_from_vpic_row(row, parsed.normalized, raw_ref)
        text_value = lambda key: str(row.get(key)).strip() if row.get(key) not in (None, "") else None
        error_code = text_value("ErrorCode")
        status = LookupStatus.PARTIAL if candidate.make else LookupStatus.NO_RESULT
        return IdentityResult(
            self.name,
            status,
            [candidate] if candidate.make else [],
            EvidenceStatus.VERIFIED,
            latency_ms=latency_ms,
            cost=0.0,
            error_code=error_code,
            raw_payload_ref=raw_ref,
        )

    def identify_by_registration(self, registration: str) -> IdentityResult:
        return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.VERIFIED, error_code="UNSUPPORTED_ROUTE")


class SelfHostedVpicProvider(VpicProvider):
    name = "vpic_self_hosted"

    def __init__(self, base_url: str = "http://127.0.0.1:9060/api", evidence_dir: Path | None = None):
        super().__init__(base_url, evidence_dir)
