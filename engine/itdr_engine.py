"""Identity Threat Detection & Response helper."""
from __future__ import annotations


SEVERITY = {
    "impossible_travel": 30,
    "multiple_failed_signins": 20,
    "unexpected_privileged_activation": 40,
    "suspicious_group_change": 30,
}


def analyze_identity_signals(signals: list[str]) -> dict:
    score = min(sum(SEVERITY.get(signal, 10) for signal in signals), 100)

    if score >= 80:
        level = "CRITICAL"
    elif score >= 50:
        level = "HIGH"
    elif score >= 25:
        level = "MEDIUM"
    else:
        level = "LOW"

    actions = []
    if "unexpected_privileged_activation" in signals:
        actions.append("Review PIM activation and privileged role assignment.")
    if "impossible_travel" in signals:
        actions.append("Review recent sign-in locations and authentication events.")
    if "multiple_failed_signins" in signals:
        actions.append("Review sign-in failures and authentication methods.")
    if "suspicious_group_change" in signals:
        actions.append("Review group membership audit events.")

    if level in {"HIGH", "CRITICAL"}:
        actions.append("Consider session revocation after analyst confirmation.")

    return {
        "score": score,
        "level": level,
        "signals": signals,
        "recommended_investigation": actions,
        "human_approval_required": True,
    }
