import unittest

from app.models import EvidenceStatus, IdentityResult, LookupStatus, PrecisionLevel, VehicleCandidate
from app.orchestrator import IdentityOrchestrator, ProviderRateLimitError, ProviderSchemaError, ProviderStep
from providers.base import VehicleIdentityProvider
from providers.mock import MockIdentityProvider


class FailingProvider(VehicleIdentityProvider):
    name = "failing"
    version = "1"
    def identify_by_vin(self, vin): raise TimeoutError()
    def identify_by_registration(self, registration): raise PermissionError()


class ExactProvider(VehicleIdentityProvider):
    name = "exact"
    version = "1"
    calls = 0
    def _result(self):
        self.calls += 1
        v = VehicleCandidate(make="Peugeot", model="5008", generation="II", engine_family="1.5 BlueHDi", engine_code="YHZ", fuel="Diesel", power_hp=130, variant="130", provider_vehicle_ids={"exact": "42"})
        return IdentityResult(self.name, LookupStatus.RESOLVED, [v], EvidenceStatus.PARTIALLY_VERIFIED)
    def identify_by_vin(self, vin): return self._result()
    def identify_by_registration(self, registration): return self._result()


class RateLimitedProvider(FailingProvider):
    name = "rate_limited"
    def identify_by_vin(self, vin): raise ProviderRateLimitError()


class SchemaDriftProvider(FailingProvider):
    name = "schema_drift"
    def identify_by_vin(self, vin): raise ProviderSchemaError()


class ProviderTests(unittest.TestCase):
    def test_mock_provider_is_explicitly_mock_only(self):
        result = MockIdentityProvider().identify_by_vin("VF3MCYHZUPS034433")
        self.assertEqual(result.evidence_status, EvidenceStatus.MOCK_ONLY)

    def test_failure_isolated_and_next_provider_used(self):
        exact = ExactProvider()
        orchestrator = IdentityOrchestrator([ProviderStep(FailingProvider(), PrecisionLevel.MODEL), ProviderStep(exact, PrecisionLevel.ENGINE)])
        result, attempts = orchestrator.identify("vin", "VF3MCYHZUPS034433")
        self.assertEqual(result.provider, "exact")
        self.assertEqual(attempts[0].error_code, "TIMEOUT")

    def test_provider_scoped_cache(self):
        exact = ExactProvider()
        orchestrator = IdentityOrchestrator([ProviderStep(exact, PrecisionLevel.ENGINE)])
        orchestrator.identify("vin", "VF3MCYHZUPS034433")
        orchestrator.identify("vin", "VF3MCYHZUPS034433")
        self.assertEqual(exact.calls, 1)

    def test_circuit_opens_after_threshold(self):
        failing = FailingProvider()
        orchestrator = IdentityOrchestrator([ProviderStep(failing, PrecisionLevel.MODEL)], failure_threshold=1)
        orchestrator.identify("vin", "VF3MCYHZUPS034433")
        _, attempts = orchestrator.identify("vin", "VF3MCYHZUPS034433")
        self.assertEqual(attempts[0].error_code, "CIRCUIT_OPEN")

    def test_rate_limit_isolated(self):
        exact = ExactProvider()
        orchestrator = IdentityOrchestrator([ProviderStep(RateLimitedProvider(), PrecisionLevel.MODEL), ProviderStep(exact, PrecisionLevel.ENGINE)])
        result, attempts = orchestrator.identify("vin", "VF3MCYHZUPS034433")
        self.assertEqual(attempts[0].error_code, "RATE_LIMIT")
        self.assertEqual(result.provider, "exact")

    def test_schema_drift_isolated(self):
        exact = ExactProvider()
        orchestrator = IdentityOrchestrator([ProviderStep(SchemaDriftProvider(), PrecisionLevel.MODEL), ProviderStep(exact, PrecisionLevel.ENGINE)])
        result, attempts = orchestrator.identify("vin", "VF3MCYHZUPS034433")
        self.assertEqual(attempts[0].error_code, "SCHEMA_DRIFT")
        self.assertEqual(result.provider, "exact")

    def test_max_cost_prevents_selection(self):
        class CostlyExact(ExactProvider):
            name = "costly"
            def _result(self):
                result = super()._result()
                result.cost = 2.0
                return result
        result, attempts = IdentityOrchestrator([ProviderStep(CostlyExact(), PrecisionLevel.ENGINE, max_cost=1.0)]).identify("vin", "VF3MCYHZUPS034433")
        self.assertIsNone(result)
        self.assertEqual(len(attempts), 1)


if __name__ == "__main__": unittest.main()
