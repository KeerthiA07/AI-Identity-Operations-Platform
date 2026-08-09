"""Run the end-to-end offline identity decision workflow."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from engine.policy_engine import evaluate
from engine.identity_context.context_loader import load_fixture
from engine.access_analysis.access_analyzer import analyze as analyze_access
from engine.risk_analysis.risk_engine import score_identity
from ai.ai_analyzer import analyze as analyze_ai


ROOT = Path(__file__).parent
REQUEST = ROOT / "data" / "access-request.json"
IDENTITY = ROOT / "data" / "identity-context.json"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--request", default=str(REQUEST))
    parser.add_argument("--identity", default=str(IDENTITY))
    parser.add_argument("--output", default=str(ROOT / "reports" / "latest-decision.json"))
    args = parser.parse_args()

    request = load_fixture(args.request)
    identity = load_fixture(args.identity)

    policy = evaluate(request, identity).to_dict()
    access = analyze_access(request, identity)
    risk = score_identity(identity, request)
    ai = analyze_ai(request, identity, policy, risk)

    result = {
        "request": request,
        "identity_context": identity,
        "access_analysis": access,
        "risk_analysis": risk,
        "policy_decision": policy,
        "ai_analysis": ai,
        "execution": {
            "status": "PENDING_HUMAN_APPROVAL",
            "identity_change_executed": False
        }
    }

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(json.dumps(result, indent=2))
    print(f"\nReport written to: {args.output}")


if __name__ == "__main__":
    main()
