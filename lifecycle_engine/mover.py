"""
Process 'movers' – users whose department has changed.
Update their department and main RBAC role.
"""

from pathlib import Path
import csv
import json

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


def process_movers():
    users = load_users()
    rbac_model = load_rbac_model()
    email_to_user = {u["email"]: u for u in users}

    with EMPLOYEES_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"].upper() != "MOVE":
                continue

            email = row["email"]
            if email not in email_to_user:
                continue

            user = email_to_user[email]
            old_department = user.get("department")
            new_department = row["department"]

            if old_department == new_department:
                continue

            new_role = rbac_model.get("department_to_role", {}).get(new_department, "Employee")

            print(
                f"[MOVER] {user['userName']} moving from "
                f"{old_department} -> {new_department}, role -> {new_role}"
            )

            user["department"] = new_department
            user["groups"] = [new_role]

    save_users(users)


if __name__ == "__main__":
    process_movers()

