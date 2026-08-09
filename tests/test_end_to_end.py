import json
import unittest
from pathlib import Path

from engine.policy_engine import evaluate
from engine.access_analysis.access_analyzer import analyze
from engine.risk_analysis.risk_engine import score_identity


ROOT = Path(__file__).parents[1]


class EndToEndTests(unittest.TestCase):
    def test_offline_pipeline(self):
        request = json.loads((ROOT / "data" / "access-request.json").read_text())
        identity = json.loads((ROOT / "data" / "identity-context.json").read_text())

        policy = evaluate(request, identity).to_dict()
        access = analyze(request, identity)
        risk = score_identity(identity, request)

        self.assertIn(policy["decision"], {"APPROVE", "REVIEW", "BLOCK"})
        self.assertIn(policy["risk"], {"LOW", "MEDIUM", "HIGH", "CRITICAL"})
        self.assertIn("already_has_application", access)
        self.assertIn("score", risk)


if __name__ == "__main__":
    unittest.main()
