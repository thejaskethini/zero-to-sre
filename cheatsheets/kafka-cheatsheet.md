# 📨 Apache Kafka Cheatsheet

> Distributed event streaming — topics, partitions, consumer groups, producers, and production tuning.

---

## 🏗️ Architecture

```
PRODUCER → TOPIC (partitioned) → CONSUMER GROUP

Topic: "orders"
├── Partition 0: [msg1, msg4, msg7, ...]  → Consumer A
├── Partition 1: [msg2, msg5, msg8, ...]  → Consumer B
└── Partition 2: [msg3, msg6, msg9, ...]  → Consumer C

KEY CONCEPTS:
  Broker        → Kafka server node
  Topic         → Named stream of records
  Partition     → Ordered, immutable sequence within a topic
  Offset        → Position of message within partition
  Consumer Group → Set of consumers sharing topic partitions
  Replication   → Copies across brokers for fault tolerance
  Leader        → Partition leader handles reads/writes
  ISR           → In-Sync Replicas (caught up with leader)
```

## 🔧 CLI Commands

```bash
# Topic management
kafka-topics.sh --bootstrap-server localhost:9092 --list
kafka-topics.sh --bootstrap-server localhost:9092 --create \
  --topic orders --partitions 6 --replication-factor 3
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic orders
kafka-topics.sh --bootstrap-server localhost:9092 --alter \
  --topic orders --partitions 12                     # Can only increase
kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic old-topic

# Producer (send messages)
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders
kafka-console-producer.sh --bootstrap-server localhost:9092 --topic orders \
  --property key.separator=: --property parse.key=true
# Type: key1:{"orderId": "123", "amount": 99.99}

# Consumer (read messages)
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders \
  --from-beginning
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders \
  --group my-app --from-beginning                    # With consumer group
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic orders \
  --partition 0 --offset 100                         # Specific partition + offset

# Consumer groups
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-app --describe                          # Show lag
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-app --reset-offsets --topic orders --to-earliest --execute
```

## ⚙️ Producer Configuration

```properties
# Key producer configs
bootstrap.servers=broker1:9092,broker2:9092,broker3:9092

# Durability
acks=all                                              # Wait for all ISR replicas
# acks=1   → Leader only (faster, risk of data loss)
# acks=0   → Fire and forget (fastest, may lose data)
# acks=all → All ISR replicas (safest)

retries=3
retry.backoff.ms=100
delivery.timeout.ms=120000

# Performance
batch.size=16384                                      # 16KB batch
linger.ms=5                                           # Wait 5ms to fill batch
buffer.memory=33554432                                # 32MB buffer
compression.type=lz4                                  # lz4, snappy, gzip, zstd

# Idempotence (exactly-once per partition)
enable.idempotence=true
max.in.flight.requests.per.connection=5
```

## ⚙️ Consumer Configuration

```properties
bootstrap.servers=broker1:9092,broker2:9092,broker3:9092
group.id=order-processor

# Offset management
auto.offset.reset=earliest                            # earliest | latest
enable.auto.commit=false                              # Manual commit (recommended)
# enable.auto.commit=true
# auto.commit.interval.ms=5000

# Performance
max.poll.records=500
max.poll.interval.ms=300000                           # 5 min max processing time
fetch.min.bytes=1
fetch.max.wait.ms=500
session.timeout.ms=45000
heartbeat.interval.ms=15000
```

## 📊 Monitoring & Lag

```bash
# Consumer lag (CRITICAL metric)
kafka-consumer-groups.sh --bootstrap-server localhost:9092 \
  --group my-app --describe
# Look at LAG column — growing lag = consumers can't keep up

# Broker info
kafka-broker-api-versions.sh --bootstrap-server localhost:9092

# Topic partition details
kafka-log-dirs.sh --bootstrap-server localhost:9092 \
  --describe --topic-list orders

# Under-replicated partitions (sign of trouble)
kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --under-replicated-partitions
```

## 🏗️ Production Configuration

```properties
# Broker settings (server.properties)
num.partitions=6                                      # Default partitions
default.replication.factor=3                          # 3 replicas
min.insync.replicas=2                                 # At least 2 ISR for acks=all

# Retention
log.retention.hours=168                               # 7 days
log.retention.bytes=-1                                # No size limit
log.segment.bytes=1073741824                          # 1GB segments
log.cleanup.policy=delete                             # delete | compact

# Compacted topics (keep latest per key)
log.cleanup.policy=compact                            # For changelog/state topics
```

## 🔗 Kafka Connect & Schema Registry

```bash
# Kafka Connect (data integration)
curl localhost:8083/connectors | jq .                 # List connectors
curl localhost:8083/connectors/my-sink/status | jq .  # Connector status

# Schema Registry
curl localhost:8081/subjects | jq .                   # List schemas
curl localhost:8081/subjects/orders-value/versions/latest | jq .
```

## 🎯 FAANG Interview Q&A

```
Q: How do you choose the number of partitions?
A: Partitions = max(producer throughput, consumer throughput).
   More partitions = more parallelism but more overhead.
   Rule of thumb: target throughput / per-partition throughput.
   Start with 6-12 for most topics. Can only increase, never decrease.

Q: How does Kafka guarantee ordering?
A: Ordering is guaranteed WITHIN a partition, not across partitions.
   Use a key (e.g., user_id) to ensure related messages go to
   the same partition. Same key → same partition → ordered processing.

Q: What happens when a consumer crashes?
A: Consumer group detects missed heartbeats → triggers rebalance.
   Partitions of crashed consumer are reassigned to remaining consumers.
   Processing resumes from last committed offset (may cause duplicates
   if auto-commit was pending → design for idempotency).

Q: Explain exactly-once semantics in Kafka.
A: Three levels: at-most-once, at-least-once, exactly-once.
   Exactly-once requires: idempotent producer + transactional writes
   + read_committed isolation. Kafka Streams provides this natively.
   For consumer apps: design for idempotency (at-least-once + dedup).

Q: Kafka vs RabbitMQ?
A: Kafka: high-throughput log (replay, ordering, retention).
   Best for event streaming, event sourcing, analytics.
   RabbitMQ: traditional message broker (routing, priorities, TTL).
   Best for task queues, RPC, complex routing patterns.
   Kafka is append-only log, RabbitMQ deletes after consumption.
```

---

> 💡 **Production Rule:** Monitor consumer lag religiously — it's the #1 indicator of Kafka health. If lag grows, either add consumers or optimize processing. Always use `acks=all` with `min.insync.replicas=2` for durability.
