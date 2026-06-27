"""CIS checks for Azure Storage Accounts (read-only)."""
from typing import List, Dict


def check_storage_accounts(storage_client) -> List[Dict]:
    """Audit every storage account in the subscription against CIS controls."""
    findings: List[Dict] = []

    for account in storage_client.storage_accounts.list():
        name = account.name
        resource_id = account.id

        # CIS 3.7 - public / anonymous blob access must be disabled
        if getattr(account, "allow_blob_public_access", True):
            findings.append({
                "severity": "HIGH",
                "resource": resource_id,
                "name": name,
                "issue": "Public blob access allowed",
                "cis_control": "CIS Azure 3.7",
                "fix": "Disable 'Allow Blob public access' on the storage account",
            })

        # CIS 3.1 - secure transfer (HTTPS) must be enforced
        if not getattr(account, "enable_https_traffic_only", False):
            findings.append({
                "severity": "HIGH",
                "resource": resource_id,
                "name": name,
                "issue": "HTTPS not enforced (secure transfer disabled)",
                "cis_control": "CIS Azure 3.1",
                "fix": "Enable 'Secure transfer required'",
            })

        # CIS 3.x - minimum TLS version should be 1.2 or higher
        min_tls = getattr(account, "minimum_tls_version", "TLS1_0")
        if min_tls in ("TLS1_0", "TLS1_1"):
            findings.append({
                "severity": "MEDIUM",
                "resource": resource_id,
                "name": name,
                "issue": f"Weak minimum TLS version ({min_tls})",
                "cis_control": "CIS Azure 3.x",
                "fix": "Set minimum TLS version to 1.2",
            })

    return findings
