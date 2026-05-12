# 🔴 Redis Cheatsheet

> Data structures, persistence, replication, Cluster, Sentinel, performance tuning, and production patterns.

---

## 📦 Data Structures & Commands

```bash
# Strings
SET user:123:name "Alice"
SET session:abc "data" EX 3600                        # Expire in 1 hour
GET user:123:name
INCR counter                                          # Atomic increment
INCRBY counter 5
MSET key1 "v1" key2 "v2"                             # Multi-set
MGET key1 key2                                        # Multi-get

# Hashes (objects)
HSET user:123 name "Alice" email "alice@example.com" age 30
HGET user:123 name
HGETALL user:123
HINCRBY user:123 age 1

# Lists (queues)
LPUSH queue:jobs "job1" "job2"                        # Push left
RPUSH queue:jobs "job3"                               # Push right
LPOP queue:jobs                                       # Pop left
RPOP queue:jobs                                       # Pop right
BRPOP queue:jobs 30                                   # Blocking pop (30s timeout)
LLEN queue:jobs                                       # Length
LRANGE queue:jobs 0 -1                                # All elements

# Sets
SADD tags:post:1 "devops" "sre" "kubernetes"
SMEMBERS tags:post:1
SISMEMBER tags:post:1 "devops"                        # Check membership
SINTER tags:post:1 tags:post:2                        # Intersection

# Sorted Sets (leaderboards)
ZADD leaderboard 100 "alice" 95 "bob" 88 "charlie"
ZRANGE leaderboard 0 -1 WITHSCORES                   # All, ascending
ZREVRANGE leaderboard 0 9 WITHSCORES                 # Top 10
ZINCRBY leaderboard 5 "alice"                        # Add to score
ZRANK leaderboard "alice"                            # Rank (0-indexed)

# Key operations
KEYS user:*                                           # Find keys (NEVER in production!)
SCAN 0 MATCH user:* COUNT 100                        # Safe key scanning
TTL mykey                                             # Time to live
EXPIRE mykey 3600                                     # Set expiry
DEL mykey                                             # Delete
EXISTS mykey                                          # Check existence
TYPE mykey                                            # Data type
```

## 💾 Persistence

```
RDB (Snapshotting):
  save 900 1                           # Snapshot if 1 key changed in 900s
  save 300 10                          # Snapshot if 10 keys changed in 300s
  save 60 10000                        # Snapshot if 10000 keys changed in 60s
  + Fast restart, compact files
  - Data loss between snapshots

AOF (Append-Only File):
  appendonly yes
  appendfsync everysec                 # Best balance (1s data loss max)
  # appendfsync always                 # Zero data loss, slower
  # appendfsync no                     # OS decides (fastest, risky)
  + Minimal data loss
  - Larger files, slower restart

RECOMMENDATION: Use BOTH RDB + AOF in production
```

## 🔄 Replication

```bash
# Set up replica
REPLICAOF primary-host 6379                           # On replica

# Check replication
INFO replication                                      # On primary or replica
# role:master, connected_slaves:2, slave0:ip=...,state=online,lag=0

# Promote replica to primary (failover)
REPLICAOF NO ONE                                      # On replica
```

## 🏰 Sentinel (HA)

```bash
# sentinel.conf
sentinel monitor mymaster primary-host 6379 2        # 2 = quorum
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# Check sentinel
redis-cli -p 26379 SENTINEL masters
redis-cli -p 26379 SENTINEL get-master-addr-by-name mymaster
redis-cli -p 26379 SENTINEL slaves mymaster
```

## 🌐 Redis Cluster

```bash
# Create cluster
redis-cli --cluster create \
  10.0.1.1:6379 10.0.1.2:6379 10.0.1.3:6379 \
  10.0.1.4:6379 10.0.1.5:6379 10.0.1.6:6379 \
  --cluster-replicas 1

# Cluster info
redis-cli -c cluster info
redis-cli -c cluster nodes
redis-cli -c cluster slots

# Add/remove nodes
redis-cli --cluster add-node new-host:6379 existing-host:6379
redis-cli --cluster reshard existing-host:6379
```

## 📊 Monitoring & Debugging

```bash
redis-cli INFO                                        # Everything
redis-cli INFO memory                                 # Memory usage
redis-cli INFO clients                                # Client connections
redis-cli INFO stats                                  # Hit rate, commands/sec
redis-cli INFO keyspace                               # Keys per database

redis-cli SLOWLOG GET 10                              # Slow queries
redis-cli CLIENT LIST                                 # Connected clients
redis-cli DBSIZE                                      # Total keys
redis-cli MEMORY USAGE mykey                          # Memory for specific key
redis-cli --latency-history                           # Latency over time
redis-cli --bigkeys                                   # Find large keys
redis-cli MONITOR                                     # Live commands (CAREFUL!)
```

## ⚡ Eviction Policies

```
noeviction        → Return error on write when full (default)
allkeys-lru       → Evict least recently used (BEST for cache)
allkeys-lfu       → Evict least frequently used
volatile-lru      → Evict LRU only from keys with TTL
volatile-lfu      → Evict LFU only from keys with TTL
allkeys-random    → Evict random keys
volatile-random   → Evict random keys with TTL
volatile-ttl      → Evict keys with shortest TTL

maxmemory 4gb
maxmemory-policy allkeys-lru
```

## 🎯 FAANG Interview Q&A

```
Q: Redis vs Memcached?
A: Redis: data structures (hashes, lists, sets), persistence,
   replication, Lua scripting, pub/sub. Memcached: simpler,
   multi-threaded (better for pure string caching at scale).
   Redis wins on features, Memcached wins on simplicity.

Q: How do you handle cache stampede?
A: 1. Lock-based: first request acquires lock, others wait
   2. Early expiration: refresh before TTL expires (background)
   3. Probabilistic: random early refresh based on TTL remaining
   4. Never set same TTL for related keys (add jitter)

Q: Redis cache vs cache-aside pattern?
A: Cache-aside: App checks cache → miss → query DB → write cache.
   App controls both cache and DB. Most common pattern.
   Read-through: Cache auto-fetches from DB on miss.
   Write-through: Cache writes to both cache and DB simultaneously.

Q: How does Redis Cluster handle partitioning?
A: 16384 hash slots distributed across master nodes.
   Key → CRC16(key) % 16384 → slot → node.
   Each master handles a range of slots.
   Replicas provide HA per master. Automatic failover via gossip.
```

---

> 💡 **Production Rule:** Always set maxmemory + eviction policy. Never use KEYS in production (use SCAN). Monitor hit rate — below 80% means your cache is ineffective. Use connection pooling.
