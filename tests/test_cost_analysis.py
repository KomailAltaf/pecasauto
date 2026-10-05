import unittest

from benchmarks.core import cost_scenarios


class CostAnalysisTests(unittest.TestCase):
    def test_expected_volumes_and_cache_policies_exist(self):
        rows = cost_scenarios()
        self.assertEqual({row["monthly_lookups"] for row in rows}, {1_000, 10_000, 50_000, 100_000})
        self.assertEqual({row["cache_policy"] for row in rows}, {"CACHE_ALLOWED", "CACHE_FORBIDDEN"})

    def test_external_costs_are_not_invented(self):
        for row in cost_scenarios():
            if row["provider"] != "Local VIN structural parser":
                self.assertIsNone(row["estimated_cost"])


if __name__ == "__main__": unittest.main()

