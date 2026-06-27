# Contributing

Thanks for your interest in improving the Azure Cloud Security Posture Scanner!
Contributions of all kinds are welcome — new checks, bug fixes, docs, or ideas.

## Ways to contribute

- **Report a bug** — open an issue describing what happened and what you expected.
- **Suggest a check** — propose a new CIS control to audit (include the control number).
- **Improve the docs** — fixes and clarifications are always appreciated.
- **Submit code** — see the workflow below.

## Development workflow

1. Fork the repository and clone your fork.
2. Create a branch for your change:
   ```bash
   git checkout -b feature/my-new-check
   ```
3. Make your change. For new checks, add a function under `src/scanner/`
   and map it to its CIS control in `docs/checks.md`.
4. Format and lint your Python:
   ```bash
   pip install ruff
   ruff check src/
   ```
5. Validate Terraform if you touched it:
   ```bash
   cd terraform && terraform fmt -check && terraform validate
   ```
6. Commit with a clear message and open a pull request.

## Ground rules

- **Never commit secrets.** No subscription IDs, tenant IDs, keys, connection
  strings, `*.tfstate`, `*.tfvars`, or generated reports. The `.gitignore`
  blocks these — please don't override it.
- Keep checks **read-only**. This tool must never modify Azure resources.
- Be respectful in issues and reviews.

## Code of conduct

Be kind, assume good faith, and help others learn.
