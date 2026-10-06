from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import Settings
from .auth import Principal, require_admin, require_customer
from .database import Base, SessionLocal, engine, get_db
from .models import Order, Product, SavedVehicle
from .providers_status import provider_statuses
from .schemas import OrderCreate, OrderOut, ProductOut, SaveVehicleRequest, SavedVehicleOut, VehicleSearchRequest, VehicleSearchResponse
from .seed import seed_products
from .vehicle_service import MANUAL_VEHICLES, VehicleIdentificationService


settings = Settings.from_env()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed_products(db)
    yield


app = FastAPI(title="PeçasAuto API", version="0.1.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[settings.web_origin, "http://127.0.0.1:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "demo_mode": settings.demo_mode, "data_boundary": "REAL_TESTED / DEMO / DOCUMENTED_CAPABILITY / WAITING_FOR_ACCESS / NOT_CONFIGURED / RESEARCH_ONLY / MOCK"}


@app.post("/api/vehicles/search", response_model=VehicleSearchResponse)
def search_vehicle(payload: VehicleSearchRequest) -> VehicleSearchResponse:
    try:
        return VehicleIdentificationService(settings).search(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/api/vehicles/demo/conflict", response_model=VehicleSearchResponse)
def demo_vehicle_conflict() -> VehicleSearchResponse:
    if not settings.demo_mode:
        raise HTTPException(status_code=404, detail="Demo mode is not enabled")
    return VehicleIdentificationService(settings).demo_conflict()


@app.get("/api/vehicles/manual")
def manual_vehicle_data() -> dict:
    return {"source_type": "DEMO", "label": "DEMO VEHICLE DATA", "vehicles": MANUAL_VEHICLES}


@app.get("/api/garage", response_model=list[SavedVehicleOut])
def garage(principal: Principal = Depends(require_customer), db: Session = Depends(get_db)) -> list[dict]:
    rows = db.scalars(select(SavedVehicle).where(SavedVehicle.user_id == principal.username).order_by(SavedVehicle.id.desc())).all()
    return [_saved_vehicle_payload(row) for row in rows]


@app.post("/api/garage", response_model=SavedVehicleOut)
def save_vehicle(payload: SaveVehicleRequest, principal: Principal = Depends(require_customer), db: Session = Depends(get_db)) -> dict:
    identity_filters = []
    if payload.vin:
        identity_filters.append(SavedVehicle.vin == payload.vin)
    if payload.registration:
        identity_filters.append(SavedVehicle.registration == payload.registration)
    existing = None
    for identity_filter in identity_filters:
        existing = db.scalar(select(SavedVehicle).where(SavedVehicle.user_id == principal.username, identity_filter))
        if existing:
            break
    if not existing:
        existing = db.scalar(
            select(SavedVehicle).where(
                SavedVehicle.user_id == principal.username,
                SavedVehicle.make == (payload.make or "Unknown"),
                SavedVehicle.model == (payload.model or "Unknown"),
                SavedVehicle.generation == payload.generation,
                SavedVehicle.year == _first_year(payload.year_range),
                SavedVehicle.engine == payload.engine,
                SavedVehicle.engine_code == payload.engine_code,
                SavedVehicle.power_kw == payload.power_kw,
                SavedVehicle.fuel == payload.fuel,
            )
        )
    if not existing:
        # Vehicles without a plate/VIN (manual or canned selections) are deduplicated on their described identity.
        existing = db.scalar(select(SavedVehicle).where(
            SavedVehicle.user_id == principal.username,
            SavedVehicle.make == (payload.make or "Unknown"), SavedVehicle.model == (payload.model or "Unknown"),
            SavedVehicle.generation.is_(payload.generation) if payload.generation is None else SavedVehicle.generation == payload.generation,
            SavedVehicle.engine.is_(payload.engine) if payload.engine is None else SavedVehicle.engine == payload.engine,
            SavedVehicle.engine_code.is_(payload.engine_code) if payload.engine_code is None else SavedVehicle.engine_code == payload.engine_code,
            SavedVehicle.year.is_(_first_year(payload.year_range)) if _first_year(payload.year_range) is None else SavedVehicle.year == _first_year(payload.year_range),
            SavedVehicle.vin.is_(None) if not payload.vin else SavedVehicle.vin == payload.vin,
            SavedVehicle.registration.is_(None) if not payload.registration else SavedVehicle.registration == payload.registration,
        ))
    if existing:
        return _saved_vehicle_payload(existing)
    row = SavedVehicle(
        user_id=principal.username,
        nickname=payload.nickname, registration=payload.registration, vin=payload.vin,
        make=payload.make or "Unknown", model=payload.model or "Unknown", generation=payload.generation,
        year=_first_year(payload.year_range), engine=payload.engine, engine_code=payload.engine_code,
        power_kw=payload.power_kw, fuel=payload.fuel, ktype=payload.ktype, provider=payload.provider,
        external_vehicle_id=payload.external_vehicle_id, verification_status="USER_CONFIRMED",
        verification_source=payload.provider, match_method=payload.match_method,
        candidate_set=[item.model_dump() for item in payload.candidate_set],
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return _saved_vehicle_payload(row, candidate_id=payload.id, year_range=payload.year_range, precision=payload.precision, ktype_status=payload.ktype_status)


@app.delete("/api/garage/{vehicle_id}", status_code=204)
def remove_vehicle(vehicle_id: int, principal: Principal = Depends(require_customer), db: Session = Depends(get_db)) -> None:
    row = db.get(SavedVehicle, vehicle_id)
    if not row or row.user_id != principal.username:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    db.delete(row)
    db.commit()


@app.get("/api/products", response_model=list[ProductOut])
def products(
    q: str | None = None,
    category: str | None = None,
    brand: list[str] = Query(default=[]),
    in_stock: bool = False,
    db: Session = Depends(get_db),
) -> list[Product]:
    stmt = select(Product)
    if category:
        stmt = stmt.where(Product.category == category)
    if brand:
        stmt = stmt.where(Product.brand.in_(brand))
    if in_stock:
        stmt = stmt.where(Product.stock > 0)
    rows = list(db.scalars(stmt.order_by(Product.brand, Product.price)).all())
    if q:
        needle = _compact_reference(q)
        rows = [row for row in rows if needle in _compact_reference(" ".join([row.name, row.sku, row.manufacturer_reference, row.ean, *row.oe_references]))]
    return rows


@app.get("/api/products/{product_id}", response_model=ProductOut)
def product(product_id: int, db: Session = Depends(get_db)) -> Product:
    row = db.get(Product, product_id)
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return row


@app.get("/api/search/oem", response_model=list[ProductOut])
def oem_search(reference: str, db: Session = Depends(get_db)) -> list[Product]:
    compact = reference.replace(" ", "").replace("-", "")
    rows = db.scalars(select(Product)).all()
    return [row for row in rows if compact.lower() in {row.sku.replace("-", "").lower(), row.manufacturer_reference.replace("-", "").lower(), row.ean.lower(), *(item.replace(" ", "").replace("-", "").lower() for item in row.oe_references)}]


@app.post("/api/orders", response_model=OrderOut)
def create_order(payload: OrderCreate, _: Principal = Depends(require_customer), db: Session = Depends(get_db)) -> Order:
    if not payload.items:
        raise HTTPException(status_code=422, detail="Cart is empty")
    product_ids = {item.product_id for item in payload.items}
    products_by_id = {item.id: item for item in db.scalars(select(Product).where(Product.id.in_(product_ids))).all()}
    if set(products_by_id) != product_ids:
        raise HTTPException(status_code=422, detail="One or more products do not exist")
    order_items = [
        {"product_id": item.product_id, "quantity": item.quantity, "unit_price": products_by_id[item.product_id].price}
        for item in payload.items
    ]
    subtotal = round(sum(products_by_id[item.product_id].price * item.quantity for item in payload.items), 2)
    shipping = 4.90 if subtotal < 75 else 0.0
    order = Order(customer_name=payload.customer_name, email=payload.email, address=payload.address, items=order_items, subtotal=subtotal, shipping=shipping, total=round(subtotal + shipping, 2), source_type="DEMO")
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@app.get("/api/admin/dashboard")
def admin_dashboard(_: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return {
        "source_type": "DEMO",
        "products": db.scalar(select(func.count(Product.id))) or 0,
        "orders": db.scalar(select(func.count(Order.id))) or 0,
        "vehicles": db.scalar(select(func.count(SavedVehicle.id))) or 0,
        "provider_summary": {status: sum(1 for item in provider_statuses() if item.status == status) for status in {item.status for item in provider_statuses()}},
    }


@app.get("/api/admin/orders")
def admin_orders(_: Principal = Depends(require_admin), db: Session = Depends(get_db)) -> list[dict]:
    return [{"id": row.id, "customer": row.customer_name, "status": row.status, "total": row.total, "source_type": row.source_type} for row in db.scalars(select(Order).order_by(Order.id.desc())).all()]


@app.get("/api/providers")
def providers(_: Principal = Depends(require_admin)) -> dict:
    return {"source_type": "MIXED_EVIDENCE", "providers": [item.model_dump() for item in provider_statuses()]}


def _first_year(value: str | None) -> int | None:
    if not value:
        return None
    try:
        return int(value[:4])
    except ValueError:
        return None


def _compact_reference(value: str) -> str:
    return "".join(character for character in value.casefold() if character.isalnum())


def _saved_vehicle_payload(row: SavedVehicle, *, candidate_id: str | None = None, year_range: str | None = None, precision: str = "ENGINE", ktype_status: str = "UNVERIFIED") -> dict:
    return {
        "database_id": row.id, "id": candidate_id or f"saved-{row.id}", "nickname": row.nickname,
        "registration": row.registration, "vin": row.vin, "make": row.make, "model": row.model,
        "generation": row.generation, "year_range": year_range or (str(row.year) if row.year else None),
        "engine": row.engine, "engine_code": row.engine_code, "power_kw": row.power_kw, "fuel": row.fuel,
        "variant": None, "provider": row.provider, "external_vehicle_id": row.external_vehicle_id,
        "ktype": row.ktype, "ktype_status": ktype_status, "precision": precision,
        "verification_state": row.verification_status, "match_method": row.match_method,
        "candidate_set": row.candidate_set or [],
    }
