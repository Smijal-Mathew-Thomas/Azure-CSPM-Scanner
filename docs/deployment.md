# Deployment

## Prerequisites

- An Azure subscription (works inside the free $100 student credit)
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli)
- Python 3.11+

## Steps

!!! warning "Never hardcode IDs"
    Your subscription ID and tenant ID are read from your `az login` session and
    environment variables. They must **never** be committed to the repository.

```bash
# 1. Sign in to Azure
az login

# 2. Point Terraform at your subscription (do NOT commit these values)
export ARM_SUBSCRIPTION_ID="<your-subscription-id>"
export ARM_TENANT_ID="<your-tenant-id>"

# 3. Deploy the infrastructure
cd terraform
cp terraform.tfvars.example terraform.tfvars   # edit non-secret values only
terraform init
terraform plan
terraform apply

# 4. Deploy the function code (from the src/ folder)
#    e.g. with Azure Functions Core Tools:
#    func azure functionapp publish <your-function-app-name>
```

## Verifying

Trigger the function manually from the Azure Portal, then check the reports
container in the storage account for the latest Markdown and JSON output.
