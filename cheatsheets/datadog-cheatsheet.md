# 🐕 Datadog Cheatsheet

> Full-stack observability platform — APM, metrics, logs, synthetics, SLOs, and Kubernetes integration.

---

## 📦 Agent Installation

```bash
# Linux
DD_API_KEY=<YOUR_KEY> DD_SITE="datadoghq.com" bash -c \
  "$(curl -L https://install.datadoghq.com/scripts/install_script_agent7.sh)"

# Docker
docker run -d --name dd-agent \
  -e DD_API_KEY=<YOUR_KEY> \
  -e DD_SITE="datadoghq.com" \
  -e DD_APM_ENABLED=true \
  -e DD_LOGS_ENABLED=true \
  -v /var/run/docker.sock:/var/run/docker.sock:ro \
  -v /proc/:/host/proc/:ro \
  -v /sys/fs/cgroup:/host/sys/fs/cgroup:ro \
  datadog/agent:7

# Kubernetes (Helm)
helm repo add datadog https://helm.datadoghq.com
helm install datadog datadog/datadog \
  --set datadog.apiKey=<YOUR_KEY> \
  --set datadog.appKey=<YOUR_APP_KEY> \
  --set datadog.logs.enabled=true \
  --set datadog.apm.portEnabled=true \
  --set datadog.processAgent.enabled=true \
  -n datadog --create-namespace
```

## 📊 DogStatsD (Custom Metrics)

```python
# Python
from datadog import statsd

statsd.increment('api.requests.count', tags=['service:api', 'env:production'])
statsd.gauge('queue.depth', 42, tags=['queue:orders'])
statsd.histogram('api.request.duration', 0.234, tags=['endpoint:/users'])
statsd.distribution('payment.amount', 99.99, tags=['currency:usd'])
statsd.set('api.unique_users', user_id, tags=['service:api'])
statsd.event('Deployment', 'Deployed v2.0.0', alert_type='info')
statsd.service_check('api.health', statsd.OK)
```

```javascript
// Node.js
const StatsD = require('hot-shots');
const dogstatsd = new StatsD({ host: 'localhost', port: 8125 });

dogstatsd.increment('api.requests', 1, { service: 'api', env: 'production' });
dogstatsd.gauge('connections.active', 42);
dogstatsd.histogram('request.duration', responseTime);
```

## 🔍 APM (Tracing)

```bash
# Auto-instrumentation (Node.js)
DD_ENV=production DD_SERVICE=api DD_VERSION=2.0.0 \
  node --require dd-trace/init server.js

# Python
DD_ENV=production DD_SERVICE=api DD_VERSION=2.0.0 \
  ddtrace-run python app.py
```

```javascript
// Manual spans
const tracer = require('dd-trace');
tracer.init({ env: 'production', service: 'api' });

const span = tracer.startSpan('process.payment');
span.setTag('payment.amount', 99.99);
span.setTag('user.id', userId);
try {
  await processPayment();
  span.setTag('payment.status', 'success');
} catch (err) {
  span.setTag('error', err);
} finally {
  span.finish();
}
```

## 📋 Log Management

```yaml
# Kubernetes pod annotations for log collection
metadata:
  annotations:
    ad.datadoghq.com/api.logs: |
      [{
        "source": "nodejs",
        "service": "api-server",
        "log_processing_rules": [{
          "type": "exclude_at_match",
          "name": "exclude_healthcheck",
          "pattern": "GET /health"
        }]
      }]
```

```python
# Structured logging (correlate logs with traces)
import logging
from ddtrace import tracer

logger = logging.getLogger(__name__)

# Datadog auto-injects trace_id and span_id into logs
logger.info("Payment processed", extra={
    "payment_id": "pay_123",
    "amount": 99.99,
    "dd.trace_id": tracer.current_trace_id(),
    "dd.span_id": tracer.current_span_id()
})
```

## 🚨 Monitors & Alerts

```
MONITOR TYPES:
  Metric Monitor    → Alert on metric thresholds
  APM Monitor       → Alert on trace metrics (latency, errors)
  Log Monitor       → Alert on log patterns/counts
  Composite Monitor → Combine multiple monitors (A AND B)
  Anomaly Monitor   → ML-based anomaly detection
  Forecast Monitor  → Predict future threshold breaches
  SLO Monitor       → Alert on SLO burn rate

ALERT CONDITIONS (YAML-style):
  metric: avg:system.cpu.user{service:api} > 80 for 5m
  apm: p99 latency > 2s for service:api
  log: count of "ERROR" > 100 in 5m
  anomaly: anomalies(avg:requests{*}, 'basic', 2) > 0
```

## 📐 SLOs in Datadog

```
SLO TYPES:
  Monitor-based → SLO from existing monitor uptime
  Metric-based  → SLO from custom metric queries

EXAMPLE:
  Name: API Availability
  Type: Metric-based
  Numerator: sum:http.requests{status:2xx,service:api}
  Denominator: sum:http.requests{service:api}
  Target: 99.9% over 30 days

  Error Budget: 0.1% = 43.2 minutes/month
  Alert when: budget consumed > 50% in rolling window
```

## ☸️ Kubernetes Integration

```yaml
# Pod annotations for Datadog
metadata:
  labels:
    tags.datadoghq.com/env: production
    tags.datadoghq.com/service: api
    tags.datadoghq.com/version: "2.0.0"
  annotations:
    # Custom checks
    ad.datadoghq.com/api.check_names: '["http_check"]'
    ad.datadoghq.com/api.init_configs: '[{}]'
    ad.datadoghq.com/api.instances: |
      [{
        "name": "API Health",
        "url": "http://%%host%%:8080/health",
        "timeout": 5
      }]
```

## 💰 Cost Optimization

```
REDUCE DATADOG COSTS:
  1. Use log exclusion filters (drop health checks, debug logs)
  2. Set log retention to minimum needed (15d vs 30d)
  3. Use metrics instead of logs for counting (cheaper)
  4. Exclude namespaces: kube-system, monitoring from APM
  5. Sample traces (not 100% — use DD_TRACE_SAMPLE_RATE=0.1)
  6. Use custom metrics wisely (each costs money)
  7. Archive logs to S3 for long-term (Datadog Rehydration)
  8. Review and remove unused monitors/dashboards
```

## 🎯 FAANG Interview Q&A

```
Q: Datadog vs open-source stack (Prometheus + Grafana + Loki)?
A: Datadog: SaaS, zero ops overhead, unified platform, APM built-in.
   Costs $15-30/host/month + per-GB log pricing.
   Open-source: free, full control, but significant ops overhead.
   Choose Datadog for small teams, open-source for large scale + budget.

Q: How do you correlate logs, traces, and metrics in Datadog?
A: Unified tagging: env, service, version on everything.
   Trace IDs injected into logs automatically.
   Click from error trace → correlated logs → related metrics.
   This is Datadog's killer feature vs fragmented tooling.

Q: How would you set up SLOs in Datadog?
A: 1. Define SLI (metric query: successful / total requests)
   2. Set target (99.9% over 30 days)
   3. Create SLO monitor with burn rate alerts
   4. Add to SLO dashboard for visibility
   5. Alert at 50% and 80% budget consumption
```

---

> 💡 **Cost Rule:** Datadog bills per host, per GB ingested, and per custom metric. Monitor your Datadog bill like infrastructure — set up Datadog usage monitors to alert when costs spike.
