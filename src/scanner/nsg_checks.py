"""CIS checks for Network Security Groups (read-only)."""
from typing import List, Dict

# Ports that should never be open to the public internet
SENSITIVE_PORTS = {
    "22": ("SSH", "CIS Azure 6.x"),
    "3389": ("RDP", "CIS Azure 6.x"),
    "1433": ("SQL Server", "CIS Azure 6.x"),
    "3306": ("MySQL", "CIS Azure 6.x"),
    "5432": ("PostgreSQL", "CIS Azure 6.x"),
    "1521": ("Oracle", "CIS Azure 6.x"),
    "27017": ("MongoDB", "CIS Azure 6.x"),
}

PUBLIC_SOURCES = {"*", "0.0.0.0/0", "internet"}


def _is_public(source: str) -> bool:
    return source.lower() in PUBLIC_SOURCES


def _rule_covers_port(rule, port: str) -> bool:
    dest = rule.destination_port_range
    ranges = rule.destination_port_ranges or ([dest] if dest else [])
    for r in ranges:
        if r == "*" or r == port:
            return True
        if "-" in r:
            low, high = r.split("-")
            if int(low) <= int(port) <= int(high):
                return True
    return False


def check_network_security_groups(network_client) -> List[Dict]:
    """Audit every NSG in the subscription for sensitive ports open to the internet."""
    findings: List[Dict] = []

    for nsg in network_client.network_security_groups.list_all():
        for rule in nsg.security_rules or []:
            if rule.direction != "Inbound" or rule.access != "Allow":
                continue
            if not _is_public(rule.source_address_prefix or ""):
                continue

            for port, (service, control) in SENSITIVE_PORTS.items():
                if _rule_covers_port(rule, port):
                    findings.append({
                        "severity": "HIGH",
                        "resource": nsg.id,
                        "name": nsg.name,
                        "issue": f"{service} (port {port}) open to the internet",
                        "cis_control": control,
                        "fix": f"Restrict the source of rule '{rule.name}' to known IPs",
                    })

    return findings
