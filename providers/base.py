from __future__ import annotations

from abc import ABC, abstractmethod

from app.models import IdentityResult, VehicleCandidate
from app.fitment import FitmentEvidence


class VehicleIdentityProvider(ABC):
    name: str
    version: str = "unknown"

    @abstractmethod
    def identify_by_vin(self, vin: str) -> IdentityResult: ...

    @abstractmethod
    def identify_by_registration(self, registration: str) -> IdentityResult: ...


class CatalogueProvider(ABC):
    name: str

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
    def get_stock(self, product_id: str) -> int | None: ...


class PricingProvider(ABC):
    name: str

    @abstractmethod
    def get_price(self, product_id: str) -> float | None: ...

