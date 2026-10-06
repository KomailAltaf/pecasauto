from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from .models import Product


PRODUCTS = [
    dict(brand="BOSCH", name="Filtro de óleo — amostra", sku="PA-FIL-001", manufacturer_reference="SAMPLE-FILTER-001", oe_references=["SAMPLE-OE-FILTER-001"], ean="DEMO-EAN-0001", category="Filtros", image_kind="oil-filter", price=12.49, stock=18, delivery_estimate="ESTIMATIVA DEMO · 1 dia", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Tipo": "Filtro de óleo", "Dados": "DEMO"}),
    dict(brand="MANN-FILTER", name="Filtro de ar — amostra", sku="PA-FIL-002", manufacturer_reference="SAMPLE-FILTER-002", oe_references=["SAMPLE-OE-FILTER-002"], ean="DEMO-EAN-0002", category="Filtros", image_kind="air-filter", price=18.90, stock=7, delivery_estimate="ESTIMATIVA DEMO · 1–2 dias úteis", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Tipo": "Filtro de ar", "Dados": "DEMO"}),
    dict(brand="MAHLE", name="Filtro de combustível — amostra", sku="PA-FIL-003", manufacturer_reference="SAMPLE-FILTER-003", oe_references=["SAMPLE-OE-FILTER-003"], ean="DEMO-EAN-0003", category="Filtros", image_kind="fuel-filter", price=31.75, stock=4, delivery_estimate="ESTIMATIVA DEMO · 1–2 dias úteis", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Tipo": "Filtro de combustível", "Dados": "DEMO"}),
    dict(brand="BREMBO", name="Pastilhas de travão — amostra", sku="PA-BRK-001", manufacturer_reference="SAMPLE-BRAKE-001", oe_references=["SAMPLE-OE-BRAKE-001"], ean="DEMO-EAN-0004", category="Pastilhas de travão", image_kind="brake-pads", price=42.90, stock=12, delivery_estimate="ESTIMATIVA DEMO · 1 dia", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="TRW", name="Jogo de pastilhas — amostra", sku="PA-BRK-002", manufacturer_reference="SAMPLE-BRAKE-002", oe_references=["SAMPLE-OE-BRAKE-002"], ean="DEMO-EAN-0005", category="Pastilhas de travão", image_kind="brake-pads", price=38.60, stock=0, delivery_estimate="ESTIMATIVA DEMO · 3–4 dias úteis", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="ATE", name="Pastilhas Ceramic — amostra", sku="PA-BRK-003", manufacturer_reference="SAMPLE-BRAKE-003", oe_references=["SAMPLE-OE-BRAKE-003"], ean="DEMO-EAN-0006", category="Pastilhas de travão", image_kind="brake-pads", price=56.20, stock=5, delivery_estimate="ESTIMATIVA DEMO · 1–2 dias úteis", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="BREMBO", name="Disco de travão — amostra", sku="PA-DIS-001", manufacturer_reference="SAMPLE-DISC-001", oe_references=["SAMPLE-OE-DISC-001"], ean="DEMO-EAN-0007", category="Discos de travão", image_kind="brake-disc", price=64.90, stock=9, delivery_estimate="ESTIMATIVA DEMO · 1 dia", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="BOSCH", name="Disco ventilado — amostra", sku="PA-DIS-002", manufacturer_reference="SAMPLE-DISC-002", oe_references=["SAMPLE-OE-DISC-002"], ean="DEMO-EAN-0008", category="Discos de travão", image_kind="brake-disc", price=58.40, stock=14, delivery_estimate="ESTIMATIVA DEMO · 1 dia", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="FEBI", name="Disco revestido — amostra", sku="PA-DIS-003", manufacturer_reference="SAMPLE-DISC-003", oe_references=["SAMPLE-OE-DISC-003"], ean="DEMO-EAN-0009", category="Discos de travão", image_kind="brake-disc", price=49.80, stock=3, delivery_estimate="ESTIMATIVA DEMO · 2–3 dias úteis", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Eixo": "Dianteiro", "Dados": "DEMO"}),
    dict(brand="VALEO", name="Filtro de habitáculo — amostra", sku="PA-FIL-004", manufacturer_reference="SAMPLE-FILTER-004", oe_references=["SAMPLE-OE-FILTER-004"], ean="DEMO-EAN-0010", category="Filtros", image_kind="cabin-filter", price=15.30, stock=21, delivery_estimate="ESTIMATIVA DEMO · 1 dia", fitment_state="CONFIRM_COMPATIBILITY", attributes={"Tipo": "Filtro de habitáculo", "Dados": "DEMO"}),
]


def seed_products(db: Session) -> None:
    existing = {row.sku: row for row in db.scalars(select(Product)).all()}
    for item in PRODUCTS:
        row = existing.get(item["sku"])
        if row is None:
            db.add(Product(**item, iva_rate=23.0, demo=True))
            continue
        for field, value in item.items():
            setattr(row, field, value)
    db.commit()
