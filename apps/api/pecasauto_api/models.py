from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    brand: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(180))
    sku: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    manufacturer_reference: Mapped[str] = mapped_column(String(80), index=True)
    oe_references: Mapped[list[str]] = mapped_column(JSON, default=list)
    ean: Mapped[str] = mapped_column(String(32), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    image_kind: Mapped[str] = mapped_column(String(40), default="part")
    price: Mapped[float] = mapped_column(Float)
    iva_rate: Mapped[float] = mapped_column(Float, default=23.0)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    delivery_estimate: Mapped[str] = mapped_column(String(80), default="ESTIMATIVA DEMO · por confirmar")
    fitment_state: Mapped[str] = mapped_column(String(40), default="UNKNOWN")
    attributes: Mapped[dict] = mapped_column(JSON, default=dict)
    demo: Mapped[bool] = mapped_column(Boolean, default=True)


class SavedVehicle(Base):
    __tablename__ = "saved_vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str] = mapped_column(String(80), index=True, default="demo-user")
    nickname: Mapped[str] = mapped_column(String(80), default="Meu Carro")
    registration: Mapped[str | None] = mapped_column(String(16), nullable=True)
    vin: Mapped[str | None] = mapped_column(String(17), nullable=True)
    make: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(80))
    generation: Mapped[str | None] = mapped_column(String(80), nullable=True)
    year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    engine: Mapped[str | None] = mapped_column(String(120), nullable=True)
    engine_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    power_kw: Mapped[float | None] = mapped_column(Float, nullable=True)
    fuel: Mapped[str | None] = mapped_column(String(40), nullable=True)
    ktype: Mapped[str | None] = mapped_column(String(40), nullable=True)
    provider: Mapped[str] = mapped_column(String(80), default="manual")
    external_vehicle_id: Mapped[str | None] = mapped_column(String(120), nullable=True)
    verification_status: Mapped[str] = mapped_column(String(40), default="USER_CONFIRMED")
    verification_source: Mapped[str] = mapped_column(String(80), default="customer")
    match_method: Mapped[str] = mapped_column(String(40), default="USER_CONFIRMED")
    candidate_set: Mapped[list[dict]] = mapped_column(JSON, default=list)
    verified_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    status: Mapped[str] = mapped_column(String(40), default="DEMO_CONFIRMED")
    customer_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160))
    address: Mapped[str] = mapped_column(Text)
    items: Mapped[list[dict]] = mapped_column(JSON)
    subtotal: Mapped[float] = mapped_column(Float)
    shipping: Mapped[float] = mapped_column(Float)
    total: Mapped[float] = mapped_column(Float)
    source_type: Mapped[str] = mapped_column(String(20), default="DEMO")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
