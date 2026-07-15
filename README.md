# Azure Cloud Security Posture Scanner

> An automated, serverless **CSPM** (Cloud Security Posture Management) tool that audits a Microsoft Azure subscription every day against the **CIS Azure Benchmark**. Read-only, secret-free, and provisioned entirely with Terraform.

![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC)
![Azure](https://img.shields.io/badge/cloud-Microsoft%20Azure-0078D4)
![CIS Benchmark](https://img.shields.io/badge/standard-CIS%20Benchmark-red)
![Build](https://github.com/Smijal-Mathew-Thomas/Azure-CSPM-Scanner/actions/workflows/ci.yml/badge.svg)

---

## Overview

Most cloud breaches don't come from clever attacks. They come from simple settings left wrong: storage left public, traffic left unencrypted, remote-access ports left open to the whole internet.

This project is an automated "security guard" for Azure. It runs on a schedule, checks your resources against the CIS Benchmark, and writes a report flagging anything misconfigured. It **can only look, never change anything**, so it can audit production safely without any risk of causing an outage.

## Features

- **Automated & serverless** — runs on a timer with zero manual effort, then sleeps. Costs a few cents a month.
- **Secret-free** — authenticates with an Azure **Managed Identity**. No passwords or keys to store or leak.
- **Least privilege** — read-only audit access across the subscription; it cannot modify any resource.
- **Standards-aligned** — every finding maps to a specific CIS Azure control.
- **Reproducible** — the entire setup is defined in Terraform and deploys with one command.
- **Readable reports** — output saved as both Markdown (for humans) and JSON (for tooling), every run.

## Architecture

A daily timer triggers an Azure Function that reads the subscription with a read-only managed identity and writes a report to blob storage. Everything is provisioned by Terraform inside a single resource group.

![Architecture: daily timer triggers an Azure Function that reads the subscription (read-only) and writes reports to storage](docs/images/architecture.png)

<details>
<summary>Text version of the diagram</summary>

```
            ┌─────────────┐
            │ Timer (cron)│  fires once a day
            └──────┬──────┘
                   ▼
        ┌────────────────────┐      Managed Identity
        │   Azure Function   │◄──── (read-only, no secrets)
        │   (Python + SDK)   │
        └─────────┬──────────┘
                  │ reads config of
                  ▼
   ┌──────────────────────────────────┐
   │  Azure resources in subscription │
   │  (Storage Accounts, NSGs, ...)   │
   └──────────────┬───────────────────┘
                  │ compared against CIS
                  ▼
        ┌────────────────────┐
        │  Report (MD + JSON)│  saved to a storage container
        └────────────────────┘
```
</details>

## What it scans

| Resource | Check | CIS control |
|----------|-------|-------------|
| Storage Account | Public / anonymous blob access allowed | CIS 3.7 |
| Storage Account | HTTPS not enforced | CIS 3.1 |
| Storage Account | Minimum TLS version below 1.2 | CIS 3.x |
| Network Security Group | SSH (port 22) open to the internet | CIS 6.x |
| Network Security Group | RDP (port 3389) open to the internet | CIS 6.x |
| Network Security Group | Database ports exposed publicly | CIS 6.x |

## Walkthrough

A quick look at the tool running end to end, from the resources Terraform builds to a real finding it catches.

**1. Terraform provisions the whole stack in one resource group** — Function App, App Service plan, storage account, Log Analytics, and Application Insights.

![Azure portal showing the five Terraform-provisioned resources in the resource group](docs/images/terraform-resources.png)

**2. Reports land in a dedicated container** inside the storage account (the `azure-webjobs-*` containers are the Function's own runtime files; `reports` is where scans are written).

![Storage account containers, including the reports container, all set to private access](docs/images/storage-containers.png)

**3. A deliberately-unsafe "bait" resource is added for testing** — a Network Security Group with SSH (port 22) open to the internet, so the scanner has something real to catch. It is a throwaway test resource, not part of the project.

![Azure portal showing the bait Network Security Group alongside the project resources](docs/images/bait-nsg.png)

**4. The Function runs on schedule and writes timestamped reports** (`.md` + `.json`) plus a rolling `latest.md`.

![Reports container listing timestamped markdown and JSON reports plus latest.md](docs/images/reports-output.png)

**5. The result: a CIS-mapped HIGH finding with a recommended fix.** Bait, automatic detection, then a graded finding. The scanner works end to end.

![Azure Security Posture Report showing a HIGH severity finding for SSH port 22 exposed, mapped to CIS Azure 6.x with a remediation recommendation](docs/images/sample-finding.png)

## Tech stack

| Component | Role |
|-----------|------|
| Microsoft Azure | The cloud being secured |
| Terraform | Infrastructure as Code |
| Azure Functions | Serverless scheduling |
| Python + Azure SDK | Scan logic and API calls |
| Managed Identity | Secret-free authentication |
| CIS Benchmark | The security standard |

## Prerequisites

- An Azure subscription (works inside the free $100 student credit)
- [Terraform](https://developer.hashicorp.com/terraform/install) installed
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) installed and signed in (`az login`)
- Python 3.11+

## Deployment

> **Note:** Your subscription ID and tenant ID are read from your `az login` session and environment variables. They are **never** hardcoded in this repo. See `terraform/terraform.tfvars.example`.

```bash
# 1. Sign in to Azure
az login

# 2. Point Terraform at your subscription (do NOT commit these values)
export ARM_SUBSCRIPTION_ID="<your-subscription-id>"
export ARM_TENANT_ID="<your-tenant-id>"

# 3. Deploy
cd terraform
cp terraform.tfvars.example terraform.tfvars   # then edit non-secret values
terraform init
terraform plan
terraform apply
```

The scanner is now deployed and will run on its schedule. To trigger it manually, run it from the Azure Portal or with the Azure Functions Core Tools.

## Sample report

```text
[HIGH] Network Security Group: bait / rule 'Bait_1'
Issue:       SSH (port 22) is open to the public internet (source = any)
CIS control: CIS Azure 6.x
Fix:         Restrict port 22 to known IP ranges, or use a bastion / VPN
```

> Real subscription IDs are redacted from published reports. Keep generated reports git-ignored so they never publish your real IDs (the included `.gitignore` already handles this).

## Cost

Serverless. You pay only for the few seconds it runs each day, which comes to roughly **a few cents per month**. It fits comfortably inside the Azure student credit, and no credit card is required.

## Roadmap

- **Auto-remediation** — optionally fix a finding the moment it appears.
- **More checks** — Key Vault, disks, identities, public IPs.
- **DevSecOps** — scan Terraform in a CI/CD pipeline before resources are even created.
- **Dashboard & alerts** — central view and notifications.

## Honest framing

This is not meant to replace enterprise CSPM tools. It's built with the same patterns real teams use in production (Infrastructure as Code, serverless, managed identities, least privilege) to demonstrate a working understanding of cloud security posture management.

## Security

Found a security issue? Please see [SECURITY.md](SECURITY.md) for how to report it responsibly.

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
