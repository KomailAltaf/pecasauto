import argparse
import unittest

from app.integrations import IntegrationStatus
from app.models import EvidenceStatus, IdentityResult, LookupStatus, PrecisionLevel, VehicleCandidate
from app.settings import PlatformSettings
from app.vehicle_resolution import ResolutionState, resolve_vehicle
from providers.autoways import AutowaysVehicleProvider
from providers.http import HTTPResponse
from providers.matriculapt import MatriculaPtVehicleProvider
from providers.registry import ProviderRegistry
from providers.tecalliance import TecAllianceVehicleProvider, TecDocCatalogueVehicleProvider
from providers.telepecas import TelePecasVehicleProvider
from providers.tips4y import Tips4yVehicleProvider
from tools.test_provider import run


class ConfiguredAdapterTests(unittest.TestCase):
    def test_all_candidate_adapters_return_not_configured_without_credentials(self):
        providers = [
            AutowaysVehicleProvider(env={}),
            Tips4yVehicleProvider(env={}),
            MatriculaPtVehicleProvider(env={}),
            TelePecasVehicleProvider(env={}),
            TecAllianceVehicleProvider(env={}),
        ]
        for provider in providers:
            with self.subTest(provider=provider.name):
                result = provider.identify_by_registration("CG-17-GC")
                self.assertEqual(result.status, LookupStatus.NOT_CONFIGURED)
                self.assertEqual(result.evidence_status, EvidenceStatus.NOT_CONFIGURED)

    def test_autoways_documented_schema_normalizes_ktype_and_engine_code_without_inventing_engine(self):
        provider = AutowaysVehicleProvider(token="test-only", env={})
        response = HTTPResponse(200, b'''{"error":false,"data":{"AWN_immat":"89XL64","AWN_VIN":"SJNFFAJ11U2588958","AWN_marque":"NISSAN","AWN_modele":"QASHQAI II SUV","AWN_k_type":"133682","AWN_puissance_chevaux":"140","AWN_puissance_KW":"103","AWN_code_moteur":"HR13DDT","AWN_energie":"ESSENCE","AWN_nbr_cylindre_energie":"1332","AWN_libelle":"QASHQAI II SUV (J11, J11_)","AWN_TID":"135591"}}''', 12.0, "application/json")
        candidates = provider.parse_response("registration", "89-XL-64", response)
        self.assertEqual(candidates[0].provider_vehicle_ids["ktype"], "133682")
        self.assertEqual(candidates[0].engine_code, "HR13DDT")
        self.assertEqual(candidates[0].precision, PrecisionLevel.MODEL)

    def test_autoways_current_schema_normalizes_engine_platform_and_selector_ids(self):
        provider = AutowaysVehicleProvider(token="test-only", env={})
        response = HTTPResponse(200, b'''{"error":false,"data":{"AWN_marque":"PEUGEOT","AWN_modele":"3008","AWN_code_platform":"MC","AWN_label_moteur":"1.5 BlueHDi 130","AWN_code_moteur":"YHZ_DV5RC","AWN_energie":"GAZOLE","AWN_puissance_KW":"96","AWN_puissance_chevaux":"131","AWN_version":"1.5 BlueHDi 130","AWN_k_type":"130708","AWN_selector_modele_id":"4607","AWN_selector_marque_id":"246","AWN_tecdoc_marque_id":"88"}}''', 12.0, "application/json")
        candidate = provider.parse_response("vin", "VF3MCYHZUPS034433", response)[0]
        self.assertEqual(candidate.generation, "MC")
        self.assertEqual(candidate.engine_family, "1.5 BlueHDi 130")
        self.assertEqual(candidate.engine_code, "YHZ_DV5RC")
        self.assertEqual(candidate.provider_vehicle_ids["ktype"], "130708")
        self.assertEqual(candidate.provider_vehicle_ids["tecdoc_brand_id"], "88")
        self.assertEqual(candidate.provider_vehicle_ids["autoways_selector_model_id"], "4607")
        self.assertEqual(candidate.precision, PrecisionLevel.EXACT_VARIANT)

    def test_matriculapt_vin_route_is_explicitly_unsupported(self):
        provider = MatriculaPtVehicleProvider(username="test-only", env={})
        result = provider.identify_by_vin("VF3MCYHZUPS034433")
        self.assertEqual(result.status, LookupStatus.NO_RESULT)
        self.assertIn("UNSUPPORTED_ROUTE", result.error_code)

    def test_environment_switches_primary_and_fallback_without_business_logic_change(self):
        settings = PlatformSettings.from_env({"VEHICLE_PROVIDER": "telepecas", "FALLBACK_PROVIDER": "tips4y"})
        registry = ProviderRegistry(settings)
        self.assertEqual(registry.primary_vehicle.name, "telepecas")
        self.assertEqual(registry.fallback_vehicle.name, "tips4y")

    def test_cli_output_is_ready_even_when_credential_is_absent(self):
        args = argparse.Namespace(provider="autoways", plate="CG-17-GC", vin=None, catalogue_provider="tecdoc", save_raw=None)
        output, code = run(args)
        self.assertEqual(code, 2)
        self.assertEqual(output["status"], "NOT_CONFIGURED")
        self.assertIn("precision_level", output)


class VehicleResolutionTests(unittest.TestCase):
    def test_client_vin_conflict_is_preserved_without_hardcoding_a_model(self):
        candidate = VehicleCandidate(
            make="Peugeot", model="3008", generation="II", engine_family="1.5 BlueHDi 130",
            fuel="Diesel", power_kw=96, vin="VF3MCYHZUPS034433", provider_vehicle_ids={"ktype": "130708"},
        )
        identity = IdentityResult("autoways", LookupStatus.RESOLVED, [candidate])
        resolution = resolve_vehicle(identity, TecDocCatalogueVehicleProvider())
        self.assertEqual(resolution.state, ResolutionState.CONFLICT)
        self.assertEqual(resolution.question.options, ("Peugeot 3008 II", "Peugeot 5008 II"))

    def test_non_conflicted_ktype_is_ready_for_catalogue_but_not_fitment(self):
        candidate = VehicleCandidate(
            make="Peugeot", model="3008", generation="II", engine_family="1.5 BlueHDi 130",
            fuel="Diesel", power_kw=96, vin="OTHERPTCONTEXTVIN", provider_vehicle_ids={"ktype": "130708"},
        )
        result = resolve_vehicle(IdentityResult("autoways", LookupStatus.RESOLVED, [candidate]), TecDocCatalogueVehicleProvider(), known_conflicts={})
        self.assertEqual(result.state, ResolutionState.CATALOGUE_ID_READY)
        self.assertEqual(result.ktype, "130708")

    def test_missing_engine_requests_one_more_detail(self):
        candidate = VehicleCandidate(make="Peugeot", model="5008", generation="II")
        result = resolve_vehicle(
            IdentityResult("matriculapt", LookupStatus.PARTIAL, [candidate]),
            TecDocCatalogueVehicleProvider(),
            candidate_engines=("1.5 BlueHDi 130", "2.0 BlueHDi 180"),
            known_conflicts={},
        )
        self.assertEqual(result.state, ResolutionState.NEEDS_MANUAL_CONFIRMATION)
        self.assertEqual(result.question.field, "engine_family")


if __name__ == "__main__":
    unittest.main()
