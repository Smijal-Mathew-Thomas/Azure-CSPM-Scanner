# Security Policy

## Reporting a vulnerability

If you discover a security issue in this project, please report it privately
rather than opening a public issue.

- Email: **<your-email@example.com>**
- Or use GitHub's **private vulnerability reporting** (Security tab → "Report a vulnerability").

Please include:
- A description of the issue and its potential impact
- Steps to reproduce
- Any relevant logs (with secrets removed)

We aim to acknowledge reports within a few days.

## Scope

This is an educational, read-only auditing tool. It is designed so that it
**cannot modify Azure resources**. If you find a way that it could write to or
change a resource, that is considered a security bug — please report it.

## Good practice for users

- Never commit `*.tfstate`, `*.tfvars`, `local.settings.json`, `.env` files,
  or generated scan reports — they can contain subscription IDs and secrets.
- Always deploy the scanner with a **read-only** role (Reader) and a
  **managed identity**, never with a stored password or key.
