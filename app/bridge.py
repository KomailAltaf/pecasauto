from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class MatchMethod(str, Enum):
    PROVIDER_ID = "PROVIDER_ID"
    VIN = "VIN"
    ENGINE_CODE = "ENGINE_CODE"
    TEXT_MATCH = "TEXT_MATCH"
    USER_CONFIRMED = "USER_CONFIRMED"


@dataclass(frozen=True)
class CatalogueBridgeResult:
    method: MatchMethod
    candidates_count: int
    catalogue_vehicle_id: str | None = None
    licensed_fitment_match: bool = False

    @property
    def may_claim_compatible(self) -> bool:
        return (
            self.candidates_count == 1
            and self.catalogue_vehicle_id is not None
            and self.licensed_fitment_match
            and self.method in {MatchMethod.PROVIDER_ID, MatchMethod.VIN, MatchMethod.ENGINE_CODE, MatchMethod.USER_CONFIRMED}
        )

