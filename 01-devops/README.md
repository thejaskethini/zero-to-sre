# 🔧 DevOps — Build & Ship

> **DevOps is a set of practices, tools, and cultural philosophies that automate and integrate the processes between software development and IT operations.**

---

## 🗺️ Learning Path

```mermaid
graph LR
    A["🐧 Linux"] --> B["🌐 Networking"]
    B --> C["📦 Git"]
    C --> D["⚡ CI/CD"]
    C --> E["🐳 Docker"]
    D --> F["☸️ Kubernetes"]
    E --> F
    F --> G["🏗️ IaC"]
    F --> H["🔄 GitOps"]
    G --> I["🏭 Platform Eng"]
    H --> I

    style A fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style B fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style C fill:#1a1a2e,stroke:#4fc3f7,color:#fff
    style D fill:#16213e,stroke:#7c4dff,color:#fff
    style E fill:#16213e,stroke:#7c4dff,color:#fff
    style F fill:#16213e,stroke:#7c4dff,color:#fff
    style G fill:#0f3460,stroke:#00e676,color:#fff
    style H fill:#0f3460,stroke:#00e676,color:#fff
    style I fill:#0f3460,stroke:#f4c542,color:#fff
```

---

## 📚 Modules

| # | Module | Description | Difficulty | Status |
|---|--------|-------------|------------|--------|
| 01 | [**Linux Fundamentals**](./01-linux-fundamentals/) | Shell, file systems, processes | 🟢 Beginner | ✅ |
| 02 | [**Networking Basics**](./02-networking-basics/) | TCP/IP, DNS, load balancing | 🟢 Beginner | ✅ |
| 03 | [**Git & Version Control**](./03-git-version-control/) | Branching, rebasing, monorepos | 🟢 Beginner | ✅ |
| 04 | [**CI/CD Pipelines**](./04-ci-cd-pipelines/) | GitHub Actions, Jenkins, GitLab CI | 🟡 Intermediate | ✅ |
| 05 | [**Containerization**](./05-containerization/) | Docker, multi-stage builds, Compose | 🟡 Intermediate | ✅ |
| 06 | [**Container Orchestration**](./06-container-orchestration/) | Kubernetes, Helm, service mesh | 🔴 Advanced | ✅ |
| 07 | [**Infrastructure as Code**](./07-infrastructure-as-code/) | Terraform, Pulumi, state mgmt | 🟡 Intermediate | ✅ |
| 08 | [**GitOps**](./08-gitops/) | ArgoCD, FluxCD, progressive delivery | 🔴 Advanced | ✅ |
| 09 | [**Platform Engineering**](./09-platform-engineering/) | IDPs, Backstage, golden paths | 🔴 Advanced | ✅ |

---

## 💡 Key Principles

| Principle | Description |
|-----------|-------------|
| 🔄 **Continuous Integration** | Merge code frequently, test automatically |
| 🚀 **Continuous Delivery** | Always be ready to deploy to production |
| 🏗️ **Infrastructure as Code** | Treat infrastructure like application code |
| 📊 **Measure Everything** | You can't improve what you can't measure |
| 🤝 **Shared Responsibility** | Dev and Ops are one team |
| 🛡️ **Shift Left** | Find problems early in the pipeline |

---

## 📖 Recommended Books

- 📘 *The Phoenix Project* — Gene Kim
- 📗 *The DevOps Handbook* — Gene Kim, Jez Humble
- 📙 *Accelerate* — Nicole Forsgren, Jez Humble, Gene Kim

---

<p align="center">
  <a href="../README.md">⬅️ Back to Main</a> · <a href="../02-sre/README.md">Next: SRE ➡️</a>
</p>
