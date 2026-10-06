from __future__ import annotations

import os
from typing import Mapping

from app.normalization import normalize_pt_registration, normalize_vin
from app.settings import env_value
from providers.configured import ConfiguredVehicleProvider, RouteRequest
from providers.http import HTTPResponse
from providers.parsing import candidate_from_record, unwrap_records


ALIASES = {
    "make": ("brand", "manufacturerName", "makeName"),
    "model": ("modelName", "vehicleModel"),
    "generation": ("generationName", "constructionType"),
    "engine": ("engineName", "vehicleTypeDescription"),
    "engine_code": ("engineCode", "motorCode"),
    "fuel": ("fuelType",),
    "power_kw": ("powerKw", "kw"),
    "power_hp": ("powerHp", "cv"),
    "displacement": ("capacityCcm", "ccm"),
    "variant": ("variant", "typeVariantVersion"),
    "vin": ("vin",),
    "ktype": ("tecdocVehicleId", "tecDocVehicleId", "kType", "ktype"),
    "provider_id": ("vehicleId", "id"),
    "first_registration": ("firstRegistration", "registrationDate"),
}


class Tips4yVehicleProvider(ConfiguredVehicleProvider):
    """Credential-ready adapter; endpoint paths must come from the client contract."""

    name = "tips4y"
    version = "contract-schema-1"

    def __init__(self, *, api_key: str | None = None, base_url: str | None = None, plate_path: str | None = None, vin_path: str | None = None, env: Mapping[str, str] | None = None):
        super().__init__()
        source = env if env is not None else os.environ
        self.api_key = api_key or env_value("TIPS4Y_API_KEY", env=source)
        self.base_url = (base_url or env_value("TIPS4Y_BASE_URL", env=source) or "").rstrip("/")
        self.plate_path = plate_path or env_value("TIPS4Y_PLATE_PATH", env=source)
        self.vin_path = vin_path or env_value("TIPS4Y_VIN_PATH", env=source)

    @property
    def configuration_error(self) -> str | None:
        missing = [name for name, value in (("TIPS4Y_API_KEY", self.api_key), ("TIPS4Y_BASE_URL", self.base_url)) if not value]
        return f"missing {', '.join(missing)}" if missing else None

    def configuration_error_for_route(self, route: str) -> str | None:
        base = self.configuration_error
        if base:
            return base
        path = self.plate_path if route == "registration" else self.vin_path
        return None if path else f"missing {'TIPS4Y_PLATE_PATH' if route == 'registration' else 'TIPS4Y_VIN_PATH'}"

    def build_request(self, route: str, value: str) -> RouteRequest:
        if route == "registration":
            path, query = self.plate_path, {"registration": normalize_pt_registration(value)}
        else:
            if not self.vin_path:
                raise NotImplementedError("TIPS4Y_VIN_PATH is not configured")
            parsed = normalize_vin(value)
            if not parsed.structurally_valid:
                raise ValueError("invalid VIN")
            path, query = self.vin_path, {"vin": parsed.normalized}
        return RouteRequest("GET", f"{self.base_url}/{(path or '').lstrip('/')}", query, {"Authorization": f"Bearer {self.api_key}"})

    def parse_response(self, route: str, value: str, response: HTTPResponse):
        registration = normalize_pt_registration(value) if route == "registration" else None
        vin = normalize_vin(value).normalized if route == "vin" else None
        return [candidate_from_record(record, provider=self.name, registration=registration, vin=vin, aliases=ALIASES) for record in unwrap_records(response.json())]
