"""Minimal Microsoft Graph client for read-only identity enrichment.

Provide a short-lived access token via GRAPH_ACCESS_TOKEN when testing.
No credentials are stored in the repository.
"""
from __future__ import annotations
import json
import os
from urllib import request
from urllib.parse import quote


GRAPH_ROOT = "https://graph.microsoft.com/v1.0"


class GraphClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv("GRAPH_ACCESS_TOKEN")
        if not self.token:
            raise ValueError("GRAPH_ACCESS_TOKEN is not configured.")

    def _get(self, path: str) -> dict:
        req = request.Request(
            GRAPH_ROOT + path,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json",
            },
        )
        with request.urlopen(req, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def get_user(self, user_id: str) -> dict:
        fields = "id,displayName,userPrincipalName,department,jobTitle,accountEnabled"
        return self._get(f"/users/{quote(user_id)}?$select={fields}")

    def get_member_of(self, user_id: str) -> dict:
        return self._get(f"/users/{quote(user_id)}/memberOf?$select=id,displayName")

    def get_app_role_assignments(self, user_id: str) -> dict:
        return self._get(f"/users/{quote(user_id)}/appRoleAssignments")

    def get_directory_role_assignments(self, user_id: str) -> dict:
        return self._get(
            "/roleManagement/directory/roleAssignments"
            f"?$filter=principalId%20eq%20'{quote(user_id)}'"
        )
