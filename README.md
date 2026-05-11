<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=32&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&multiline=true&repeat=true&width=800&height=100&lines=%F0%9F%9A%80+Zero+to+SRE;The+Complete+DevOps+%2B+Cloud+%2B+SRE+%2B+AIOps+Guide" alt="Zero to SRE" />
</p>

<p align="center">
  <strong>🎯 Your ultimate open-source roadmap — from absolute beginner to production-ready engineer.</strong>
  <br />
  <sub>100+ files · 23 deep-dive modules · 9 cheatsheets · 10 projects · Real-world scripts</sub>
</p>

<p align="center">
  <a href="https://github.com/thejas0501/zero-to-sre/stargazers"><img src="https://img.shields.io/github/stars/thejas0501/zero-to-sre?style=for-the-badge&logo=github&color=f4c542" alt="Stars" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/network/members"><img src="https://img.shields.io/github/forks/thejas0501/zero-to-sre?style=for-the-badge&logo=github&color=4fc3f7" alt="Forks" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/blob/main/LICENSE"><img src="https://img.shields.io/github/license/thejas0501/zero-to-sre?style=for-the-badge&color=43a047" alt="License" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/pulls"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=for-the-badge" alt="PRs Welcome" /></a>
  <a href="https://github.com/thejas0501/zero-to-sre/issues"><img src="https://img.shields.io/github/issues/thejas0501/zero-to-sre?style=for-the-badge&color=ef5350" alt="Issues" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/AWS-232F3E?style=flat-square&logo=amazon-aws&logoColor=white" alt="AWS" />
  <img src="https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoft-azure&logoColor=white" alt="Azure" />
  <img src="https://img.shields.io/badge/GCP-4285F4?style=flat-square&logo=google-cloud&logoColor=white" alt="GCP" />
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" alt="Kubernetes" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white" alt="Terraform" />
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" alt="Prometheus" />
  <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" alt="Grafana" />
  <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white" alt="ArgoCD" />
  <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=github-actions&logoColor=white" alt="GitHub Actions" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Ansible-EE0000?style=flat-square&logo=ansible&logoColor=white" alt="Ansible" />
</p>

---

## 🎯 What is Zero to SRE?

**Zero to SRE** is a free, open-source, community-driven knowledge base that takes you from absolute beginner to production-ready expertise across **four critical pillars** of modern infrastructure:

<table>
<tr>
<td align="center" width="25%">

### 🔧 DevOps
**Build & Ship**
<br />
CI/CD · Containers · K8s
IaC · GitOps · Platform

</td>
<td align="center" width="25%">

### ☁️ Cloud
**Deploy Anywhere**
<br />
AWS · Azure · GCP
Multi-Cloud · Cost Ops

</td>
<td align="center" width="25%">

### 🔥 SRE
**Run & Reliability**
<br />
SLOs · Observability
Chaos · Incidents

</td>
<td align="center" width="25%">

### 🤖 AIOps
**Intelligent Ops**
<br />
Anomaly Detection
LLMOps · Prediction

</td>
</tr>
</table>

> **📖 Every module includes:** Concepts → 🔧 Hands-on Labs → 🏢 Real-world Cases → ⚠️ Pitfalls → 📚 Further Reading

---

## 🗺️ Learning Roadmap

> **Follow the path. Master each phase. Become production-ready.** 🚀

```mermaid
graph TD
    START["🚀 START HERE"]:::start

    START --> PHASE1

    subgraph PHASE1["  🟢 PHASE 1 — Foundations  "]
        LINUX["🐧 Linux<br/>Fundamentals"]:::green
        NET["🌐 Networking<br/>Basics"]:::green
        GIT["📦 Git & Version<br/>Control"]:::green
        LINUX --> GIT
        NET --> GIT
    end

    PHASE1 --> PHASE2

    subgraph PHASE2["  🔵 PHASE 2 — Build & Ship  "]
        CICD["⚡ CI/CD<br/>Pipelines"]:::blue
        DOCKER["🐳 Containers<br/>& Docker"]:::blue
        K8S["☸️ Kubernetes<br/>& Helm"]:::blue
        CICD --> K8S
        DOCKER --> K8S
    end

    PHASE2 --> PHASE3

    subgraph PHASE3["  🟣 PHASE 3 — Infrastructure  "]
        IAC["🏗️ Infrastructure<br/>as Code"]:::purple
        GITOPS["🔄 GitOps<br/>ArgoCD"]:::purple
        CLOUD["☁️ Cloud<br/>AWS / Azure / GCP"]:::purple
        IAC --> CLOUD
        GITOPS --> CLOUD
    end

    PHASE3 --> PHASE4

    subgraph PHASE4["  🔴 PHASE 4 — Reliability  "]
        SRE["📘 SRE<br/>Fundamentals"]:::red
        SLOS["📊 SLOs<br/>& Error Budgets"]:::red
        OBS["🔭 Observability<br/>Metrics · Logs · Traces"]:::red
        INCIDENT["🚨 Incident<br/>Management"]:::red
        CHAOS["💥 Chaos<br/>Engineering"]:::red
        SRE --> SLOS
        SRE --> OBS
        SLOS --> INCIDENT
        OBS --> INCIDENT
        INCIDENT --> CHAOS
    end

    PHASE4 --> PHASE5

    subgraph PHASE5["  🟡 PHASE 5 — Intelligent Ops  "]
        AIOPS["🧠 AIOps<br/>Fundamentals"]:::gold
        ANOMALY["📉 Anomaly<br/>Detection"]:::gold
        LOG["📝 Log<br/>Intelligence"]:::gold
        LLMOPS["🤖 LLMOps"]:::gold
        PREDICT["⚡ Predictive<br/>Scaling"]:::gold
        AIOPS --> ANOMALY
        AIOPS --> LOG
        ANOMALY --> LLMOPS
        LOG --> PREDICT
    end

    PHASE5 --> FINISH["🏆 PRODUCTION-READY<br/>ENGINEER"]:::finish

    classDef start fill:#00d4ff,stroke:#0097a7,color:#000,stroke-width:3px,font-weight:bold
    classDef green fill:#1a1a2e,stroke:#4caf50,color:#fff,stroke-width:2px
    classDef blue fill:#16213e,stroke:#42a5f5,color:#fff,stroke-width:2px
    classDef purple fill:#1b1040,stroke:#ab47bc,color:#fff,stroke-width:2px
    classDef red fill:#2a0a0a,stroke:#ef5350,color:#fff,stroke-width:2px
    classDef gold fill:#1a1500,stroke:#ffc107,color:#fff,stroke-width:2px
    classDef finish fill:#f4c542,stroke:#f9a825,color:#000,stroke-width:3px,font-weight:bold
```

<p align="center">
  <sub>🟢 Foundations → 🔵 Build & Ship → 🟣 Infrastructure → 🔴 Reliability → 🟡 Intelligent Ops → 🏆 Production-Ready</sub>
</p>

---

## 📂 Repository Structure

```
zero-to-sre/
│
├── 🔧 01-devops/                      # DevOps Pillar (10 modules)
│   ├── 01-linux-fundamentals/         ✅  + system healthcheck script
│   ├── 02-networking-basics/          ✅  + network debug toolkit
│   ├── 03-git-version-control/        ✅
│   ├── 04-ci-cd-pipelines/            ✅  (GitHub Actions, Jenkins, GitLab CI)
│   ├── 05-containerization/           ✅  (Dockerfile, Compose, Podman)
│   ├── 06-container-orchestration/    ✅  (K8s manifests + Helm chart)
│   ├── 07-infrastructure-as-code/     ✅  (Terraform AWS/Azure/GCP + Ansible)
│   ├── 08-gitops/                     ✅  (ArgoCD + FluxCD)
│   ├── 09-platform-engineering/       ✅
│   └── 10-cloud-engineering/          ✅  ☁️ AWS + Azure + GCP
│
├── 🔥 02-sre/                         # SRE Pillar (7 modules)
│   ├── 01-sre-fundamentals/           ✅
│   ├── 02-slos-slas-slis/             ✅  + SLO tracker script
│   ├── 03-observability/              ✅  (Prometheus + Grafana + Jaeger + ELK)
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
| 10 | [**☁️ Cloud Engineering**](./01-devops/10-cloud-engineering/) | AWS, Azure, GCP — services, CLI, architecture, cost optimization | 🟡 Intermediate | ✅ Complete |

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
| [☁️ Cloud CLI Cheatsheet](./cheatsheets/cloud-cli-cheatsheet.md) | AWS, Azure, GCP commands side-by-side |
| [Helm Cheatsheet](./cheatsheets/helm-cheatsheet.md) | Install, upgrade, debug, chart development |
| [DevOps Interview Q&A](./interview-prep/devops-questions.md) | Beginner to advanced questions |
| [SRE Interview Q&A](./interview-prep/sre-questions.md) | Google-style SRE interview prep |
| [Kubernetes Interview Q&A](./interview-prep/kubernetes-questions.md) | Pods, networking, security, debugging |
| [☁️ Cloud Interview Q&A](./interview-prep/cloud-questions.md) | AWS, Azure, GCP — beginner to advanced |
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

## 👨‍💻 Author

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&duration=3000&pause=1000&color=00D4FF&center=true&vCenter=true&repeat=true&width=600&lines=K+A+THEJAS;DevOps+%26+Cloud+Engineer;Building+Reliable+Infrastructure+at+Scale" alt="K A THEJAS" />

<br />

### 🚀 **K A THEJAS**

#### **DevOps Engineer | Cloud Engineer**

<br />

<a href="https://github.com/thejas0501"><img src="https://img.shields.io/badge/GitHub-thejas0501-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" /></a>
<a href="https://linkedin.com/in/thejas0501"><img src="https://img.shields.io/badge/LinkedIn-K_A_THEJAS-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
<a href="mailto:thejas0501@gmail.com"><img src="https://img.shields.io/badge/Gmail-thejas0501-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email" /></a>

<br /><br />

**🛠️ Tech Stack & Expertise**

<img src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="AWS" />
<img src="https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white" alt="Azure" />
<img src="https://img.shields.io/badge/GCP-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white" alt="GCP" />
<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white" alt="Terraform" />
<br />
<img src="https://img.shields.io/badge/Ansible-EE0000?style=for-the-badge&logo=ansible&logoColor=white" alt="Ansible" />
<img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus" />
<img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana" />
<img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=for-the-badge&logo=argo&logoColor=white" alt="ArgoCD" />
<img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white" alt="GitHub Actions" />
<img src="https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black" alt="Linux" />
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />

<br /><br />

> *🔧 Passionate about building reliable, scalable, and automated cloud infrastructure.*
> *📚 This repository is my contribution to the DevOps & SRE community — built from real-world experience and industry best practices.*

<br />

</div>

---

<p align="center">
  <strong>Built with ❤️ by K A THEJAS for the DevOps & SRE community</strong>
  <br />
  <sub>If this helped you, consider giving it a ⭐ — it helps others find it too!</sub>
  <br /><br />
  <img src="https://img.shields.io/badge/101_Files-13%2C254_Lines-00d4ff?style=flat-square" alt="Repo Stats" />
  <img src="https://img.shields.io/badge/22_Modules-7_Cheatsheets-f4c542?style=flat-square" alt="Content" />
  <img src="https://img.shields.io/badge/9_Scripts-10_Projects-43a047?style=flat-square" alt="Code" />
</p>

