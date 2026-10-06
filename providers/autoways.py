from __future__ import annotations

import os
from typing import Any, Mapping

from app.normalization import normalize_pt_registration, normalize_vin
from app.settings import env_value
from providers.configured import ConfiguredVehicleProvider, RouteRequest
from providers.http import HTTPResponse
from providers.parsing import candidate_from_record, clean, first, unwrap_records


ALIASES = {
    "make": ("AWN_marque",),
    "model": ("AWN_modele", "AWN_modele_etude"),
    "label": ("AWN_label", "AWN_libelle"),
    "generation": ("AWN_code_platform",),
    "engine": ("AWN_label_engine", "AWN_label_moteur", "AWN_version"),
    "engine_code": ("AWN_code_moteur",),
    "fuel": ("AWN_energie",),
    "power_kw": ("AWN_puissance_KW",),
    "power_hp": ("AWN_puissance_chevaux",),
    "displacement": ("AWN_nbr_cylindre_energie",),
    "variant": ("AWN_finition", "AWN_type_variante_version", "AWN_version"),
    "body": ("AWN_carrosserie",),
    "transmission": ("AWN_type_boite_vites",),
    "drive": ("AWN_propulsion",),
    "vin": ("AWN_VIN",),
    "ktype": ("AWN_k_type",),
    "provider_id": ("AWN_id_version", "AWN_selector_modele_id", "AWN_TID", "AWN_modele_id"),
    "first_registration": ("AWN_date_mise_en_circulation",),
}


class AutowaysVehicleProvider(ConfiguredVehicleProvider):
    name = "autoways"
    version = "openapi-2026-10"

    def __init__(self, *, token: str | None = None, base_url: str | None = None, env: Mapping[str, str] | None = None):
        super().__init__()
        source = env if env is not None else os.environ
        self.token = token or env_value("AUTOWAYS_API_KEY", env=source) or env_value("AUTOWAYS_API_TOKEN", env=source)
        self.base_url = (base_url or env_value("AUTOWAYS_BASE_URL", "https://app.auto-ways.net/api/v1", source) or "").rstrip("/")
        self.plate_path = env_value("AUTOWAYS_PLATE_PATH", "/pt", source) or "/pt"
        self.vin_path = env_value("AUTOWAYS_VIN_PATH", "/vin/", source) or "/vin/"

    @property
    def configuration_error(self) -> str | None:
        return None if self.token else "AUTOWAYS_API_KEY (or AUTOWAYS_API_TOKEN) is missing"

    def build_request(self, route: str, value: str) -> RouteRequest:
        if route == "registration":
            return RouteRequest("GET", f"{self.base_url}/{self.plate_path.lstrip('/')}", {"plaque": normalize_pt_registration(value).replace("-", ""), "token": self.token or "", "output_lang": "en"}, {})
        parsed = normalize_vin(value)
        if not parsed.structurally_valid:
            raise ValueError("invalid VIN")
        return RouteRequest("GET", f"{self.base_url}/{self.vin_path.lstrip('/')}", {"vin": parsed.normalized, "country": "PT", "token": self.token or "", "output_lang": "en"}, {})

    def parse_response(self, route: str, value: str, response: HTTPResponse):
        payload = response.json()
        if isinstance(payload, dict) and payload.get("error") not in (None, False, 0, "false"):
            return []
        registration = normalize_pt_registration(value) if route == "registration" else None
        vin = normalize_vin(value).normalized if route == "vin" else None
        candidates = []
        for record in unwrap_records(payload):
            candidate = candidate_from_record(record, provider=self.name, registration=registration, vin=vin, aliases=ALIASES)
            tecdoc_model_id = clean(first(record, "AWN_tecdoc_modele_id", "AWN_tecdoc_model_id"))
            tecdoc_brand_id = clean(first(record, "AWN_tecdoc_brand_id", "AWN_tecdoc_marque_id"))
            selector_model_id = clean(first(record, "AWN_selector_modele_id"))
            selector_brand_id = clean(first(record, "AWN_selector_marque_id"))
            if tecdoc_model_id:
                candidate.provider_vehicle_ids["tecdoc_model_id"] = tecdoc_model_id
            if tecdoc_brand_id:
                candidate.provider_vehicle_ids["tecdoc_brand_id"] = tecdoc_brand_id
            if selector_model_id:
                candidate.provider_vehicle_ids["autoways_selector_model_id"] = selector_model_id
            if selector_brand_id:
                candidate.provider_vehicle_ids["autoways_selector_brand_id"] = selector_brand_id
            candidates.append(candidate)
        return candidates
