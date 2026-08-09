"""Deterministic IAM policy engine.

Security boundary: AI recommendations are advisory. This module is the
authoritative policy gate before any identity-changing action.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any


APPLICATION_POLICIES = {
    "LAB-APP-FINANCE": {"department": "Finance", "sensitivity": "medium"},
    "LAB-APP-HR": {"department": "HR", "sensitivity": "high"},
    "LAB-APP-IT": {"department": "IT", "sensitivity": "medium"},
    "LAB-APP-SECURITY": {"department": "Security", "sensitivity": "high"},
}

PRIVILEGED_ROLES = {
    "Global Administrator",
    "Privileged Role Administrator",
    "User Administrator",
}


@dataclass
class PolicyDecision:
    decision: str
    risk: str
    risk_score: int
    reasons: list[str]
    recommended_action: str
    requires_human_approval: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate(request: dict[str, Any], identity: dict[str, Any] | None = None) -> PolicyDecision:
    """Evaluate an access request against deterministic IAM controls."""
    identity = identity or {}
    user = request["user"]
    access = request["requested_access"]

    department = user.get("department", "")
    application = access.get("application", "")
    access_level = access.get("access_level", "Standard")
    manager_approved = bool(request.get("manager_approved", False))

    reasons: list[str] = []
    score = 0

    # Fail closed for malformed/unknown applications.
    app_policy = APPLICATION_POLICIES.get(application)
    if not app_policy:
        return PolicyDecision(
            "REVIEW", "HIGH", 70,
            ["Application is not registered in the identity policy."],
            "PERFORM_APPLICATION_REVIEW",
        )

    # Approval gate.
    if not manager_approved:
        score += 25
        reasons.append("Manager approval is missing.")

    # Business entitlement alignment.
    if department != app_policy["department"]:
        score += 30
        reasons.append(
            f"User department '{department}' does not match "
            f"application department '{app_policy['department']}'."
        )

    # Sensitive application.
    if app_policy["sensitivity"] == "high":
        score += 10
        reasons.append("Application is classified as high sensitivity.")

    # Privileged existing access.
    existing_roles = set(identity.get("directory_roles", []))
    privileged = sorted(existing_roles.intersection(PRIVILEGED_ROLES))
    if privileged:
        score += 35
        reasons.append(
            "User already holds privileged directory role(s): "
            + ", ".join(privileged)
            + "."
        )

    # Excessive access signal.
    existing_apps = set(identity.get("applications", []))
    if application in existing_apps:
        score += 15
        reasons.append("User already has the requested application access.")

    # Explicitly disallow elevated access through this simple workflow.
    if access_level.lower() in {"admin", "privileged", "elevated"}:
        score += 50
        reasons.append("Elevated access cannot be automatically granted.")

    # Decision logic: fail closed.
    if access_level.lower() in {"admin", "privileged", "elevated"}:
        decision = "BLOCK"
        action = "ESCALATE_PRIVILEGED_ACCESS"
    elif score >= 70:
        decision = "BLOCK"
        action = "BLOCK_AND_ESCALATE"
    elif score >= 25:
        decision = "REVIEW"
        action = "PERFORM_ACCESS_REVIEW"
    else:
        decision = "APPROVE"
        action = "GRANT_APPLICATION_ACCESS"

    risk = "LOW" if score < 25 else "MEDIUM" if score < 50 else "HIGH" if score < 80 else "CRITICAL"

    if not reasons:
        reasons = [
            "User department matches the application policy.",
            "Manager approval is present.",
            "No elevated access was requested.",
        ]

    return PolicyDecision(
        decision=decision,
        risk=risk,
        risk_score=min(score, 100),
        reasons=reasons,
        recommended_action=action,
    )


def evaluate_file(request: dict[str, Any], identity: dict[str, Any] | None = None) -> dict[str, Any]:
    return evaluate(request, identity).to_dict()
