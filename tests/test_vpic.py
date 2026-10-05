import json
import unittest
from pathlib import Path
from unittest.mock import patch

from app.models import LookupStatus, PrecisionLevel
from providers.autofrance import AutofranceProvider, candidate_from_autofrance


ROOT = Path(__file__).resolve().parents[1]


class VpicEvidenceTests(unittest.TestCase):
    def test_live_pt_client_payload_is_basic_only(self):
        payload = json.loads((ROOT / "reports/raw_evidence/vpic_public_VF3MCYHZUPS034433.json").read_text())
        row = payload["Results"][0]
        self.assertEqual(row["Make"], "PEUGEOT")
        self.assertEqual(row["Model"], "")
        self.assertEqual(row["EngineModel"], "")
        self.assertIn("8", row["ErrorCode"].split(","))

    def test_autofrance_real_payload_reaches_engine_and_preserves_ktype(self):
        payload = json.loads((ROOT / "reports/raw_evidence/autofrance_VF3MCYHZUPS034433.json").read_text())
        candidate = candidate_from_autofrance(payload)
        self.assertEqual(candidate.precision, PrecisionLevel.ENGINE)
        self.assertEqual(candidate.provider_vehicle_ids["autofrance_ktype"], "130708")
        self.assertEqual(candidate.model, "3008 SUV (MC_, MR_, MJ_, M4_)")
        self.assertEqual(candidate.generation, "MC_, MR_, MJ_, M4_")
        self.assertIsNone(candidate.model_year)
        self.assertIsNone(candidate.country_of_registration)

    def test_autofrance_adapter_is_research_only_even_at_engine_level(self):
        raw = (ROOT / "reports/raw_evidence/autofrance_VF3MCYHZUPS034433.json").read_bytes()

        class FakeResponse:
            def __enter__(self): return self
            def __exit__(self, *_): return False
            def read(self): return raw

        with patch("providers.autofrance.urllib.request.urlopen", return_value=FakeResponse()):
            result = AutofranceProvider().identify_by_vin("VF3MCYHZUPS034433")
        self.assertEqual(result.status, LookupStatus.PARTIAL)
        self.assertEqual(result.best_precision, PrecisionLevel.ENGINE)
        self.assertEqual(result.error_code, "RESEARCH_ONLY_NO_EXISTENCE_CHECK")
