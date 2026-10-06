from __future__ import annotations

from collections.abc import Callable

from app.settings import PlatformSettings
from providers.autoways import AutowaysVehicleProvider
from providers.base import CatalogueVehicleProvider, ERPProvider, FitmentProvider, SupplierProvider, VehicleIdentityProvider
from providers.matriculapt import MatriculaPtVehicleProvider
from providers.partslink24 import Partslink24Boundary
from providers.placeholders import NotConfiguredSupplierProvider, TecDocFitmentProvider
from providers.primavera import PrimaveraERPProvider
from providers.tecalliance import TecAllianceVehicleProvider, TecDocCatalogueVehicleProvider
from providers.telepecas import TelePecasVehicleProvider
from providers.tips4y import Tips4yVehicleProvider
from providers.vpic import VpicProvider


VEHICLE_FACTORIES: dict[str, Callable[[], VehicleIdentityProvider]] = {
    "autoways": AutowaysVehicleProvider,
    "tips4y": Tips4yVehicleProvider,
    "matriculapt": MatriculaPtVehicleProvider,
    "telepecas": TelePecasVehicleProvider,
    "tecalliance": TecAllianceVehicleProvider,
    "vpic": VpicProvider,
}


def vehicle_provider(name: str) -> VehicleIdentityProvider:
    try:
        return VEHICLE_FACTORIES[name.lower()]()
    except KeyError as exc:
        raise ValueError(f"unknown vehicle provider: {name}; choose {', '.join(sorted(VEHICLE_FACTORIES))}") from exc


def catalogue_vehicle_provider(name: str) -> CatalogueVehicleProvider:
    providers: dict[str, CatalogueVehicleProvider] = {
        "tecdoc": TecDocCatalogueVehicleProvider(),
        "partslink24": Partslink24Boundary(),
    }
    try:
        return providers[name.lower()]
    except KeyError as exc:
        raise ValueError(f"unknown catalogue vehicle provider: {name}") from exc


def fitment_provider(name: str) -> FitmentProvider:
    if name.lower() == "tecdoc":
        return TecDocFitmentProvider()
    raise ValueError(f"unknown fitment provider: {name}")


def erp_provider(name: str) -> ERPProvider:
    if name.lower() == "primavera":
        return PrimaveraERPProvider()
    raise ValueError(f"unknown ERP provider: {name}")


def supplier_provider(name: str) -> SupplierProvider:
    if name.lower() == "none":
        return NotConfiguredSupplierProvider()
    raise ValueError(f"unknown supplier provider: {name}")


class ProviderRegistry:
    def __init__(self, settings: PlatformSettings | None = None):
        self.settings = settings or PlatformSettings.from_env()

    @property
    def primary_vehicle(self) -> VehicleIdentityProvider:
        return vehicle_provider(self.settings.vehicle_provider)

    @property
    def fallback_vehicle(self) -> VehicleIdentityProvider:
        return vehicle_provider(self.settings.fallback_provider)

    @property
    def catalogue_vehicle(self) -> CatalogueVehicleProvider:
        return catalogue_vehicle_provider(self.settings.catalogue_vehicle_provider)

    @property
    def fitment(self) -> FitmentProvider:
        return fitment_provider(self.settings.fitment_provider)

    @property
    def erp(self) -> ERPProvider:
        return erp_provider(self.settings.erp_provider)

    @property
    def supplier(self) -> SupplierProvider:
        return supplier_provider(self.settings.supplier_provider)
