# 🏆 Projects & Labs Index

> **10 hands-on projects — from beginner to advanced — that will make you production-ready.**

<p align="center">
  <img src="https://img.shields.io/badge/Projects-10-00d4ff?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Beginner_to_Advanced-f4c542?style=for-the-badge" />
</p>

---

## 📋 Project Index

| # | Project | Difficulty | Duration | Tools |
|---|---------|:----------:|:--------:|-------|
| 1 | [Personal Blog CI/CD](#-project-1--personal-blog-cicd) | 🟢 Beginner | 2-3 hrs | GitHub Actions, Docker |
| 2 | [Dockerize a Full-Stack App](#-project-2--dockerize-a-full-stack-app) | 🟢 Beginner | 2-3 hrs | Docker, Compose |
| 3 | [Linux Server Hardening](#-project-3--linux-server-hardening) | 🟢 Beginner | 2 hrs | Bash, SSH, UFW |
| 4 | [Kubernetes Deployment Lab](#-project-4--kubernetes-deployment-lab) | 🟡 Intermediate | 3-4 hrs | K8s, Helm, kubectl |
| 5 | [Terraform AWS Infrastructure](#-project-5--terraform-aws-infrastructure) | 🟡 Intermediate | 3-4 hrs | Terraform, AWS |
| 6 | [Monitoring Stack Setup](#-project-6--monitoring-stack-setup) | 🟡 Intermediate | 3-4 hrs | Prometheus, Grafana |
| 7 | [GitOps with ArgoCD](#-project-7--gitops-with-argocd) | 🟡 Intermediate | 3-4 hrs | ArgoCD, K8s, Git |
| 8 | [Incident Response Simulation](#-project-8--incident-response-simulation) | 🔴 Advanced | 4-5 hrs | PagerDuty/Opsgenie, Runbooks |
| 9 | [Chaos Engineering Game Day](#-project-9--chaos-engineering-game-day) | 🔴 Advanced | 4-6 hrs | LitmusChaos, k6 |
| 10 | [🏆 End-to-End: Build → Ship → Run](#-project-10--end-to-end-capstone) | 🔴 Advanced | 6-8 hrs | All tools |

---

## 🟢 Project 1 — Personal Blog CI/CD

**What you'll learn:** GitHub Actions fundamentals, automated testing, auto-deploy on push.

```
project-1-blog-cicd/
├── .github/workflows/
│   └── deploy.yml          # Build, test, deploy pipeline
├── src/
│   └── index.html          # Static site
├── tests/
│   └── test_links.sh       # Simple link validator
├── Dockerfile
└── README.md               # Lab instructions
```

**Steps:**
1. Create a simple static site (HTML/CSS)
2. Write a GitHub Actions pipeline: lint → build → test → deploy
3. Add branch protection rules
4. Configure auto-deploy to GitHub Pages on merge to `main`
5. Add a badge to your README showing build status

**Skills:** Git branching, CI/CD concepts, YAML, GitHub Actions

---

## 🟢 Project 2 — Dockerize a Full-Stack App

**What you'll learn:** Docker multi-stage builds, Compose, networking, volume mounts.

```
project-2-dockerize/
├── frontend/
│   ├── Dockerfile
│   └── src/
├── backend/
│   ├── Dockerfile.multistage
│   └── src/
├── docker-compose.yml       # App + DB + Redis
├── .dockerignore
└── README.md
```

**Steps:**
1. Write a REST API (Node.js/Python) with a database
2. Create an optimized multi-stage Dockerfile
3. Set up Docker Compose with app + PostgreSQL + Redis
4. Add health checks and resource limits
5. Implement a `.dockerignore` for lean images
6. Compare image sizes: naive vs multi-stage

**Skills:** Docker, multi-stage builds, Compose, container networking

---

## 🟢 Project 3 — Linux Server Hardening

**What you'll learn:** SSH hardening, firewall config, user management, system auditing.

```
project-3-hardening/
├── scripts/
│   ├── harden.sh            # Automated hardening script
│   ├── audit.sh             # Security audit checker
│   └── setup-monitoring.sh  # Install node_exporter
└── README.md
```

**Steps:**
1. Disable root SSH login and password auth
2. Configure UFW firewall (allow only 22, 80, 443)
3. Set up fail2ban for brute-force protection
4. Create a non-root deploy user with sudo
5. Enable automatic security updates
6. Run the audit script to verify hardening

**Skills:** Linux administration, SSH, firewalls, security

---

## 🟡 Project 4 — Kubernetes Deployment Lab

**What you'll learn:** K8s core resources, rolling updates, HPA, network policies.

```
project-4-k8s-lab/
├── manifests/
│   ├── namespace.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   └── network-policy.yaml
├── helm-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
└── README.md
```

**Steps:**
1. Start minikube/kind cluster
2. Deploy app with 3 replicas, resource limits, probes
3. Expose via Service and Ingress
4. Set up HPA — load test and watch it auto-scale
5. Apply network policies (deny all → allow specific)
6. Practice rolling update and rollback
7. Convert raw manifests to a Helm chart

**Skills:** kubectl, deployments, services, Helm, auto-scaling

---

## 🟡 Project 5 — Terraform AWS Infrastructure

**What you'll learn:** IaC workflow, state management, modules, drift detection.

```
project-5-terraform/
├── environments/
│   ├── dev/
│   │   └── main.tf
│   └── prod/
│       └── main.tf
├── modules/
│   ├── vpc/
│   └── ec2/
├── backend.tf               # S3 remote state
└── README.md
```

**Steps:**
1. Create a VPC with public/private subnets
2. Launch an EC2 instance in the private subnet
3. Set up an S3 backend for remote state
4. Create reusable modules (VPC, EC2)
5. Use `terraform plan` to detect drift
6. Practice `terraform destroy` safely

**Skills:** Terraform, AWS, state management, modules

---

## 🟡 Project 6 — Monitoring Stack Setup

**What you'll learn:** Prometheus, Grafana, alerting, Golden Signals dashboards.

```
project-6-monitoring/
├── docker-compose.yml       # Prometheus + Grafana + Alertmanager
├── prometheus/
│   ├── prometheus.yml
│   └── alert-rules.yml
├── grafana/
│   └── dashboards/
│       └── golden-signals.json
├── app/                     # Instrumented sample app
└── README.md
```

**Steps:**
1. Deploy Prometheus + Grafana + Alertmanager via Docker Compose
2. Instrument a sample app with /metrics endpoint
3. Configure Prometheus to scrape the app
4. Build a Golden Signals dashboard in Grafana
5. Create alert rules (high error rate, high latency)
6. Configure Alertmanager to send alerts to Slack/email
7. Generate artificial traffic and trigger alerts

**Skills:** Prometheus, Grafana, PromQL, alerting

---

## 🟡 Project 7 — GitOps with ArgoCD

**What you'll learn:** GitOps workflow, ArgoCD, auto-sync, progressive delivery.

```
project-7-gitops/
├── app-manifests/           # K8s manifests (the "desired state")
│   ├── deployment.yaml
│   └── service.yaml
├── argocd/
│   └── application.yaml     # ArgoCD Application
└── README.md
```

**Steps:**
1. Install ArgoCD on your K8s cluster
2. Create a Git repo with K8s manifests
3. Configure ArgoCD Application pointing to the repo
4. Change a manifest in Git → watch ArgoCD auto-sync
5. Practice rollback via Git revert
6. Set up auto-sync with self-heal

**Skills:** GitOps, ArgoCD, declarative infrastructure

---

## 🔴 Project 8 — Incident Response Simulation

**What you'll learn:** On-call workflows, severity classification, postmortems.

```
project-8-incident-sim/
├── scenarios/
│   ├── scenario-1-db-down.md
│   ├── scenario-2-memory-leak.md
│   └── scenario-3-cert-expiry.md
├── templates/
│   ├── incident-report.md
│   └── postmortem.md
├── runbooks/
│   └── (from SRE module)
└── README.md
```

**Steps:**
1. Set up alert routing (PagerDuty free tier or Opsgenie)
2. Create 3 incident scenarios with injected failures
3. Practice the full incident lifecycle: detect → triage → mitigate → resolve
4. Write a blameless postmortem for each scenario
5. Create action items and track resolution
6. Hold a post-incident review meeting

**Skills:** Incident management, postmortems, communication

---

## 🔴 Project 9 — Chaos Engineering Game Day

**What you'll learn:** Chaos experiments, blast radius, game day facilitation.

```
project-9-chaos/
├── experiments/
│   ├── pod-kill.yaml
│   ├── network-latency.yaml
│   └── cpu-stress.yaml
├── load-tests/
│   └── load-test.js         # k6 script
├── game-day-runbook.md
└── README.md
```

**Steps:**
1. Deploy a multi-replica app to K8s
2. Set up monitoring (Prometheus + Grafana)
3. Run k6 load test to establish baseline
4. Execute chaos experiments during load test:
   - Kill 1 pod → does traffic recover?
   - Add 500ms network latency → does SLO hold?
   - Stress CPU to 90% → does HPA scale up?
5. Document findings for each experiment
6. Write improvement action items

**Skills:** Chaos engineering, resilience testing, game days

---

## 🔴 Project 10 — End-to-End Capstone

**The ultimate project — from code to production-grade observability.**

➡️ **[Full lab instructions →](./end-to-end-lab.md)**

```
project-10-capstone/
├── app/                     # Instrumented REST API
├── docker/                  # Multi-stage Dockerfile + Compose
├── k8s/                     # Deployment, Service, HPA, NetworkPolicy
├── helm/                    # Helm chart
├── terraform/               # Infrastructure provisioning
├── monitoring/              # Prometheus, Grafana, alerts
├── chaos/                   # Chaos experiments
├── ci-cd/                   # GitHub Actions pipeline
└── docs/
    ├── slo-definition.md
    ├── runbooks/
    └── postmortem.md
```

**Steps:**
1. Write a REST API with Prometheus metrics
2. Containerize with multi-stage Docker build
3. Deploy to K8s with Helm chart
4. Set up CI/CD with GitHub Actions → ArgoCD
5. Deploy Prometheus + Grafana monitoring
6. Define SLOs and create burn-rate alerts
7. Run chaos experiments during load test
8. Write a blameless postmortem
9. Calculate error budget consumed

**Skills:** Everything. This is your portfolio project.

---

## 💡 Tips for Maximum Learning

| Tip | Why |
|-----|-----|
| **Don't copy-paste** | Type every command manually to build muscle memory |
| **Break things intentionally** | Delete a pod, corrupt a config — learn what happens |
| **Time yourself** | Track how long each project takes, compare on retry |
| **Document as you go** | Write a mini-README for each project |
| **Pair with someone** | Teaching reinforces learning |

---

<p align="center">
  <a href="../README.md">⬅️ Back to Main</a>
</p>
