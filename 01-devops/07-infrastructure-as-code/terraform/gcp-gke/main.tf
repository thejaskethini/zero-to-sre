# =============================================================================
# ☁️ GCP — VPC Network + GKE Cluster (Terraform)
# =============================================================================
# Creates: VPC, Subnet, GKE Cluster, Node Pool
#
# Usage:
#   terraform init
#   terraform plan -var="project_id=my-gcp-project"
#   terraform apply
# =============================================================================

terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# ─── Variables ────────────────────────────────────────────────────────
variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "region" {
  description = "GCP region"
  default     = "us-central1"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

locals {
  prefix = "zero-to-sre-${var.environment}"
}

# ─── VPC Network ──────────────────────────────────────────────────────
resource "google_compute_network" "main" {
  name                    = "${local.prefix}-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "main" {
  name          = "${local.prefix}-subnet"
  ip_cidr_range = "10.0.0.0/20"
  region        = var.region
  network       = google_compute_network.main.id

  secondary_ip_range {
    range_name    = "pods"
    ip_cidr_range = "10.1.0.0/16"
  }

  secondary_ip_range {
    range_name    = "services"
    ip_cidr_range = "10.2.0.0/20"
  }
}

# ─── GKE Cluster ──────────────────────────────────────────────────────
resource "google_container_cluster" "primary" {
  name     = "${local.prefix}-gke"
  location = var.region

  network    = google_compute_network.main.name
  subnetwork = google_compute_subnetwork.main.name

  # Use separately managed node pool
  remove_default_node_pool = true
  initial_node_count       = 1

  ip_allocation_policy {
    cluster_secondary_range_name  = "pods"
    services_secondary_range_name = "services"
  }

  # Security
  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }
}

resource "google_container_node_pool" "primary" {
  name       = "${local.prefix}-node-pool"
  location   = var.region
  cluster    = google_container_cluster.primary.name
  node_count = 2

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 50

    oauth_scopes = [
      "https://www.googleapis.com/auth/cloud-platform",
    ]

    labels = {
      environment = var.environment
    }
  }

  autoscaling {
    min_node_count = 1
    max_node_count = 5
  }
}

# ─── Outputs ──────────────────────────────────────────────────────────
output "cluster_name" {
  value = google_container_cluster.primary.name
}

output "cluster_endpoint" {
  value     = google_container_cluster.primary.endpoint
  sensitive = true
}

output "kubeconfig_command" {
  value = "gcloud container clusters get-credentials ${google_container_cluster.primary.name} --region ${var.region} --project ${var.project_id}"
}
