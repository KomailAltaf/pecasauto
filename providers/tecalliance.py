from __future__ import annotations

import os
from typing import Mapping

from app.integrations import CatalogueVehicleResult
from app.normalization import normalize_pt_registration, normalize_vin
from app.settings import env_value
from providers.base import CatalogueVehicleProvider
from providers.configured import ConfiguredVehicleProvider, RouteRequest
from providers.http import HTTPResponse
from providers.parsing import candidate_from_record, unwrap_records


ALIASES = {
    "make": ("manuName", "manufacturerName", "make"),
    "model": ("modelName", "model"),
    "generation": ("constructionType", "platform"),
    "engine": ("typeName", "engineName"),
    "engine_code": ("engineCode", "motorCode"),
    "fuel": ("fuelType", "fuel"),
    "power_kw": ("powerKw", "kw"),
    "power_hp": ("powerHp", "hp"),
    "displacement": ("capacityCcm", "ccm"),
    "variant": ("vehicleTypeDescription", "variant"),
    "vin": ("vin",),
    "ktype": ("carId", "ktype", "kType", "vehicleId"),
    "provider_id": ("vehicleId", "carId"),
    "first_registration": ("firstRegistration",),
}


class TecAllianceVehicleProvider(ConfiguredVehicleProvider):
    """Placeholder until the contracted API paths/schema are supplied."""

    name = "tecalliance"
    version = "contract-schema-1"

    def __init__(self, *, api_key: str | None = None, base_url: str | None = None, plate_path: str | None = None, vin_path: str | None = None, env: Mapping[str, str] | None = None):
        super().__init__()
        source = env if env is not None else os.environ
        self.api_key = api_key or env_value("TECALLIANCE_API_KEY", env=source)
        self.base_url = (base_url or env_value("TECALLIANCE_BASE_URL", env=source) or "").rstrip("/")
        self.plate_path = plate_path or env_value("TECALLIANCE_PLATE_PATH", env=source)
        self.vin_path = vin_path or env_value("TECALLIANCE_VIN_PATH", env=source)

    @property
    def configuration_error(self) -> str | None:
        missing = [name for name, value in (("TECALLIANCE_API_KEY", self.api_key), ("TECALLIANCE_BASE_URL", self.base_url)) if not value]
        return f"missing {', '.join(missing)}" if missing else None

    def configuration_error_for_route(self, route: str) -> str | None:
        base = self.configuration_error
        if base:
            return base
        path = self.plate_path if route == "registration" else self.vin_path
        return None if path else f"missing {'TECALLIANCE_PLATE_PATH' if route == 'registration' else 'TECALLIANCE_VIN_PATH'}"

    def build_request(self, route: str, value: str) -> RouteRequest:
        if route == "registration":
            if not self.plate_path:
                raise NotImplementedError("TECALLIANCE_PLATE_PATH is not configured")
            path, query = self.plate_path, {"registration": normalize_pt_registration(value), "countryCode": "PT"}
        else:
            if not self.vin_path:
                raise NotImplementedError("TECALLIANCE_VIN_PATH is not configured")
            parsed = normalize_vin(value)
            if not parsed.structurally_valid:
                raise ValueError("invalid VIN")
            path, query = self.vin_path, {"vin": parsed.normalized, "countryCode": "PT"}
        return RouteRequest("GET", f"{self.base_url}/{path.lstrip('/')}", query, {"Authorization": f"Bearer {self.api_key}"})

    def parse_response(self, route: str, value: str, response: HTTPResponse):
        registration = normalize_pt_registration(value) if route == "registration" else None
        vin = normalize_vin(value).normalized if route == "vin" else None
        return [candidate_from_record(record, provider=self.name, registration=registration, vin=vin, aliases=ALIASES) for record in unwrap_records(response.json())]


class TecDocCatalogueVehicleProvider(CatalogueVehicleProvider):
    name = "tecdoc"

    def resolve_catalogue_vehicle(self, vehicle):
        return CatalogueVehicleResult.not_configured(self.name, "TecDoc catalogue credentials and contracted endpoint are missing")

    def list_vehicle_options(self, vehicle):
        return CatalogueVehicleResult.not_configured(self.name, "TecDoc catalogue credentials and contracted endpoint are missing")
