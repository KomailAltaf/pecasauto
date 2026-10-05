from __future__ import annotations

from dataclasses import dataclass

from app.models import VehicleCandidate


COMPARABLE_FIELDS = ("make", "model", "generation", "model_year", "engine_family", "engine_code", "fuel", "power_kw", "variant")


@dataclass(frozen=True)
class AgreementResult:
    state: str
    disagreements: tuple[str, ...]
    missing: tuple[str, ...]


def compare_candidates(candidates: list[VehicleCandidate]) -> AgreementResult:
    if not candidates:
        return AgreementResult("NO_RESULT", (), COMPARABLE_FIELDS)
    disagreements: list[str] = []
    missing: list[str] = []
    for field in COMPARABLE_FIELDS:
        values = {str(getattr(candidate, field)).strip().lower() for candidate in candidates if getattr(candidate, field) not in (None, "")}
        if len(values) > 1:
            disagreements.append(field)
        if len(values) < len(candidates):
            missing.append(field)
    if disagreements:
        return AgreementResult("REVIEW", tuple(disagreements), tuple(missing))
    return AgreementResult("AGREE", (), tuple(missing))

