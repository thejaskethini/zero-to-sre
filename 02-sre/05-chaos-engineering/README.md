# 💥 Chaos Engineering

> **"The discipline of experimenting on a system to build confidence in its ability to withstand turbulent conditions in production." — Principles of Chaos Engineering**

<p align="center">
  <img src="https://img.shields.io/badge/Module-Chaos_Engineering-ef5350?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Difficulty-Advanced-ef5350?style=for-the-badge" />
</p>

---

## 📖 Conceptual Overview

Chaos engineering is NOT random destruction. It's **scientific experimentation** applied to production systems.

### The Chaos Experiment Loop

```mermaid
graph LR
    A["1️⃣ Define Steady State"] --> B["2️⃣ Form Hypothesis"]
    B --> C["3️⃣ Introduce Failure"]
    C --> D["4️⃣ Observe Results"]
    D --> E["5️⃣ Fix or Validate"]
    E --> A

    style A fill:#16213e,stroke:#4fc3f7,color:#fff
    style B fill:#16213e,stroke:#f4c542,color:#fff
    style C fill:#b71c1c,stroke:#ef5350,color:#fff
    style D fill:#0f3460,stroke:#43a047,color:#fff
    style E fill:#162447,stroke:#7c4dff,color:#fff
```

**Example Experiment:**
1. **Steady state:** API responds in < 200ms with < 0.1% errors
2. **Hypothesis:** "If we lose 1 of 3 database replicas, the system continues operating within SLO"
3. **Inject failure:** Kill one database replica
4. **Observe:** Did latency increase? Did errors spike? Did failover work?
5. **Result:** Fix the gaps or confirm resilience

---

## 🔑 Key Concepts

### Types of Chaos Experiments

| Category | Experiment | Tools |
|----------|-----------|-------|
| **Infrastructure** | Kill VM/container, fill disk, network partition | Chaos Monkey, Litmus |
| **Application** | Inject latency, return errors, corrupt data | Gremlin, Toxiproxy |
| **Network** | Packet loss, DNS failure, bandwidth throttle | tc (Linux), Chaos Mesh |
| **Dependencies** | External API failure, database down | WireMock, Fault Injection |
| **People** | Game days, unannounced drills | Tabletop exercises |

### Blast Radius Management

```
Start small → Grow confidence → Expand scope

Dev environment → Staging → Canary (1% prod) → Full production
                                                      ↑
                                              Only after proven safe
```

### Game Days

Scheduled chaos experiments where the team:
1. Plans the scenario in advance
2. Has all hands on deck
3. Runs the experiment with a kill switch
4. Practices incident response
5. Holds a debrief afterward

---

## 🏢 Real-world Use Case

### Netflix Simian Army

Netflix pioneered chaos engineering with their **Simian Army**:

| Tool | What It Does |
|------|-------------|
| **Chaos Monkey** | Randomly kills production instances during business hours |
| **Latency Monkey** | Injects artificial delays into services |
| **Chaos Kong** | Simulates entire AWS region failure |
| **Conformity Monkey** | Finds instances not following best practices |

> 🔑 **Key Insight:** Netflix runs Chaos Monkey **every business day** in production. If a service can't handle losing an instance, they want to know at 2 PM, not 2 AM.

---

## ⚠️ Common Pitfalls

| # | Pitfall | How to Avoid |
|---|---------|-------------|
| 1 | Starting in production day one | Start in dev/staging, graduate to production |
| 2 | No kill switch | Always have a way to immediately stop the experiment |
| 3 | No monitoring during experiments | Enhanced monitoring is essential during chaos |
| 4 | Running experiments during incidents | Only run chaos when system is healthy |
| 5 | No buy-in from leadership | Start with game days to build trust |

---

## 📚 Further Reading

| Resource | Type | Description |
|----------|------|-------------|
| [Principles of Chaos](https://principlesofchaos.org/) | 📖 Principles | The foundational document |
| [Chaos Monkey (Netflix)](https://netflix.github.io/chaosmonkey/) | 🔧 Tool | The original chaos tool |
| [Litmus Chaos](https://litmuschaos.io/) | 🔧 Tool | CNCF chaos engineering for K8s |
| [Chaos Mesh](https://chaos-mesh.org/) | 🔧 Tool | CNCF chaos for K8s |
| [Gremlin](https://www.gremlin.com/) | 🔧 Tool | Enterprise chaos platform |
| [Chaos Engineering Book](https://www.oreilly.com/library/view/chaos-engineering/9781492043850/) | 📘 Book | O'Reilly comprehensive guide |

---

<p align="center">
  <a href="../04-incident-management/README.md">⬅️ Previous: Incidents</a> · <a href="../README.md">SRE Home</a> · <a href="../06-capacity-planning/README.md">Next: Capacity ➡️</a>
</p>
