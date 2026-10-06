from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from app.models import VehicleCandidate


class IntegrationStatus(str, Enum):
    OK = "OK"
    NOT_CONFIGURED = "NOT_CONFIGURED"
    NOT_FOUND = "NOT_FOUND"
    AMBIGUOUS = "AMBIGUOUS"
    ERROR = "ERROR"


@dataclass(frozen=True)
class IntegrationResult:
    provider: str
    status: IntegrationStatus
    reason: str | None = None

    @classmethod
    def not_configured(cls, provider: str, reason: str) -> "IntegrationResult":
        return cls(provider, IntegrationStatus.NOT_CONFIGURED, reason)


@dataclass(frozen=True)
class CatalogueVehicleOption:
    catalogue_vehicle_id: str
    label: str
    ktype: str | None = None
    engine: str | None = None
    engine_code: str | None = None
    power_kw: float | None = None
    fuel: str | None = None
    provider: str | None = None


@dataclass(frozen=True)
class CatalogueVehicleResult:
    provider: str
    status: IntegrationStatus
    options: tuple[CatalogueVehicleOption, ...] = ()
    match_basis: str | None = None
    reason: str | None = None

    @classmethod
    def not_configured(cls, provider: str, reason: str) -> "CatalogueVehicleResult":
        return cls(provider, IntegrationStatus.NOT_CONFIGURED, reason=reason)


@dataclass(frozen=True)
class StockRecord:
    product_id: str
    quantity: int
    warehouse: str | None = None
    observed_at: str | None = None


@dataclass(frozen=True)
class PriceRecord:
    product_id: str
    amount: float
    currency: str = "EUR"
    includes_vat: bool = False
    price_list: str | None = None


@dataclass(frozen=True)
class SupplierOffer:
    supplier_id: str
    product_id: str
    supplier_sku: str
    cost: float | None = None
    stock: int | None = None
    delivery_days: int | None = None
    currency: str = "EUR"


@dataclass(frozen=True)
class CustomerRecord:
    external_id: str
    name: str
    email: str | None = None
    vat_number: str | None = None


@dataclass(frozen=True)
class OrderLine:
    product_id: str
    quantity: int
    unit_price: float


@dataclass(frozen=True)
class OrderDraft:
    external_id: str
    customer_id: str
    lines: tuple[OrderLine, ...]
    currency: str = "EUR"


@dataclass(frozen=True)
class OrderRecord:
    external_id: str
    erp_order_id: str
    status: str


@dataclass(frozen=True)
class InvoiceRecord:
    order_id: str
    invoice_id: str
    document_url: str | None = None


@dataclass(frozen=True)
class VehicleResolutionTrace:
    input_type: str
    input_value: str
    provider: str
    vehicle: VehicleCandidate | None
    catalogue_vehicle: CatalogueVehicleResult | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
