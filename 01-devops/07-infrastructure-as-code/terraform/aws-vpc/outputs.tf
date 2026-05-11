# =============================================================================
# 🏗️ AWS VPC Terraform — Outputs
# =============================================================================
# Description: Output values exposed after terraform apply.
#              These can be used by other Terraform modules or scripts.
#
# Usage:
#   terraform output                    # Show all outputs
#   terraform output vpc_id             # Show specific output
#   terraform output -json              # Machine-readable format
# =============================================================================

output "vpc_id" {
  description = "The ID of the VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "The CIDR block of the VPC"
  value       = aws_vpc.main.cidr_block
}

output "public_subnet_ids" {
  description = "List of public subnet IDs"
  value       = aws_subnet.public[*].id
}

output "private_subnet_ids" {
  description = "List of private subnet IDs"
  value       = aws_subnet.private[*].id
}

output "public_subnet_cidrs" {
  description = "List of public subnet CIDR blocks"
  value       = aws_subnet.public[*].cidr_block
}

output "private_subnet_cidrs" {
  description = "List of private subnet CIDR blocks"
  value       = aws_subnet.private[*].cidr_block
}

output "nat_gateway_ip" {
  description = "The public IP of the NAT Gateway"
  value       = aws_eip.nat.public_ip
}

output "web_security_group_id" {
  description = "Security group ID for web-facing services"
  value       = aws_security_group.web.id
}

output "app_security_group_id" {
  description = "Security group ID for application services"
  value       = aws_security_group.app.id
}

output "internet_gateway_id" {
  description = "The ID of the Internet Gateway"
  value       = aws_internet_gateway.main.id
}

# This output is useful for other modules that need VPC info
output "vpc_summary" {
  description = "Summary of VPC configuration"
  value = {
    vpc_id             = aws_vpc.main.id
    vpc_cidr           = aws_vpc.main.cidr_block
    public_subnets     = aws_subnet.public[*].id
    private_subnets    = aws_subnet.private[*].id
    nat_gateway_ip     = aws_eip.nat.public_ip
    availability_zones = local.azs
  }
}
