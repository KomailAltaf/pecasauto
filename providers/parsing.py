from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any, Iterable

from app.models import Provenance, VehicleCandidate


EMPTY = {"", "0", "unknown", "inconnue", "inconnu", "n/a", "null", "none", "-"}


def clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return None if text.lower() in EMPTY else text


def first(record: dict[str, Any], *keys: str) -> Any:
    lowered = {str(key).lower(): value for key, value in record.items()}
    for key in keys:
        value = record.get(key, lowered.get(key.lower()))
        if clean(value) is not None:
            return value
    return None


def number(value: Any) -> float | None:
    text = clean(value)
    if not text:
        return None
    match = re.search(r"-?\d+(?:[.,]\d+)?", text)
    return float(match.group(0).replace(",", ".")) if match else None


def integer(value: Any) -> int | None:
    parsed = number(value)
    return int(parsed) if parsed is not None else None


def year(value: Any) -> int | None:
    text = clean(value)
    if not text:
        return None
    match = re.search(r"(?:19|20)\d{2}", text)
    return int(match.group(0)) if match else None


def generation_from_label(value: Any) -> str | None:
    text = clean(value)
    if not text:
        return None
    match = re.search(r"\(([^)]+)\)", text)
    return match.group(1).strip() if match else None


def unwrap_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("data", "results", "result", "vehicles", "vehicle"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
        if isinstance(value, dict):
            return [value]
    return [payload]


def candidate_from_record(
    record: dict[str, Any],
    *,
    provider: str,
    registration: str | None = None,
    vin: str | None = None,
    aliases: dict[str, tuple[str, ...]] | None = None,
) -> VehicleCandidate:
    aliases = aliases or {}

    def get(field: str, *defaults: str) -> Any:
        return first(record, *(aliases.get(field, ()) + defaults))

    make = clean(get("make", "make", "manufacturer", "brand", "marque"))
    model = clean(get("model", "model", "modele"))
    label = get("label", "label", "description", "libelle")
    generation = clean(get("generation", "generation", "platform", "chassis_code")) or generation_from_label(label)
    ktype = clean(get("ktype", "ktype", "k_type", "tecdoc_vehicle_id", "tecdocmodelid"))
    provider_id = clean(get("provider_id", "vehicle_id", "id", "model_id"))
    observed_at = datetime.now(timezone.utc).isoformat()
    values = {
        "make": make,
        "model": model,
        "generation": generation,
        "engine_family": clean(get("engine", "engine", "engine_name", "motor", "cartype")),
        "engine_code": clean(get("engine_code", "engine_code", "motor_code", "code_moteur")),
        "fuel": clean(get("fuel", "fuel", "fuel_type", "energy", "energia")),
        "variant": clean(get("variant", "variant", "version", "trim", "type_variant_version")),
    }
    ids: dict[str, str] = {}
    if ktype:
        ids["ktype"] = ktype
    if provider_id:
        ids[f"{provider}_vehicle_id"] = provider_id
    candidate = VehicleCandidate(
        **values,
        model_year=year(get("year", "year", "model_year", "registration_year", "date_first_registration")),
        first_registration_year=year(get("first_registration", "first_registration", "first_registration_date", "date_first_registration")),
        power_kw=number(get("power_kw", "power_kw", "kw")),
        power_hp=number(get("power_hp", "power_hp", "hp", "horsepower", "cv")),
        displacement_cc=integer(get("displacement", "displacement_cc", "engine_size", "cc", "ccm")),
        body=clean(get("body", "body", "body_type")),
        transmission=clean(get("transmission", "transmission", "gearbox")),
        drive=clean(get("drive", "drive", "propulsion")),
        vin=clean(get("vin", "vin", "chassis", "chassis_number")) or vin,
        registration=registration,
        country_of_registration="PT" if registration else None,
        provider_vehicle_ids=ids,
        field_provenance={
            field: Provenance(provider, observed_at=observed_at)
            for field, value in values.items()
            if value is not None
        },
    )
    return candidate
