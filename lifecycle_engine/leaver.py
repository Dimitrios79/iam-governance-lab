"""
Process 'leavers' – deactivate accounts for users whose status is LEAVE.
"""

from pathlib import Path
import csv
import json

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SCIM_DIR = BASE_DIR / "scim_simulator"

EMPLOYEES_CSV = DATA_DIR / "employees.csv"
USERS_FILE = SCIM_DIR / "users.json"


def load_users():
    if not USERS_FILE.exists():
        return []
    with USERS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_users(users):
    with USERS_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)


def process_leavers():
    users = load_users()
    email_to_user = {u["email"]: u for u in users}

    with EMPLOYEES_CSV.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["status"].upper() != "LEAVE":
                continue

            email = row["email"]
            user = email_to_user.get(email)
            if not user:
                continue

            if not user.get("active", True):
                continue

            print(f"[LEAVER] Deactivating {user['userName']} ({email})")
            user["active"] = False
            user["groups"] = []

    save_users(users)


if __name__ == "__main__":
    process_leavers()

