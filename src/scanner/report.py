"""Build and save scan reports as Markdown and JSON."""
import json
import os
from datetime import datetime, timezone
from typing import List, Dict, Tuple

from azure.storage.blob import BlobServiceClient


def build_report(findings: List[Dict], subscription_id: str) -> Tuple[str, str]:
    """Return (markdown, json) representations of the findings."""
    timestamp = datetime.now(timezone.utc).isoformat()

    payload = {
        "scanned_at": timestamp,
        "subscription_id": subscription_id,
        "finding_count": len(findings),
        "findings": findings,
    }
    report_json = json.dumps(payload, indent=2)

    lines = [
        "# Azure CSPM Scan Report",
        "",
        f"- Scanned at: {timestamp}",
        f"- Findings: {len(findings)}",
        "",
    ]
    if not findings:
        lines.append("No misconfigurations found. ✅")
    for f in findings:
        lines += [
            f"## [{f['severity']}] {f['name']}",
            f"- **Issue:** {f['issue']}",
            f"- **CIS control:** {f['cis_control']}",
            f"- **Fix:** {f['fix']}",
            f"- **Resource:** `{f['resource']}`",
            "",
        ]
    report_md = "\n".join(lines)
    return report_md, report_json


def save_report(credential, report_md: str, report_json: str) -> None:
    """Upload both reports to the reports container in the storage account."""
    account_url = os.environ["REPORTS_STORAGE_URL"]      # e.g. https://acct.blob.core.windows.net
    container = os.environ.get("REPORTS_CONTAINER", "reports")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M%S")

    blob_service = BlobServiceClient(account_url=account_url, credential=credential)
    container_client = blob_service.get_container_client(container)

    container_client.upload_blob(f"scan-{stamp}.md", report_md, overwrite=True)
    container_client.upload_blob(f"scan-{stamp}.json", report_json, overwrite=True)
