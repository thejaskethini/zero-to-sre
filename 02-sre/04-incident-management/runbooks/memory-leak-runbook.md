# 🚨 Runbook: Application Memory Leak

## 📋 Overview

| Field | Value |
|-------|-------|
| **Alert Name** | `AppMemoryHigh` |
| **Severity** | P2 — High |
| **Service** | Application pods |
| **Symptom** | Pod memory usage continuously growing, OOM kills |
| **Impact** | Pod restarts, potential request failures during restart |

---

## 🔍 Diagnosis Steps

### Step 1: Confirm Memory Growth Pattern

```bash
# Check current memory usage
kubectl top pods -n production --sort-by=memory

# Check for OOM kills
kubectl get events -n production --sort-by='.lastTimestamp' | grep OOM

# Check pod restart count
kubectl get pods -n production -o custom-columns="NAME:.metadata.name,RESTARTS:.status.containerStatuses[0].restartCount,STATUS:.status.phase"
```

### Step 2: Check Prometheus Metrics

```promql
# Memory usage over time (should be sawtooth pattern for leak)
container_memory_working_set_bytes{namespace="production", pod=~"myapp.*"}

# Memory usage as % of limit
container_memory_working_set_bytes{namespace="production"}
  / container_spec_memory_limit_bytes{namespace="production"} * 100

# Rate of memory growth
deriv(container_memory_working_set_bytes{namespace="production", pod=~"myapp.*"}[1h])
```

### Step 3: Identify the Leak Source

```bash
# Get a heap dump (Node.js)
kubectl exec -it <pod-name> -n production -- node --inspect=0.0.0.0:9229 &
kubectl port-forward <pod-name> 9229:9229 -n production
# Connect Chrome DevTools → chrome://inspect

# Check connection pools
kubectl exec -it <pod-name> -n production -- sh -c 'ss -s'

# Check file descriptors
kubectl exec -it <pod-name> -n production -- sh -c 'ls /proc/1/fd | wc -l'
```

---

## 🔧 Mitigation

### Immediate (Reduce Impact)

```bash
# Rolling restart to free memory (zero-downtime)
kubectl rollout restart deployment/myapp -n production

# Temporarily increase memory limits
kubectl set resources deployment/myapp -n production --limits=memory=1Gi
```

### Short-term (Prevent OOM)

1. Add a startup probe to catch memory leaks early:
   ```yaml
   startupProbe:
     httpGet:
       path: /health
       port: 3000
     failureThreshold: 30
     periodSeconds: 10
   ```

2. Set up memory-based alerts:
   ```promql
   # Alert when memory > 80% of limit for 10 min
   container_memory_working_set_bytes / container_spec_memory_limit_bytes > 0.8
   ```

### Long-term (Fix Root Cause)

1. **Profile the application** with heap dumps
2. **Common leak sources:**
   - Unclosed database connections
   - Event listener accumulation
   - Growing caches without eviction
   - Circular references preventing GC
   - Global variable accumulation
3. **Add memory monitoring** to CI/CD pipeline

---

## ✅ Resolution Verification

```bash
# Watch memory over next 30 minutes (should be stable, not growing)
kubectl top pods -n production -w

# Verify no OOM events
kubectl get events -n production --field-selector=reason=OOMKilling --sort-by='.lastTimestamp'

# Check error rate returned to normal
curl -s http://localhost:8080/metrics | grep http_requests_total
```
