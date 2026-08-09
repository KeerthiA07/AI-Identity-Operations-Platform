import sys
import json
from pathlib import Path
import importlib.util


# ============================================
# Load entra_identity.py from the same folder
# ============================================

SCRIPT_DIR = Path(__file__).resolve().parent

ENTRA_IDENTITY_FILE = (
    SCRIPT_DIR / "entra_identity.py"
)

spec = importlib.util.spec_from_file_location(
    "entra_identity",
    ENTRA_IDENTITY_FILE
)

entra_identity = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    entra_identity
)

build_identity_context = (
    entra_identity.build_identity_context
)


# ============================================
# Main
# ============================================

def main():

    if len(sys.argv) != 2:

        print(
            "Usage:"
        )

        print(
            "python "
            "integrations\\entra\\run_real_identity.py "
            "<user-upn>"
        )

        sys.exit(1)

    user_upn = sys.argv[1]

    identity_context = (
        build_identity_context(
            user_upn
        )
    )

    print("\n========================================")
    print(" REAL ENTRA IDENTITY CONTEXT")
    print("========================================")

    print(
        json.dumps(
            identity_context,
            indent=2
        )
    )

    print("\n========================================")


if __name__ == "__main__":
    main()