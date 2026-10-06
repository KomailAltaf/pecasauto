from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.integrations import CatalogueVehicleResult
from app.models import VehicleCandidate
from providers.base import CatalogueVehicleProvider


class PartslinkRole(str, Enum):
    MANUAL_VALIDATION = "MANUAL_VALIDATION"
    OE_REFERENCE_SOURCE = "OE_REFERENCE_SOURCE"
    FUTURE_LICENSED_INTEGRATION = "FUTURE_LICENSED_INTEGRATION"


@dataclass(frozen=True)
class ManualValidationRecord:
    vin: str
    vehicle_label: str
    oe_reference: str | None
    validated_by: str
    evidence_reference: str


class Partslink24Boundary(CatalogueVehicleProvider):
    """No HTTP/browser automation. Programmatic use requires a separate licence."""

    name = "partslink24"
    permitted_roles = (PartslinkRole.MANUAL_VALIDATION, PartslinkRole.OE_REFERENCE_SOURCE)

    def resolve_catalogue_vehicle(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult:
        return CatalogueVehicleResult.not_configured(self.name, "manual validation only; programmatic integration rights are not confirmed")

    def list_vehicle_options(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult:
        return CatalogueVehicleResult.not_configured(self.name, "manual validation only; no scraping or browser automation")
