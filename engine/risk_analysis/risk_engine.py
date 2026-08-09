"""Identity risk scoring independent of the policy decision."""
from __future__ import annotations
from typing import Any


def score_identity(identity: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    score = 0
    signals = []

    if not identity.get("account_enabled", True):
        score += 30
        signals.append("Account is disabled.")

    if identity.get("directory_roles"):
        score += 30
        signals.append("User has directory role assignments.")

    if len(identity.get("applications", [])) >= 5:
        score += 20
        signals.append("User has a high number of application entitlements.")

    if len(identity.get("groups", [])) >= 8:
        score += 10
        signals.append("User has a high number of group memberships.")

    if request["requested_access"].get("access_level", "").lower() in {"admin", "privileged", "elevated"}:
        score += 40
        signals.append("Elevated access was requested.")

    level = "LOW" if score < 25 else "MEDIUM" if score < 50 else "HIGH" if score < 80 else "CRITICAL"
    return {"score": min(score, 100), "level": level, "signals": signals}
