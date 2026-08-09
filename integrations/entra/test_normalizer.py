import sys
import json
from pathlib import Path
import importlib.util


# ============================================
# Load entra_identity.py
# ============================================

SCRIPT_DIR = Path(__file__).resolve().parent

identity_file = (
    SCRIPT_DIR / "entra_identity.py"
)

identity_spec = (
    importlib.util.spec_from_file_location(
        "entra_identity",
        identity_file
    )
)

identity_module = (
    importlib.util.module_from_spec(
        identity_spec
    )
)

identity_spec.loader.exec_module(
    identity_module
)


# ============================================
# Load normalizer.py
# ============================================

normalizer_file = (
    SCRIPT_DIR / "normalizer.py"
)

normalizer_spec = (
    importlib.util.spec_from_file_location(
        "normalizer",
        normalizer_file
    )
)

normalizer_module = (
    importlib.util.module_from_spec(
        normalizer_spec
    )
)

normalizer_spec.loader.exec_module(
    normalizer_module
)


# ============================================
# Validate arguments
# ============================================

if len(sys.argv) != 2:

    print(
        "Usage:"
    )

    print(
        "python "
        "integrations\\entra\\test_normalizer.py "
        "<user-upn>"
    )

    sys.exit(1)


# ============================================
# Collect real identity
# ============================================

user_upn = sys.argv[1]

identity = (
    identity_module.build_identity_context(
        user_upn
    )
)


# ============================================
# Normalize
# ============================================

normalized = (
    normalizer_module.normalize_identity_context(
        identity
    )
)


# ============================================
# Display
# ============================================

print("\n========================================")
print(" NORMALIZED ENTRA IDENTITY")
print("========================================")

print(
    json.dumps(
        normalized,
        indent=2
    )
)

print("\n========================================")