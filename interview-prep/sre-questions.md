# 🎓 SRE Interview Questions

> Curated questions with answers for SRE interviews at Google, Meta, Netflix, and similar companies.

---

## 🟢 Fundamentals

### 1. What is SRE? How does it differ from DevOps?
**Answer:** SRE is a specific implementation of DevOps principles, originated at Google. Key differences: SRE prescribes specific practices (error budgets, SLOs), requires 50% time on engineering, and uses software engineering to solve operations problems. DevOps is a broader cultural movement.

### 2. Explain error budgets.
**Answer:** Error budget = 100% − SLO. If SLO is 99.9%, error budget is 0.1% (43 min/month). When budget is available, teams ship features fast. When exhausted, feature releases freeze and the team focuses on reliability. This aligns dev velocity with operational stability.

### 3. What's the difference between SLI, SLO, and SLA?
**Answer:**
- **SLI** (Indicator): The measurement (e.g., request latency p99)
- **SLO** (Objective): The target (e.g., p99 latency < 300ms, 99.9% of the time)
- **SLA** (Agreement): The contract (e.g., 99.9% uptime or customer gets credits)
- Rule: SLO should be stricter than SLA.

---

## 🟡 Intermediate

### 4. How do you choose the right SLIs?
**Answer:** Focus on user-facing signals. For request-driven services: availability, latency (percentiles), error rate. For data pipelines: freshness, coverage, correctness. Measure from the user's perspective (load balancer/client), not the server.

### 5. Describe the incident management lifecycle.
**Answer:** Detection → Triage → Mitigation → Resolution → Postmortem → Improvement. Key roles: Incident Commander (coordinates), Comms Lead (stakeholders), Operations Lead (debugging). Always prioritize mitigation over root cause during active incidents.

### 6. What is toil and how do you reduce it?
**Answer:** Toil is manual, repetitive, automatable work that scales linearly with service size. Google's rule: ≤ 50% toil. Reduction: automate top toil sources, build self-healing (K8s probes, auto-scaling), create self-service tooling. Track toil hours weekly.

### 7. Explain the four Golden Signals.
**Answer:** (From Google SRE book)
- **Latency:** Time to serve a request (separate success vs error latency)
- **Traffic:** Demand on the system (requests/sec)
- **Errors:** Rate of failed requests (explicit 5xx and implicit like slow responses)
- **Saturation:** How "full" the service is (CPU, memory, queue depth)

---

## 🔴 Advanced

### 8. Design a monitoring and alerting strategy for a new microservice.
**Answer:**
1. **Instrument** the 4 Golden Signals + business metrics
2. **SLO-based alerting** using burn rate (not raw thresholds)
3. **Multi-window alerts:** 1h/6h window for paging, 1d/3d for tickets
4. **Structured logging** with trace/span IDs for correlation
5. **Distributed tracing** for cross-service debugging
6. **Dashboard:** Start with 4 Golden Signals per service
7. **Runbooks** linked to every alert
8. **On-call rotation:** primary + secondary, max 2 incidents/shift

### 9. How would you handle a cascading failure?
**Answer:** Prevention: circuit breakers, bulkheads, timeouts, retry budgets, load shedding, graceful degradation. Detection: monitor dependency health, track error budget burn rate. Response: isolate the failing component, activate fallback, communicate to affected teams. Post-incident: improve circuit breaker configs, add chaos experiments.

### 10. Design an SLO for a payment service.
**Answer:**
- **SLI 1 — Availability:** Proportion of successful payment requests (non-5xx) = `successful requests / total requests`
- **SLO 1:** 99.99% availability (measured over 30-day rolling window)
- **SLI 2 — Latency:** p99 latency of successful payment transactions
- **SLO 2:** p99 < 2 seconds, 99.9% of the time
- **Error budget:** 0.01% = 4.3 minutes/month
- **Alerting:** Burn rate > 14x in 1h window → page; > 6x in 6h → page; > 1x in 3d → ticket

### 11. Your error budget is exhausted with 2 weeks left in the quarter. What do you do?
**Answer:**
1. **Freeze non-critical deployments** until budget recovers
2. **Conduct RCA** on what consumed the budget
3. **Prioritize reliability work:** fix the root causes
4. **Communicate** to product team why feature releases are paused
5. **Review SLO:** Is it too aggressive? Does it reflect user expectations?
6. **Exception process:** If a critical feature must ship, get VP approval with explicit risk acknowledgment

---

## 💡 System Design for SRE

### 12. Design a global load balancing system.
**Key components:** DNS-based (GeoDNS), Anycast, health-checking, failover. Consider: latency-based routing, capacity-aware routing, session stickiness, DDoS mitigation.

### 13. Design a log aggregation pipeline that handles 1TB/day.
**Key components:** Agents (Fluent Bit) → Kafka (buffer) → Processing (Flink/Spark) → Storage (Elasticsearch/S3) → UI (Kibana/Grafana). Consider: schema evolution, retention policies, hot/cold storage tiers, cost optimization.

---

> 💡 **Tip:** Google SRE interviews focus heavily on **system design**, **troubleshooting scenarios**, and **SLO design**. Practice designing monitoring for systems and explaining your on-call philosophy.
