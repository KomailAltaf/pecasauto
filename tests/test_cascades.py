import unittest

from app.cascades import registration_cascade, vin_cascade, vin_research_cascade


class CascadeTests(unittest.TestCase):
    def test_plate_trace_continues_past_every_access_blocker(self):
        result, attempts = registration_cascade().identify("registration", "CG-17-GC")
        self.assertIsNone(result)
        self.assertEqual([a.provider for a in attempts], [
            "existing_client_source", "telepecas", "matricula_co_pt", "tecalliance_vrm", "manual_selection"
        ])
        self.assertTrue(all(a.error_code for a in attempts))

    def test_research_only_autofrance_is_not_in_production_cascade(self):
        self.assertNotIn("autofrance_public", [step.provider.name for step in vin_cascade().steps])
        self.assertEqual(vin_research_cascade().steps[0].provider.name, "autofrance_public")
