import os
import sys
import requests
import msal
from dotenv import load_dotenv

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GRAPH_URL = "https://graph.microsoft.com/v1.0"


# ============================================
# Authentication
# ============================================

def get_access_token():

    authority = (
        f"https://login.microsoftonline.com/{TENANT_ID}"
    )

    app = msal.ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )

    result = app.acquire_token_for_client(
        scopes=["https://graph.microsoft.com/.default"]
    )

    if "access_token" not in result:

        raise RuntimeError(
            f"Authentication failed: "
            f"{result.get('error_description', result)}"
        )

    return result["access_token"]


# ============================================
# Generic Microsoft Graph GET
# ============================================

def graph_get(path, token, params=None):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(
        f"{GRAPH_URL}{path}",
        headers=headers,
        params=params,
        timeout=30
    )

    if response.status_code != 200:

        raise RuntimeError(
            f"Graph returned {response.status_code}: "
            f"{response.text}"
        )

    return response.json()


# ============================================
# Get User
# ============================================

def get_user(user_identifier, token):

    return graph_get(
        f"/users/{user_identifier}",
        token,
        {
            "$select": (
                "id,displayName,userPrincipalName,"
                "department,jobTitle,accountEnabled"
            )
        }
    )


# ============================================
# Get Groups
# ============================================

def get_groups(user_id, token):

    data = graph_get(
        f"/users/{user_id}/memberOf",
        token,
        {
            "$select": "id"
        }
    )

    groups = []

    for item in data.get("value", []):

        object_type = item.get("@odata.type")
        object_id = item.get("id")

        if object_type == "#microsoft.graph.group":

            group = graph_get(
                f"/groups/{object_id}",
                token,
                {
                    "$select": (
                        "id,displayName,description,"
                        "securityEnabled,mailEnabled"
                    )
                }
            )

            groups.append({
                "id": group.get("id"),
                "display_name": group.get("displayName"),
                "description": group.get("description"),
                "security_enabled": group.get(
                    "securityEnabled"
                ),
                "mail_enabled": group.get(
                    "mailEnabled"
                )
            })

    return groups


# ============================================
# Get Administrative Units
# ============================================

def get_administrative_units(user_id, token):

    data = graph_get(
        f"/users/{user_id}/memberOf",
        token,
        {
            "$select": "id"
        }
    )

    administrative_units = []

    for item in data.get("value", []):

        object_type = item.get("@odata.type")
        object_id = item.get("id")

        if (
            object_type
            == "#microsoft.graph.administrativeUnit"
        ):

            administrative_unit = graph_get(
                f"/directory/administrativeUnits/{object_id}",
                token,
                {
                    "$select": (
                        "id,displayName,description"
                    )
                }
            )

            administrative_units.append({
                "id": administrative_unit.get("id"),
                "display_name": administrative_unit.get(
                    "displayName"
                ),
                "description": administrative_unit.get(
                    "description"
                )
            })

    return administrative_units


# ============================================
# Get Directory Roles
# ============================================

def get_directory_roles(user_id, token):

    data = graph_get(
        f"/users/{user_id}/memberOf",
        token,
        {
            "$select": "id"
        }
    )

    roles = []

    for item in data.get("value", []):

        object_type = item.get("@odata.type")
        object_id = item.get("id")

        if (
            object_type
            == "#microsoft.graph.directoryRole"
        ):

            role = graph_get(
                f"/directoryRoles/{object_id}",
                token,
                {
                    "$select": "id,displayName"
                }
            )

            roles.append({
                "id": role.get("id"),
                "display_name": role.get(
                    "displayName"
                )
            })

    return roles


# ============================================
# Get Application Assignments
# ============================================

def get_application_assignments(user_id, token):

    data = graph_get(
        f"/users/{user_id}/appRoleAssignments",
        token,
        {
            "$select": (
                "id,appRoleId,resourceDisplayName"
            )
        }
    )

    applications = []

    for item in data.get("value", []):

        applications.append({
            "id": item.get("id"),
            "app_role_id": item.get("appRoleId"),
            "resource_display_name": item.get(
                "resourceDisplayName"
            )
        })

    return applications


# ============================================
# Build Complete Identity Context
# ============================================

def build_identity_context(user_identifier):

    token = get_access_token()

    # User
    user = get_user(
        user_identifier,
        token
    )

    user_id = user["id"]

    # Groups
    groups = get_groups(
        user_id,
        token
    )

    # Administrative Units
    administrative_units = get_administrative_units(
        user_id,
        token
    )

    # Directory Roles
    roles = get_directory_roles(
        user_id,
        token
    )

    # Applications
    applications = get_application_assignments(
        user_id,
        token
    )

    return {
        "id": user_id,

        "display_name": user.get(
            "displayName"
        ),

        "user_principal_name": user.get(
            "userPrincipalName"
        ),

        "department": user.get(
            "department"
        ),

        "job_title": user.get(
            "jobTitle"
        ),

        "account_enabled": user.get(
            "accountEnabled"
        ),

        "groups": groups,

        "administrative_units": (
            administrative_units
        ),

        "directory_roles": roles,

        "applications": applications
    }


# ============================================
# Main
# ============================================

if __name__ == "__main__":

    if len(sys.argv) != 2:

        print(
            "Usage: python integrations\\entra_identity.py "
            "<actual-user-upn>"
        )

        sys.exit(1)

    identity = build_identity_context(
        sys.argv[1]
    )

    print("\n========================================")
    print(" REAL ENTRA IDENTITY CONTEXT")
    print("========================================")

    print(
        f"Display Name : "
        f"{identity['display_name']}"
    )

    print(
        f"UPN          : "
        f"{identity['user_principal_name']}"
    )

    print(
        f"Department   : "
        f"{identity['department']}"
    )

    print(
        f"Job Title    : "
        f"{identity['job_title']}"
    )

    print(
        f"Enabled      : "
        f"{identity['account_enabled']}"
    )

    # ----------------------------
    # Groups
    # ----------------------------

    print("\nGroups:")

    if identity["groups"]:

        for group in identity["groups"]:

            print(
                f" - {group['display_name']}"
            )

    else:

        print(" - None")

    # ----------------------------
    # Administrative Units
    # ----------------------------

    print("\nAdministrative Units:")

    if identity["administrative_units"]:

        for unit in identity[
            "administrative_units"
        ]:

            print(
                f" - {unit['display_name']}"
            )

    else:

        print(" - None")

    # ----------------------------
    # Directory Roles
    # ----------------------------

    print("\nDirectory Roles:")

    if identity["directory_roles"]:

        for role in identity[
            "directory_roles"
        ]:

            print(
                f" - {role['display_name']}"
            )

    else:

        print(" - None")

    # ----------------------------
    # Applications
    # ----------------------------

    print("\nApplications:")

    if identity["applications"]:

        for application in identity[
            "applications"
        ]:

            print(
                f" - "
                f"{application['resource_display_name']}"
            )

    else:

        print(" - None")

    print("\n========================================")