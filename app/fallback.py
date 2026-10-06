from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.models import PrecisionLevel, VehicleCandidate


@dataclass(frozen=True)
class ManualQuestion:
    state: str
    prompt: str
    field: str | None
    options: tuple[str, ...] = ()
    may_claim_compatibility: bool = False


class ConfirmationStatus(str, Enum):
    WAITING = "WAITING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


@dataclass
class ManualConfirmationSession:
    vehicle: VehicleCandidate
    question: ManualQuestion
    status: ConfirmationStatus = ConfirmationStatus.WAITING
    confirmed_value: str | None = None

    def confirm(self, value: str) -> VehicleCandidate:
        if self.status is not ConfirmationStatus.WAITING:
            raise ValueError("manual confirmation session is no longer open")
        if self.question.options and value not in self.question.options:
            raise ValueError("confirmation value is not one of the offered options")
        if not self.question.field:
            raise ValueError("question has no confirmable field")
        field = self.question.field
        if field == "power":
            self.vehicle.power_hp = float(value)
        elif field == "catalogue_vehicle_id":
            self.vehicle.provider_vehicle_ids["user_confirmed_catalogue_vehicle_id"] = value
        elif hasattr(self.vehicle, field):
            setattr(self.vehicle, field, value)
        else:
            raise ValueError(f"unsupported confirmation field: {field}")
        self.vehicle.ambiguity = False
        self.vehicle.candidate_count = 1
        self.confirmed_value = value
        self.status = ConfirmationStatus.CONFIRMED
        return self.vehicle


def next_manual_step(candidate: VehicleCandidate, candidate_engines: tuple[str, ...] = ()) -> ManualQuestion:
    if not candidate.make or not candidate.model:
        return ManualQuestion("MANUAL_VEHICLE_REQUIRED", "Selecione a marca e o modelo.", "model")
    if not candidate.engine_family:
        return ManualQuestion(
            "NEEDS_ENGINE_CONFIRMATION",
            "Encontrámos o modelo do seu veículo. Confirme a motorização.",
            "engine_family",
            candidate_engines,
        )
    if not candidate.fuel:
        return ManualQuestion("NEEDS_FUEL_CONFIRMATION", "Confirme o combustível.", "fuel")
    if not (candidate.power_kw or candidate.power_hp):
        return ManualQuestion("NEEDS_POWER_CONFIRMATION", "Confirme a potência do motor.", "power")
    if candidate.precision < PrecisionLevel.ENGINE:
        return ManualQuestion("NEEDS_MORE_DETAIL", "Precisamos de mais dados para confirmar a viatura.", None)
    return ManualQuestion("VEHICLE_IDENTIFIED", "Viatura identificada. A compatibilidade da peça ainda será validada.", None)
