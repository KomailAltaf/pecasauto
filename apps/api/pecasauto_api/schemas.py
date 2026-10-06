from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


SourceType = Literal[
    "REAL_TESTED",
    "DEMO",
    "MOCK",
    "DOCUMENTED_CAPABILITY",
    "WAITING_FOR_ACCESS",
    "NOT_CONFIGURED",
    "RESEARCH_ONLY",
]


class VehicleSearchRequest(BaseModel):
    method: Literal["registration", "vin"]
    value: str


class VehicleCandidateOut(BaseModel):
    id: str
    make: str | None = None
    model: str | None = None
    generation: str | None = None
    year_range: str | None = None
    engine: str | None = None
    engine_code: str | None = None
    power_kw: float | None = None
    fuel: str | None = None
    variant: str | None = None
    provider: str
    external_vehicle_id: str | None = None
    ktype: str | None = None
    ktype_status: Literal["VERIFIED", "UNVERIFIED", "CONFLICT", "NOT_AVAILABLE"] = "NOT_AVAILABLE"
    precision: Literal["BASIC", "MODEL", "ENGINE", "EXACT_VARIANT"] = "BASIC"
    verification_state: str


class TraceStep(BaseModel):
    provider: str
    status: str
    detail: str
    source_type: SourceType
    latency_ms: float | None = None


class VehicleSearchResponse(BaseModel):
    outcome: Literal["EXACT", "MULTIPLE", "MORE_INFORMATION_REQUIRED", "WAITING_FOR_PROVIDER", "NO_RESULT", "CONFLICT"]
    source_type: SourceType
    input: dict[str, str]
    candidates: list[VehicleCandidateOut]
    trace: list[TraceStep]
    raw_provider_result: dict | list | None = None
    message: str
    may_claim_compatibility: bool = False


class SaveVehicleRequest(VehicleCandidateOut):
    nickname: str = "Meu Carro"
    registration: str | None = None
    vin: str | None = None
    match_method: Literal["PROVIDER_ID", "VIN", "ENGINE_CODE", "TEXT_MATCH", "USER_CONFIRMED"] = "USER_CONFIRMED"
    candidate_set: list[VehicleCandidateOut] = Field(default_factory=list)


class SavedVehicleOut(SaveVehicleRequest):
    model_config = ConfigDict(from_attributes=True)
    database_id: int


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    brand: str
    name: str
    sku: str
    manufacturer_reference: str
    oe_references: list[str]
    ean: str
    category: str
    image_kind: str
    price: float
    iva_rate: float
    stock: int
    delivery_estimate: str
    fitment_state: str
    attributes: dict
    demo: bool


class OrderItem(BaseModel):
    product_id: int
    quantity: int = Field(ge=1, le=20)


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=2)
    email: str
    address: str = Field(min_length=5)
    items: list[OrderItem]


class OrderOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: str
    total: float
    source_type: str


class ProviderStatusOut(BaseModel):
    name: str
    role: str
    status: str
    registration: bool
    vin: bool
    ktype: bool
    catalogue: bool
    fitment: bool
    inventory: bool
    approximate_cost: str
    note: str
    evidence_state: Literal["TESTED", "DOCUMENTED CAPABILITY", "WAITING FOR ACCESS", "NOT CONFIGURED", "RESEARCH ONLY", "MANUAL ONLY", "FUTURE"]
    tested_inputs: list[Literal["VIN", "MATRICULA"]] = Field(default_factory=list)
    capability_basis: Literal["ACTUAL TEST", "VENDOR DOCUMENTATION", "RESEARCH", "CONTRACT/ACCOUNT", "PLACEHOLDER"]
