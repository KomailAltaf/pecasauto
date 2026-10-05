import unittest

from app.models import VehicleCandidate
from app.normalization import next_required_discriminator, normalize_pt_registration, normalize_reference, normalize_vin


class NormalizationTests(unittest.TestCase):
    def test_client_eu_vin_checksum_is_non_blocking(self):
        result = normalize_vin("VF3MCYHZUPS034433", region="EU")
        self.assertTrue(result.structurally_valid)
        self.assertFalse(result.checksum_valid)
        self.assertFalse(result.checksum_applicable)
        self.assertIn("CHECKSUM_MISMATCH_NON_BLOCKING_FOR_REGION", result.warnings)

    def test_forbidden_vin_characters(self):
        self.assertFalse(normalize_vin("VF3MCYHZUPI034433").structurally_valid)

    def test_pt_plate_variants_and_normalization(self):
        for raw, expected in [("CG-17-GC", "CG-17-GC"), ("cg17gc", "CG-17-GC"), ("00 00 AA", "00-00-AA"), ("00AA00", "00-AA-00"), ("AA0000", "AA-00-00")]:
            self.assertEqual(normalize_pt_registration(raw), expected)

    def test_invalid_plate_rejected(self):
        with self.assertRaises(ValueError): normalize_pt_registration("ABC-123")

    def test_reference_normalization(self):
        self.assertEqual(normalize_reference("1K1 614-724E"), "1K1614724E")

    def test_partial_vehicle_asks_one_field(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II")
        self.assertEqual(next_required_discriminator(vehicle), "engine_family")


if __name__ == "__main__": unittest.main()

