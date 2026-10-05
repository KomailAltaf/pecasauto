from __future__ import annotations

from dataclasses import dataclass, field

from app.models import VehicleCandidate


@dataclass
class CustomerGarage:
    """Customer-confirmed data; intentionally separate from provider cache."""

    vehicles: dict[str, VehicleCandidate] = field(default_factory=dict)

    def save(self, customer_vehicle_id: str, vehicle: VehicleCandidate, confirmed: bool) -> None:
        if not confirmed:
            raise ValueError("garage vehicles require explicit customer confirmation")
        self.vehicles[customer_vehicle_id] = vehicle

