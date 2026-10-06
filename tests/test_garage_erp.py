import unittest

from app.garage import CustomerGarage, SavedVehicle, VehicleVerificationStatus
from app.integrations import IntegrationStatus
from app.models import VehicleCandidate
from app.provider_policy import ProviderPolicy
from providers.partslink24 import Partslink24Boundary, PartslinkRole
from providers.primavera import PrimaveraERPProvider


class GarageAndERPTests(unittest.TestCase):
    def test_customer_confirmed_profile_can_be_reused_without_provider_cache(self):
        candidate = VehicleCandidate(registration="CG-17-GC", make="Peugeot", model="5008", engine_family="1.5 BlueHDi 130")
        profile = SavedVehicle.from_candidate(
            candidate,
            provider="manual",
            verification_status=VehicleVerificationStatus.CUSTOMER_CONFIRMED,
            verification_source="customer_selection",
        )
        garage = CustomerGarage()
        garage.save_profile(profile)
        self.assertEqual(garage.reusable_by_registration("CG-17-GC"), profile)

    def test_provider_verified_profile_requires_verified_storage_rights(self):
        profile = SavedVehicle.from_candidate(
            VehicleCandidate(vin="VF3MCYHZUPS034433", make="Peugeot"),
            provider="commercial",
            verification_status=VehicleVerificationStatus.PROVIDER_VERIFIED,
            verification_source="commercial_api",
        )
        garage = CustomerGarage()
        with self.assertRaises(PermissionError):
            garage.save_profile(profile)
        garage.save_profile(profile, ProviderPolicy("commercial", "CONTRACT", True, True, 3600, True))

    def test_primavera_boundary_is_operational_only_and_not_configured(self):
        provider = PrimaveraERPProvider(env={})
        result = provider.get_stock("product-1")
        self.assertEqual(result.status, IntegrationStatus.NOT_CONFIGURED)
        self.assertFalse(hasattr(provider, "identify_by_vin"))

    def test_partslink_boundary_never_automates_without_rights(self):
        boundary = Partslink24Boundary()
        result = boundary.resolve_catalogue_vehicle(VehicleCandidate(vin="VF3MCYHZUPS034433"))
        self.assertEqual(result.status, IntegrationStatus.NOT_CONFIGURED)
        self.assertNotIn(PartslinkRole.FUTURE_LICENSED_INTEGRATION, boundary.permitted_roles)


if __name__ == "__main__":
    unittest.main()
