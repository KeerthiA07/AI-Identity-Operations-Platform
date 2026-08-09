import unittest

from engine.policy_engine import evaluate


BASE_REQUEST = {
    "request_id": "REQ-TEST",
    "user": {"id": "U1", "department": "Finance", "job_title": "Analyst"},
    "requested_access": {"application": "LAB-APP-FINANCE", "access_level": "Standard"},
    "manager_approved": True,
}


class PolicyEngineTests(unittest.TestCase):

    def test_valid_finance_request(self):
        result = evaluate(BASE_REQUEST)
        self.assertEqual(result.decision, "APPROVE")
        self.assertEqual(result.risk, "LOW")

    def test_department_mismatch_requires_review(self):
        request = {**BASE_REQUEST, "user": {**BASE_REQUEST["user"], "department": "HR"}}
        result = evaluate(request)
        self.assertEqual(result.decision, "REVIEW")
        self.assertEqual(result.risk, "MEDIUM")

    def test_missing_manager_approval(self):
        request = {**BASE_REQUEST, "manager_approved": False}
        result = evaluate(request)
        self.assertEqual(result.decision, "REVIEW")
        self.assertIn("Manager approval is missing.", result.reasons)

    def test_unknown_application_fails_closed(self):
        request = {**BASE_REQUEST, "requested_access": {"application": "UNKNOWN", "access_level": "Standard"}}
        result = evaluate(request)
        self.assertEqual(result.decision, "REVIEW")
        self.assertEqual(result.risk, "HIGH")

    def test_privileged_request_is_blocked(self):
        request = {**BASE_REQUEST, "requested_access": {"application": "LAB-APP-FINANCE", "access_level": "Privileged"}}
        result = evaluate(request)
        self.assertEqual(result.decision, "BLOCK")


if __name__ == "__main__":
    unittest.main()
