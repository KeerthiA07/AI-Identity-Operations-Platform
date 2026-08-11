import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


AUDIT_DIR = Path(__file__).resolve().parent / "evidence"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)


def create_request_id():
    return f"REQ-{uuid.uuid4().hex[:12].upper()}"


def write_audit_record(
    user,
    application,
    requested_access,
    risk_level,
    risk_score,
    policy_decision,
    reasons,
    action,
    human_approval_required,
    human_approval=False,
    ai_recommendation=None
):
    record = {
        "request_id": create_request_id(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user": {
            "display_name": user.get("display_name"),
            "user_principal_name": user.get("user_principal_name"),
            "department": user.get("department")
        },
        "application": application,
        "requested_access": requested_access,
        "risk": {
            "level": risk_level,
            "score": risk_score
        },
        "policy_decision": policy_decision,
        "reasons": reasons,
        "ai_recommendation": ai_recommendation or {},
        "human_approval": {
            "required": human_approval_required,
            "approved": human_approval
        },
        "action": action
    }

    filename = (
        f"{record['request_id']}.json"
    )

    output_path = AUDIT_DIR / filename

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(record, file, indent=2)

    return output_path


if __name__ == "__main__":
    sample_user = {
        "display_name": "LAB-USER-FIN01",
        "user_principal_name": "lab-user-fin01@example.com",
        "department": "Finance"
    }

    path = write_audit_record(
        user=sample_user,
        application="LAB-APP-HR",
        requested_access="Standard",
        risk_level="MEDIUM",
        risk_score=40,
        policy_decision="REVIEW",
        reasons=[
            "User department does not match application department.",
            "Application is classified as high sensitivity."
        ],
        action="PERFORM_ACCESS_REVIEW",
        human_approval_required=True,
        human_approval=False,
        ai_recommendation={
            "decision": "REVIEW",
            "risk": "MEDIUM"
        }
    )

    print(f"Audit record written to: {path}")