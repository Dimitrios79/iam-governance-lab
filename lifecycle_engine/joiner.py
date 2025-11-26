"""
Process 'joiners' (new hires) based on data/employees.csv
and assign initial RBAC roles according to policies/rbac_model.json.
"""

from pathlib import Path
import csv
import json
import uuid

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
POLICY_DIR = BASE_DIR / "policies"
SCIM_DIR = BASE_DIR / "scim_simulator"

EMPLOYEES_CSV = DATA_DIR / "employees.csv"
RBAC_MODEL = POLICY_DIR / "rbac_model.json"
USERS_FILE = SCIM_DIR / "users.json"


def load_users():
    if not USERS_FILE.exists():
        return []
    with USERS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def load_rbac_model():
    with RBAC_MODEL.open("r", encoding="utf-8") as f:
        return json.load(f)


def process_joiners():
    users = load_users()
    existing_usernames = {u["userName"] for u in users}
    rbac_model = load_rbac_model()

    with EMPLOYEES_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"].upper() != "NEW":
                continue

            username = row["email"].split("@")[0]
            if username in existing_usernames:
                continue  # already provisioned

            department = row["department"]
            role = rbac_model.get("department_to_role", {}).get(department, "Employee")

            user = {
                "id": str(uuid.uuid4()),
                "userName": username,
                "displayName": row["displayName"],
                "email": row["email"],
                "department": department,
                "active": True,
                "groups": [role],
            }

            print(f"[JOINER] Creating user {user['userName']} with role {role}")
            users.append(user)
            existing_usernames.add(username)

    save_users(users)


if __name__ == "__main__":
    process_joiners()

