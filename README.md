<p align="center">
  <img src="IAM git.png" width="90%" />
</p>
# IAM Governance Lab

A small hands-on lab focused on **Identity & Access Management (IAM)** concepts:

- Identity lifecycle: **Joiner → Mover → Leaver**
- **SCIM-like provisioning** simulator
- **RBAC analysis** and entitlement drift detection
- Example **Zero Trust** and **ABAC** policy models

This is not a production system — it’s a learning lab designed to show how IAM concepts map to simple automation scripts, JSON policy models, and CSV-based access data.

---

## 🧱 Project Structure

```text
iam-governance-lab/
│
├── scim_simulator/
│   ├── scim_server.py        # Simple SCIM-like API simulator (FastAPI)
│   ├── users.json            # Current provisioned users
│   └── groups.json           # Current provisioned groups
│
├── lifecycle_engine/
│   ├── joiner.py             # Handle new hires (Joiners)
│   ├── mover.py              # Handle role/department changes (Movers)
│   └── leaver.py             # Handle terminations (Leavers)
│
├── rbac_analyzer/
│   ├── analyze_roles.py      # RBAC/entitlement overview & high-risk roles
│   ├── entitlements.json     # Example application entitlements
│   └── drift_detector.py     # Detect entitlement drift vs RBAC model
│
├── policies/
│   ├── rbac_model.json       # Example RBAC role → permission mapping
│   ├── abac_policies.json    # Example ABAC-style attribute policies
│   └── zero_trust_baseline.md# Identity-related Zero Trust baseline
│
├── data/
│   ├── employees.csv         # HR-like source of truth for identities
│   └── access_matrix.csv     # Who has access to what (for RBAC analysis)
│
├── requirements.txt
└── README.md

🚀 Getting Started
1️⃣ Create and activate a virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

2️⃣ Install dependencies
pip install -r requirements.txt

🛰 SCIM Simulator

Run a simple SCIM-like API with FastAPI:

cd scim_simulator
uvicorn scim_server:app --reload


Endpoints:

GET /Users – list all users

POST /Users – create user

PATCH /Users/{user_id} – update user (e.g. department, active)

DELETE /Users/{user_id} – soft delete user

GET /Groups – list groups

Data is stored in users.json and groups.json.

👤 Identity Lifecycle (Joiner–Mover–Leaver)

Scripts under lifecycle_engine/ simulate basic lifecycle actions based on data/employees.csv and the RBAC model in policies/rbac_model.json.

From the project root:

# Process new hires
python3 lifecycle_engine/joiner.py

# Process department/role changes
python3 lifecycle_engine/mover.py

# Process leavers (terminate access)
python3 lifecycle_engine/leaver.py


These scripts update scim_simulator/users.json and scim_simulator/groups.json to reflect identity state and access.

🔎 RBAC Analysis & Drift Detection

Analyze current access and detect risky patterns:

# Overview of entitlements and high-risk roles
python3 rbac_analyzer/analyze_roles.py

# Compare current access vs expected RBAC model and detect drift
python3 rbac_analyzer/drift_detector.py

🧠 Concepts Illustrated

Identity lifecycle management

SCIM-style provisioning

RBAC and entitlements

Entitlement drift & access creep

Simple ABAC-style policies

Zero Trust identity baseline

This lab is intentionally simplified but can be extended with:

Real SCIM endpoints

Integration to IAM platforms

More advanced ABAC engines

Audit logging and reporting

👤 Author

Created as a learning lab by Dimitrios Kallimanis
AI Security & IAM – exploring the intersection of identity, access, and modern systems.


---

## 📦 2. `requirements.txt`

```text
fastapi
uvicorn


