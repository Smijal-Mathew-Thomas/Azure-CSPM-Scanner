# Architecture

Everything is provisioned by Terraform inside a single resource group.

```
            +-------------+
            | Timer (cron)|  fires once a day
            +------+------+
                   |
                   v
        +--------------------+      Managed Identity
        |   Azure Function   |<---- (read-only, no secrets)
        |   (Python + SDK)   |
        +---------+----------+
                  | reads config of
                  v
   +----------------------------------+
   |  Azure resources in subscription |
   |  (Storage Accounts, NSGs, ...)   |
   +----------------+-----------------+
                    | compared against CIS
                    v
        +--------------------+
        |  Report (MD + JSON)|  saved to a storage container
        +--------------------+
```

## Daily cycle

1. **Timer fires** on a schedule (e.g. once a day).
2. **Function wakes** and authenticates using its managed identity.
3. **Reads config** of resources across the subscription.
4. **Checks vs CIS** benchmark controls.
5. **Writes a report** (Markdown + JSON) and can raise an alert.

The function runs for only a few seconds, then sleeps until the next run.

## Security model

- **Managed identity** — Azure handles authentication; there are no secrets to leak.
- **Least privilege** — the identity holds the built-in **Reader** role, scoped
  to the subscription. It can read configuration but cannot modify any resource.
- **Read-only auditing** — because it can never change resources, it can never
  cause an outage.
- **Infrastructure as Code** — the entire deployment is defined in Terraform and
  is reproducible and reviewable.
