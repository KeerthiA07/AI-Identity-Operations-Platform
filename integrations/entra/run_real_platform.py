import sys
import json
from pathlib import Path
import importlib.util


# ============================================
# Project root
# ============================================

ROOT = Path(__file__).resolve().parents[2]


# ============================================
# Load Entra identity collector
# ============================================

SCRIPT_DIR = Path(__file__).resolve().parent

identity_file = SCRIPT_DIR / "entra_identity.py"

identity_spec = importlib.util.spec_from_file_location(
    "entra_identity",
    identity_file
)

identity_module = importlib.util.module_from_spec(
    identity_spec
)

identity_spec.loader.exec_module(
    identity_module
)


# ============================================
# Load normalizer
# ============================================

normalizer_file = SCRIPT_DIR / "normalizer.py"

normalizer_spec = importlib.util.spec_from_file_location(
    "normalizer",
    normalizer_file
)

normalizer_module = importlib.util.module_from_spec(
    normalizer_spec
)

normalizer_spec.loader.exec_module(
    normalizer_module
)


# ============================================
# Import existing security engines
# ============================================

sys.path.insert(
    0,
    str(ROOT)
)

from engine.policy_engine import evaluate
from engine.access_analysis.access_analyzer import analyze
from engine.risk_analysis.risk_engine import score_identity
from ai.ai_analyzer import analyze as analyze_ai


# ============================================
# Main
# ============================================

def main():

    if len(sys.argv) != 3:

        print(
            "Usage:"
        )

        print(
            "python "
            "integrations\\entra\\run_real_platform.py "
            "<user-upn>"
        )

        sys.exit(1)


    user_upn = sys.argv[1]
    requested_application = sys.argv[2]


    # ========================================
    # 1. Get real identity from Entra
    # ========================================

    print("\n[1/5] Collecting identity from Microsoft Entra...")

    raw_identity = (
        identity_module.build_identity_context(
            user_upn
        )
    )


    # ========================================
    # 2. Normalize Graph response
    # ========================================

    print("[2/5] Normalizing identity context...")

    identity = (
        normalizer_module.normalize_identity_context(
            raw_identity
        )
    )


    # ========================================
    # 3. Build access request
    # ========================================

    print("[3/5] Building access request...")

    request = {
        "request_id": "REAL-ENTRA-001",

        "user": {
            "id": identity["id"],
            "department": identity["department"],
            "job_title": identity["job_title"]
        },

        "requested_access": {
           "application": requested_application,
            "access_level": "Standard"
        },

        "request_reason": (
            "Finance user requires access to "
            "perform finance reporting activities."
        ),

        "manager_approved": True
    }


    # ========================================
    # 4. Run existing security engines
    # ========================================

    print("[4/5] Running access, risk and policy analysis...")

    access_analysis = analyze(
        request,
        identity
    )

    risk_analysis = score_identity(
        identity,
        request
    )

    policy_decision = evaluate(
        request,
        identity
    ).to_dict()


    # ========================================
    # 5. AI analysis
    # ========================================

    print("[5/5] Running AI security analysis...")

    ai_analysis = analyze_ai(
        request,
        identity,
        policy_decision,
        risk_analysis
    )


    # ========================================
    # Final result
    # ========================================

    result = {

        "request": request,

        "identity_context": identity,

        "access_analysis": access_analysis,

        "risk_analysis": risk_analysis,

        "policy_decision": policy_decision,

        "ai_analysis": ai_analysis,

        "execution": {
            "status": "PENDING_HUMAN_APPROVAL",
            "identity_change_executed": False
        }
    }


    # ========================================
    # Save report
    # ========================================

    report_path = (
        ROOT
        / "reports"
        / "real-entra-decision.json"
    )

    report_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    report_path.write_text(
        json.dumps(
            result,
            indent=2
        ),
        encoding="utf-8"
    )


    # ========================================
    # Display decision
    # ========================================

    print("\n")
    print("========================================")
    print(" REAL ENTRA IDENTITY SECURITY DECISION")
    print("========================================")

    print(
        f"User       : "
        f"{identity['display_name']}"
    )

    print(
        f"Department : "
        f"{identity['department']}"
    )

    print(
        f"Application: "
        f"{request['requested_access']['application']}"
    )

    print(
        f"Decision   : "
        f"{policy_decision['decision']}"
    )

    print(
        f"Risk       : "
        f"{policy_decision['risk']}"
    )

    print(
        f"Risk Score : "
        f"{policy_decision['risk_score']}"
    )

    print(
        f"Action     : "
        f"{policy_decision['recommended_action']}"
    )

    print(
        f"Approval   : "
        f"{policy_decision['requires_human_approval']}"
    )

    print("\nReasons:")

    for reason in policy_decision["reasons"]:

        print(
            f" - {reason}"
        )

    print("\n========================================")

    print(
        f"Report written to: {report_path}"
    )


if __name__ == "__main__":
    main()