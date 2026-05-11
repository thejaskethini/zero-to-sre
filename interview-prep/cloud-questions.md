# 🎓 Cloud Engineering Interview Questions

> Curated questions for Cloud/DevOps engineer roles covering AWS, Azure, and GCP.

---

## 🟢 Beginner

### 1. What is the difference between IaaS, PaaS, and SaaS?
**Answer:**
- **IaaS** — You manage OS and above. Provider manages hardware, networking. *Ex: EC2, Azure VM, Compute Engine.*
- **PaaS** — You manage only code and data. Provider manages runtime, OS, infra. *Ex: Elastic Beanstalk, App Service, App Engine.*
- **SaaS** — You just use the software. *Ex: Gmail, Office 365, Salesforce.*

### 2. What is a VPC and why do you need one?
**Answer:** A Virtual Private Cloud is an isolated network within the cloud where you control IP ranges, subnets, route tables, and security groups. You need it to isolate workloads, control traffic flow, and enforce security boundaries. Think of it as your own private data center inside the cloud.

### 3. What's the difference between a Security Group and a NACL (AWS)?
**Answer:**
| Feature | Security Group | NACL |
|---------|---------------|------|
| Level | Instance level | Subnet level |
| State | Stateful (return traffic automatic) | Stateless (must allow both directions) |
| Rules | Allow only | Allow AND deny |
| Default | Deny all inbound | Allow all |
| Use case | Per-instance firewall | Subnet-wide guardrails |

### 4. What are Availability Zones vs Regions?
**Answer:**
- **Region** — A geographic location (e.g., us-east-1, eastus, us-central1). Services replicate across regions for DR.
- **AZ** — Independent data centers within a region (e.g., us-east-1a, 1b, 1c). Connected via low-latency links. Deploy across 2+ AZs for high availability.

---

## 🟡 Intermediate

### 5. How would you design a highly available web application on AWS?
**Answer:**
1. **Multi-AZ deployment** — EC2 instances in 2+ AZs behind an ALB
2. **Auto Scaling Group** — Min 2, desired 3, max 10 instances
3. **RDS Multi-AZ** — Automatic failover for database
4. **ElastiCache** — Redis for session storage (not local to instances)
5. **S3 + CloudFront** — Static assets on CDN
6. **Route 53** — Health-checked DNS with failover routing
7. **Monitoring** — CloudWatch alarms + SNS notifications

### 6. Explain IAM best practices.
**Answer:**
- **Never use root account** — Create IAM users, enable MFA on root
- **Least privilege** — Grant minimum permissions needed
- **Use roles, not keys** — EC2 instance profiles, service accounts
- **Rotate credentials** — 90-day key rotation policy
- **Use IAM policies** — JSON-based, attach to groups not users
- **Enable CloudTrail** — Audit all API calls
- **Use SCPs** — Organization-level guardrails

### 7. What is the difference between S3 storage classes?
**Answer:**
| Class | Use Case | Retrieval | Cost |
|-------|----------|-----------|:----:|
| S3 Standard | Frequently accessed | Instant | $$$$ |
| S3 IA | Infrequent access | Instant | $$$ |
| S3 One Zone-IA | Non-critical infrequent | Instant | $$ |
| S3 Glacier Instant | Archive, instant access | Instant | $$ |
| S3 Glacier Flexible | Archive, minutes-hours | 1-12 hours | $ |
| S3 Glacier Deep | Long-term archive | 12-48 hours | ¢ |

Use **lifecycle policies** to automatically transition objects between classes.

### 8. How do you secure an S3 bucket?
**Answer:**
1. Block all public access (account-level setting)
2. Enable versioning + MFA delete
3. Encrypt at rest (SSE-S3 or SSE-KMS)
4. Encrypt in transit (enforce HTTPS via bucket policy)
5. Use bucket policies for cross-account access
6. Enable CloudTrail data events for audit logging
7. Use VPC endpoints for private access

---

## 🔴 Advanced

### 9. Design a CI/CD pipeline on AWS for a microservices application.
**Answer:**
```
Developer → GitHub → CodePipeline → CodeBuild → ECR → ECS/EKS
                                                   ↓
                                            CodeDeploy (Blue/Green)
                                                   ↓
                                            CloudWatch (monitoring)
```
- **Source:** GitHub webhook triggers CodePipeline
- **Build:** CodeBuild runs tests, builds Docker image, pushes to ECR
- **Deploy:** CodeDeploy does blue/green to ECS, or ArgoCD to EKS
- **Monitor:** CloudWatch Container Insights + X-Ray tracing
- **Rollback:** Automatic on failed health checks

### 10. How would you migrate a monolithic app to the cloud?
**Answer:** Use the **6 R's of Migration:**
1. **Rehost** (lift & shift) — Move VMs to EC2 as-is. Fastest, least benefit.
2. **Replatform** — Minor tweaks (e.g., move DB to RDS, use ELB)
3. **Repurchase** — Replace with SaaS (e.g., move email to Office 365)
4. **Refactor** — Break into microservices. Highest effort, highest benefit.
5. **Retire** — Turn off unused applications
6. **Retain** — Keep on-premises (compliance, latency requirements)

### 11. Explain Kubernetes networking on a cloud provider.
**Answer:**
- **Pod networking:** CNI plugin (VPC CNI on AWS, Azure CNI, GKE native)
- **Service networking:** ClusterIP (internal), LoadBalancer (cloud LB), NodePort
- **Ingress:** ALB Ingress Controller (AWS), Application Gateway (Azure), GKE Ingress
- **Network Policies:** Calico or Cilium for pod-to-pod firewall rules
- **DNS:** CoreDNS for service discovery, external-dns for Route53/Cloud DNS
- **Service Mesh:** Istio or Linkerd for mTLS, traffic management

### 12. How do you optimize cloud costs for a large organization?
**Answer:**
1. **Visibility first** — Tagging strategy + cost allocation reports
2. **Right-size** — CloudWatch/Monitoring metrics → downsize over-provisioned
3. **Reserved/Committed use** — 1-3 year commitments for stable workloads (30-60% savings)
4. **Spot/Preemptible** — For stateless, fault-tolerant workloads (60-90% savings)
5. **Auto-scaling** — Scale to zero in dev/staging at night
6. **Storage lifecycle** — S3/Blob lifecycle policies to archive old data
7. **FinOps team** — Dedicated team for cost governance + showback/chargeback
8. **Budget alerts** — At 50%, 80%, 100% of expected spend

---

> 💡 **Tip:** For cloud interviews, always mention the Well-Architected Framework pillars and tie your answers to security, cost, and reliability.
