# 🏗️ Terraform Cheatsheet

> Quick reference for Terraform CLI commands and patterns.

---

## 🔧 Core Workflow

```bash
terraform init                           # Initialize, download providers
terraform init -upgrade                  # Upgrade provider versions
terraform plan                           # Preview changes
terraform plan -out=tfplan               # Save plan to file
terraform apply                          # Apply changes (interactive)
terraform apply tfplan                   # Apply saved plan
terraform apply -auto-approve            # Skip confirmation (CI/CD)
terraform destroy                        # Destroy all resources
terraform destroy -target=aws_instance.web  # Destroy specific resource
```

## 📊 State Management

```bash
terraform state list                     # List all resources
terraform state show aws_vpc.main        # Show resource details
terraform state mv aws_vpc.main module.vpc.aws_vpc.main  # Move resource
terraform state rm aws_instance.old      # Remove from state (not cloud!)
terraform state pull > state.json        # Download state
terraform import aws_instance.web i-abc123  # Import existing resource
terraform refresh                        # Sync state with real infra
```

## 📝 Output & Validation

```bash
terraform output                         # Show all outputs
terraform output vpc_id                  # Specific output
terraform output -json                   # JSON format
terraform validate                       # Validate config syntax
terraform fmt                            # Format code
terraform fmt -check                     # Check formatting (CI)
terraform graph | dot -Tpng > graph.png  # Dependency graph
```

## 🏗️ Workspaces

```bash
terraform workspace list                 # List workspaces
terraform workspace new staging          # Create workspace
terraform workspace select staging       # Switch workspace
terraform workspace show                 # Current workspace
terraform workspace delete staging       # Delete workspace
```

## 🔍 Debugging

```bash
TF_LOG=DEBUG terraform plan              # Enable debug logging
TF_LOG_PATH=terraform.log terraform plan # Log to file
terraform plan -refresh-only             # Detect drift
terraform taint aws_instance.web         # Force recreation
terraform untaint aws_instance.web       # Cancel taint
```

## 📦 Modules

```hcl
# Using a module
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.0.0"
  
  name = "my-vpc"
  cidr = "10.0.0.0/16"
}

# Module output reference
output "vpc_id" {
  value = module.vpc.vpc_id
}
```

## 💡 Common Patterns

```hcl
# Dynamic blocks
resource "aws_security_group" "web" {
  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.port
      to_port     = ingress.value.port
      protocol    = "tcp"
      cidr_blocks = ingress.value.cidrs
    }
  }
}

# Conditional resource creation
resource "aws_eip" "nat" {
  count  = var.create_nat_gateway ? 1 : 0
  domain = "vpc"
}

# For_each with map
resource "aws_iam_user" "users" {
  for_each = toset(var.usernames)
  name     = each.value
}
```

---

> 💡 **Tips:** Use `terraform plan -out=tfplan` always. Use [tfsec](https://github.com/aquasecurity/tfsec) for security scanning. Use [Infracost](https://infracost.io/) for cost estimation.
