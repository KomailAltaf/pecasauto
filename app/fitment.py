from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.models import PrecisionLevel, VehicleCandidate


class SourceVerdict(str, Enum):
    MATCH = "MATCH"
    NO_MATCH = "NO_MATCH"
    UNKNOWN = "UNKNOWN"
    CONFLICT = "CONFLICT"


class CustomerFitmentState(str, Enum):
    COMPATIBLE = "COMPATIBLE"
    CONFIRM_COMPATIBILITY = "CONFIRM_COMPATIBILITY"
    UNKNOWN = "UNKNOWN"
    NOT_COMPATIBLE = "NOT_COMPATIBLE"


@dataclass(frozen=True)
class FitmentEvidence:
    source: str
    verdict: SourceVerdict
    licensed_catalogue: bool
    source_reference: str | None = None
    restrictions: tuple[str, ...] = ()
    verified_at: str | None = None


@dataclass(frozen=True)
class FitmentDecision:
    source_verdict: SourceVerdict
    customer_state: CustomerFitmentState
    reasons: tuple[str, ...]


def evaluate_fitment(
    vehicle: VehicleCandidate,
    evidence: list[FitmentEvidence],
    minimum_precision: PrecisionLevel = PrecisionLevel.ENGINE,
) -> FitmentDecision:
    if vehicle.precision < minimum_precision:
        return FitmentDecision(SourceVerdict.UNKNOWN, CustomerFitmentState.CONFIRM_COMPATIBILITY, ("IDENTITY_PRECISION_TOO_LOW",))
    verdicts = {item.verdict for item in evidence}
    if SourceVerdict.CONFLICT in verdicts or (SourceVerdict.MATCH in verdicts and SourceVerdict.NO_MATCH in verdicts):
        return FitmentDecision(SourceVerdict.CONFLICT, CustomerFitmentState.CONFIRM_COMPATIBILITY, ("SOURCE_DISAGREEMENT",))
    if verdicts == {SourceVerdict.NO_MATCH}:
        return FitmentDecision(SourceVerdict.NO_MATCH, CustomerFitmentState.NOT_COMPATIBLE, ("ALL_SOURCES_NO_MATCH",))
    licensed_match = any(item.verdict is SourceVerdict.MATCH and item.licensed_catalogue for item in evidence)
    restrictions = tuple(restriction for item in evidence for restriction in item.restrictions)
    if licensed_match and SourceVerdict.NO_MATCH not in verdicts and not restrictions:
        return FitmentDecision(SourceVerdict.MATCH, CustomerFitmentState.COMPATIBLE, ("LICENSED_MATCH",))
    if SourceVerdict.MATCH in verdicts:
        reason = "RESTRICTIONS_REQUIRE_CONFIRMATION" if restrictions else "NO_LICENSED_CATALOGUE_MATCH"
        return FitmentDecision(SourceVerdict.MATCH, CustomerFitmentState.CONFIRM_COMPATIBILITY, (reason, *restrictions))
    return FitmentDecision(SourceVerdict.UNKNOWN, CustomerFitmentState.UNKNOWN, ("NO_DECISIVE_EVIDENCE",))

