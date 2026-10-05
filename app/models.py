from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, IntEnum
from typing import Any


class PrecisionLevel(IntEnum):
    BASIC = 1
    MODEL = 2
    ENGINE = 3
    EXACT_VARIANT = 4


class LookupStatus(str, Enum):
    NO_RESULT = "NO_RESULT"
    AMBIGUOUS = "AMBIGUOUS"
    PARTIAL = "PARTIAL"
    RESOLVED = "RESOLVED"
    CONFLICT = "CONFLICT"
    ERROR = "ERROR"


class EvidenceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PARTIALLY_VERIFIED = "PARTIALLY VERIFIED"
    NOT_VERIFIED = "NOT VERIFIED"
    WAITING_FOR_CREDENTIALS = "WAITING FOR CREDENTIALS"
    MOCK_ONLY = "MOCK ONLY"


@dataclass(frozen=True)
class Provenance:
    source: str
    external_reference: str | None = None
    observed_at: str | None = None


@dataclass
class VehicleCandidate:
    make: str | None = None
    model: str | None = None
    generation: str | None = None
    model_year: int | None = None
    first_registration_year: int | None = None
    production_from: str | None = None
    production_to: str | None = None
    engine_family: str | None = None
    engine_code: str | None = None
    fuel: str | None = None
    power_kw: float | None = None
    power_hp: float | None = None
    displacement_cc: int | None = None
    variant: str | None = None
    body: str | None = None
    transmission: str | None = None
    drive: str | None = None
    vehicle_class: str | None = None
    emission_standard: str | None = None
    market: str | None = None
    steering: str | None = None
    vin: str | None = None
    registration: str | None = None
    country_of_registration: str | None = None
    provider_vehicle_ids: dict[str, str] = field(default_factory=dict)
    field_provenance: dict[str, Provenance] = field(default_factory=dict)
    raw_payload_ref: str | None = None
    ambiguity: bool = False
    candidate_count: int = 1

    @property
    def precision(self) -> PrecisionLevel:
        if not self.make:
            return PrecisionLevel.BASIC
        if not (self.model and (self.generation or self.model_year)):
            return PrecisionLevel.BASIC
        if not (self.engine_family and self.fuel and (self.power_kw or self.power_hp)):
            return PrecisionLevel.MODEL
        if not (self.engine_code and self.variant and self.provider_vehicle_ids):
            return PrecisionLevel.ENGINE
        return PrecisionLevel.EXACT_VARIANT


@dataclass
class IdentityResult:
    provider: str
    status: LookupStatus
    candidates: list[VehicleCandidate] = field(default_factory=list)
    evidence_status: EvidenceStatus = EvidenceStatus.NOT_VERIFIED
    latency_ms: float | None = None
    cost: float | None = None
    error_code: str | None = None
    raw_payload_ref: str | None = None

    @property
    def best_precision(self) -> PrecisionLevel:
        return max((c.precision for c in self.candidates), default=PrecisionLevel.BASIC)


def as_dict(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if hasattr(value, "__dataclass_fields__"):
        return {name: as_dict(getattr(value, name)) for name in value.__dataclass_fields__}
    if isinstance(value, dict):
        return {key: as_dict(item) for key, item in value.items()}
    if isinstance(value, list):
        return [as_dict(item) for item in value]
    return value

