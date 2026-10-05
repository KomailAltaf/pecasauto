from __future__ import annotations

from app.models import EvidenceStatus, IdentityResult, LookupStatus, Provenance, VehicleCandidate
from app.normalization import normalize_pt_registration, normalize_reference, normalize_vin
from providers.base import CatalogueProvider, VehicleIdentityProvider


class MockIdentityProvider(VehicleIdentityProvider):
    """Plumbing-only provider. Its answers are never production evidence."""

    name = "mock_identity"
    version = "1"

    def identify_by_vin(self, vin: str) -> IdentityResult:
        validation = normalize_vin(vin)
        if not validation.structurally_valid:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.MOCK_ONLY)
        candidate = VehicleCandidate(
            make="Peugeot",
            model="5008",
            generation="II",
            model_year=2023,
            vin=validation.normalized,
            field_provenance={"make": Provenance(self.name), "model": Provenance(self.name)},
            raw_payload_ref="fixtures/raw/mock_identity_responses.json",
        )
        return IdentityResult(self.name, LookupStatus.PARTIAL, [candidate], EvidenceStatus.MOCK_ONLY)

    def identify_by_registration(self, registration: str) -> IdentityResult:
        try:
            normalized = normalize_pt_registration(registration)
        except ValueError:
            return IdentityResult(self.name, LookupStatus.NO_RESULT, evidence_status=EvidenceStatus.MOCK_ONLY)
        candidate = VehicleCandidate(make="Peugeot", model="5008", generation="II", registration=normalized)
        return IdentityResult(self.name, LookupStatus.PARTIAL, [candidate], EvidenceStatus.MOCK_ONLY)


class MockCatalogueProvider(CatalogueProvider):
    name = "mock_catalogue"

    def __init__(self, products: list[dict]):
        if any(item.get("data_status") != "MOCK ONLY" for item in products):
            raise ValueError("test catalogue must be labelled MOCK ONLY")
        self.products = products

    def search_by_oe(self, reference: str) -> list[dict]:
        needle = normalize_reference(reference)
        return [item for item in self.products if needle in {normalize_reference(ref) for ref in item.get("oe_references", [])}]

    def search_products(self, query: str) -> list[dict]:
        needle = normalize_reference(query)
        return [item for item in self.products if needle in normalize_reference(" ".join(map(str, item.values())))]

