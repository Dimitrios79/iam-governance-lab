"""
Analyze roles and entitlements based on entitlements.json
and print a summary of high-risk roles.
"""

from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parents[1]
RBAC_ANALYZER_DIR = BASE_DIR / "rbac_analyzer"
ENTITLEMENTS_FILE = RBAC_ANALYZER_DIR / "entitlements.json"


def main():
    with ENTITLEMENTS_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    roles = data.get("roles", {})
    high_risk = set(data.get("high_risk_permissions", []))

    print("=== RBAC Role Analysis ===\n")
    for role_name, details in roles.items():
        perms = set(details.get("permissions", []))
        risky = perms.intersection(high_risk)

        print(f"Role: {role_name}")
        print(f"  Apps: {', '.join(details.get('apps', [])) or 'None'}")
        print(f"  Permissions: {', '.join(perms) or 'None'}")

        if risky:
            print(f"  ⚠ High-risk permissions: {', '.join(risky)}")
        else:
            print("  ✓ No high-risk permissions detected")

        print()

    print("Analysis complete.")


if __name__ == "__main__":
    main()

