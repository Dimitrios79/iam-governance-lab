# Zero Trust Identity Baseline (Example)

This file defines a simple, identity-focused Zero Trust baseline:

- Verify **every identity** (human and non-human)
- Require **MFA** for all interactive user logins
- Enforce **strong device posture checks** for admin actions
- Limit privileged roles to **just-in-time elevation** where possible
- Apply **least privilege**:
  - Map departments → roles
  - Use entitlements only where needed
- Continuously **monitor sign-in patterns** for anomalies
- Re-certify access regularly:
  - Quarterly access reviews for HR and Security-Admin roles
- Explicitly block:
  - Shared accounts (where possible)
  - Use of personal email addresses
- Log all:
  - Admin actions in IAM-Console
  - Changes to role → permission mappings
  - Provisioning and deprovisioning events

This baseline is intentionally simplified and can be extended for real-world architectures.

