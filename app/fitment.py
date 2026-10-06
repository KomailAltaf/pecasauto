from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.bridge import CatalogueBridgeResult
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
    terms_verified: bool = False
    source_reference: str | None = None
    restrictions: tuple[str, ...] = ()
    verified_at: str | None = None


@dataclass(frozen=True)
class FitmentDecision:
    source_verdict: SourceVerdict
    customer_state: CustomerFitmentState
    reasons: tuple[str, ...]

    @property
    def customer_message_pt(self) -> str:
        return {
            CustomerFitmentState.COMPATIBLE: "Compatível com o seu veículo",
            CustomerFitmentState.CONFIRM_COMPATIBILITY: "Confirmar compatibilidade",
            CustomerFitmentState.UNKNOWN: "Compatibilidade precisa de verificação",
            CustomerFitmentState.NOT_COMPATIBLE: "Não compatível com o seu veículo",
        }[self.customer_state]


def evaluate_fitment(
    vehicle: VehicleCandidate,
    evidence: list[FitmentEvidence],
    bridge: CatalogueBridgeResult | None = None,
    minimum_precision: PrecisionLevel = PrecisionLevel.ENGINE,
) -> FitmentDecision:
    if vehicle.precision < minimum_precision:
        return FitmentDecision(SourceVerdict.UNKNOWN, CustomerFitmentState.CONFIRM_COMPATIBILITY, ("IDENTITY_PRECISION_TOO_LOW",))
    verdicts = {item.verdict for item in evidence}
    if SourceVerdict.CONFLICT in verdicts or (SourceVerdict.MATCH in verdicts and SourceVerdict.NO_MATCH in verdicts):
        return FitmentDecision(SourceVerdict.CONFLICT, CustomerFitmentState.CONFIRM_COMPATIBILITY, ("SOURCE_DISAGREEMENT",))
    trusted_no_match = any(item.verdict is SourceVerdict.NO_MATCH and item.licensed_catalogue and item.terms_verified for item in evidence)
    if verdicts == {SourceVerdict.NO_MATCH} and trusted_no_match:
        return FitmentDecision(SourceVerdict.NO_MATCH, CustomerFitmentState.NOT_COMPATIBLE, ("ALL_SOURCES_NO_MATCH",))
    if verdicts == {SourceVerdict.NO_MATCH}:
        return FitmentDecision(SourceVerdict.UNKNOWN, CustomerFitmentState.CONFIRM_COMPATIBILITY, ("UNTRUSTED_NO_MATCH",))
    licensed_match = any(item.verdict is SourceVerdict.MATCH and item.licensed_catalogue and item.terms_verified for item in evidence)
    restrictions = tuple(restriction for item in evidence for restriction in item.restrictions)
    if licensed_match and bridge and bridge.may_claim_compatible and SourceVerdict.NO_MATCH not in verdicts and not restrictions:
        return FitmentDecision(SourceVerdict.MATCH, CustomerFitmentState.COMPATIBLE, ("LICENSED_MATCH",))
    if SourceVerdict.MATCH in verdicts:
        reason = "RESTRICTIONS_REQUIRE_CONFIRMATION" if restrictions else ("CATALOGUE_BRIDGE_NOT_VALIDATED" if licensed_match else "NO_LICENSED_CATALOGUE_MATCH")
        return FitmentDecision(SourceVerdict.MATCH, CustomerFitmentState.CONFIRM_COMPATIBILITY, (reason, *restrictions))
    return FitmentDecision(SourceVerdict.UNKNOWN, CustomerFitmentState.UNKNOWN, ("NO_DECISIVE_EVIDENCE",))
