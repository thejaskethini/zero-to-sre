# 🔧 Runbook: Database Failover

> **Severity:** SEV-1 (immediate)  
> **Alert:** `DatabaseDown` or `DatabaseReplicationLag`  
> **On-call team:** Database / Infrastructure  
> **Last updated:** 2025-01-15  

---

## 🎯 Objective

Perform a safe database failover from primary to replica to restore service.

---

## ⚠️ Before You Begin

> **READ THIS FIRST:**
> - A database failover can cause **brief downtime** (seconds to minutes)
> - Ensure you have **manager approval** for manual failover
> - Check if your cloud provider has **automated failover** enabled first

---

## ⚡ Quick Assessment

```bash
# Step 1: Check if automated failover is handling it
# AWS RDS — Check for automated failover event
aws rds describe-events \
  --source-identifier mydb-instance \
  --source-type db-instance \
  --duration 30

# Step 2: Check primary status
aws rds describe-db-instances \
  --db-instance-identifier mydb-primary \
  --query 'DBInstances[0].{Status:DBInstanceStatus,AZ:AvailabilityZone}'

# Step 3: Check replica status and replication lag
aws rds describe-db-instances \
  --db-instance-identifier mydb-replica \
  --query 'DBInstances[0].{Status:DBInstanceStatus,Lag:StatusInfos}'
```

---

## 🔧 Failover Procedures

### Option A: AWS RDS Automated Failover (Multi-AZ)

```bash
# Trigger failover (AWS handles everything)
aws rds reboot-db-instance \
  --db-instance-identifier mydb-primary \
  --force-failover

# Monitor failover progress
watch -n 5 'aws rds describe-db-instances \
  --db-instance-identifier mydb-primary \
  --query "DBInstances[0].DBInstanceStatus"'

# Expected: "rebooting" → "available" (typically 1-3 minutes)
```

### Option B: PostgreSQL Manual Failover

```bash
# 1. Verify replica is caught up
psql -h replica-host -U postgres -c "SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn(), pg_last_xact_replay_timestamp();"

# 2. Stop writes to primary (if still accessible)
psql -h primary-host -U postgres -c "SELECT pg_switch_wal();"

# 3. Promote replica to primary
psql -h replica-host -U postgres -c "SELECT pg_promote();"
# OR
pg_ctl promote -D /var/lib/postgresql/data

# 4. Verify promotion
psql -h replica-host -U postgres -c "SELECT pg_is_in_recovery();"
# Should return: false (meaning it's now a primary)

# 5. Update application connection string
# Update DNS/connection string to point to the new primary
```

### Option C: Kubernetes (with operator)

```bash
# CloudNativePG operator
kubectl cnpg promote <cluster-name> <replica-pod-name> -n production

# Patroni-based PostgreSQL
kubectl exec -it <patroni-pod> -n production -- \
  patronictl switchover --master <current-primary> --candidate <replica>
```

---

## 📝 Post-Failover Verification

```bash
# 1. Verify new primary is accepting writes
psql -h new-primary -U postgres -c "CREATE TABLE failover_test (id int); DROP TABLE failover_test;"

# 2. Check application connectivity
curl -f https://api.example.com/health

# 3. Monitor error rates for 15 minutes
# Check Grafana dashboard for any error spikes

# 4. Verify replica is set up for the new primary
psql -h new-replica -U postgres -c "SELECT pg_is_in_recovery();"
# Should return: true
```

---

## ✅ Checklist

- [ ] Confirmed automated failover did not handle it
- [ ] Verified replica is caught up (zero or minimal lag)
- [ ] Failover executed successfully
- [ ] Application is connecting to new primary
- [ ] Error rates returned to normal
- [ ] New replica is replicating from new primary
- [ ] DNS/connection strings updated (if needed)
- [ ] Old primary investigated for root cause
- [ ] Incident report filed

---

## 🔗 Related Links

- [Database Dashboard](http://grafana.example.com/d/postgres)
- [RDS Console](https://console.aws.amazon.com/rds/)
- [Connection String Config](https://github.com/org/app/blob/main/config/database.yml)
