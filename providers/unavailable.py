from __future__ import annotations

from app.models import EvidenceStatus, IdentityResult, LookupStatus
from providers.base import VehicleIdentityProvider


class AccessRequiredProvider(VehicleIdentityProvider):
    version = "access-required"

    def __init__(self, name: str, reason: str):
        self.name = name
        self.reason = reason

    def _blocked(self) -> IdentityResult:
        return IdentityResult(
            self.name,
            LookupStatus.ERROR,
            evidence_status=EvidenceStatus.WAITING_FOR_CREDENTIALS,
            error_code=f"ACCESS_REQUIRED:{self.reason}",
        )

    def identify_by_vin(self, vin: str) -> IdentityResult:
        return self._blocked()

    def identify_by_registration(self, registration: str) -> IdentityResult:
        return self._blocked()


class ManualSelectionProvider(VehicleIdentityProvider):
    name = "manual_selection"
    version = "1"

    def _manual(self) -> IdentityResult:
        return IdentityResult(self.name, LookupStatus.AMBIGUOUS, evidence_status=EvidenceStatus.PARTIALLY_VERIFIED, error_code="USER_INPUT_REQUIRED")

    def identify_by_vin(self, vin: str) -> IdentityResult:
        return self._manual()

    def identify_by_registration(self, registration: str) -> IdentityResult:
        return self._manual()

