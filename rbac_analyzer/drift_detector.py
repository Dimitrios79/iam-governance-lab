"""
Compare expected RBAC model vs actual access in data/access_matrix.csv
to detect entitlement drift.
"""

from pathlib import Path
import csv
import json
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
POLICY_DIR = BASE_DIR / "policies"

ACCESS_MATRIX = DATA_DIR / "access_matrix.csv"
RBAC_MODEL = POLICY_DIR / "rbac_model.json"


def load_rbac_model():
    with RBAC_MODEL.open("r", encoding="utf-8") as f:
        return json.load(f)


def main():
    rbac_model = load_rbac_model()
    role_permissions = rbac_model.get("role_permissions", {})
    expected_by_role = {r: set(p) for r, p in role_permissions.items()}

    # access_matrix.csv columns: user_id,role,permission
    actual_by_role = defaultdict(set)

    with ACCESS_MATRIX.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            role = row["role"]
            perm = row["permission"]
            actual_by_role[role].add(perm)

    print("=== Entitlement Drift Detection ===\n")

    for role, actual_perms in actual_by_role.items():
        expected_perms = expected_by_role.get(role, set())
        extra = actual_perms - expected_perms
        missing = expected_perms - actual_perms

        print(f"Role: {role}")
        print(f"  Expected: {', '.join(sorted(expected_perms)) or 'None'}")
        print(f"  Actual:   {', '.join(sorted(actual_perms)) or 'None'}")

        if extra:
            print(f"  ⚠ Extra entitlements (drift): {', '.join(sorted(extra))}")
        if missing:
            print(f"  ⚠ Missing entitlements: {', '.join(sorted(missing))}")
        if not extra and not missing:
            print("  ✓ No entitlement drift detected.")

        print()

    print("Drift detection complete.")


if __name__ == "__main__":
    main()

