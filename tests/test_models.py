import unittest

from app.models import PrecisionLevel, VehicleCandidate


class PrecisionTests(unittest.TestCase):
    def test_missing_fields_stay_null_and_basic(self):
        vehicle = VehicleCandidate(make="Peugeot")
        self.assertIsNone(vehicle.engine_code)
        self.assertEqual(vehicle.precision, PrecisionLevel.BASIC)

    def test_model_ceiling_without_engine(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II", model_year=2023)
        self.assertEqual(vehicle.precision, PrecisionLevel.MODEL)

    def test_engine_requires_evidence_fields(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.5 BlueHDi", fuel="Diesel", power_hp=130)
        self.assertEqual(vehicle.precision, PrecisionLevel.ENGINE)

    def test_exact_requires_code_variant_and_provider_id(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.5 BlueHDi", fuel="Diesel", power_hp=130, engine_code="YHZ", variant="130", provider_vehicle_ids={"licensed": "123"})
        self.assertEqual(vehicle.precision, PrecisionLevel.EXACT_VARIANT)


if __name__ == "__main__": unittest.main()

