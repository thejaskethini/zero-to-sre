# 🐘 PostgreSQL Cheatsheet

> psql commands, query optimization, EXPLAIN ANALYZE, replication, PgBouncer, and production tuning.

---

## 🔧 psql Commands

```bash
psql -U postgres -d mydb                              # Connect
psql -h db.internal -U appuser -d production          # Remote connect
psql -c "SELECT version();"                            # Single command

# Inside psql
\l                                                    # List databases
\dt                                                   # List tables
\dt+                                                  # Tables with size
\di                                                   # List indexes
\du                                                   # List users/roles
\d tablename                                          # Describe table
\x                                                    # Toggle expanded display
\timing                                               # Show query timing
\q                                                    # Quit
```

## 🔍 Query Optimization

```sql
-- EXPLAIN ANALYZE (always use this for optimization)
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT u.name, COUNT(o.id) as order_count
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.created_at > NOW() - INTERVAL '30 days'
GROUP BY u.name
ORDER BY order_count DESC
LIMIT 10;

-- Reading EXPLAIN output:
-- Seq Scan      → Full table scan (usually bad for large tables)
-- Index Scan    → Using index (good)
-- Bitmap Scan   → Multiple index conditions (good)
-- Nested Loop   → Good for small datasets
-- Hash Join     → Good for large datasets
-- Sort          → Check if index can eliminate sort
-- Rows          → Estimated vs Actual (big diff = stale stats)

-- Fix: Run ANALYZE to update statistics
ANALYZE tablename;
ANALYZE;                                              -- All tables
```

## 📊 Indexes

```sql
-- Create indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_orders_created ON orders(created_at DESC);
CREATE INDEX idx_orders_composite ON orders(user_id, status, created_at);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX CONCURRENTLY idx_big_table ON big_table(col);  -- Non-blocking

-- Partial indexes (index subset of rows)
CREATE INDEX idx_active_orders ON orders(user_id) WHERE status = 'active';

-- Expression indexes
CREATE INDEX idx_users_lower_email ON users(LOWER(email));

-- Index analysis
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes ORDER BY idx_scan ASC;      -- Unused indexes

-- Drop unused indexes
DROP INDEX CONCURRENTLY idx_old_unused;
```

## 🧹 Vacuuming & Maintenance

```sql
-- Manual vacuum
VACUUM tablename;                                     -- Reclaim space
VACUUM FULL tablename;                                -- Reclaim + compact (locks table!)
VACUUM ANALYZE tablename;                             -- Vacuum + update stats

-- Check for bloat
SELECT schemaname, relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::float / GREATEST(n_live_tup, 1) * 100, 2) as dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY dead_pct DESC;

-- Autovacuum settings (per table)
ALTER TABLE hot_table SET (autovacuum_vacuum_scale_factor = 0.01);
ALTER TABLE hot_table SET (autovacuum_analyze_scale_factor = 0.005);
```

## 🔒 Active Queries & Locks

```sql
-- Active queries (find slow queries)
SELECT pid, state, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Kill long-running query
SELECT pg_cancel_backend(pid);                        -- Graceful
SELECT pg_terminate_backend(pid);                     -- Force kill

-- Lock detection
SELECT blocked.pid AS blocked_pid, blocked.query AS blocked_query,
  blocking.pid AS blocking_pid, blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_locks bl ON bl.pid = blocked.pid
JOIN pg_locks bk ON bk.locktype = bl.locktype AND bk.database IS NOT DISTINCT FROM bl.database
  AND bk.relation IS NOT DISTINCT FROM bl.relation AND bk.page IS NOT DISTINCT FROM bl.page
  AND bk.tuple IS NOT DISTINCT FROM bl.tuple AND bl.pid != bk.pid
JOIN pg_stat_activity blocking ON bk.pid = blocking.pid
WHERE NOT bl.granted;

-- Connection stats
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
SHOW max_connections;
```

## 🔄 Replication & Backup

```bash
# Streaming replication status (on primary)
psql -c "SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn FROM pg_stat_replication;"

# Replication lag
psql -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"

# Backup
pg_dump -Fc -d production > backup.dump               # Custom format (best)
pg_dump -Fc -d production -j 4 > backup.dump          # Parallel
pg_dumpall > all_databases.sql                         # All databases

# Restore
pg_restore -d production backup.dump
pg_restore -d production -j 4 --clean backup.dump     # Parallel + clean
```

## ⚡ Connection Pooling (PgBouncer)

```ini
; /etc/pgbouncer/pgbouncer.ini
[databases]
production = host=db.internal port=5432 dbname=production

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt
pool_mode = transaction           ; transaction | session | statement
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
server_idle_timeout = 300
```

## 🎯 FAANG Interview Q&A

```
Q: How do you optimize a slow query?
A: 1. EXPLAIN ANALYZE to see execution plan
   2. Check for Seq Scans → add appropriate indexes
   3. Check row estimates vs actual → run ANALYZE
   4. Check for unused/redundant indexes
   5. Consider partial indexes for filtered queries
   6. Rewrite query: avoid SELECT *, use CTEs wisely

Q: When to use PgBouncer?
A: PostgreSQL has expensive per-connection overhead (~10MB).
   PgBouncer pools connections: 1000 app connections → 25 DB connections.
   Use transaction pooling for most workloads.
   Essential when: many short-lived connections (serverless, microservices).

Q: How does MVCC work?
A: Multi-Version Concurrency Control: each transaction sees a snapshot.
   Writers don't block readers. Old row versions kept until VACUUM.
   Dead tuples accumulate → bloat. Autovacuum cleans them up.
   This is why VACUUM is critical for PostgreSQL performance.
```

---

> 💡 **Production Rule:** Always use PgBouncer. Always run EXPLAIN ANALYZE before deploying new queries. Monitor dead tuple ratio — high bloat kills performance. Never run VACUUM FULL in production peak hours.
