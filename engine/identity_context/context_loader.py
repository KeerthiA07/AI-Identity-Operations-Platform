"""Identity context providers.

The project can run offline with a fixture, then switch to Microsoft Graph
without changing the policy engine.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any


def load_fixture(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_graph_user(user: dict[str, Any], groups=None, roles=None, apps=None) -> dict[str, Any]:
    return {
        "id": user.get("id"),
        "display_name": user.get("displayName"),
        "user_principal_name": user.get("userPrincipalName"),
        "department": user.get("department"),
        "job_title": user.get("jobTitle"),
        "account_enabled": user.get("accountEnabled"),
        "groups": groups or [],
        "directory_roles": roles or [],
        "applications": apps or [],
    }
