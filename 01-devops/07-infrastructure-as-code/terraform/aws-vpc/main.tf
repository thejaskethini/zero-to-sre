# =============================================================================
# 🏗️ AWS VPC Terraform Configuration — Main
# =============================================================================
# Description: Creates a production-ready VPC with:
#   - Public and private subnets across multiple AZs
#   - Internet Gateway for public subnets
#   - NAT Gateway for private subnet internet access
#   - Route tables with proper routing
#   - Security groups with least-privilege rules
#
# Usage:
#   terraform init
#   terraform plan -out=tfplan
#   terraform apply tfplan
#
# Architecture:
#   ┌─────────────────────────────────────────────────────┐
#   │ VPC (10.0.0.0/16)                                   │
#   │                                                     │
#   │  ┌──────────────┐  ┌──────────────┐                │
#   │  │ Public Sub 1 │  │ Public Sub 2 │  ← IGW        │
#   │  │ 10.0.1.0/24  │  │ 10.0.2.0/24  │                │
#   │  └──────────────┘  └──────────────┘                │
#   │                                                     │
#   │  ┌──────────────┐  ┌──────────────┐                │
#   │  │ Private Sub 1│  │ Private Sub 2│  ← NAT GW     │
#   │  │ 10.0.10.0/24 │  │ 10.0.20.0/24 │                │
#   │  └──────────────┘  └──────────────┘                │
#   └─────────────────────────────────────────────────────┘
# =============================================================================

# ─── Terraform Configuration ────────────────────────────────────────────────
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # IMPORTANT: Uncomment this block for production to use remote state
  # backend "s3" {
  #   bucket         = "my-terraform-state-bucket"
  #   key            = "vpc/terraform.tfstate"
  #   region         = "us-east-1"
  #   dynamodb_table = "terraform-locks"  # For state locking
  #   encrypt        = true
  # }
}

# ─── Provider Configuration ─────────────────────────────────────────────────
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
      Repository  = "zero-to-sre"
    }
  }
}

# ─── Data Sources ────────────────────────────────────────────────────────────
# Fetch available AZs dynamically (don't hardcode AZ names!)
data "aws_availability_zones" "available" {
  state = "available"
}

# ─── Local Variables ────────────────────────────────────────────────────────
locals {
  # Use first 2 AZs for high availability
  azs = slice(data.aws_availability_zones.available.names, 0, 2)

  # Common name prefix for all resources
  name_prefix = "${var.project_name}-${var.environment}"
}

# =============================================================================
# VPC
# =============================================================================
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  # Enable DNS support (required for RDS, EKS, etc.)
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    Name = "${local.name_prefix}-vpc"
  }
}

# =============================================================================
# INTERNET GATEWAY — Provides internet access to public subnets
# =============================================================================
resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${local.name_prefix}-igw"
  }
}

# =============================================================================
# SUBNETS — Public (internet-facing) and Private (internal)
# =============================================================================

# --- Public Subnets ---
# These subnets can directly reach the internet via the Internet Gateway
resource "aws_subnet" "public" {
  count = length(local.azs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 1)
  availability_zone = local.azs[count.index]

  # Auto-assign public IPs (needed for instances that need direct internet access)
  map_public_ip_on_launch = true

  tags = {
    Name = "${local.name_prefix}-public-${local.azs[count.index]}"
    Tier = "public"
    # Tags required for EKS if you plan to use it later
    "kubernetes.io/role/elb" = "1"
  }
}

# --- Private Subnets ---
# These subnets can only reach the internet through NAT Gateway
resource "aws_subnet" "private" {
  count = length(local.azs)

  vpc_id            = aws_vpc.main.id
  cidr_block        = cidrsubnet(var.vpc_cidr, 8, count.index + 10)
  availability_zone = local.azs[count.index]

  tags = {
    Name = "${local.name_prefix}-private-${local.azs[count.index]}"
    Tier = "private"
    "kubernetes.io/role/internal-elb" = "1"
  }
}

# =============================================================================
# NAT GATEWAY — Allows private subnets to reach the internet (for updates, etc.)
# =============================================================================

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"

  tags = {
    Name = "${local.name_prefix}-nat-eip"
  }

  # EIP may require IGW to exist
  depends_on = [aws_internet_gateway.main]
}

# NAT Gateway (in first public subnet)
resource "aws_nat_gateway" "main" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public[0].id

  tags = {
    Name = "${local.name_prefix}-nat-gw"
  }

  depends_on = [aws_internet_gateway.main]
}

# Pro Tip: For production, create one NAT Gateway per AZ for high availability
# This costs more (~$32/month per NAT GW) but eliminates cross-AZ traffic

# =============================================================================
# ROUTE TABLES — Control traffic routing
# =============================================================================

# --- Public Route Table ---
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  # Route internet traffic through the Internet Gateway
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = {
    Name = "${local.name_prefix}-public-rt"
  }
}

# Associate public subnets with public route table
resource "aws_route_table_association" "public" {
  count = length(aws_subnet.public)

  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

# --- Private Route Table ---
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  # Route internet traffic through NAT Gateway
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main.id
  }

  tags = {
    Name = "${local.name_prefix}-private-rt"
  }
}

# Associate private subnets with private route table
resource "aws_route_table_association" "private" {
  count = length(aws_subnet.private)

  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}

# =============================================================================
# SECURITY GROUPS — Firewall rules
# =============================================================================

# --- Web Security Group (Public-facing) ---
resource "aws_security_group" "web" {
  name_prefix = "${local.name_prefix}-web-"
  description = "Security group for web-facing services"
  vpc_id      = aws_vpc.main.id

  # HTTP
  ingress {
    description = "HTTP from anywhere"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # HTTPS
  ingress {
    description = "HTTPS from anywhere"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Allow all outbound traffic
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name_prefix}-web-sg"
  }

  # Prevent destruction before replacement
  lifecycle {
    create_before_destroy = true
  }
}

# --- Application Security Group (Private) ---
resource "aws_security_group" "app" {
  name_prefix = "${local.name_prefix}-app-"
  description = "Security group for application services"
  vpc_id      = aws_vpc.main.id

  # Only allow traffic from the web security group
  ingress {
    description     = "Traffic from web tier"
    from_port       = 3000
    to_port         = 3000
    protocol        = "tcp"
    security_groups = [aws_security_group.web.id]
  }

  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name_prefix}-app-sg"
  }

  lifecycle {
    create_before_destroy = true
  }
}

# =============================================================================
# VPC FLOW LOGS — Network monitoring and troubleshooting
# =============================================================================
resource "aws_flow_log" "main" {
  vpc_id          = aws_vpc.main.id
  traffic_type    = "ALL"
  iam_role_arn    = aws_iam_role.flow_log.arn
  log_destination = aws_cloudwatch_log_group.flow_log.arn

  tags = {
    Name = "${local.name_prefix}-flow-log"
  }
}

resource "aws_cloudwatch_log_group" "flow_log" {
  name              = "/vpc/${local.name_prefix}/flow-logs"
  retention_in_days = 30

  tags = {
    Name = "${local.name_prefix}-flow-log-group"
  }
}

resource "aws_iam_role" "flow_log" {
  name_prefix = "${local.name_prefix}-flow-log-"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "vpc-flow-logs.amazonaws.com"
      }
    }]
  })
}

resource "aws_iam_role_policy" "flow_log" {
  name_prefix = "${local.name_prefix}-flow-log-"
  role        = aws_iam_role.flow_log.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams"
      ]
      Effect   = "Allow"
      Resource = "*"
    }]
  })
}
