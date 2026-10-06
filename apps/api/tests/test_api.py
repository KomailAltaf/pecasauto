from __future__ import annotations

import os

os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DEMO_MODE"] = "true"
os.environ["CUSTOMER_USERNAME"] = "demo-customer"
os.environ["CUSTOMER_PASSWORD"] = "customer-secret"
os.environ["ADMIN_USERNAME"] = "demo-admin"
os.environ["ADMIN_PASSWORD"] = "admin-secret"

from fastapi.testclient import TestClient

from apps.api.pecasauto_api.config import Settings
from apps.api.pecasauto_api.main import app
from apps.api.pecasauto_api.vehicle_service import VehicleIdentificationService
from app.models import EvidenceStatus, IdentityResult, LookupStatus, VehicleCandidate


CUSTOMER = ("demo-customer", "customer-secret")
ADMIN = ("demo-admin", "admin-secret")


def test_plate_without_provider_never_returns_canned_client_vehicle():
    with TestClient(app) as client:
        response = client.post("/api/vehicles/search", json={"method": "registration", "value": "cg 17 gc"})
        assert response.status_code == 200
        data = response.json()
        assert data["outcome"] == "WAITING_FOR_PROVIDER"
        assert data["source_type"] == "WAITING_FOR_ACCESS"
        assert data["candidates"] == []
        assert "WAITING_FOR_PROVIDER" in data["message"]


def test_demo_conflict_is_separate_and_unmistakably_canned():
    with TestClient(app) as client:
        data = client.get("/api/vehicles/demo/conflict").json()
        assert data["source_type"] == "DEMO"
        assert data["outcome"] == "MULTIPLE"
        assert "DEMO CANNED RESULT" in data["message"]
        assert {item["precision"] for item in data["candidates"]} == {"ENGINE"}
        assert all(item["external_vehicle_id"] is None for item in data["candidates"])
        assert all(item["ktype"] is None for item in data["candidates"])


def test_demo_mode_defaults_false(monkeypatch):
    monkeypatch.delenv("DEMO_MODE", raising=False)
    assert Settings.from_env().demo_mode is False


def test_manual_data_is_explicit_demo():
    with TestClient(app) as client:
        data = client.get("/api/vehicles/manual").json()
        assert data["source_type"] == "DEMO"
        assert "Peugeot" in data["vehicles"]


def test_vehicle_save_is_authenticated_deduplicated_and_preserves_year():
    payload = {"id":"manual-1","nickname":"Meu Carro","vin":"DEMO0000000000001","make":"Peugeot","model":"5008","generation":"II","year_range":"2023","engine":"1.5 BlueHDi 130","power_kw":96,"fuel":"Diesel","provider":"manual_demo","precision":"ENGINE","ktype_status":"NOT_AVAILABLE","verification_state":"USER_CONFIRMED","match_method":"USER_CONFIRMED","candidate_set":[]}
    with TestClient(app) as client:
        assert client.post("/api/garage", json=payload).status_code == 401
        saved = client.post("/api/garage", json=payload, auth=CUSTOMER)
        assert saved.status_code == 200
        assert saved.json()["year_range"] == "2023"
        duplicate = client.post("/api/garage", json=payload, auth=CUSTOMER).json()
        assert duplicate["database_id"] == saved.json()["database_id"]
        vehicles = client.get("/api/garage", auth=CUSTOMER).json()
        assert len([item for item in vehicles if item["vin"] == payload["vin"]]) == 1
        assert client.delete(f"/api/garage/{saved.json()['database_id']}", auth=CUSTOMER).status_code == 204


def test_vehicle_save_deduplicates_manual_candidate_without_vin_or_plate():
    payload = {"id":"manual-no-id","nickname":"Meu Carro","make":"Volkswagen","model":"Golf","generation":"VII","year_range":"2019","engine":"1.6 TDI 110","power_kw":81,"fuel":"Diesel","provider":"manual_demo","precision":"ENGINE","ktype_status":"NOT_AVAILABLE","verification_state":"USER_CONFIRMED","match_method":"USER_CONFIRMED","candidate_set":[]}
    with TestClient(app) as client:
        first = client.post("/api/garage", json=payload, auth=CUSTOMER).json()
        second = client.post("/api/garage", json=payload, auth=CUSTOMER).json()
        assert second["database_id"] == first["database_id"]
        assert client.delete(f"/api/garage/{first['database_id']}", auth=CUSTOMER).status_code == 204


def test_vehicle_without_plate_or_vin_is_deduplicated_on_described_identity():
    with TestClient(app) as client:
        candidate = client.get("/api/vehicles/demo/conflict").json()["candidates"][0]
        payload = {**candidate, "nickname": "dedupe-regression", "match_method": "USER_CONFIRMED", "candidate_set": [candidate]}
        first = client.post("/api/garage", json=payload, auth=CUSTOMER).json()
        second = client.post("/api/garage", json=payload, auth=CUSTOMER).json()
        assert first["database_id"] == second["database_id"]
        # a different engine is a different vehicle
        other = client.get("/api/vehicles/demo/conflict").json()["candidates"][1]
        third = client.post("/api/garage", json={**other, "nickname": "dedupe-regression", "match_method": "USER_CONFIRMED", "candidate_set": [other]}, auth=CUSTOMER).json()
        assert third["database_id"] != first["database_id"]
        for row in (first, third):
            client.delete(f"/api/garage/{row['database_id']}", auth=CUSTOMER)


def test_demo_catalogue_uses_synthetic_refs_and_no_positive_fitment():
    with TestClient(app) as client:
        products = client.get("/api/search/oem", params={"reference":"SAMPLE-BRAKE-001"}).json()
        assert products
        assert all(item["demo"] for item in products)
        assert all(item["fitment_state"] == "CONFIRM_COMPATIBILITY" for item in products)
        listing = client.get("/api/products", params={"q":"1K1614724E"}).json()
        assert listing == []


def test_order_price_is_server_side_and_endpoint_is_authenticated():
    with TestClient(app) as client:
        product = client.get("/api/products/1").json()
        payload = {"customer_name":"Komail Test","email":"test@example.com","address":"Rua de Teste 1, Lisboa","items":[{"product_id":1,"quantity":2,"price":0.01}]}
        assert client.post("/api/orders", json=payload).status_code == 401
        response = client.post("/api/orders", json=payload, auth=CUSTOMER)
        assert response.status_code == 200
        expected_subtotal = round(product["price"] * 2, 2)
        expected_shipping = 4.90 if expected_subtotal < 75 else 0
        assert response.json()["total"] == round(expected_subtotal + expected_shipping, 2)
        assert client.get("/api/products/9999").status_code == 404


def test_provider_status_is_authenticated_and_separates_documentation_from_tests():
    with TestClient(app) as client:
        assert client.get("/api/providers").status_code == 401
        rows = client.get("/api/providers", auth=ADMIN).json()["providers"]
        autoways = next(row for row in rows if row["name"] == "Auto Ways")
        assert autoways["tested_inputs"] == []
        assert autoways["capability_basis"] == "VENDOR DOCUMENTATION"
        assert "VIN testado" not in autoways["note"]
        telepecas = next(row for row in rows if row["name"] == "TelePeças")
        assert telepecas["approximate_cost"] == "UNKNOWN"
        assert any(row["name"].startswith("Autofrance") and row["evidence_state"] == "RESEARCH ONLY" for row in rows)


def test_admin_requires_admin_role():
    with TestClient(app) as client:
        assert client.get("/api/admin/dashboard", auth=CUSTOMER).status_code == 401
        assert client.get("/api/admin/dashboard", auth=ADMIN).status_code == 200


def test_one_provider_with_multiple_variants_is_not_a_provider_conflict():
    result = IdentityResult(
        provider="single-provider",
        status=LookupStatus.AMBIGUOUS,
        candidates=[
            VehicleCandidate(make="Peugeot", model="5008", engine_code="DV5"),
            VehicleCandidate(make="Peugeot", model="5008", engine_code="DW10"),
        ],
    )
    assert VehicleIdentificationService._provider_disagreements([result]) == []


def test_two_providers_with_disjoint_results_are_a_provider_conflict():
    first = IdentityResult(
        provider="provider-a",
        status=LookupStatus.RESOLVED,
        candidates=[VehicleCandidate(make="Peugeot", model="5008", engine_code="DV5")],
    )
    second = IdentityResult(
        provider="provider-b",
        status=LookupStatus.RESOLVED,
        candidates=[VehicleCandidate(make="Renault", model="Clio", engine_code="H4D")],
    )
    assert VehicleIdentificationService._provider_disagreements([first, second]) == ["make", "model", "engine_code"]


def test_unvalidated_provider_cannot_claim_exact_variant_precision():
    candidate = VehicleCandidate(
        make="Peugeot",
        model="5008",
        generation="II",
        model_year=2023,
        engine_family="1.5 BlueHDi 130",
        engine_code="DV5RC",
        fuel="Diesel",
        power_kw=96,
        variant="GT",
        provider_vehicle_ids={"provider_id": "external-1", "ktype": "12345"},
    )
    output = VehicleIdentificationService._candidate_from_domain(candidate, "provider", validated=False)
    assert output.precision == "ENGINE"
    assert output.verification_state == "NEEDS_SECOND_SOURCE_OR_USER_CONFIRMATION"
