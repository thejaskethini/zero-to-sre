# ⚡ SRE Quick Reference Card

> **🚨 The top 5 commands from every cheatsheet in one file.**
> Print this. Tape it to your monitor. Use it at 3 AM when the pager goes off.

---

## 🔥 FIRST RESPONSE (Do This First)

```bash
uptime                                                # Load averages
free -h                                               # Memory
df -h                                                 # Disk
dmesg -T | tail -20                                   # Kernel messages
curl -o /dev/null -s -w "%{http_code} %{time_total}s\n" http://localhost:8080/health
```

---

## 🐧 Linux

```bash
top -bn1 | head -20                                   # System overview
ps aux --sort=-%cpu | head -10                        # Top CPU
ps aux --sort=-%mem | head -10                        # Top memory
tail -f /var/log/syslog                               # Follow system log
find / -xdev -type f -size +100M 2>/dev/null          # Large files
```

## 🐳 Docker

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
docker logs <container> -f --since 5m
docker stats --no-stream
docker exec -it <container> sh
docker system prune -af --volumes                     # Nuclear cleanup
```

## ☸️ Kubernetes

```bash
kubectl get pods -o wide -A | grep -v Running
kubectl top pods -A --sort-by=cpu | head -10
kubectl logs <pod> --since=1h --tail=200
kubectl describe pod <pod>                            # Events section
kubectl rollout undo deployment/<name>                # Emergency rollback
```

## 🌐 Nginx

```bash
sudo nginx -t                                         # Test config
sudo nginx -s reload                                  # Graceful reload
sudo tail -f /var/log/nginx/error.log
curl -I https://myapp.example.com                     # Response headers
sudo ss -tlnp | grep nginx                            # Listening ports
```

## ⚙️ PM2

```bash
pm2 list                                              # All processes
pm2 logs --lines 100                                  # Recent logs
pm2 reload all                                        # Zero-downtime restart
pm2 monit                                             # Terminal dashboard
pm2 save                                              # Save process list
```

## 📊 Prometheus/PromQL

```promql
rate(http_requests_total[5m])                         # Request rate
sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])) * 100  # Error %
histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))  # p99 latency
up == 0                                               # Down targets
node_filesystem_avail_bytes / node_filesystem_size_bytes < 0.1  # Disk < 10%
```

## 🌐 Network

```bash
ss -s                                                 # Connection summary
ss -tnp state close-wait                              # Connection leaks
dig example.com +short                                # DNS lookup
curl -w "DNS:%{time_namelookup} TCP:%{time_connect} TLS:%{time_appconnect} Total:%{time_total}\n" -o /dev/null -s https://api.example.com
echo | openssl s_client -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate  # Cert expiry
```

## 🔒 SSL/TLS

```bash
openssl s_client -connect example.com:443 -servername example.com </dev/null 2>/dev/null | openssl x509 -noout -dates
sudo certbot renew --dry-run
openssl x509 -in cert.pem -noout -text | head -20
openssl verify -CAfile ca.crt server.crt
nmap --script ssl-enum-ciphers -p 443 example.com
```

## 🗄️ PostgreSQL

```sql
SELECT pid, state, now()-query_start AS duration, query FROM pg_stat_activity WHERE state != 'idle' ORDER BY duration DESC;
SELECT pg_cancel_backend(pid);                        -- Kill slow query
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;                -- Query analysis
SELECT count(*), state FROM pg_stat_activity GROUP BY state;  -- Connection stats
VACUUM ANALYZE tablename;                             -- Maintenance
```

## 🔴 Redis

```bash
redis-cli INFO memory                                 # Memory usage
redis-cli INFO clients                                # Connections
redis-cli SLOWLOG GET 10                              # Slow queries
redis-cli --bigkeys                                   # Find large keys
redis-cli --latency-history                           # Latency trend
```

## 📨 Kafka

```bash
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-app --describe  # Consumer lag
kafka-topics.sh --bootstrap-server localhost:9092 --describe --under-replicated-partitions
kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic my-topic
kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic my-topic --from-beginning --max-messages 10
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

## ☁️ AWS

```bash
aws sts get-caller-identity                           # Who am I?
aws ec2 describe-instances --filters "Name=tag:Env,Values=prod" --query "Reservations[].Instances[].[InstanceId,State.Name]" --output table
aws cloudwatch describe-alarms --state-value ALARM --output table
aws logs tail /aws/ecs/api --follow --since 1h
aws ecs list-services --cluster prod --output table
```

## 🔧 Git

```bash
git log --oneline -10                                 # Recent commits
git diff HEAD~1                                       # Last change
git stash && git pull && git stash pop                # Safe pull
git blame file.py                                     # Who changed what
git bisect start && git bisect bad && git bisect good v1.0  # Find bad commit
```

## 🏗️ Terraform

```bash
terraform plan                                        # Preview changes
terraform apply -auto-approve                         # Apply (careful!)
terraform state list                                  # List resources
terraform state show aws_instance.web                 # Resource details
terraform import aws_instance.web i-abc123            # Import existing
```

## 🔐 Vault

```bash
vault kv get secret/production/db                     # Read secret
vault kv put secret/production/db password="new"      # Write secret
vault token lookup                                    # Current token info
vault status                                          # Seal status
vault audit list                                      # Audit backends
```

---

## 📐 SRE Decision Framework

```
INCIDENT?
├── Is it user-facing? → Yes → SEV1/SEV2, page on-call
├── Can you rollback? → Yes → ROLLBACK NOW, investigate later
├── Can you scale up? → Yes → Scale, then investigate
├── Is it a single host? → Yes → Drain node, replace
└── Unknown? → Follow the request path:
    DNS → LB → App → Cache → DB → Response

GOLDEN RULE: Mitigate first, debug second.
```

---

<p align="center">
  <strong>⚡ Bookmark this file. Your future 3-AM self will thank you.</strong>
  <br />
  <a href="./README.md">📋 Full Cheatsheet Index</a> · <a href="../README.md">⬅️ Back to Main</a>
</p>
