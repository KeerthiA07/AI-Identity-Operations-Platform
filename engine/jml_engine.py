"""Joiner-Mover-Leaver decision helpers."""
from __future__ import annotations
from typing import Any


def evaluate_joiner(event: dict[str, Any]) -> dict[str, Any]:
    approved = bool(event.get("manager_approved", False))
    department = event.get("event", {}).get("department")
    application = event.get("requested_access", {}).get("application")

    if not approved:
        return {"state": "REVIEW", "action": "WAIT_FOR_MANAGER_APPROVAL"}

    return {
        "state": "READY_FOR_APPROVAL",
        "action": "PROVISION_BASELINE_ACCESS",
        "department": department,
        "application": application,
        "human_approval_required": True,
    }


def evaluate_mover(event: dict[str, Any]) -> dict[str, Any]:
    details = event.get("event", {})
    old_department = details.get("old_department")
    new_department = details.get("new_department")

    if old_department == new_department:
        return {"state": "NO_CHANGE", "action": "NO_ACTION"}

    return {
        "state": "REVIEW",
        "action": "RECONCILE_ENTITLEMENTS",
        "remove_access_for": old_department,
        "add_access_for": new_department,
        "human_approval_required": True,
    }


def evaluate_leaver(event: dict[str, Any]) -> dict[str, Any]:
    confirmed = bool(event.get("event", {}).get("termination_confirmed", False))

    if not confirmed:
        return {"state": "BLOCKED", "action": "REQUIRE_TERMINATION_CONFIRMATION"}

    return {
        "state": "READY_FOR_APPROVAL",
        "action": "DISABLE_AND_REVOKE_SESSIONS",
        "human_approval_required": True,
    }
