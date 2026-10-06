from __future__ import annotations

import json
import os
import xml.etree.ElementTree as ET
from typing import Mapping

from app.normalization import normalize_pt_registration
from app.settings import env_value
from providers.configured import ConfiguredVehicleProvider, RouteRequest
from providers.http import HTTPResponse
from providers.parsing import candidate_from_record, unwrap_records


ALIASES = {
    "make": ("CarMake", "Make", "Manufacturer"),
    "model": ("CarModel", "Model"),
    "engine": ("Description", "Variant", "Version"),
    "fuel": ("FuelType", "Fuel"),
    "power_hp": ("Power", "HorsePower"),
    "displacement": ("EngineSize",),
    "vin": ("VIN", "VehicleIdentificationNumber"),
    "year": ("RegistrationYear", "YearOfManufacture"),
    "first_registration": ("RegistrationDate",),
    "provider_id": ("ABI", "AbiCode"),
}


class MatriculaPtVehicleProvider(ConfiguredVehicleProvider):
    name = "matriculapt"
    version = "check-portugal-2026-10"
    estimated_cost_per_call = 0.20

    def __init__(self, *, username: str | None = None, endpoint: str | None = None, env: Mapping[str, str] | None = None):
        super().__init__()
        source = env if env is not None else os.environ
        self.username = username or env_value("MATRICULAPT_USERNAME", env=source)
        self.endpoint = endpoint or env_value("MATRICULAPT_ENDPOINT", "https://www.matricula.co.pt/api/reg.asmx/CheckPortugal", source)

    @property
    def configuration_error(self) -> str | None:
        return None if self.username and self.endpoint else "MATRICULAPT_USERNAME or endpoint is missing"

    def build_request(self, route: str, value: str) -> RouteRequest:
        if route != "registration":
            raise NotImplementedError("Matricula.co.pt adapter supports Portuguese registration only")
        return RouteRequest("GET", self.endpoint or "", {"RegistrationNumber": normalize_pt_registration(value), "username": self.username or ""}, {})

    def parse_response(self, route: str, value: str, response: HTTPResponse):
        text = response.body.decode("utf-8", errors="replace").strip()
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            root = ET.fromstring(text)
            embedded = (root.text or "").strip()
            payload = json.loads(embedded) if embedded.startswith(("{", "[")) else {"Description": embedded}
        registration = normalize_pt_registration(value)
        return [candidate_from_record(record, provider=self.name, registration=registration, aliases=ALIASES) for record in unwrap_records(payload)]
