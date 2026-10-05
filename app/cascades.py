from __future__ import annotations

from app.models import PrecisionLevel
from app.orchestrator import IdentityOrchestrator, ProviderStep
from providers.unavailable import AccessRequiredProvider, ManualSelectionProvider
from providers.autofrance import AutofranceProvider
from providers.vpic import VpicProvider


def vin_cascade(vpic: VpicProvider | None = None) -> IdentityOrchestrator:
    """Production-safe cascade: excludes research-only storefront endpoints."""
    return IdentityOrchestrator([
        # Local structure validation is performed before orchestration.
        ProviderStep(vpic or VpicProvider(), PrecisionLevel.ENGINE, max_cost=0.0),
        ProviderStep(AccessRequiredProvider("commercial_vin", "provider/token not selected"), PrecisionLevel.ENGINE),
        ProviderStep(AccessRequiredProvider("tecalliance_vin", "contract and credentials"), PrecisionLevel.ENGINE),
        ProviderStep(ManualSelectionProvider(), PrecisionLevel.ENGINE),
    ])


def vin_research_cascade(vpic: VpicProvider | None = None) -> IdentityOrchestrator:
    """Evidence campaign cascade; Autofrance is an oracle, never production selection."""
    return IdentityOrchestrator([
        ProviderStep(AutofranceProvider(), PrecisionLevel.ENGINE, max_cost=0.0),
        *vin_cascade(vpic).steps,
    ])


def registration_cascade() -> IdentityOrchestrator:
    return IdentityOrchestrator([
        ProviderStep(AccessRequiredProvider("existing_client_source", "software/API not available locally"), PrecisionLevel.ENGINE),
        ProviderStep(AccessRequiredProvider("telepecas", "OAuth client credentials"), PrecisionLevel.ENGINE),
        ProviderStep(AccessRequiredProvider("matricula_co_pt", "test username"), PrecisionLevel.ENGINE, max_cost=0.20),
        ProviderStep(AccessRequiredProvider("tecalliance_vrm", "contract and credentials"), PrecisionLevel.ENGINE),
        ProviderStep(ManualSelectionProvider(), PrecisionLevel.ENGINE),
    ])
