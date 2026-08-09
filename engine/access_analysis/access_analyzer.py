"""Access and entitlement analysis."""
from __future__ import annotations
from typing import Any


def analyze(request: dict[str, Any], identity: dict[str, Any]) -> dict[str, Any]:
    requested_app = request["requested_access"]["application"]
    current_apps = set(identity.get("applications", []))
    groups = set(identity.get("groups", []))
    roles = set(identity.get("directory_roles", []))

    return {
        "already_has_application": requested_app in current_apps,
        "group_count": len(groups),
        "role_count": len(roles),
        "privileged": bool(roles),
        "potential_access_accumulation": len(current_apps) >= 3,
        "requested_application": requested_app,
    }
