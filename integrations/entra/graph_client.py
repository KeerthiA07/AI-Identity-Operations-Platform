import os
import requests
import msal
from dotenv import load_dotenv


# ============================================
# Load environment variables
# ============================================

load_dotenv()

TENANT_ID = os.getenv("TENANT_ID")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

GRAPH_URL = "https://graph.microsoft.com/v1.0"


# ============================================
# Validate configuration
# ============================================

if not TENANT_ID:
    raise ValueError("TENANT_ID is missing from .env")

if not CLIENT_ID:
    raise ValueError("CLIENT_ID is missing from .env")

if not CLIENT_SECRET:
    raise ValueError("CLIENT_SECRET is missing from .env")


# ============================================
# Authenticate using Microsoft identity platform
# ============================================

authority = (
    f"https://login.microsoftonline.com/{TENANT_ID}"
)

app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=authority,
    client_credential=CLIENT_SECRET
)


# ============================================
# Request Microsoft Graph token
# ============================================

result = app.acquire_token_for_client(
    scopes=["https://graph.microsoft.com/.default"]
)


if "access_token" not in result:

    error = result.get(
        "error_description",
        "Unknown authentication error"
    )

    raise RuntimeError(
        f"Graph authentication failed: {error}"
    )


access_token = result["access_token"]


# ============================================
# Call Microsoft Graph
# ============================================

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get(
    f"{GRAPH_URL}/users",
    headers=headers,
    params={
        "$select": (
            "id,displayName,userPrincipalName,"
            "department,jobTitle,accountEnabled"
        ),
        "$top": 20
    },
    timeout=30
)


# ============================================
# Handle response
# ============================================

if response.status_code != 200:

    raise RuntimeError(
        f"Graph request failed "
        f"({response.status_code}): "
        f"{response.text}"
    )


data = response.json()


# ============================================
# Display users
# ============================================

print("\n========================================")
print(" MICROSOFT GRAPH — ENTRA USERS")
print("========================================")

for user in data.get("value", []):

    print(
        f"\nUser: {user.get('displayName')}"
    )

    print(
        f"UPN: {user.get('userPrincipalName')}"
    )

    print(
        f"Department: {user.get('department')}"
    )

    print(
        f"Job Title: {user.get('jobTitle')}"
    )

    print(
        f"Enabled: {user.get('accountEnabled')}"
    )

print("\n========================================")