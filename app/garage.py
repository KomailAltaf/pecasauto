from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from uuid import uuid4

from app.models import VehicleCandidate
from app.provider_policy import ProviderPolicy


class VehicleVerificationStatus(str, Enum):
    CUSTOMER_CONFIRMED = "CUSTOMER_CONFIRMED"
    PROVIDER_VERIFIED = "PROVIDER_VERIFIED"
    MANUAL_VERIFIED = "MANUAL_VERIFIED"
    DISPUTED = "DISPUTED"


@dataclass(frozen=True)
class SavedVehicle:
    internal_vehicle_id: str
    registration: str | None
    vin: str | None
    make: str | None
    model: str | None
    generation: str | None
    year: int | None
    engine: str | None
    engine_code: str | None
    power_kw: float | None
    power_hp: float | None
    fuel: str | None
    ktype: str | None
    provider: str
    verification_status: VehicleVerificationStatus
    verification_source: str
    verified_at: str

    @classmethod
    def from_candidate(
        cls,
        candidate: VehicleCandidate,
        *,
        provider: str,
        verification_status: VehicleVerificationStatus,
        verification_source: str,
        internal_vehicle_id: str | None = None,
    ) -> "SavedVehicle":
        return cls(
            internal_vehicle_id=internal_vehicle_id or str(uuid4()),
            registration=candidate.registration,
            vin=candidate.vin,
            make=candidate.make,
            model=candidate.model,
            generation=candidate.generation,
            year=candidate.model_year or candidate.first_registration_year,
            engine=candidate.engine_family,
            engine_code=candidate.engine_code,
            power_kw=candidate.power_kw,
            power_hp=candidate.power_hp,
            fuel=candidate.fuel,
            ktype=candidate.provider_vehicle_ids.get("ktype"),
            provider=provider,
            verification_status=verification_status,
            verification_source=verification_source,
            verified_at=datetime.now(timezone.utc).isoformat(),
        )


@dataclass
class CustomerGarage:
    """Customer-confirmed data; intentionally separate from provider cache."""

    vehicles: dict[str, VehicleCandidate] = field(default_factory=dict)
    saved_profiles: dict[str, SavedVehicle] = field(default_factory=dict)

    def save(self, customer_vehicle_id: str, vehicle: VehicleCandidate, confirmed: bool) -> None:
        if not confirmed:
            raise ValueError("garage vehicles require explicit customer confirmation")
        self.vehicles[customer_vehicle_id] = vehicle

    def save_profile(self, profile: SavedVehicle, policy: ProviderPolicy | None = None) -> None:
        customer_owned = profile.verification_status in {
            VehicleVerificationStatus.CUSTOMER_CONFIRMED,
            VehicleVerificationStatus.MANUAL_VERIFIED,
        }
        provider_storage_allowed = bool(policy and policy.terms_verified and policy.storage_allowed)
        if not customer_owned and not provider_storage_allowed:
            raise PermissionError("provider-derived vehicle storage is not permitted by verified terms")
        self.saved_profiles[profile.internal_vehicle_id] = profile

    def reusable_by_registration(self, registration: str) -> SavedVehicle | None:
        return next((vehicle for vehicle in self.saved_profiles.values() if vehicle.registration == registration), None)

    def reusable_by_vin(self, vin: str) -> SavedVehicle | None:
        return next((vehicle for vehicle in self.saved_profiles.values() if vehicle.vin == vin), None)
