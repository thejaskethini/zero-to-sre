# 🧠 SRE Interview Cheatsheet (Google/FAANG Level)

> The concepts, frameworks, and answers that FAANG interviewers expect from SRE candidates.

---

## 📐 Core SRE Concepts (Know These Cold)

```
SLI (Service Level Indicator):
  A quantitative measure of service behavior.
  "What we measure" — latency p99, error rate, throughput.

SLO (Service Level Objective):
  A target value or range for an SLI.
  "What we promise internally" — 99.9% availability per quarter.

SLA (Service Level Agreement):
  An SLO with business consequences.
  "What we promise customers" — 99.9% uptime or service credits.

ERROR BUDGET:
  = 100% - SLO = allowed unreliability
  99.9% → 43.8 min downtime/month
  99.95% → 21.9 min/month
  99.99% → 4.38 min/month
  Policy: Budget exhausted → freeze deploys, focus on reliability.

TOIL:
  Manual, repetitive, automatable, tactical, no lasting value.
  Google target: < 50% time on toil.
  If it can be automated, it should be automated.

ELIMINATION OF TOIL EXAMPLES:
  Manual deploys → CI/CD pipeline
  Manual scaling → HPA/autoscaling
  Manual cert renewal → cert-manager/Let's Encrypt
  Manual runbooks → self-healing automation
```

## 🔥 Reliability Patterns

```
CIRCUIT BREAKER:
  Closed → requests flow normally
  Open → requests fail fast (don't overwhelm failing service)
  Half-Open → try a few requests to test recovery
  Tools: Hystrix, Resilience4j, Istio

RETRY WITH EXPONENTIAL BACKOFF + JITTER:
  Attempt 1: wait 1s + random(0, 500ms)
  Attempt 2: wait 2s + random(0, 1000ms)
  Attempt 3: wait 4s + random(0, 2000ms)
  MAX retries: 3-5 (never infinite)
  Jitter prevents thundering herd.

BULKHEAD:
  Isolate failures — one component's failure doesn't cascade.
  Example: Separate thread pools per downstream service.

TIMEOUT BUDGETS:
  Total request budget: 3s
  ├── Auth service: 200ms
  ├── API logic: 500ms
  ├── Database: 1s
  └── External API: 1s
  Each hop gets a portion; don't let one service consume all.

GRACEFUL DEGRADATION:
  Full service → Feature flags → Read-only mode → Static page
  Example: Cart service down → show cached cart, disable checkout.
```

## 💬 Common Interview Questions & Frameworks

```
Q: "How would you improve the reliability of service X?"

FRAMEWORK:
  1. Define SLIs (latency, errors, saturation)
  2. Set SLOs with stakeholders
  3. Measure current performance vs SLOs
  4. Identify top reliability risks:
     - Single points of failure?
     - No autoscaling?
     - Missing health checks?
     - No circuit breakers?
  5. Prioritize by error budget burn rate
  6. Implement: redundancy, caching, circuit breakers, retries
  7. Add observability: dashboards, alerts, distributed tracing
  8. Run game days / chaos engineering


Q: "Walk me through a production incident you handled."

STAR FORMAT:
  Situation: What was the service? What was the impact?
  Task: What was your role? (IC / Incident Commander)
  Action: Step-by-step what you did
    → Detected via [alert/dashboard]
    → Triaged: [user impact, blast radius]
    → Mitigated: [rollback/scale/failover]
    → Root caused: [specific technical detail]
  Result: Resolution time, users impacted, follow-up actions


Q: "Design the monitoring for a microservices system."

ANSWER STRUCTURE:
  1. Four Golden Signals per service
  2. Infrastructure metrics (CPU, memory, disk, network)
  3. Business metrics (orders/min, revenue)
  4. Distributed tracing (OpenTelemetry)
  5. Structured logging (JSON → ELK/Loki)
  6. Alerting with severity levels + runbooks
  7. SLO dashboards with error budget tracking
```

## 🏗️ Infrastructure Design Patterns

```
HIGH AVAILABILITY:
  Multi-AZ deployment (minimum 2 AZs)
  Auto-scaling groups (min 2, desired 3+)
  Database: Primary + read replicas + automated failover
  Load balancer health checks (10s interval, 3 failures = unhealthy)

DISASTER RECOVERY STRATEGIES:
  Backup & Restore:  RPO: hours, RTO: hours, Cost: $
  Pilot Light:       RPO: minutes, RTO: 10-30min, Cost: $$
  Warm Standby:      RPO: seconds, RTO: minutes, Cost: $$$
  Multi-Region Active: RPO: ~0, RTO: ~0, Cost: $$$$

  RPO = Recovery Point Objective (how much data can you lose?)
  RTO = Recovery Time Objective (how fast must you recover?)

CAPACITY PLANNING:
  1. Measure current utilization
  2. Identify growth rate (users, data, traffic)
  3. Project 6-12 months ahead
  4. Add 30% headroom for spikes
  5. Plan for N+1 redundancy (lose 1 instance, still handle load)
```

## 🧪 Chaos Engineering

```
PRINCIPLES:
  1. Define "steady state" (normal SLI values)
  2. Hypothesize: "system will tolerate X failure"
  3. Introduce failure in production (controlled)
  4. Observe: did SLOs hold?
  5. Fix what broke

EXPERIMENTS TO RUN:
  ├── Kill a pod / instance → Does traffic reroute?
  ├── Increase latency to DB → Do timeouts trigger correctly?
  ├── Fill disk to 95% → Does alerting fire?
  ├── DNS failure → Does the app have fallbacks?
  ├── Dependency outage → Does circuit breaker activate?
  └── AZ failure → Does multi-AZ failover work?

TOOLS:
  Chaos Monkey (Netflix) → Random instance termination
  Litmus Chaos → Kubernetes-native chaos
  Gremlin → Enterprise chaos platform
  tc (traffic control) → Network latency injection
  stress-ng → CPU/memory stress testing
```

## 📊 On-Call Best Practices

```
ON-CALL HYGIENE:
  ├── Max 1 week rotation (2 weeks max)
  ├── Follow-the-sun for global teams
  ├── Primary + secondary on-call
  ├── Target: < 2 pages per shift
  ├── Every alert must be actionable
  ├── Every alert must have a runbook
  └── Compensation: time off or pay

HANDOFF CHECKLIST:
  [ ] Review recent incidents
  [ ] Check pending deployments
  [ ] Verify alert channels working
  [ ] Review known issues document
  [ ] Confirm access to all dashboards
  [ ] Test pager/notification system
```

---

> 💡 **Google SRE Interview Tip:** Interviewers want to see structured thinking, not memorized answers. Use frameworks (STAR, Four Golden Signals, SLI/SLO) to organize your response. Always discuss trade-offs.
