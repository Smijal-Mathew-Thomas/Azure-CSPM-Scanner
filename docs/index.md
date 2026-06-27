# Azure Cloud Security Posture Scanner

An automated, serverless **CSPM** tool that audits a Microsoft Azure subscription
every day against the **CIS Azure Benchmark** — read-only, secret-free, and
provisioned entirely with Terraform.

## Why

Most cloud breaches don't come from clever attacks. They come from simple
settings left wrong: storage left public, traffic left unencrypted, and
remote-access ports left open to the internet. This tool catches those
misconfigurations automatically, every day.

## Key properties

- **Automated & serverless** — runs on a timer, costs a few cents a month.
- **Secret-free** — uses an Azure Managed Identity, no stored passwords or keys.
- **Least privilege** — read-only across the subscription; it cannot change anything.
- **Standards-aligned** — every finding maps to a CIS Azure control.
- **Reproducible** — the whole setup lives in Terraform.

Continue to [Architecture](architecture.md) to see how it fits together.
