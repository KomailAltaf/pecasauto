from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from app.fallback import ManualQuestion, next_manual_step
from app.integrations import CatalogueVehicleResult, IntegrationStatus
from app.models import IdentityResult, LookupStatus, VehicleCandidate
from providers.base import CatalogueVehicleProvider


class ResolutionState(str, Enum):
    NOT_CONFIGURED = "NOT_CONFIGURED"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    NEEDS_MANUAL_CONFIRMATION = "NEEDS_MANUAL_CONFIRMATION"
    CATALOGUE_ID_READY = "CATALOGUE_ID_READY"
    CATALOGUE_MAPPING_REQUIRED = "CATALOGUE_MAPPING_REQUIRED"


@dataclass(frozen=True)
class VehicleResolution:
    state: ResolutionState
    vehicle: VehicleCandidate | None = None
    catalogue_vehicle_id: str | None = None
    ktype: str | None = None
    question: ManualQuestion | None = None
    warnings: tuple[str, ...] = ()
    provider: str | None = None


def load_known_conflicts(path: Path | None = None) -> dict[str, dict[str, str]]:
    source = path or Path(__file__).resolve().parents[1] / "fixtures" / "identity_conflicts.json"
    return json.loads(source.read_text(encoding="utf-8")) if source.exists() else {}


def resolve_vehicle(
    identity: IdentityResult,
    catalogue: CatalogueVehicleProvider,
    *,
    candidate_engines: tuple[str, ...] = (),
    known_conflicts: dict[str, dict[str, str]] | None = None,
    authoritative_sources: tuple[str, ...] = ("registration_document", "partslink24_manual", "tecalliance"),
) -> VehicleResolution:
    if identity.status is LookupStatus.NOT_CONFIGURED:
        return VehicleResolution(ResolutionState.NOT_CONFIGURED, provider=identity.provider, warnings=(identity.error_code or "NOT_CONFIGURED",))
    if not identity.candidates:
        return VehicleResolution(ResolutionState.NOT_FOUND, provider=identity.provider, warnings=(identity.error_code or "NO_RESULT",))
    if len(identity.candidates) > 1 or identity.status in {LookupStatus.AMBIGUOUS, LookupStatus.CONFLICT, LookupStatus.FALSE_CONFIDENT_RESULT}:
        return VehicleResolution(ResolutionState.NEEDS_MANUAL_CONFIRMATION, identity.candidates[0], question=next_manual_step(identity.candidates[0], candidate_engines), provider=identity.provider, warnings=("MULTIPLE_OR_CONFLICTING_CANDIDATES",))

    vehicle = identity.candidates[0]
    conflicts = known_conflicts if known_conflicts is not None else load_known_conflicts()
    conflict = conflicts.get(vehicle.vin or "")
    if conflict and identity.provider not in authoritative_sources:
        return VehicleResolution(
            ResolutionState.CONFLICT,
            vehicle,
            ktype=vehicle.provider_vehicle_ids.get("ktype"),
            question=ManualQuestion("MODEL_CONFIRMATION_REQUIRED", conflict["message_pt"], "model", tuple(conflict.get("candidate_models", []))),
            provider=identity.provider,
            warnings=(conflict["code"],),
        )

    ktype = vehicle.provider_vehicle_ids.get("ktype")
    if ktype:
        return VehicleResolution(ResolutionState.CATALOGUE_ID_READY, vehicle, ktype, ktype, provider=identity.provider)

    question = next_manual_step(vehicle, candidate_engines)
    if question.state != "VEHICLE_IDENTIFIED":
        return VehicleResolution(ResolutionState.NEEDS_MANUAL_CONFIRMATION, vehicle, question=question, provider=identity.provider)

    catalogue_result = catalogue.resolve_catalogue_vehicle(vehicle)
    if catalogue_result.status is IntegrationStatus.NOT_CONFIGURED:
        return VehicleResolution(ResolutionState.CATALOGUE_MAPPING_REQUIRED, vehicle, provider=identity.provider, warnings=(catalogue_result.reason or "CATALOGUE_NOT_CONFIGURED",))
    if len(catalogue_result.options) == 1:
        option = catalogue_result.options[0]
        return VehicleResolution(ResolutionState.CATALOGUE_ID_READY, vehicle, option.catalogue_vehicle_id, option.ktype, provider=identity.provider)
    options = tuple(option.label for option in catalogue_result.options)
    return VehicleResolution(
        ResolutionState.NEEDS_MANUAL_CONFIRMATION,
        vehicle,
        question=ManualQuestion("CATALOGUE_VEHICLE_CONFIRMATION", "Encontrámos várias configurações. Confirme a sua viatura.", "catalogue_vehicle_id", options),
        provider=identity.provider,
    )


def apply_manual_confirmation(vehicle: VehicleCandidate, field: str, value: str) -> VehicleCandidate:
    allowed = {"model", "generation", "model_year", "engine_family", "engine_code", "fuel", "variant"}
    if field not in allowed:
        raise ValueError(f"unsupported manual confirmation field: {field}")
    if field == "model_year":
        setattr(vehicle, field, int(value))
    else:
        setattr(vehicle, field, value)
    vehicle.ambiguity = False
    vehicle.candidate_count = 1
    return vehicle
