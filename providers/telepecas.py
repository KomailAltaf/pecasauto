from __future__ import annotations

import json
import os
from typing import Mapping

from app.normalization import normalize_pt_registration, normalize_vin
from app.settings import env_value
from providers.configured import ConfiguredVehicleProvider, RouteRequest
from providers.http import HTTPResponse, http_request
from providers.parsing import candidate_from_record, unwrap_records


ALIASES = {
    "make": ("brand", "brandName", "make"),
    "model": ("model", "modelName"),
    "generation": ("generation", "version"),
    "engine": ("engine", "motorization", "version"),
    "engine_code": ("engineCode", "motorCode"),
    "fuel": ("fuel", "fuelType"),
    "power_kw": ("powerKw", "kw"),
    "power_hp": ("powerHp", "cv"),
    "displacement": ("displacement", "cc"),
    "variant": ("variant", "version"),
    "vin": ("vin",),
    "ktype": ("ktype", "kType", "tecDocModelId"),
    "provider_id": ("telepecasModelId", "vehicleId", "id"),
    "first_registration": ("firstRegistration", "registrationDate"),
}


class TelePecasVehicleProvider(ConfiguredVehicleProvider):
    name = "telepecas"
    version = "contract-schema-1"

    def __init__(self, *, access_token: str | None = None, client_id: str | None = None, client_secret: str | None = None, token_url: str | None = None, base_url: str | None = None, plate_path: str | None = None, vin_path: str | None = None, env: Mapping[str, str] | None = None):
        super().__init__()
        source = env if env is not None else os.environ
        self.access_token = access_token or env_value("TELEPECAS_ACCESS_TOKEN", env=source)
        self.client_id = client_id or env_value("TELEPECAS_CLIENT_ID", env=source)
        self.client_secret = client_secret or env_value("TELEPECAS_CLIENT_SECRET", env=source)
        self.token_url = token_url or env_value("TELEPECAS_TOKEN_URL", env=source)
        self.base_url = (base_url or env_value("TELEPECAS_BASE_URL", "https://api.telepecas.com/v1", source) or "").rstrip("/")
        self.plate_path = plate_path or env_value("TELEPECAS_PLATE_PATH", env=source)
        self.vin_path = vin_path or env_value("TELEPECAS_VIN_PATH", env=source)

    @property
    def configuration_error(self) -> str | None:
        credential_ok = self.access_token or (self.client_id and self.client_secret and self.token_url)
        if not credential_ok:
            return "TELEPECAS_ACCESS_TOKEN or OAuth client credentials are missing"
        return None

    def configuration_error_for_route(self, route: str) -> str | None:
        base = self.configuration_error
        if base:
            return base
        path = self.plate_path if route == "registration" else self.vin_path
        return None if path else f"missing {'TELEPECAS_PLATE_PATH' if route == 'registration' else 'TELEPECAS_VIN_PATH'} from contract"

    def _token(self) -> str:
        if self.access_token:
            return self.access_token
        response = http_request("POST", self.token_url or "", form={"grant_type": "client_credentials", "client_id": self.client_id or "", "client_secret": self.client_secret or ""})
        if not 200 <= response.status < 300:
            raise PermissionError("TelePeças OAuth failed")
        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise ValueError("TelePeças OAuth response has no access_token")
        return str(token)

    def build_request(self, route: str, value: str) -> RouteRequest:
        if route == "registration":
            if not self.plate_path:
                raise NotImplementedError("TELEPECAS_PLATE_PATH is not configured")
            path, query = self.plate_path, {"registration": normalize_pt_registration(value), "country": "PT"}
        else:
            if not self.vin_path:
                raise NotImplementedError("TELEPECAS_VIN_PATH is not configured")
            parsed = normalize_vin(value)
            if not parsed.structurally_valid:
                raise ValueError("invalid VIN")
            path, query = self.vin_path, {"vin": parsed.normalized, "country": "PT"}
        return RouteRequest("GET", f"{self.base_url}/{path.lstrip('/')}", query, {"Authorization": f"Bearer {self._token()}"})

    def parse_response(self, route: str, value: str, response: HTTPResponse):
        registration = normalize_pt_registration(value) if route == "registration" else None
        vin = normalize_vin(value).normalized if route == "vin" else None
        return [candidate_from_record(record, provider=self.name, registration=registration, vin=vin, aliases=ALIASES) for record in unwrap_records(response.json())]
