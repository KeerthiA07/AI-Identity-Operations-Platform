"""Run one of the portfolio scenarios."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

from engine.policy_engine import evaluate
from engine.jml_engine import evaluate_joiner, evaluate_mover, evaluate_leaver
from engine.itdr_engine import analyze_identity_signals
from engine.access_review import review_identity


ROOT = Path(__file__).parent
SCENARIO_DIR = ROOT / "scenarios"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "scenario",
        choices=["joiner", "mover", "leaver", "excessive_access", "suspicious_signin"]
    )
    args = parser.parse_args()

    path = SCENARIO_DIR / args.scenario / "request.json"
    data = json.loads(path.read_text(encoding="utf-8"))

    if args.scenario == "joiner":
        result = evaluate_joiner(data)
    elif args.scenario == "mover":
        result = evaluate_mover(data)
    elif args.scenario == "leaver":
        result = evaluate_leaver(data)
    elif args.scenario == "suspicious_signin":
        result = analyze_identity_signals(data.get("signals", []))
    else:
        identity = dict(data["identity"])
        identity.setdefault("department", data["user"].get("department"))
        identity.setdefault("job_title", data["user"].get("job_title"))
        request = {
            "request_id": data["request_id"],
            "user": data["user"],
            "requested_access": data["requested_access"],
            "manager_approved": data["manager_approved"],
        }
        result = {
            "policy": evaluate(request, identity).to_dict(),
            "access_review": review_identity(identity),
        }

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
