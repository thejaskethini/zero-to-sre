# 🔭 Observability & Monitoring Cheatsheet

> The three pillars of observability — Metrics, Logs, Traces — plus the Golden Signals framework used at Google/FAANG.

---

## 📊 The Four Golden Signals (Google SRE)

```
1. LATENCY    → How long requests take (p50, p95, p99)
2. TRAFFIC    → Demand on the system (requests/sec)
3. ERRORS     → Rate of failed requests (5xx, timeouts)
4. SATURATION → How "full" the system is (CPU, memory, disk, connections)

USE Method (Brendan Gregg — for infrastructure):
  U → Utilization: % time resource is busy
  S → Saturation: Queue depth / backlog
  E → Errors: Error count for resource

RED Method (for microservices):
  R → Rate: Requests per second
  E → Errors: Failed requests per second
  D → Duration: Distribution of request latencies
```

## 📈 Prometheus & PromQL Essentials

```promql
# Request Rate (Traffic)
rate(http_requests_total[5m])
sum(rate(http_requests_total[5m])) by (service)

# Error Rate
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) * 100

# Latency (p99)
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

# Saturation
node_cpu_seconds_total
node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
node_filesystem_avail_bytes / node_filesystem_size_bytes

# Alert: High Error Rate
- alert: HighErrorRate
  expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) > 0.05
  for: 5m
  labels:
    severity: critical
  annotations:
    summary: "Error rate > 5% for 5 minutes"
```

## 📋 Structured Logging Best Practices

```json
{
  "timestamp": "2026-01-15T10:30:00.123Z",
  "level": "error",
  "service": "payment-api",
  "trace_id": "abc123def456",
  "span_id": "span789",
  "message": "Payment processing failed",
  "error": "insufficient_funds",
  "user_id": "usr_12345",
  "amount": 99.99,
  "duration_ms": 234,
  "environment": "production"
}
```

```bash
# ELK Stack queries (Kibana KQL)
level: "error" AND service: "payment-api"
status >= 500 AND response_time > 2000
message: "timeout" AND NOT service: "health-check"

# Loki LogQL
{service="payment-api"} |= "error"
{namespace="production"} | json | duration > 2s
sum(rate({service="api"} |= "error" [5m])) by (endpoint)
```

## 🔗 Distributed Tracing

```
TRACE STRUCTURE:
──────────────────────────────────────────
Trace (end-to-end request)
├── Span: API Gateway (2ms)
├── Span: Auth Service (15ms)
├── Span: Order Service (45ms)
│   ├── Span: DB Query (20ms)
│   └── Span: Cache Lookup (1ms)
└── Span: Notification Service (30ms)

TOOLS:
  Jaeger         → Open-source, CNCF graduated
  Zipkin         → Open-source, lightweight
  AWS X-Ray      → AWS native
  Datadog APM    → Commercial, full-featured
  OpenTelemetry  → Vendor-neutral standard (USE THIS)
```

## 🎯 SLI/SLO/SLA (Google SRE Framework)

```
SLI (Service Level Indicator):
  = A measurable metric of service behavior
  Examples:
    - Request latency < 200ms (p99)
    - Availability = successful requests / total requests
    - Throughput = requests processed per second

SLO (Service Level Objective):
  = Target value for an SLI
  Examples:
    - 99.9% of requests complete in < 200ms
    - 99.95% availability per month
    - Error rate < 0.1%

SLA (Service Level Agreement):
  = SLO + consequences (contractual)
  Example: 99.9% uptime; below = service credits

ERROR BUDGET:
  = 100% - SLO = allowed downtime
  99.9% SLO = 0.1% budget = 43.8 min/month
  99.95% SLO = 0.05% budget = 21.9 min/month
  99.99% SLO = 0.01% budget = 4.38 min/month

  Error budget spent → freeze deployments, focus on reliability
  Error budget remaining → ship features faster
```

## 🛠️ Grafana Dashboard Patterns

```
PRODUCTION DASHBOARD LAYOUT:
──────────────────────────────────────────
Row 1: Service Health Overview
  ├── Traffic (req/s) — Time series
  ├── Error Rate (%) — Stat panel with thresholds
  ├── p50/p95/p99 Latency — Time series
  └── Active Instances — Stat panel

Row 2: Infrastructure
  ├── CPU Usage by Instance — Time series
  ├── Memory Usage — Gauge
  ├── Disk I/O — Time series
  └── Network Traffic — Time series

Row 3: Dependencies
  ├── Database Query Time — Time series
  ├── Cache Hit Rate — Stat panel
  ├── Queue Depth — Time series
  └── External API Latency — Time series

Row 4: Business Metrics
  ├── Orders/min — Time series
  ├── Revenue/hour — Stat panel
  ├── Active Users — Time series
  └── Conversion Rate — Gauge
```

## 🚨 Alerting Best Practices

```
ALERT SEVERITY LEVELS:
──────────────────────────────────────────
P1 (Critical): Customer-facing outage → Page on-call, all hands
P2 (High):     Degraded service → Page on-call during business hours
P3 (Medium):   Non-critical issue → Ticket, fix within 24h
P4 (Low):      Cosmetic/minor → Backlog

ALERT RULES:
──────────────────────────────────────────
✅ DO:
  - Alert on symptoms (high latency), not causes (high CPU)
  - Use multi-window, multi-burn-rate alerts
  - Include runbook links in every alert
  - Test alerts regularly (chaos engineering)

❌ DON'T:
  - Alert on metrics you won't act on (alert fatigue)
  - Use static thresholds for dynamic workloads
  - Page for non-urgent issues (use tickets)
  - Create alerts without corresponding runbooks
```

---

> 💡 **FAANG Principle:** "If you can't measure it, you can't manage it." Every production service must have dashboards, alerts, and SLOs on day one — not as an afterthought.
