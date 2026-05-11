# 🎓 DevOps Interview Questions

> Curated questions with answers for DevOps engineer interviews at top companies.

---

## 🟢 Beginner Level

### 1. What is DevOps?
**Answer:** DevOps is a set of practices that combines software development (Dev) and IT operations (Ops), aiming to shorten the development lifecycle while delivering features, fixes, and updates frequently with high quality. It emphasizes automation, collaboration, CI/CD, and monitoring.

### 2. Explain CI/CD.
**Answer:**
- **CI (Continuous Integration):** Developers merge code frequently. Each merge triggers automated builds and tests.
- **CD (Continuous Delivery):** Code is always in a deployable state. Deployment to production requires manual approval.
- **CD (Continuous Deployment):** Every passing change is automatically deployed to production.

### 3. What is Infrastructure as Code?
**Answer:** IaC manages infrastructure through machine-readable definition files instead of manual processes. Benefits: version control, reproducibility, consistency, peer review. Tools: Terraform, CloudFormation, Pulumi.

### 4. What is a container vs a VM?
**Answer:** Containers share the host OS kernel and are lightweight (MBs, boot in seconds). VMs include a full guest OS and are heavier (GBs, boot in minutes). Containers are ideal for microservices; VMs provide stronger isolation.

---

## 🟡 Intermediate Level

### 5. Explain Docker multi-stage builds.
**Answer:** Multi-stage builds use multiple FROM statements. Build-time dependencies stay in earlier stages; only production artifacts are copied to the final stage. This reduces image size by 80-90%.

### 6. Describe Kubernetes pod lifecycle.
**Answer:** Pending → ContainerCreating → Running → Succeeded/Failed. Key phases: scheduling, image pulling, init containers, readiness probes, liveness probes, graceful shutdown (preStop hooks + SIGTERM).

### 7. What is GitOps?
**Answer:** GitOps uses Git as the single source of truth for declarative infrastructure. A GitOps agent (ArgoCD, Flux) watches the Git repo and reconciles the cluster state. Benefits: audit trail, rollback via git revert, no direct cluster access needed.

### 8. Explain Terraform state. Why is it important?
**Answer:** Terraform state maps resources in your config to real-world resources. It tracks metadata, dependencies, and resource attributes. Critical rules: use remote state (S3/GCS), enable state locking (DynamoDB), never manually edit state files.

### 9. How would you implement zero-downtime deployments?
**Answer:** Use rolling updates (K8s default), blue-green deployments, or canary releases. Key requirements: health checks (readiness probes), graceful shutdown, database backward compatibility, feature flags for incomplete features.

---

## 🔴 Advanced Level

### 10. Design a CI/CD pipeline for a microservices architecture.
**Answer:** Key considerations:
- **Per-service pipelines** with independent deployability
- **Shared library** for common pipeline stages
- **Contract testing** between services (Pact)
- **Canary deployment** with automated rollback
- **Parallel execution** for test stages
- **Security scanning** integrated (SAST, DAST, dependency scanning)
- **GitOps** for deployment (ArgoCD syncs from config repo)

### 11. How do you handle secrets in Kubernetes?
**Answer:** Kubernetes Secrets are base64-encoded (NOT encrypted by default). Production approaches:
- **Sealed Secrets** — Encrypt secrets that only the cluster can decrypt
- **External Secrets Operator** — Sync from Vault/AWS Secrets Manager
- **SOPS** — Encrypt secret files in Git
- **HashiCorp Vault** — Dynamic secrets, rotation, audit logging
- Enable **etcd encryption at rest** for K8s secrets

### 12. Explain the CAP theorem and its implications for distributed systems.
**Answer:** In a distributed system, you can only guarantee 2 of 3: Consistency (all nodes see same data), Availability (every request gets a response), Partition tolerance (system works despite network failures). Since partitions are inevitable in distributed systems, the real choice is CP (consistent but may be unavailable) vs AP (available but may be inconsistent).

---

## 💡 Behavioral Questions

### 13. Tell me about a production incident you handled.
**Framework:** Use STAR (Situation, Task, Action, Result). Focus on: how you detected it, how you communicated, what you learned, and what you improved afterward.

### 14. How do you prioritize between feature work and reliability work?
**Answer:** Use error budgets. If the SLO is met and error budget remains, prioritize features. If error budget is depleted, prioritize reliability. This creates a data-driven framework that aligns engineering and product.

---

> 💡 **Tip:** For senior roles, focus on **system design** and **production experience**. Interviewers want to hear about real decisions you've made under pressure.
