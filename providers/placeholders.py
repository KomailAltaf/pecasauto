from __future__ import annotations

from app.fitment import FitmentEvidence, SourceVerdict
from app.integrations import IntegrationResult
from app.models import VehicleCandidate
from providers.base import FitmentProvider, SupplierProvider


class NotConfiguredSupplierProvider(SupplierProvider):
    name = "none"

    def get_offers(self, product_id: str):
        return IntegrationResult.not_configured(self.name, "SUPPLIER_PROVIDER is not configured")


class TecDocFitmentProvider(FitmentProvider):
    name = "tecdoc"

    def get_products_for_vehicle(self, vehicle: VehicleCandidate) -> list[dict]:
        return []

    def validate_product(self, vehicle: VehicleCandidate, product_id: str) -> FitmentEvidence:
        return FitmentEvidence(
            source=self.name,
            verdict=SourceVerdict.UNKNOWN,
            licensed_catalogue=False,
            source_reference="NOT_CONFIGURED:TecDoc fitment contract/credentials missing",
        )
