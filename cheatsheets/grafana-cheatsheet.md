# 📊 Grafana Cheatsheet

> Dashboards, data sources, alerting, provisioning, and production dashboard patterns.

---

## 📦 Installation

```bash
# Docker
docker run -d -p 3000:3000 --name grafana grafana/grafana-oss

# Helm (Kubernetes)
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana -n monitoring --create-namespace \
  --set adminPassword='admin' --set persistence.enabled=true

# Default login: admin / admin
```

## 📡 Data Sources

```yaml
# Provisioning via YAML (GitOps-friendly)
# /etc/grafana/provisioning/datasources/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    jsonData:
      timeInterval: 15s

  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100

  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686

  - name: PostgreSQL
    type: postgres
    url: postgres:5432
    database: metrics
    user: grafana
    secureJsonData:
      password: $POSTGRES_PASSWORD
```

## 📐 Essential PromQL for Dashboards

```promql
# Request Rate (Traffic)
sum(rate(http_requests_total[5m])) by (service)

# Error Rate (%)
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
/ sum(rate(http_requests_total[5m])) by (service) * 100

# Latency Percentiles
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))

# CPU Usage
100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance) * 100)

# Memory Usage (%)
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100

# Disk Usage (%)
(1 - node_filesystem_avail_bytes{mountpoint="/"} / node_filesystem_size_bytes{mountpoint="/"}) * 100

# Pod restarts
sum(increase(kube_pod_container_status_restarts_total[1h])) by (pod) > 0

# Container CPU throttling
sum(rate(container_cpu_cfs_throttled_periods_total[5m])) by (pod)
/ sum(rate(container_cpu_cfs_periods_total[5m])) by (pod) * 100
```

## 🎛️ Variables & Templating

```
# Dashboard variables (dynamic dropdowns)
Type: Query
Query: label_values(http_requests_total, service)     # All service names
Query: label_values(node_cpu_seconds_total, instance)  # All instances
Query: label_values(kube_pod_info{namespace="$namespace"}, pod)  # Filtered

Type: Custom
Values: 5m,15m,30m,1h,6h,24h                         # Time range selector

Type: Interval
Values: 1m,5m,15m,1h                                  # Rate interval

# Using variables in queries
rate(http_requests_total{service="$service"}[$__rate_interval])
```

## 🚨 Alerting

```yaml
# Grafana alert rule (YAML provisioning)
apiVersion: 1
groups:
  - orgId: 1
    name: SRE Alerts
    folder: Production
    interval: 1m
    rules:
      - uid: high-error-rate
        title: High Error Rate
        condition: C
        data:
          - refId: A
            queryType: ''
            model:
              expr: sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100
          - refId: C
            queryType: ''
            model:
              type: threshold
              conditions:
                - evaluator:
                    type: gt
                    params: [5]
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: 'Error rate is {{ $value }}%'
          runbook_url: https://wiki.internal/runbooks/high-error-rate

# Contact points
contactPoints:
  - name: slack-critical
    type: slack
    settings:
      url: https://hooks.slack.com/services/xxx
      channel: '#sre-alerts'
  - name: pagerduty
    type: pagerduty
    settings:
      integrationKey: xxx
```

## 📊 Production Dashboard Layout

```
ROW 1: SERVICE OVERVIEW (Stat + Gauge panels)
┌──────────┬──────────┬──────────┬──────────┐
│ Requests │  Error   │  p99     │  Active  │
│  /sec    │  Rate %  │ Latency  │ Instances│
│  [Stat]  │ [Gauge]  │  [Stat]  │  [Stat]  │
└──────────┴──────────┴──────────┴──────────┘

ROW 2: TRAFFIC & ERRORS (Time series)
┌────────────────────────┬────────────────────────┐
│   Request Rate by      │   Error Rate by        │
│   Service (time series)│   Status Code          │
└────────────────────────┴────────────────────────┘

ROW 3: LATENCY (Time series + Heatmap)
┌────────────────────────┬────────────────────────┐
│   p50/p95/p99 Latency  │  Latency Heatmap       │
│   (time series)        │  (histogram_quantile)  │
└────────────────────────┴────────────────────────┘

ROW 4: INFRASTRUCTURE (Time series)
┌──────────┬──────────┬──────────┬──────────┐
│ CPU by   │ Memory   │ Disk I/O │ Network  │
│ Instance │ Usage    │          │ Traffic  │
└──────────┴──────────┴──────────┴──────────┘

ROW 5: DEPENDENCIES (Time series)
┌────────────────────────┬────────────────────────┐
│  Database Query Time   │  Cache Hit Rate /      │
│  + Connection Pool     │  Queue Depth           │
└────────────────────────┴────────────────────────┘
```

## 🏗️ Dashboard Provisioning (GitOps)

```yaml
# /etc/grafana/provisioning/dashboards/dashboards.yml
apiVersion: 1
providers:
  - name: 'production-dashboards'
    orgId: 1
    folder: 'Production'
    type: file
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true
```

```bash
# Export dashboard JSON
curl -H "Authorization: Bearer $API_KEY" \
  http://grafana:3000/api/dashboards/uid/abc123 | jq .dashboard > dashboard.json

# Import dashboard
curl -X POST -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @dashboard.json http://grafana:3000/api/dashboards/db
```

## 🎯 FAANG Interview Q&A

```
Q: How do you design a production monitoring dashboard?
A: Follow the Four Golden Signals layout:
   Row 1: Traffic (req/s), Errors (%), Latency (p99), Saturation
   Row 2-3: Detailed time series for each signal
   Row 4: Infrastructure metrics
   Row 5: Dependencies. Use variables for service/env selection.
   Add alerts directly to panels with runbook links.

Q: Grafana vs Datadog dashboards?
A: Grafana: open-source, any data source, self-hosted, free.
   Datadog: SaaS, built-in agents, APM correlation, costly at scale.
   Grafana wins on flexibility and cost. Datadog wins on ease of setup.

Q: How do you prevent dashboard sprawl?
A: Standardized templates per service type, folder organization,
   naming conventions, provisioning via code (GitOps),
   dashboard review process, auto-delete unused dashboards.
```

---

> 💡 **Dashboard Rule:** A good dashboard answers "Is the service healthy?" in 5 seconds. If you need to scroll or click to find the answer, the layout needs work.
