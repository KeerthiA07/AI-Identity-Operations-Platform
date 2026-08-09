import unittest

from engine.jml_engine import evaluate_joiner, evaluate_mover, evaluate_leaver
from engine.itdr_engine import analyze_identity_signals


class ScenarioTests(unittest.TestCase):

    def test_joiner(self):
        event = {
            "event": {"department": "Finance"},
            "requested_access": {"application": "LAB-APP-FINANCE"},
            "manager_approved": True,
        }
        result = evaluate_joiner(event)
        self.assertEqual(result["state"], "READY_FOR_APPROVAL")

    def test_mover(self):
        event = {"event": {"old_department": "Finance", "new_department": "HR"}}
        result = evaluate_mover(event)
        self.assertEqual(result["action"], "RECONCILE_ENTITLEMENTS")

    def test_leaver_requires_confirmation(self):
        event = {"event": {"termination_confirmed": False}}
        result = evaluate_leaver(event)
        self.assertEqual(result["state"], "BLOCKED")

    def test_itdr_high_risk(self):
        result = analyze_identity_signals(
            ["impossible_travel", "unexpected_privileged_activation"]
        )
        self.assertEqual(result["level"], "HIGH")


if __name__ == "__main__":
    unittest.main()
