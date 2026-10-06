import unittest

from app.agreement import compare_candidates
from app.fallback import ConfirmationStatus, ManualConfirmationSession, next_manual_step
from app.models import VehicleCandidate


class FallbackTests(unittest.TestCase):
    def test_partial_model_asks_for_engine_and_never_claims_compatibility(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II")
        step = next_manual_step(vehicle, ("1.5 BlueHDi 130", "1.2 PureTech 130"))
        self.assertEqual(step.state, "NEEDS_ENGINE_CONFIRMATION")
        self.assertFalse(step.may_claim_compatibility)
        self.assertEqual(len(step.options), 2)

    def test_manual_engine_confirmation_updates_canonical_vehicle(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II")
        step = next_manual_step(vehicle, ("1.5 BlueHDi 130", "2.0 BlueHDi 180"))
        session = ManualConfirmationSession(vehicle, step)
        confirmed = session.confirm("1.5 BlueHDi 130")
        self.assertEqual(session.status, ConfirmationStatus.CONFIRMED)
        self.assertEqual(confirmed.engine_family, "1.5 BlueHDi 130")

    def test_disagreement_requires_review(self):
        a = VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.5 BlueHDi")
        b = VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.2 PureTech")
        result = compare_candidates([a, b])
        self.assertEqual(result.state, "REVIEW")
        self.assertIn("engine_family", result.disagreements)

    def test_agreement_does_not_fill_missing_fields(self):
        a = VehicleCandidate(make="Peugeot", model="5008")
        b = VehicleCandidate(make="Peugeot", model="5008")
        result = compare_candidates([a, b])
        self.assertEqual(result.state, "AGREE")
        self.assertIn("engine_code", result.missing)
