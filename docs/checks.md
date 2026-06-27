# Checks (CIS mapping)

Every finding the scanner produces maps to a specific CIS Azure Benchmark control.

## Storage Accounts

| Check | CIS control | Severity |
|-------|-------------|----------|
| Public / anonymous blob access allowed | CIS 3.7 | HIGH |
| HTTPS not enforced (secure transfer off) | CIS 3.1 | HIGH |
| Minimum TLS version below 1.2 | CIS 3.x | MEDIUM |

## Network Security Groups

| Check | CIS control | Severity |
|-------|-------------|----------|
| SSH (port 22) open to the internet | CIS 6.x | HIGH |
| RDP (port 3389) open to the internet | CIS 6.x | HIGH |
| Database ports (1433, 3306, 5432, ...) exposed publicly | CIS 6.x | HIGH |

## Adding a new check

1. Add a function to the relevant module under `src/scanner/`.
2. Return findings in the standard shape (`severity`, `resource`, `issue`,
   `cis_control`, `fix`).
3. Document the new control in the tables above.
