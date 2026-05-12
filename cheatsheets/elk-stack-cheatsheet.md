# 📚 ELK Stack Cheatsheet

> Elasticsearch + Logstash + Kibana — log aggregation, search, dashboards, and production management.

---

## 🔍 Elasticsearch Query DSL

```json
// Match (full-text search)
GET /logs-*/_search
{
  "query": {
    "match": { "message": "connection timeout" }
  }
}

// Bool query (complex filters)
GET /logs-*/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": { "level": "error" } }
      ],
      "filter": [
        { "term": { "service": "api-server" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ],
      "must_not": [
        { "term": { "status": 404 } }
      ]
    }
  },
  "sort": [{ "@timestamp": "desc" }],
  "size": 50
}

// Aggregations
GET /logs-*/_search
{
  "size": 0,
  "aggs": {
    "error_count_by_service": {
      "terms": { "field": "service.keyword", "size": 10 },
      "aggs": {
        "error_rate": {
          "date_histogram": {
            "field": "@timestamp",
            "calendar_interval": "1h"
          }
        }
      }
    },
    "status_codes": {
      "terms": { "field": "status", "size": 20 }
    },
    "avg_response_time": {
      "avg": { "field": "response_time" }
    },
    "p99_latency": {
      "percentiles": { "field": "response_time", "percents": [50, 95, 99] }
    }
  }
}
```

## 🔧 Elasticsearch Operations

```bash
# Cluster health
curl -s localhost:9200/_cluster/health?pretty
curl -s localhost:9200/_cat/health?v
curl -s localhost:9200/_cat/nodes?v
curl -s localhost:9200/_cat/indices?v&s=store.size:desc

# Index management
curl -s localhost:9200/_cat/indices/logs-*?v&s=index
curl -X DELETE localhost:9200/logs-2024.01.01
curl -s localhost:9200/logs-*/_count

# Shard allocation
curl -s localhost:9200/_cat/shards?v&s=state
curl -s localhost:9200/_cat/allocation?v
curl -s localhost:9200/_cluster/allocation/explain?pretty
```

## 📡 Logstash Pipeline

```ruby
# /etc/logstash/conf.d/pipeline.conf
input {
  beats {
    port => 5044
  }
  kafka {
    bootstrap_servers => "kafka:9092"
    topics => ["app-logs"]
    codec => json
    group_id => "logstash-consumers"
  }
}

filter {
  # Parse JSON logs
  json {
    source => "message"
    target => "parsed"
  }

  # Grok pattern (for unstructured logs)
  grok {
    match => {
      "message" => '%{IPORHOST:client_ip} - %{USER:ident} \[%{HTTPDATE:timestamp}\] "%{WORD:method} %{URIPATHPARAM:request} HTTP/%{NUMBER:httpversion}" %{NUMBER:status} %{NUMBER:bytes}'
    }
  }

  # Date parsing
  date {
    match => ["timestamp", "dd/MMM/yyyy:HH:mm:ss Z"]
    target => "@timestamp"
  }

  # GeoIP enrichment
  geoip {
    source => "client_ip"
    target => "geoip"
  }

  # Drop health checks
  if [request] == "/health" {
    drop {}
  }

  # Add fields
  mutate {
    add_field => { "environment" => "production" }
    remove_field => ["agent", "ecs", "host"]
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "logs-%{[service]}-%{+YYYY.MM.dd}"
    user => "elastic"
    password => "${ES_PASSWORD}"
  }
}
```

## 📦 Filebeat (Log Shipping)

```yaml
# filebeat.yml
filebeat.inputs:
  - type: container
    paths:
      - '/var/lib/docker/containers/*/*.log'
    processors:
      - add_kubernetes_metadata:
          host: ${NODE_NAME}
          matchers:
            - logs_path:
                logs_path: "/var/lib/docker/containers/"

  - type: log
    paths:
      - /var/log/nginx/access.log
    fields:
      service: nginx
    json.keys_under_root: true

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "filebeat-%{+yyyy.MM.dd}"

# Or send to Logstash
output.logstash:
  hosts: ["logstash:5044"]
```

## 📊 Index Lifecycle Management (ILM)

```json
// PUT _ilm/policy/logs-policy
{
  "policy": {
    "phases": {
      "hot": {
        "min_age": "0ms",
        "actions": {
          "rollover": {
            "max_primary_shard_size": "50gb",
            "max_age": "1d"
          },
          "set_priority": { "priority": 100 }
        }
      },
      "warm": {
        "min_age": "7d",
        "actions": {
          "shrink": { "number_of_shards": 1 },
          "forcemerge": { "max_num_segments": 1 },
          "set_priority": { "priority": 50 }
        }
      },
      "cold": {
        "min_age": "30d",
        "actions": {
          "freeze": {},
          "set_priority": { "priority": 0 }
        }
      },
      "delete": {
        "min_age": "90d",
        "actions": { "delete": {} }
      }
    }
  }
}
```

## 🐞 Performance Tuning

```
ELASTICSEARCH:
  - Heap: 50% of RAM, max 31GB (compressed oops)
  - Shards: aim for 20-40GB per shard
  - Replicas: 1 for production (2 for critical)
  - Refresh interval: 30s for logs (default 1s is too frequent)
  - Bulk indexing: batch size 5-15MB

LOGSTASH:
  - Pipeline workers: match CPU cores
  - Batch size: 125-500
  - Pipeline.ordered: auto

FILEBEAT:
  - Bulk max size: 2048 events
  - Harvesters: limit per input to prevent FD exhaustion
```

## 🎯 FAANG Interview Q&A

```
Q: ELK vs Loki+Grafana for log management?
A: ELK: full-text search, structured queries, aggregations.
   Best for complex log analysis and compliance.
   Loki: label-based indexing (like Prometheus), much cheaper
   storage, simpler operations. Best for K8s-native log tailing.
   ELK for analytics, Loki for operational log viewing.

Q: How do you handle high-volume log ingestion?
A: 1. Kafka as buffer between Filebeat and Logstash
   2. Logstash pipeline workers = CPU cores
   3. Bulk indexing with appropriate batch sizes
   4. ILM for automatic index lifecycle management
   5. Hot-warm-cold architecture for cost optimization
   6. Drop noisy/health-check logs early in pipeline

Q: How do you size an Elasticsearch cluster?
A: Calculate: daily_ingest × retention_days × (1 + replicas)
   Add 15% overhead. Shard size: 20-40GB each.
   Example: 100GB/day × 30 days × 2 replicas = 6TB
   Minimum 3 master nodes, data nodes sized for storage + CPU.
```

---

> 💡 **Production Rule:** Always use ILM policies. Always put Kafka between log shippers and Elasticsearch for buffering. Monitor cluster health daily — a yellow cluster is a ticking time bomb.
