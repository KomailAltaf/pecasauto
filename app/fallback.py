from __future__ import annotations

from dataclasses import dataclass

from app.models import PrecisionLevel, VehicleCandidate


@dataclass(frozen=True)
class ManualQuestion:
    state: str
    prompt: str
    field: str | None
    options: tuple[str, ...] = ()
    may_claim_compatibility: bool = False


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

