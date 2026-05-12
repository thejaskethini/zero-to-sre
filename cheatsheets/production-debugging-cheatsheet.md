# 🔥 Production Debugging Cheatsheet

> Battle-tested debugging techniques for production systems — the playbook FAANG SREs use when pagers go off at 3 AM.

---

## 🚨 First Response (The Golden 5 Minutes)

```bash
# 1. What's the blast radius?
# Check system overview
uptime                                                # Load average, uptime
top -bn1 | head -20                                   # Quick system snapshot
free -h                                               # Memory overview
df -h                                                 # Disk usage
dmesg -T | tail -20                                   # Kernel messages (OOM killer?)

# 2. Is it the app or the infra?
curl -o /dev/null -s -w "%{http_code} %{time_total}s\n" http://localhost:8080/health
systemctl status myapp
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
kubectl get pods -o wide | grep -v Running
```

## 🧠 CPU Debugging

```bash
# Who's eating CPU?
top -c                                                # Interactive (press P to sort by CPU)
htop                                                  # Better interactive view
ps aux --sort=-%cpu | head -10                        # Top CPU consumers
pidstat 1 5                                           # Per-process CPU stats (5 samples)

# CPU profiling
perf top                                              # Real-time kernel profiling
perf record -g -p <PID> sleep 30                      # Record 30s profile
perf report                                           # Analyze the recording

# Java/Node specific
jstack <PID> > /tmp/thread_dump.txt                   # Java thread dump
kill -USR1 <NODE_PID>                                 # Node.js: generate heap snapshot
```

## 💾 Memory Debugging

```bash
# Memory overview
free -h                                               # System memory
cat /proc/meminfo | head -10                          # Detailed memory info
ps aux --sort=-%mem | head -10                        # Top memory consumers
pmap -x <PID> | tail -5                              # Process memory map

# OOM Killer detection
dmesg -T | grep -i "oom\|killed\|out of memory"
journalctl -k | grep -i "oom\|killed"
cat /proc/<PID>/oom_score                            # OOM score (higher = more likely killed)

# Memory leak hunting
smem -tk                                              # Per-process USS/PSS/RSS
watch -n 5 'ps -p <PID> -o rss,vsz,pid,comm'        # Watch memory growth
valgrind --leak-check=full ./myapp                    # C/C++ leak detection
```

## 💽 Disk & I/O Debugging

```bash
# Disk space
df -h                                                 # Filesystem usage
df -i                                                 # Inode usage (can fill up!)
du -sh /var/log/* | sort -rh | head -10              # Largest log dirs
find / -xdev -type f -size +100M -exec ls -lh {} \;  # Large files

# I/O performance
iostat -xz 1 5                                        # Disk I/O stats
iotop -oPa                                            # Per-process I/O (cumulative)
lsof +D /var/log                                      # Who has files open?
lsof -p <PID>                                         # Files opened by process

# Disk latency
ioping /var/lib/data                                  # Disk latency test
dd if=/dev/zero of=/tmp/test bs=1M count=1024 oflag=direct  # Write speed
```

## 🌐 Network Debugging

```bash
# Connection overview
ss -tlnp                                              # Listening ports
ss -s                                                 # Socket statistics summary
ss -tnp state established | wc -l                    # Active connections count
ss -tnp | grep CLOSE-WAIT | wc -l                    # Connection leak indicator

# DNS debugging
dig myservice.example.com +trace                      # Full DNS resolution trace
nslookup myservice.example.com                        # Quick DNS lookup
host myservice.example.com                            # Simple DNS check

# HTTP debugging
curl -vvv https://api.example.com/health 2>&1         # Verbose HTTP
curl -w "\nDNS: %{time_namelookup}s\nConnect: %{time_connect}s\nTLS: %{time_appconnect}s\nTotal: %{time_total}s\n" -o /dev/null -s https://api.example.com
time curl -s http://backend:8080/api/slow-endpoint    # Time an endpoint

# TCP debugging
tcpdump -i any port 5432 -c 50                        # Capture DB traffic
tcpdump -i any host 10.0.1.50 -w /tmp/capture.pcap   # Save packet capture
nmap -sT -p 80,443,8080 10.0.1.50                    # Port scan

# Bandwidth & throughput
iftop -i eth0                                         # Real-time bandwidth
nethogs                                               # Per-process bandwidth
```

## 📋 Log Analysis (Production Patterns)

```bash
# Quick log search
tail -f /var/log/app/error.log                        # Follow errors live
tail -1000 /var/log/app/app.log | grep -i "error\|exception\|fatal"
journalctl -u myapp --since "1 hour ago" --no-pager

# Log frequency analysis
awk '{print $9}' access.log | sort | uniq -c | sort -rn | head  # HTTP status codes
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head  # Top IPs

# Error rate over time
grep "ERROR" app.log | awk '{print $1, $2}' | cut -d: -f1,2 | uniq -c

# JSON logs (jq is essential)
cat app.log | jq 'select(.level == "error")' | head
cat app.log | jq 'select(.status >= 500) | {time, path, status, error}'
cat app.log | jq -r '.request_time' | awk '{sum+=$1; count++} END {print "avg:", sum/count "s"}'

# Kubernetes logs
kubectl logs <pod> --since=1h --tail=500
kubectl logs <pod> -c <container> --previous          # Previous crash logs
kubectl logs -l app=myapp --all-containers           # All pods of a service
stern myapp -n production                             # Multi-pod log tailing
```

## 🐳 Container Debugging

```bash
# Container health
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker stats --no-stream                              # Resource usage snapshot
docker inspect <container> | jq '.[0].State'         # Container state

# Debug a crashed container
docker logs <container> --tail 100
docker inspect <container> | jq '.[0].State.ExitCode'
docker inspect <container> | jq '.[0].State.OOMKilled'

# Shell into container
docker exec -it <container> /bin/sh                   # Alpine/minimal
docker exec -it <container> /bin/bash                 # Ubuntu/Debian

# Debug from sidecar (distroless images)
docker run -it --pid=container:<target> --net=container:<target> nicolaka/netshoot
kubectl debug <pod> -it --image=nicolaka/netshoot     # K8s ephemeral container
```

## ☸️ Kubernetes Production Debugging

```bash
# Cluster overview
kubectl top nodes                                     # Node resource usage
kubectl top pods -A --sort-by=cpu                     # Pod CPU usage
kubectl get events --sort-by=.lastTimestamp -A | tail -20

# Pod debugging
kubectl describe pod <pod>                            # Events, conditions, mounts
kubectl get pod <pod> -o yaml                         # Full pod spec
kubectl exec -it <pod> -- /bin/sh                     # Shell into pod
kubectl port-forward <pod> 8080:8080                  # Direct access

# Common failure patterns
kubectl get pods | grep -E "CrashLoop|Error|OOM"     # Find broken pods
kubectl describe pod <pod> | grep -A5 "Last State"   # Why it crashed
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[0].lastState}'
```

## 🗄️ Database Debugging

```bash
# PostgreSQL
psql -c "SELECT pid, state, query, now() - query_start AS duration FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;"
psql -c "SELECT blocked.pid, blocked.query, blocking.pid AS blocking_pid, blocking.query AS blocking_query FROM pg_stat_activity blocked JOIN pg_locks bl ON bl.pid = blocked.pid JOIN pg_locks bk ON bk.locktype = bl.locktype AND bk.database IS NOT DISTINCT FROM bl.database JOIN pg_stat_activity blocking ON bk.pid = blocking.pid WHERE NOT bl.granted;"

# MySQL
mysql -e "SHOW PROCESSLIST;"
mysql -e "SHOW ENGINE INNODB STATUS\G"
mysql -e "SELECT * FROM information_schema.innodb_lock_waits;"

# Redis
redis-cli info memory                                 # Memory usage
redis-cli info clients                                # Client connections
redis-cli slowlog get 10                              # Slow queries
redis-cli --latency-history                           # Latency over time
redis-cli monitor                                     # Live command stream (CAREFUL)
```

## 📐 The SRE Debugging Framework

```
1. DETECT    → What metric/alert triggered?
2. TRIAGE    → What's the user impact? (P1/P2/P3/P4)
3. SCOPE     → Is it a single host, service, region, or global?
4. MITIGATE  → Can we rollback, scale up, or failover? (fix later, mitigate now)
5. DIAGNOSE  → Follow the request path: DNS → LB → App → DB → Response
6. FIX       → Apply the root-cause fix
7. POSTMORTEM → Blameless review within 48 hours
```

---

> 💡 **Golden Rule:** In production, your #1 job is to **mitigate** (restore service), not to **debug** (find root cause). Rollback first, investigate after. Every minute of downtime costs money and trust.
