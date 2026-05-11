# 🔧 Runbook: High CPU Usage

> **Severity:** SEV-2 (if sustained) / SEV-3 (if intermittent)  
> **Alert:** `HighCPUUsage` — CPU usage > 80% for 10+ minutes  
> **On-call team:** Infrastructure / Backend  
> **Last updated:** 2025-01-15  

---

## 🎯 Objective

Diagnose and resolve high CPU usage on application servers before it impacts users.

---

## ⚡ Quick Mitigation (Do This First)

If the service is degraded and users are impacted, mitigate immediately:

```bash
# Option 1: Scale horizontally (Kubernetes)
kubectl scale deployment/<app-name> --replicas=<current+2> -n production

# Option 2: Scale horizontally (AWS Auto Scaling)
aws autoscaling set-desired-capacity \
  --auto-scaling-group-name <asg-name> \
  --desired-capacity <current+2>

# Option 3: Restart the problematic pod/instance
kubectl rollout restart deployment/<app-name> -n production
```

> ⚠️ **This buys you time.** Continue with diagnosis below.

---

## 🔍 Diagnosis Steps

### Step 1: Identify Which Process Is Using CPU

```bash
# On the host / inside the container
top -o %CPU -bn1 | head -20

# For containers (get the pod name first)
kubectl top pods -n production --sort-by=cpu

# Detailed per-container view
kubectl exec -it <pod-name> -n production -- top -bn1
```

### Step 2: Check Application-Level Metrics

```bash
# Prometheus queries (run in Grafana or Prometheus UI)

# CPU usage by container
rate(container_cpu_usage_seconds_total{namespace="production"}[5m])

# Request rate (traffic spike?)
rate(http_requests_total[5m])

# Active goroutines/threads
process_threads_total
# OR for Go apps:
go_goroutines
```

### Step 3: Common Causes & Solutions

| Cause | How to Identify | Solution |
|-------|----------------|----------|
| **Traffic spike** | Request rate increased | Scale up, enable rate limiting |
| **Infinite loop / bug** | Single pod at 100%, others normal | Identify code path, hotfix + rollback |
| **Regex backtracking** | CPU spikes on specific input | Fix regex pattern (use non-greedy) |
| **Garbage collection** | GC metrics show long pauses | Tune GC settings, reduce allocations |
| **Database N+1** | Many small DB queries | Add eager loading, fix queries |
| **Crypto operations** | SSL/TLS heavy operations | Offload TLS to load balancer |
| **Log flooding** | Excessive logging | Reduce log level, fix log loop |

### Step 4: Check Recent Changes

```bash
# What was deployed recently?
kubectl rollout history deployment/<app-name> -n production

# Check recent deployments
git log --oneline -10

# Check for config changes
kubectl get configmap -n production -o yaml
```

### Step 5: Profile the Application

```bash
# For Node.js — Generate CPU profile
kubectl exec -it <pod-name> -- node --prof app.js
# OR use clinic.js
npx clinic doctor -- node app.js

# For Go — pprof
curl http://localhost:6060/debug/pprof/profile?seconds=30 > cpu.prof
go tool pprof cpu.prof

# For Python — py-spy
py-spy record -o profile.svg --pid <PID>

# For Java — async-profiler
./profiler.sh -d 30 -f profile.html <PID>
```

---

## ✅ Resolution Checklist

- [ ] Root cause identified
- [ ] Fix applied (code change / config change / scaling)
- [ ] CPU returned to normal levels
- [ ] No impact visible in error rates or latency
- [ ] Monitoring confirms stability for 15+ minutes
- [ ] Temporary scaling reverted (if applied)
- [ ] Incident report updated

---

## 🔗 Related Links

- [Observability Dashboard](http://grafana.example.com/d/cpu-dashboard)
- [Application Logs](http://kibana.example.com/app/discover)
- [Deployment Pipeline](https://github.com/org/app/actions)
- [Escalation Contacts](https://pagerduty.example.com/escalation-policies)
