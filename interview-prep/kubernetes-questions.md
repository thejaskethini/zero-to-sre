# 🎓 Kubernetes Interview Questions

> Curated questions for K8s-focused interviews (DevOps/SRE roles).

---

## 🟢 Beginner

### 1. What is the difference between a Pod and a Container?
**Answer:** A Pod is the smallest deployable unit in Kubernetes and can contain one or more containers. Containers within the same pod share the same network namespace (localhost), storage volumes, and lifecycle. Typically, a pod runs one main container, with optional sidecar containers for logging, proxying, etc.

### 2. What happens when a Pod crashes?
**Answer:** Depends on `restartPolicy` (default: `Always`). The kubelet restarts the container with exponential backoff (10s, 20s, 40s, up to 5 min). If managed by a Deployment/ReplicaSet, a new pod may be scheduled on a different node if the current node is unhealthy.

### 3. What's the difference between a Deployment and a StatefulSet?
**Answer:**
- **Deployment:** Stateless apps. Pods are interchangeable, get random names, no stable storage.
- **StatefulSet:** Stateful apps (databases, Kafka). Pods get ordered names (mydb-0, mydb-1), stable persistent storage, ordered startup/shutdown.

### 4. Explain ClusterIP vs NodePort vs LoadBalancer.
**Answer:**
- **ClusterIP:** Internal only. Other pods reach it via DNS (svc-name.namespace.svc.cluster.local).
- **NodePort:** Exposes on every node at a specific port (30000-32767). Not for production.
- **LoadBalancer:** Creates a cloud load balancer (AWS ELB/NLB, GCP LB). Production external access.

---

## 🟡 Intermediate

### 5. How do readiness and liveness probes differ?
**Answer:**
- **Readiness:** "Can this pod accept traffic?" Failed = removed from service endpoints (no traffic). Used during startup and temporary issues.
- **Liveness:** "Is this pod alive?" Failed = pod gets restarted. Used for deadlock/stuck detection.
- **Startup:** Used for slow-starting apps. Delays liveness checks until startup completes.

### 6. What is a PodDisruptionBudget?
**Answer:** PDB limits voluntary disruptions (node drain, upgrades) — not crashes. Example: `minAvailable: 2` ensures at least 2 pods are always running. Without PDBs, `kubectl drain` could evict ALL pods simultaneously, causing downtime.

### 7. Explain how Kubernetes networking works.
**Answer:** Three rules: (1) Every pod gets a unique IP, (2) Pods on any node can communicate with any other pod without NAT, (3) Agents (kubelet, kube-proxy) can communicate with all pods. Implemented via CNI plugins (Calico, Cilium, Flannel). Services provide stable virtual IPs with kube-proxy handling the routing.

### 8. How do you debug a pod stuck in CrashLoopBackOff?
**Answer:**
```bash
kubectl describe pod <name>          # Check events and conditions
kubectl logs <name> --previous       # Logs from crashed container
kubectl get events --sort-by=.lastTimestamp  # Cluster events
# Common causes: missing config/secret, wrong command, permission error,
# resource limits too low, failing health checks
```

---

## 🔴 Advanced

### 9. Design a zero-downtime deployment strategy for a database migration.
**Answer:**
1. Make schema changes **backward compatible** (add columns, don't rename/remove)
2. Deploy new app version that works with both old and new schema
3. Run migration job (separate K8s Job)
4. Verify migration succeeded
5. Deploy version that uses only new schema
6. Clean up old columns in a future release
Key: Separate schema changes from code changes. Never do both in one deploy.

### 10. How would you secure a Kubernetes cluster?
**Answer:**
- **RBAC:** Least privilege, namespace-scoped roles
- **Network Policies:** Default deny, explicit allow
- **Pod Security:** runAsNonRoot, readOnlyRootFilesystem, drop ALL capabilities
- **Secrets:** Encrypt at rest (etcd encryption), use external secrets (Vault)
- **Image Security:** Signed images, vulnerability scanning (Trivy), no latest tag
- **API Server:** Audit logging, admission controllers (OPA/Kyverno)
- **Supply Chain:** SBOM, Cosign for image signing

### 11. Explain how Kubernetes scheduler makes placement decisions.
**Answer:** The scheduler uses a two-phase approach:
1. **Filtering:** Eliminates nodes that can't run the pod (resource constraints, taints, node selectors, affinity rules, PVC availability)
2. **Scoring:** Ranks remaining nodes by criteria (resource balancing, affinity preferences, spreading)
Custom schedulers or scheduling profiles can extend this behavior.

### 12. What happens during `kubectl apply -f deployment.yaml`?
**Answer:** Full flow:
1. kubectl validates and serializes to JSON
2. Sends POST/PATCH to API server
3. API server authenticates, authorizes (RBAC), and runs admission controllers
4. Object stored in etcd
5. Deployment controller creates/updates ReplicaSet
6. ReplicaSet controller creates pods
7. Scheduler assigns pods to nodes
8. kubelet on target node pulls image and starts containers
9. kube-proxy updates iptables/IPVS rules for service routing

---

> 💡 **Tip:** For K8s interviews, practice on a real cluster. Use [killer.sh](https://killer.sh/) for CKA/CKAD exam simulation.
