from __future__ import annotations

from abc import ABC, abstractmethod

from app.integrations import (
    CatalogueVehicleResult,
    CustomerRecord,
    IntegrationResult,
    InvoiceRecord,
    OrderDraft,
    OrderRecord,
    PriceRecord,
    StockRecord,
    SupplierOffer,
)
from app.models import IdentityResult, VehicleCandidate
from app.fitment import FitmentEvidence


class VehicleIdentityProvider(ABC):
    name: str
    version: str = "unknown"

    @abstractmethod
    def identify_by_vin(self, vin: str) -> IdentityResult: ...

    @abstractmethod
    def identify_by_registration(self, registration: str) -> IdentityResult: ...


class CatalogueVehicleProvider(ABC):
    """Maps canonical vehicle evidence to provider catalogue vehicle IDs."""

    name: str

    @abstractmethod
    def resolve_catalogue_vehicle(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult: ...

    @abstractmethod
    def list_vehicle_options(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult: ...


class CatalogueProvider(CatalogueVehicleProvider):
    """Product catalogue operations, separate from vehicle identity."""

    name: str

    def resolve_catalogue_vehicle(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult:
        return CatalogueVehicleResult.not_configured(self.name, "catalogue vehicle mapping not implemented")

    def list_vehicle_options(self, vehicle: VehicleCandidate) -> CatalogueVehicleResult:
        return CatalogueVehicleResult.not_configured(self.name, "catalogue vehicle options not implemented")

    @abstractmethod
    def search_by_oe(self, reference: str) -> list[dict]: ...

    @abstractmethod
    def search_products(self, query: str) -> list[dict]: ...


class FitmentProvider(ABC):
    name: str

    @abstractmethod
    def get_products_for_vehicle(self, vehicle: VehicleCandidate) -> list[dict]: ...

    @abstractmethod
    def validate_product(self, vehicle: VehicleCandidate, product_id: str) -> FitmentEvidence: ...


class InventoryProvider(ABC):
    name: str

    @abstractmethod
    def get_stock(self, product_id: str) -> StockRecord | IntegrationResult: ...


class PricingProvider(ABC):
    name: str

    @abstractmethod
    def get_price(self, product_id: str, customer_id: str | None = None) -> PriceRecord | IntegrationResult: ...


class SupplierProvider(ABC):
    name: str

    @abstractmethod
    def get_offers(self, product_id: str) -> list[SupplierOffer] | IntegrationResult: ...


class ERPProvider(InventoryProvider, PricingProvider, ABC):
    """Operational boundary only: never vehicle identity or fitment."""

    @abstractmethod
    def upsert_customer(self, customer: CustomerRecord) -> IntegrationResult: ...

    @abstractmethod
    def create_order(self, order: OrderDraft) -> OrderRecord | IntegrationResult: ...

    @abstractmethod
    def create_invoice(self, order_id: str) -> InvoiceRecord | IntegrationResult: ...
