import unittest

from app.bridge import CatalogueBridgeResult, MatchMethod
from app.garage import CustomerGarage
from app.models import VehicleCandidate
from providers.vpic import candidate_from_vpic_row


class BridgeTests(unittest.TestCase):
    def test_text_match_never_claims_compatible(self):
        result = CatalogueBridgeResult(MatchMethod.TEXT_MATCH, 1, "ktype-1", licensed_fitment_match=True)
        self.assertFalse(result.may_claim_compatible)

    def test_provider_id_still_requires_single_candidate_and_licensed_fitment(self):
        self.assertTrue(CatalogueBridgeResult(MatchMethod.PROVIDER_ID, 1, "ktype-1", True, True).may_claim_compatible)
        self.assertFalse(CatalogueBridgeResult(MatchMethod.PROVIDER_ID, 2, "ktype-1", True, True).may_claim_compatible)

    def test_engine_code_or_unvalidated_ktype_never_claims_compatible(self):
        self.assertFalse(CatalogueBridgeResult(MatchMethod.ENGINE_CODE, 1, "ktype-1", True, True).may_claim_compatible)
        self.assertFalse(CatalogueBridgeResult(MatchMethod.PROVIDER_ID, 1, "ktype-1", True, False).may_claim_compatible)

    def test_customer_garage_requires_confirmation(self):
        garage = CustomerGarage()
        with self.assertRaises(ValueError):
            garage.save("mine", VehicleCandidate(make="Peugeot"), confirmed=False)

    def test_vpic_eu_model_year_not_promoted(self):
        candidate = candidate_from_vpic_row({"Make":"PEUGEOT", "Model":"", "ModelYear":"2023"}, "VF3MCYHZUPS034433")
        self.assertEqual(candidate.make, "PEUGEOT")
        self.assertIsNone(candidate.model_year)
        self.assertIsNone(candidate.country_of_registration)
