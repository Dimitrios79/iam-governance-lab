from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from pathlib import Path
import json
import uuid

BASE_DIR = Path(__file__).resolve().parent
USERS_FILE = BASE_DIR / "users.json"
GROUPS_FILE = BASE_DIR / "groups.json"

app = FastAPI(title="SCIM Simulator", version="0.1.0")


class User(BaseModel):
    id: str
    userName: str
    displayName: str
    email: str
    department: Optional[str] = None
    active: bool = True
    groups: List[str] = []


class Group(BaseModel):
    id: str
    displayName: str
    members: List[str] = []


def load_json(path: Path, default):
    if not path.exists():
        return default
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data):
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


@app.get("/Users", response_model=List[User])
def list_users():
    data = load_json(USERS_FILE, [])
    return data


@app.post("/Users", response_model=User)
def create_user(user: User):
    users = load_json(USERS_FILE, [])
    if any(u["userName"] == user.userName for u in users):
        raise HTTPException(status_code=400, detail="userName already exists")

    users.append(user.dict())
    save_json(USERS_FILE, users)
    return user


@app.patch("/Users/{user_id}", response_model=User)
def update_user(user_id: str, update: dict):
    users = load_json(USERS_FILE, [])
    for u in users:
        if u["id"] == user_id:
            u.update(update)
            save_json(USERS_FILE, users)
            return u
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/Users/{user_id}")
def delete_user(user_id: str):
    users = load_json(USERS_FILE, [])
    found = False
    for u in users:
        if u["id"] == user_id:
            u["active"] = False
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="User not found")
    save_json(USERS_FILE, users)
    return {"status": "deactivated"}


@app.get("/Groups", response_model=List[Group])
def list_groups():
    data = load_json(GROUPS_FILE, [])
    return data


@app.post("/Groups", response_model=Group)
def create_group(group: Group):
    groups = load_json(GROUPS_FILE, [])
    if any(g["displayName"] == group.displayName for g in groups):
        raise HTTPException(status_code=400, detail="Group already exists")
    groups.append(group.dict())
    save_json(GROUPS_FILE, groups)
    return group


@app.post("/Groups/{group_id}/members/{user_id}")
def add_member_to_group(group_id: str, user_id: str):
    groups = load_json(GROUPS_FILE, [])
    users = load_json(USERS_FILE, [])

    if not any(u["id"] == user_id for u in users):
        raise HTTPException(status_code=404, detail="User not found")

    for g in groups:
        if g["id"] == group_id:
            if user_id not in g["members"]:
                g["members"].append(user_id)
                save_json(GROUPS_FILE, groups)
            return g
    raise HTTPException(status_code=404, detail="Group not found")


def init_files():
    """Initialize users.json and groups.json with minimal content if empty."""
    if not USERS_FILE.exists():
        save_json(USERS_FILE, [
            {
                "id": str(uuid.uuid4()),
                "userName": "admin",
                "displayName": "Admin User",
                "email": "admin@example.com",
                "department": "Security",
                "active": True,
                "groups": []
            }
        ])

    if not GROUPS_FILE.exists():
        save_json(GROUPS_FILE, [
            {
                "id": str(uuid.uuid4()),
                "displayName": "Security-Admins",
                "members": []
            },
            {
                "id": str(uuid.uuid4()),
                "displayName": "HR-Users",
                "members": []
            },
        ])


init_files()

