# 📋 Cheatsheets

> **35+ FAANG-grade quick reference guides** for the tools you'll use every day as a DevOps/SRE engineer.
> Every cheatsheet includes production patterns, debugging tips, and **FAANG interview Q&A**.

---

<p align="center">
  <img src="https://img.shields.io/badge/35+_Cheatsheets-FAANG_Level-00d4ff?style=for-the-badge" alt="Cheatsheets" />
  <img src="https://img.shields.io/badge/Every_Cheatsheet-Interview_Q&A-f4c542?style=for-the-badge" alt="Interview Q&A" />
  <img src="https://img.shields.io/badge/Production-Patterns-43a047?style=for-the-badge" alt="Production" />
</p>

---

## 🌐 Web & Proxy

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🌐 Nginx](./nginx-cheatsheet.md) | Reverse proxy, load balancing, SSL, caching, rate limiting | 🟡 Intermediate |
| [🔒 Caddy](./caddy-cheatsheet.md) | Automatic HTTPS, Caddyfile, reverse proxy, static files | 🟢 Beginner |
| [🔀 Traefik](./traefik-cheatsheet.md) | Docker/K8s provider, middlewares, Let's Encrypt, routing | 🟡 Intermediate |
| [⚖️ HAProxy](./haproxy-cheatsheet.md) | Frontend/backend, algorithms, health checks, ACLs, stick tables | 🔴 Advanced |

## ⚙️ Process & Runtime

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [⚙️ PM2](./pm2-cheatsheet.md) | Cluster mode, ecosystem config, zero-downtime, log management | 🟡 Intermediate |
| [🖥️ Systemd](./systemd-cheatsheet.md) | Unit files, journalctl, timers, cgroups, debugging | 🟡 Intermediate |
| [📜 Bash Scripting](./bash-scripting-cheatsheet.md) | Error handling, functions, text processing, script templates | 🟡 Intermediate |

## 🔍 Production Debugging

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🔥 Production Debugging](./production-debugging-cheatsheet.md) | CPU, memory, disk, network, container, K8s debugging | 🔴 Advanced |
| [🔥 Linux Performance](./linux-performance-cheatsheet.md) | USE method, perf, flamegraphs, vmstat, iostat, Brendan Gregg | 🔴 Advanced |
| [🔬 Network Debugging](./network-debugging-cheatsheet.md) | ss, dig, curl timing, TLS debug, firewall inspection | 🟡 Intermediate |
| [🦈 tcpdump & Wireshark](./tcpdump-wireshark-cheatsheet.md) | Capture filters, display filters, packet analysis, tshark | 🔴 Advanced |

## ☁️ Cloud & Infrastructure

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [☁️ AWS](./aws-production-cheatsheet.md) | EC2, S3, RDS, EKS, CloudWatch, IAM, cost management | 🟡 Intermediate |
| [☁️ GCP](./gcp-cheatsheet.md) | Compute, GKE, Storage, Cloud SQL, BigQuery, Cloud Run | 🟡 Intermediate |
| [🔷 Azure](./azure-cheatsheet.md) | VMs, AKS, Blob, Azure SQL, Functions, Key Vault | 🟡 Intermediate |
| [☁️ Cloud CLI](./cloud-cli-cheatsheet.md) | AWS, Azure, GCP commands side-by-side | 🟢 Beginner |
| [🤖 Ansible](./ansible-cheatsheet.md) | Playbooks, roles, Jinja2, vault, idempotency | 🟡 Intermediate |
| [🏗️ Terraform](./terraform-cheatsheet.md) | Providers, modules, state, workspaces, patterns | 🟡 Intermediate |

## 📦 Kubernetes Extended

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [📦 kubectl](./kubectl-cheatsheet.md) | Essential K8s resource management | 🟡 Intermediate |
| [☸️ kubectl Advanced](./kubectl-advanced-cheatsheet.md) | JSONPath, RBAC, NetworkPolicy, node management, debugging | 🔴 Advanced |
| [🏗️ Helm](./helm-cheatsheet.md) | Install, upgrade, debug, repos | 🟡 Intermediate |
| [🏗️ Helm Advanced](./helm-advanced-cheatsheet.md) | Chart dev, templating, hooks, OCI, secrets, diff | 🔴 Advanced |
| [🔄 ArgoCD](./argocd-cheatsheet.md) | GitOps, Application CRD, app-of-apps, ApplicationSet | 🔴 Advanced |
| [🕸️ Istio](./istio-cheatsheet.md) | Service mesh, VirtualService, mTLS, traffic management | 🔴 Advanced |
| [📐 Kustomize](./kustomize-cheatsheet.md) | Bases, overlays, patches, generators, multi-env | 🟡 Intermediate |

## 📊 Observability & Monitoring

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [📊 Prometheus/PromQL](./prometheus-cheatsheet.md) | Golden Signals queries, aggregation, alerting | 🟡 Intermediate |
| [📊 Grafana](./grafana-cheatsheet.md) | Data sources, dashboards, variables, alerting, provisioning | 🟡 Intermediate |
| [🔭 Observability](./observability-cheatsheet.md) | Metrics, logs, traces, SLI/SLO/SLA, RED/USE methods | 🟡 Intermediate |
| [🔭 OpenTelemetry](./opentelemetry-cheatsheet.md) | OTel SDK, Collector, auto-instrumentation, sampling | 🔴 Advanced |
| [📚 ELK Stack](./elk-stack-cheatsheet.md) | Elasticsearch DSL, Logstash, Kibana, Filebeat, ILM | 🔴 Advanced |
| [🐕 Datadog](./datadog-cheatsheet.md) | Agent, APM, DogStatsD, monitors, SLOs, K8s integration | 🟡 Intermediate |

## 🔐 Security

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🛡️ Security Hardening](./security-hardening-cheatsheet.md) | Server, container, API security, audit checklists | 🟡 Intermediate |
| [🔐 SSL/TLS](./ssl-tls-cheatsheet.md) | TLS handshake, openssl, Let's Encrypt, mTLS, debugging | 🟡 Intermediate |
| [🔑 SSH](./ssh-cheatsheet.md) | Keys, config, tunneling, hardening, certificates, bastion | 🟡 Intermediate |
| [🔐 HashiCorp Vault](./vault-hashicorp-cheatsheet.md) | KV secrets, dynamic secrets, PKI, K8s integration | 🔴 Advanced |

## 🗄️ Databases & Messaging

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🐘 PostgreSQL](./postgresql-cheatsheet.md) | psql, EXPLAIN ANALYZE, indexes, replication, PgBouncer | 🟡 Intermediate |
| [🔴 Redis](./redis-cheatsheet.md) | Data structures, persistence, Sentinel, Cluster, eviction | 🟡 Intermediate |
| [📨 Kafka](./kafka-cheatsheet.md) | Topics, partitions, consumer groups, Connect, tuning | 🔴 Advanced |

## 🚀 CI/CD

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🔄 CI/CD Pipelines](./cicd-pipeline-cheatsheet.md) | Deployment strategies, DORA metrics, testing pyramid | 🟡 Intermediate |
| [🔄 GitHub Actions](./github-actions-cheatsheet.md) | Workflows, matrix, OIDC, reusable workflows, caching | 🟡 Intermediate |
| [🦊 GitLab CI](./gitlab-ci-cheatsheet.md) | Stages, rules, includes, runners, security scanning | 🟡 Intermediate |

## 🎯 Core Tools

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🐧 Linux](./linux-cheatsheet.md) | File ops, processes, networking, text processing | 🟢 Beginner |
| [📦 Git](./git-cheatsheet.md) | Branching, merging, undoing, investigation | 🟢 Beginner |
| [🐳 Docker](./docker-cheatsheet.md) | Images, containers, compose, volumes, cleanup | 🟢 Beginner |
| [🌐 Networking](./networking-cheatsheet.md) | TCP/IP, DNS, HTTP, subnetting, TLS | 🟡 Intermediate |

## 🧠 FAANG Interview

| Cheatsheet | Key Tools | Difficulty |
|-----------|-----------|------------|
| [🏗️ System Design](./system-design-cheatsheet.md) | Interview framework, estimation, CAP, scaling patterns | 🔴 Advanced |
| [🧠 SRE Interview](./sre-interview-cheatsheet.md) | SLI/SLO, reliability patterns, chaos engineering, on-call | 🔴 Advanced |
| [📟 Incident Response](./incident-response-cheatsheet.md) | Severity levels, response steps, postmortem templates | 🟡 Intermediate |

---

## ⚡ [Quick Reference Card](./QUICK-REFERENCE.md)

> 🚨 **The top 5 commands from every cheatsheet in one file** — your fast-lookup card during incidents.

---

## 💡 How to Use

1. **🔖 Bookmark** the ones you use most
2. **🖨️ Print** them for your desk (they're designed to be scannable)
3. **⚡ Quick Ref** — use the [Quick Reference Card](./QUICK-REFERENCE.md) during incidents
4. **🤝 Contribute** — see a missing command? [Submit a PR](../CONTRIBUTING.md)!

---

<p align="center">
  <a href="../README.md">⬅️ Back to Main</a>
</p>
