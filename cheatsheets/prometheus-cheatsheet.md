# 📊 Prometheus & PromQL Cheatsheet

> Essential queries for monitoring and alerting.

---

## 🔍 Basic Queries

```promql
# Instant vector — current value
up                                          # Is target up? (1=yes, 0=no)
http_requests_total                        # Total requests (counter)
process_resident_memory_bytes              # Memory usage (gauge)

# Range vector — values over time
http_requests_total[5m]                    # Values in last 5 minutes
http_requests_total[1h]                    # Values in last 1 hour
```

## 📈 Rate & Increase

```promql
# rate() — Per-second average rate (for counters)
rate(http_requests_total[5m])              # Request rate

# irate() — Instant rate (last 2 data points)
irate(http_requests_total[5m])             # Spikier, more reactive

# increase() — Total increase over time window
increase(http_requests_total[1h])          # Total requests in last hour
```

## ➕ Aggregation

```promql
# Sum across all instances
sum(rate(http_requests_total[5m]))

# Sum by label
sum by (service) (rate(http_requests_total[5m]))
sum by (method, status) (rate(http_requests_total[5m]))

# Average, min, max
avg(rate(http_requests_total[5m]))
min by (instance) (node_filesystem_avail_bytes)
max by (instance) (process_resident_memory_bytes)

# Count distinct
count by (job) (up)

# Top-K
topk(5, sum by (service) (rate(http_requests_total[5m])))
```

## 📊 The 4 Golden Signals

```promql
# 1. LATENCY — Response time percentiles
histogram_quantile(0.50, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))  # p50
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))  # p95
histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))  # p99

# 2. TRAFFIC — Request rate
sum(rate(http_requests_total[5m]))

# 3. ERRORS — Error percentage
sum(rate(http_requests_total{status=~"5.."}[5m]))
  / sum(rate(http_requests_total[5m])) * 100

# 4. SATURATION — Resource utilization
# CPU
100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)
# Memory
(1 - node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) * 100
# Disk
(1 - node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100
```

## 🚨 Alerting Queries

```promql
# High error rate (>5% for 5 min)
sum(rate(http_requests_total{status=~"5.."}[5m])) by (service)
  / sum(rate(http_requests_total[5m])) by (service) > 0.05

# High latency (p95 > 500ms)
histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le, service)) > 0.5

# Pod not ready
kube_pod_status_ready{condition="false"} == 1

# Node disk filling up (predict when it'll be full)
predict_linear(node_filesystem_avail_bytes[6h], 24*3600) < 0
```

## 🔧 Useful Functions

```promql
# Math
abs(value)                                 # Absolute value
ceil(value)                                # Round up
floor(value)                               # Round down
round(value, 0.1)                          # Round to precision

# Time
time()                                     # Current Unix timestamp
timestamp(metric)                          # When metric was last scraped
day_of_week()                              # 0=Sun, 6=Sat
hour()                                     # Current hour (0-23)

# Labels
label_replace(metric, "dst", "$1", "src", "regex")  # Modify labels
label_join(metric, "dst", ",", "src1", "src2")       # Join labels

# Predictions
predict_linear(metric[1h], 3600)           # Predict value in 1 hour
deriv(metric[5m])                          # Rate of change (gauge)
delta(metric[5m])                          # Difference over time (gauge)
```

## 🏷️ Label Matchers

```promql
metric{label="exact"}                      # Exact match
metric{label!="value"}                     # Not equal
metric{label=~"api|web"}                   # Regex match
metric{label!~"test.*"}                    # Negative regex
metric{label=~".+"}                        # Has label (non-empty)
```

---

> 💡 **Tips:** Always use `rate()` for counters, never raw values. Use `by()` to control aggregation dimensions. Use `predict_linear()` for proactive alerting.
