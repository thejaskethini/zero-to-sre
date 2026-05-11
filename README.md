<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=100&lines=%F0%9F%9B%A0%EF%B8%8F+Zero+to+SRE;DevOps+%E2%80%A2+Site+Reliability+%E2%80%A2+AIOps" alt="Zero to SRE" />
</p>

<p align="center">
  <strong>Your ultimate roadmap for DevOps, Site Reliability Engineering & AIOps mastery.</strong>
</p>

<p align="center">
  <a href="https://github.com/thejas0501/zero-to-sre/stargazers"><img src="https://img.shields.io/github/stars/thejas0501/zero-to-sre?style=for-the-badge&logo=github&color=f4c542" alt="Stars" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/network/members"><img src="https://img.shields.io/github/forks/thejas0501/zero-to-sre?style=for-the-badge&logo=github&color=4fc3f7" alt="Forks" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/blob/main/LICENSE"><img src="https://img.shields.io/github/license/thejas0501/zero-to-sre?style=for-the-badge&color=43a047" alt="License" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/issues"><img src="https://img.shields.io/github/issues/thejas0501/zero-to-sre?style=for-the-badge&color=ef5350" alt="Issues" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white" alt="Terraform" />
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus" />
  <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana" />
  <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white" alt="ArgoCD" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white" alt="GCP" />
</p>

---

## 🎯 What is Zero to SRE?

**Zero to SRE** is a free, open-source, community-driven knowledge base that takes you from absolute beginner to production-ready expertise across three critical pillars of modern infrastructure:

| Pillar | Focus | You'll Learn |
|--------|-------|-------------|
| 🔧 **DevOps** | Build & Ship | CI/CD, Containers, IaC, GitOps, Platform Engineering |
| 🔥 **SRE** | Run & Reliability | Observability, Incidents, SLOs, Chaos Engineering, Toil Reduction |
| 🤖 **AIOps** | Intelligent Ops | Anomaly Detection, Smart Alerting, Log Intelligence, LLMOps |

> **Every module includes:** 📖 Concepts → 🔧 Hands-on Labs → 🏢 Real-world Use Cases → ⚠️ Pitfalls → 📚 Further Reading

---

## 🗺️ Learning Roadmap

```mermaid
graph TD
    START["🚀 Start Here"] --> LINUX["🐧 Linux Fundamentals"]
    START --> NET["🌐 Networking Basics"]
    
    LINUX --> GIT["📦 Git & Version Control"]
    NET --> GIT
    
    GIT --> CICD["⚡ CI/CD Pipelines"]
    GIT --> DOCKER["🐳 Containerization"]
    
    CICD --> K8S["☸️ Container Orchestration"]
    DOCKER --> K8S
    
    K8S --> IAC["🏗️ Infrastructure as Code"]
    K8S --> GITOPS["🔄 GitOps"]
    
    IAC --> PLATENG["🏭 Platform Engineering"]
    GITOPS --> PLATENG
    
    PLATENG --> SRE_FUND["📘 SRE Fundamentals"]
    
    SRE_FUND --> SLOS["📊 SLOs / SLAs / SLIs"]
    SRE_FUND --> OBS["🔭 Observability"]
    
    SLOS --> INCIDENT["🚨 Incident Management"]
    OBS --> INCIDENT
    
    INCIDENT --> CHAOS["💥 Chaos Engineering"]
    INCIDENT --> CAPACITY["📈 Capacity Planning"]
    
    CHAOS --> TOIL["🤖 Toil Reduction"]
    CAPACITY --> TOIL
    
    TOIL --> AIOPS_FUND["🧠 AIOps Fundamentals"]
    
    AIOPS_FUND --> ANOMALY["📉 Anomaly Detection"]
    AIOPS_FUND --> ALERT["🔔 Intelligent Alerting"]
    
    ANOMALY --> LOG["📝 Log Intelligence"]
    ALERT --> LOG
    
    LOG --> LLMOPS["🤖 LLMOps"]
    LOG --> PREDICT["⚡ Predictive Scaling"]
    
    LLMOPS --> MASTER["🏆 SRE Master"]
    PREDICT --> MASTER

    style START fill:#00d4ff,stroke:#0097a7,color:#000,stroke-width:2px
    style MASTER fill:#f4c542,stroke:#f9a825,color:#000,stroke-width:3px
    style LINUX fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style NET fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style GIT fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style CICD fill:#16213e,stroke:#7c4dff,color:#fff
    style DOCKER fill:#16213e,stroke:#7c4dff,color:#fff
    style K8S fill:#16213e,stroke:#7c4dff,color:#fff
    style IAC fill:#16213e,stroke:#7c4dff,color:#fff
    style GITOPS fill:#16213e,stroke:#7c4dff,color:#fff
    style PLATENG fill:#0f3460,stroke:#00e676,color:#fff
    style SRE_FUND fill:#1b1b2f,stroke:#e94560,color:#fff
    style SLOS fill:#1b1b2f,stroke:#e94560,color:#fff
    style OBS fill:#1b1b2f,stroke:#e94560,color:#fff
    style INCIDENT fill:#1b1b2f,stroke:#e94560,color:#fff
    style CHAOS fill:#1b1b2f,stroke:#e94560,color:#fff
    style CAPACITY fill:#1b1b2f,stroke:#e94560,color:#fff
    style TOIL fill:#1b1b2f,stroke:#e94560,color:#fff
    style AIOPS_FUND fill:#162447,stroke:#f4c542,color:#fff
    style ANOMALY fill:#162447,stroke:#f4c542,color:#fff
    style ALERT fill:#162447,stroke:#f4c542,color:#fff
    style LOG fill:#162447,stroke:#f4c542,color:#fff
    style LLMOPS fill:#162447,stroke:#f4c542,color:#fff
    style PREDICT fill:#162447,stroke:#f4c542,color:#fff
```

---

## 📂 Repository Structure

```
zero-to-sre/
│
├── 🔧 01-devops/                      # DevOps Pillar (9 modules)
│   ├── 01-linux-fundamentals/         ✅  + system healthcheck script
│   ├── 02-networking-basics/          ✅  + network debug toolkit
│   ├── 03-git-version-control/        ✅
│   ├── 04-ci-cd-pipelines/            ✅  (GitHub Actions, Jenkins, GitLab CI)
│   ├── 05-containerization/           ✅  (Dockerfile, Compose)
│   ├── 06-container-orchestration/    ✅  (K8s manifests + Helm chart)
│   ├── 07-infrastructure-as-code/     ✅  (Terraform + Ansible playbook)
│   ├── 08-gitops/                     ✅  (ArgoCD application)
│   └── 09-platform-engineering/       ✅
│
├── 🔥 02-sre/                         # SRE Pillar (7 modules)
│   ├── 01-sre-fundamentals/           ✅
│   ├── 02-slos-slas-slis/             ✅  + SLO tracker script
│   ├── 03-observability/              ✅  (Prometheus + Grafana dashboard)
│   ├── 04-incident-management/        ✅  (Templates + 4 runbooks)
│   ├── 05-chaos-engineering/          ✅  + LitmusChaos experiments
│   ├── 06-capacity-planning/          ✅  + k6 load test script
│   └── 07-toil-reduction/             ✅
│
├── 🤖 03-aiops/                       # AIOps Pillar (6 modules)
│   ├── 01-aiops-fundamentals/         ✅
│   ├── 02-anomaly-detection/          ✅  + Python ML script
│   ├── 03-intelligent-alerting/       ✅
│   ├── 04-log-intelligence/           ✅  + log analyzer script
│   ├── 05-llmops/                     ✅
│   └── 06-predictive-scaling/         ✅  + forecasting script
│
├── 📋 cheatsheets/                    # 6 Quick References
│   ├── kubectl, docker, terraform, linux, git, prometheus
│
├── 🎓 interview-prep/                # 4 Interview Guides
│   ├── devops, sre, kubernetes, system-design
│
├── 🏆 labs/                           # Hands-on Projects
│   └── end-to-end-lab.md             ✅  (Capstone: build → deploy → monitor → chaos)
│
├── ⚙️ .github/                       # Repository Infrastructure
│   ├── workflows/docs-ci.yml         ✅  (Lint, link check, security)
│   ├── ISSUE_TEMPLATE/               ✅  (Bug report, module request)
│   └── PULL_REQUEST_TEMPLATE.md      ✅
│
├── LICENSE                            MIT
├── CHANGELOG.md                       v1.0.0 release notes
├── CONTRIBUTING.md
└── CODE_OF_CONDUCT.md
```

---

## 📚 Module Overview

### 🔧 DevOps — Build & Ship

| # | Module | Description | Difficulty | Status |
|---|--------|-------------|------------|--------|
| 01 | [**Linux Fundamentals**](./01-devops/01-linux-fundamentals/) | Shell, file systems, processes, permissions | 🟢 Beginner | ✅ Complete |
| 02 | [**Networking Basics**](./01-devops/02-networking-basics/) | TCP/IP, DNS, load balancing, firewalls | 🟢 Beginner | ✅ Complete |
| 03 | [**Git & Version Control**](./01-devops/03-git-version-control/) | Branching strategies, rebasing, monorepos | 🟢 Beginner | ✅ Complete |
| 04 | [**CI/CD Pipelines**](./01-devops/04-ci-cd-pipelines/) | GitHub Actions, Jenkins, GitLab CI, multi-stage pipelines | 🟡 Intermediate | ✅ Complete |
| 05 | [**Containerization**](./01-devops/05-containerization/) | Docker, multi-stage builds, security, Compose | 🟡 Intermediate | ✅ Complete |
| 06 | [**Container Orchestration**](./01-devops/06-container-orchestration/) | Kubernetes, Helm, operators, service mesh | 🔴 Advanced | ✅ Complete |
| 07 | [**Infrastructure as Code**](./01-devops/07-infrastructure-as-code/) | Terraform, Pulumi, state management, modules | 🟡 Intermediate | ✅ Complete |
| 08 | [**GitOps**](./01-devops/08-gitops/) | ArgoCD, FluxCD, progressive delivery | 🔴 Advanced | ✅ Complete |
| 09 | [**Platform Engineering**](./01-devops/09-platform-engineering/) | IDPs, Backstage, golden paths | 🔴 Advanced | ✅ Complete |

### 🔥 SRE — Run & Reliability

| # | Module | Description | Difficulty | Status |
|---|--------|-------------|------------|--------|
| 01 | [**SRE Fundamentals**](./02-sre/01-sre-fundamentals/) | Google's SRE philosophy, error budgets, risk | 🟢 Beginner | ✅ Complete |
| 02 | [**SLOs / SLAs / SLIs**](./02-sre/02-slos-slas-slis/) | Defining, measuring, and alerting on service levels | 🟡 Intermediate | ✅ Complete |
| 03 | [**Observability**](./02-sre/03-observability/) | Metrics, logs, traces — Prometheus, Grafana, OTel | 🟡 Intermediate | ✅ Complete |
| 04 | [**Incident Management**](./02-sre/04-incident-management/) | On-call, runbooks, postmortems, severity levels | 🟡 Intermediate | ✅ Complete |
| 05 | [**Chaos Engineering**](./02-sre/05-chaos-engineering/) | Litmus, Chaos Monkey, game days, blast radius | 🔴 Advanced | ✅ Complete |
| 06 | [**Capacity Planning**](./02-sre/06-capacity-planning/) | Load testing, resource forecasting, scaling strategies | 🔴 Advanced | ✅ Complete |
| 07 | [**Toil Reduction**](./02-sre/07-toil-reduction/) | Automation, self-healing, eliminating repetitive work | 🟡 Intermediate | ✅ Complete |

### 🤖 AIOps — Intelligent Operations

| # | Module | Description | Difficulty | Status |
|---|--------|-------------|------------|--------|
| 01 | [**AIOps Fundamentals**](./03-aiops/01-aiops-fundamentals/) | What is AIOps, maturity model, tools landscape | 🟢 Beginner | ✅ Complete |
| 02 | [**Anomaly Detection**](./03-aiops/02-anomaly-detection/) | Statistical methods, ML approaches, time-series | 🔴 Advanced | ✅ Complete |
| 03 | [**Intelligent Alerting**](./03-aiops/03-intelligent-alerting/) | Alert correlation, noise reduction, smart routing | 🔴 Advanced | ✅ Complete |
| 04 | [**Log Intelligence**](./03-aiops/04-log-intelligence/) | Log parsing, pattern recognition, NLP on logs | 🔴 Advanced | ✅ Complete |
| 05 | [**LLMOps**](./03-aiops/05-llmops/) | LLMs for ops, incident summarization, RCA | 🔴 Advanced | ✅ Complete |
| 06 | [**Predictive Scaling**](./03-aiops/06-predictive-scaling/) | Forecasting demand, proactive auto-scaling | 🔴 Advanced | ✅ Complete |

### 📋 Quick References & Interview Prep

| Resource | Description |
|----------|-------------|
| [kubectl Cheatsheet](./cheatsheets/kubectl-cheatsheet.md) | Essential Kubernetes commands |
| [Docker Cheatsheet](./cheatsheets/docker-cheatsheet.md) | Container management quick reference |
| [Terraform Cheatsheet](./cheatsheets/terraform-cheatsheet.md) | IaC workflow and patterns |
| [Linux Cheatsheet](./cheatsheets/linux-cheatsheet.md) | Essential CLI commands |
| [Git Cheatsheet](./cheatsheets/git-cheatsheet.md) | Branching, merging, undoing mistakes |
| [Prometheus/PromQL Cheatsheet](./cheatsheets/prometheus-cheatsheet.md) | Golden Signals queries and alerting |
| [DevOps Interview Q&A](./interview-prep/devops-questions.md) | Beginner to advanced questions |
| [SRE Interview Q&A](./interview-prep/sre-questions.md) | Google-style SRE interview prep |
| [Kubernetes Interview Q&A](./interview-prep/kubernetes-questions.md) | Pods, networking, security, debugging |
| [System Design Scenarios](./interview-prep/system-design-scenarios.md) | Infrastructure design practice |
| [🏆 End-to-End Capstone Lab](./labs/end-to-end-lab.md) | Build → Deploy → Monitor → Chaos → Postmortem |

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/thejas0501/zero-to-sre.git
cd zero-to-sre

# Start with your first module
# If you're a beginner:
cat 01-devops/04-ci-cd-pipelines/README.md

# If you're intermediate:
cat 02-sre/03-observability/README.md

# If you're advanced:
cat 03-aiops/02-anomaly-detection/README.md
```

---

## 🏗️ How Each Module is Structured

Every module in this repository follows a consistent, battle-tested format:

```
📖 Conceptual Explanation
   └── What it is, why it matters, how it works
   
🔧 Hands-on Lab
   └── Step-by-step instructions with real tools
   
🏢 Real-world Use Case
   └── How companies like Google, Netflix, Meta use this
   
⚠️ Common Pitfalls
   └── Mistakes that trip up even experienced engineers
   
📚 Further Reading
   └── Curated links to deepen your understanding
```

---

## 🤝 Contributing

We love contributions! Whether it's fixing a typo, adding a new module, or improving an existing one — every contribution matters.

Please read our [Contributing Guide](./CONTRIBUTING.md) and [Code of Conduct](./CODE_OF_CONDUCT.md) before submitting.

### Ways to Contribute

| Type | Description |
|------|-------------|
| 📝 **Documentation** | Fix typos, improve explanations, add diagrams |
| 💻 **Code** | Add scripts, configs, or automation examples |
| 🧪 **Labs** | Create hands-on exercises and projects |
| 🐛 **Issues** | Report bugs or suggest improvements |
| 🌟 **Star** | Star this repo to show your support! |

---

## 📖 Philosophy

This project is guided by principles borrowed from the best:

- **📘 Google SRE Book** — "Hope is not a strategy"
- **🔄 DevOps Handbook** — "Automate everything, measure everything"
- **🧪 Chaos Engineering** — "Break things on purpose, in production"
- **🤖 AIOps** — "Let machines handle the noise, humans handle the signal"

---

## 🌟 Star History

<p align="center">
  <a href="https://star-history.com/#thejas0501/zero-to-sre&Date">
    <img src="https://api.star-history.com/svg?repos=thejas0501/zero-to-sre&type=Date" alt="Star History Chart" width="600" />
  </a>
</p>

---

## 📜 License

This project is licensed under the [MIT License](./LICENSE) — use it, share it, build upon it.

---

<p align="center">
  <strong>Built with ❤️ for the DevOps & SRE community</strong>
  <br />
  <sub>If this helped you, consider giving it a ⭐ — it helps others find it too!</sub>
</p>
