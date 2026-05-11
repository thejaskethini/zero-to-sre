# ☁️ Pulumi — Infrastructure as Code with Real Languages

> **Pulumi lets you define infrastructure using TypeScript, Python, Go, or C# instead of HCL.**

## Terraform vs Pulumi

| Feature | Terraform | Pulumi |
|---------|-----------|--------|
| Language | HCL (domain-specific) | Python, TypeScript, Go, C# |
| State | terraform.tfstate | Pulumi Cloud or self-managed |
| Testing | Limited (terratest) | Native unit testing |
| IDE support | Basic | Full (autocomplete, types) |
| Learning curve | Learn HCL | Use languages you know |

## Quick Start (Python)

```bash
# Install
curl -fsSL https://get.pulumi.com | sh

# New project
pulumi new aws-python

# Example: Create an S3 bucket
# __main__.py
import pulumi
import pulumi_aws as aws

bucket = aws.s3.Bucket("my-bucket",
    website=aws.s3.BucketWebsiteArgs(
        index_document="index.html",
    ),
)

pulumi.export("bucket_url", bucket.website_endpoint)
```

```bash
# Deploy
pulumi up

# Destroy
pulumi destroy
```

## When to Use Pulumi

- Teams that prefer real programming languages over DSLs
- Complex infrastructure requiring loops, conditionals, abstractions
- Projects that benefit from unit testing infrastructure code
- Multi-cloud deployments with shared abstractions

## Further Reading

- [Pulumi Docs](https://www.pulumi.com/docs/)
- [Pulumi vs Terraform](https://www.pulumi.com/docs/concepts/vs/terraform/)
