import unittest

from app.fitment import CustomerFitmentState, FitmentEvidence, SourceVerdict, evaluate_fitment
from app.bridge import CatalogueBridgeResult, MatchMethod
from app.models import VehicleCandidate


def engine_vehicle():
    return VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.5 BlueHDi", fuel="Diesel", power_hp=130)


def trusted_bridge():
    return CatalogueBridgeResult(MatchMethod.PROVIDER_ID, 1, "ktype-verified", True, True)


class FitmentTests(unittest.TestCase):
    def test_model_only_cannot_be_compatible(self):
        vehicle = VehicleCandidate(make="Peugeot", model="5008", generation="II")
        decision = evaluate_fitment(vehicle, [FitmentEvidence("licensed", SourceVerdict.MATCH, True)])
        self.assertEqual(decision.customer_state, CustomerFitmentState.CONFIRM_COMPATIBILITY)
        self.assertEqual(decision.customer_message_pt, "Confirmar compatibilidade")

    def test_free_vin_match_never_proves_compatibility(self):
        decision = evaluate_fitment(engine_vehicle(), [FitmentEvidence("free_vin", SourceVerdict.MATCH, False)])
        self.assertEqual(decision.customer_state, CustomerFitmentState.CONFIRM_COMPATIBILITY)

    def test_licensed_match_at_engine_precision_is_compatible(self):
        decision = evaluate_fitment(engine_vehicle(), [FitmentEvidence("licensed", SourceVerdict.MATCH, True, True)], trusted_bridge())
        self.assertEqual(decision.customer_state, CustomerFitmentState.COMPATIBLE)

    def test_match_and_no_match_become_conflict(self):
        evidence = [FitmentEvidence("a", SourceVerdict.MATCH, True, True), FitmentEvidence("b", SourceVerdict.NO_MATCH, True, True)]
        decision = evaluate_fitment(engine_vehicle(), evidence)
        self.assertEqual(decision.source_verdict, SourceVerdict.CONFLICT)
        self.assertEqual(decision.customer_state, CustomerFitmentState.CONFIRM_COMPATIBILITY)

    def test_restriction_requires_confirmation(self):
        decision = evaluate_fitment(engine_vehicle(), [FitmentEvidence("licensed", SourceVerdict.MATCH, True, True, restrictions=("front axle only",))], trusted_bridge())
        self.assertEqual(decision.customer_state, CustomerFitmentState.CONFIRM_COMPATIBILITY)

    def test_unlicensed_no_match_cannot_claim_not_compatible(self):
        decision = evaluate_fitment(engine_vehicle(), [FitmentEvidence("research", SourceVerdict.NO_MATCH, False)])
        self.assertEqual(decision.customer_state, CustomerFitmentState.CONFIRM_COMPATIBILITY)


if __name__ == "__main__": unittest.main()
