"""
Azure Function entry point.

A timer fires once a day, the function authenticates with its managed identity,
runs the CIS checks across the subscription, and writes a Markdown + JSON report.
"""
import logging
import os

import azure.functions as func
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import SubscriptionClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient

from scanner.storage_checks import check_storage_accounts
from scanner.nsg_checks import check_network_security_groups
from scanner.report import build_report, save_report

app = func.FunctionApp()


@app.timer_trigger(schedule="0 0 6 * * *", arg_name="timer", run_on_startup=False)
def daily_scan(timer: func.TimerRequest) -> None:
    """Runs every day at 06:00 UTC."""
    logging.info("Starting Azure CSPM scan")

    # Managed identity -> no secrets stored anywhere
    credential = DefaultAzureCredential()

    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]

    storage_client = StorageManagementClient(credential, subscription_id)
    network_client = NetworkManagementClient(credential, subscription_id)

    findings = []
    findings += check_storage_accounts(storage_client)
    findings += check_network_security_groups(network_client)

    report_md, report_json = build_report(findings, subscription_id)
    save_report(credential, report_md, report_json)

    logging.info("Scan complete: %d finding(s)", len(findings))
