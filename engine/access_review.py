"""Access review recommendation engine."""
from __future__ import annotations
from typing import Any


def review_identity(identity: dict[str, Any]) -> list[dict[str, Any]]:
    results = []
    department = identity.get("department", "")
    apps = identity.get("applications", [])

    for app in apps:
        expected = app.replace("LAB-APP-", "").title()
        if expected and expected != department:
            results.append({
                "application": app,
                "recommendation": "REVIEW",
                "reason": (
                    f"Application naming indicates '{expected}' access while "
                    f"user department is '{department}'."
                ),
            })
        else:
            results.append({
                "application": app,
                "recommendation": "KEEP",
                "reason": "Application aligns with current department.",
            })

    if identity.get("directory_roles"):
        results.append({
            "entitlement": "DIRECTORY_ROLE",
            "recommendation": "REVIEW",
            "reason": "Privileged directory role requires periodic certification.",
        })

    return results
