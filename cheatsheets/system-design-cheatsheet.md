# 🏗️ System Design Cheatsheet (FAANG Interview Level)

> The exact mental models and frameworks used in Google/Meta/Amazon system design interviews and on-the-job architecture decisions.

---

## 📐 The System Design Framework (Use This in Every Interview)

```
1. REQUIREMENTS (5 min)
   ├── Functional: What does the system DO?
   ├── Non-functional: Latency, throughput, availability, consistency
   └── Scale: Users, requests/sec, data size, growth rate

2. ESTIMATION (3 min)
   ├── QPS (Queries Per Second)
   ├── Storage requirements
   ├── Bandwidth requirements
   └── Cache sizing

3. HIGH-LEVEL DESIGN (10 min)
   ├── API design (REST/gRPC endpoints)
   ├── Data model (entities, relationships)
   ├── Core components (services, databases, caches)
   └── Data flow diagram

4. DEEP DIVE (15 min)
   ├── Scaling bottlenecks
   ├── Database choice & partitioning strategy
   ├── Caching strategy
   ├── Consistency vs availability trade-offs
   └── Failure scenarios

5. WRAP UP (2 min)
   ├── Monitoring & alerting
   ├── Bottlenecks & future improvements
   └── Cost optimization
```

## 📊 Back-of-the-Envelope Estimation

```
LATENCY NUMBERS EVERY SRE SHOULD KNOW:
──────────────────────────────────────────
L1 cache reference                    0.5 ns
L2 cache reference                      7 ns
Main memory reference                 100 ns
SSD random read                   150,000 ns  (150 μs)
HDD seek                      10,000,000 ns  (10 ms)
Same datacenter roundtrip        500,000 ns  (0.5 ms)
Cross-continent roundtrip    150,000,000 ns  (150 ms)

SCALE NUMBERS:
──────────────────────────────────────────
1 Million   = 10^6    (1 MB = 1 million bytes)
1 Billion   = 10^9    (1 GB = 1 billion bytes)
1 Trillion  = 10^12   (1 TB = 1 trillion bytes)

QPS ESTIMATION:
──────────────────────────────────────────
100M DAU × 5 actions/day = 500M requests/day
500M / 100,000 sec/day ≈ 5,000 QPS (average)
Peak = 2-3× average ≈ 10,000-15,000 QPS

STORAGE ESTIMATION:
──────────────────────────────────────────
1 Tweet (280 chars)  ≈ 300 bytes
1 Photo (compressed) ≈ 200 KB
1 Video (1 min, 720p) ≈ 10 MB
1 User profile ≈ 1 KB
500M tweets/day × 300B = 150 GB/day ≈ 55 TB/year
```

## ⚖️ CAP Theorem & Consistency Models

```
CAP THEOREM: Pick 2 of 3 (in practice: CP or AP)
──────────────────────────────────────────
CP Systems (Consistency + Partition Tolerance):
  → HBase, MongoDB (default), Redis Cluster, ZooKeeper
  → Use when: Banking, inventory, leader election

AP Systems (Availability + Partition Tolerance):
  → Cassandra, DynamoDB, CouchDB
  → Use when: Social feeds, analytics, shopping cart

CONSISTENCY MODELS:
──────────────────────────────────────────
Strong       → Read always returns latest write (PostgreSQL)
Eventual     → Read may return stale data temporarily (DynamoDB)
Causal       → Preserves cause-effect ordering (MongoDB sessions)
Read-your-writes → Writer always sees own writes
```

## 🗄️ Database Selection Guide

```
RELATIONAL (PostgreSQL, MySQL):
  ✅ ACID transactions, complex queries, joins
  ✅ When: Banking, e-commerce orders, user accounts
  ❌ Hard to scale writes horizontally

DOCUMENT (MongoDB, DynamoDB):
  ✅ Flexible schema, horizontal scaling, fast reads
  ✅ When: User profiles, content management, catalogs
  ❌ No joins, eventual consistency gotchas

WIDE-COLUMN (Cassandra, HBase):
  ✅ Extreme write throughput, time-series, geo-distribution
  ✅ When: Metrics, IoT sensor data, activity logs
  ❌ Limited query patterns

KEY-VALUE (Redis, Memcached):
  ✅ Sub-millisecond reads, simple data model
  ✅ When: Caching, sessions, rate limiting, leaderboards
  ❌ Limited query capability, data size limits

GRAPH (Neo4j, Neptune):
  ✅ Relationship traversal, complex connections
  ✅ When: Social networks, fraud detection, recommendations
  ❌ Not great for simple CRUD

SEARCH (Elasticsearch, OpenSearch):
  ✅ Full-text search, log analytics, aggregations
  ✅ When: Product search, log analysis, monitoring
  ❌ Not a primary data store
```

## 🔧 Core Building Blocks

```
LOAD BALANCERS:
  L4 (TCP): NLB, HAProxy → Raw throughput, simple routing
  L7 (HTTP): ALB, Nginx, Envoy → Path routing, SSL termination, headers

CACHING STRATEGIES:
  Cache-Aside    → App checks cache → miss → read DB → write cache
  Read-Through   → Cache auto-fetches from DB on miss
  Write-Through  → Write to cache + DB simultaneously
  Write-Behind   → Write to cache → async write to DB (risk: data loss)

MESSAGE QUEUES:
  Kafka    → High-throughput, ordered, replay (event streaming)
  RabbitMQ → Flexible routing, priorities (task queues)
  SQS      → Managed, simple, auto-scaling (AWS native)

CDN: CloudFront, Cloudflare → Cache static assets at edge
API Gateway: Kong, AWS API GW → Auth, rate limiting, routing
Service Mesh: Istio, Linkerd → mTLS, traffic management, observability
```

## 🎯 Scaling Patterns

```
HORIZONTAL SCALING:
  ├── Stateless services behind load balancer
  ├── Database sharding (hash-based, range-based, geo-based)
  ├── Read replicas for read-heavy workloads
  └── Microservices decomposition

VERTICAL SCALING:
  └── Bigger machines (quick fix, has ceiling)

DATA PARTITIONING:
  Hash-based:  hash(user_id) % N → Uniform distribution
  Range-based: A-M → Shard 1, N-Z → Shard 2 → Risk: hotspots
  Geo-based:   US → Shard 1, EU → Shard 2 → Compliance-friendly

RATE LIMITING ALGORITHMS:
  Token Bucket     → Smooth, allows bursts (most common)
  Sliding Window   → Precise, memory-intensive
  Fixed Window     → Simple, boundary spike issue
  Leaky Bucket     → Smooth output rate
```

## 🏛️ Classic System Designs (Interview Patterns)

```
URL SHORTENER (Easy):
  API → Hash(URL) → Base62 encode → Store in DB
  Components: App Server, NoSQL DB (DynamoDB), Cache (Redis), CDN

RATE LIMITER (Medium):
  Redis + Token Bucket per user/IP
  Components: API Gateway, Redis, Sliding Window Counter

CHAT SYSTEM (Medium):
  WebSocket connections, message queue, presence service
  Components: WebSocket Server, Kafka, Redis (presence), Cassandra (messages)

NEWS FEED (Hard):
  Fan-out-on-write (push) vs Fan-out-on-read (pull)
  Push for users with few followers, Pull for celebrities
  Components: Post Service, Fan-out Service, Redis Cache, Timeline DB

DISTRIBUTED CACHE (Hard):
  Consistent hashing, virtual nodes, replication
  Components: Hash Ring, Cache Nodes, Gossip Protocol

VIDEO STREAMING (Hard):
  Upload → Transcode → Store → CDN → Adaptive Bitrate Streaming
  Components: Upload Service, Transcoding Pipeline, S3/GCS, CDN, DRM
```

---

> 💡 **Interview Tip:** Always start with requirements and estimation. Interviewers want to see structured thinking, not a perfect architecture. Trade-offs > perfection.
