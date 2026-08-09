def normalize_identity_context(identity):
    """
    Convert the rich Microsoft Graph identity response
    into the simplified identity structure used by
    the security analysis engines.
    """

    return {
        "id": identity.get("id"),

        "display_name": identity.get(
            "display_name"
        ),

        "user_principal_name": identity.get(
            "user_principal_name"
        ),

        "department": identity.get(
            "department"
        ),

        "job_title": identity.get(
            "job_title"
        ),

        "account_enabled": identity.get(
            "account_enabled"
        ),

        "groups": [
            group.get("display_name")
            for group in identity.get(
                "groups",
                []
            )
            if group.get("display_name")
        ],

        "administrative_units": [
            unit.get("display_name")
            for unit in identity.get(
                "administrative_units",
                []
            )
            if unit.get("display_name")
        ],

        "directory_roles": [
            role.get("display_name")
            for role in identity.get(
                "directory_roles",
                []
            )
            if role.get("display_name")
        ],

        "applications": [
            application.get(
                "resource_display_name"
            )
            for application in identity.get(
                "applications",
                []
            )
            if application.get(
                "resource_display_name"
            )
        ]
    }