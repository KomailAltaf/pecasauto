import json
import tempfile
import unittest
from pathlib import Path

from benchmarks.core import is_portuguese_market, is_production_score_eligible, load_campaign_inputs, load_ground_truth, provider_summaries
from providers.mock import MockCatalogueProvider


ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTests(unittest.TestCase):
    def test_synthetic_rows_excluded_by_default(self):
        rows = load_ground_truth(ROOT / "fixtures" / "vehicle_ground_truth.csv")
        self.assertNotIn("SYNTHETIC", {row["truth_class"] for row in rows})

    def test_synthetic_rows_can_only_be_loaded_explicitly(self):
        rows = load_ground_truth(ROOT / "fixtures" / "vehicle_ground_truth.csv", include_synthetic=True)
        self.assertIn("SYNTHETIC", {row["truth_class"] for row in rows})

    def test_default_campaign_is_portugal_only(self):
        rows = load_campaign_inputs(ROOT / "fixtures" / "vehicle_ground_truth.csv")
        self.assertTrue(rows)
        self.assertTrue(all(row["country"] == "PT" for row in rows))

    def test_production_metrics_require_verified_pt_market(self):
        rows = load_ground_truth(ROOT / "fixtures" / "vehicle_ground_truth.csv")
        self.assertTrue(all(row["country"] == "PT" for row in rows))
        self.assertTrue(all(is_portuguese_market(row) for row in rows))

    def test_client_expectation_is_not_production_ground_truth(self):
        row = load_campaign_inputs(ROOT / "fixtures" / "vehicle_ground_truth.csv")[0]
        self.assertFalse(is_portuguese_market(row))
        self.assertFalse(is_production_score_eligible(row))

    def test_mock_provider_has_zero_verified_n(self):
        mock = next(item for item in provider_summaries() if item.status == "MOCK ONLY")
        self.assertEqual(mock.verified_n, 0)

    def test_catalogue_is_search_mechanics_only(self):
        data = json.loads((ROOT / "fixtures" / "test_catalogue.json").read_text())
        self.assertEqual(data["data_status"], "MOCK ONLY")
        self.assertIn("SEARCH MECHANICS ONLY", data["purpose"])
        self.assertNotIn("compatible", json.dumps(data).lower())

    def test_mock_oem_search_mechanics(self):
        data = json.loads((ROOT / "fixtures" / "test_catalogue.json").read_text())
        provider = MockCatalogueProvider(data["products"])
        results = provider.search_by_oe("1K1 614-724E")
        self.assertEqual([item["internal_sku"] for item in results], ["DEMO-002"])
        self.assertTrue(all(item["data_status"] == "MOCK ONLY" for item in results))


if __name__ == "__main__": unittest.main()
