# ☸️ kubectl Advanced Cheatsheet

> Power-user kubectl — jsonpath, RBAC, network policies, debugging patterns, and node management.

---

## 🔍 JSONPath & Custom Output

```bash
# JSONPath queries
kubectl get pods -o jsonpath='{.items[*].metadata.name}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
kubectl get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'
kubectl get pods -o jsonpath='{.items[?(@.status.phase=="Running")].metadata.name}'
kubectl get pod mypod -o jsonpath='{.spec.containers[*].image}'
kubectl get secret mysecret -o jsonpath='{.data.password}' | base64 -d

# Custom columns
kubectl get pods -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName,IP:.status.podIP'
kubectl get pods -o custom-columns='NAME:.metadata.name,CPU:.spec.containers[0].resources.requests.cpu,MEM:.spec.containers[0].resources.requests.memory'

# Sort by field
kubectl get pods --sort-by=.status.startTime
kubectl get pods --sort-by=.spec.containers[0].resources.requests.memory
kubectl get events --sort-by=.lastTimestamp
```

## 🔐 RBAC

```bash
# Check permissions
kubectl auth can-i create deployments --namespace=production
kubectl auth can-i '*' '*' --all-namespaces           # Am I cluster-admin?
kubectl auth can-i get pods --as=system:serviceaccount:default:my-sa

# List RBAC resources
kubectl get clusterroles | grep -v system
kubectl get clusterrolebindings
kubectl get roles -n production
kubectl get rolebindings -n production

# Describe role permissions
kubectl describe clusterrole admin
kubectl describe rolebinding my-binding -n production

# Create role & binding
kubectl create role pod-reader --verb=get,list,watch --resource=pods -n production
kubectl create rolebinding pod-reader-binding --role=pod-reader \
  --serviceaccount=production:my-sa -n production
kubectl create clusterrolebinding admin-binding --clusterrole=admin \
  --user=admin@example.com
```

```yaml
# RBAC YAML
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: deployment-manager
  namespace: production
rules:
  - apiGroups: ["apps"]
    resources: ["deployments"]
    verbs: ["get", "list", "watch", "create", "update", "patch"]
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]
```

## 🌐 Network Policies

```yaml
# Deny all ingress by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: deny-all
  namespace: production
spec:
  podSelector: {}
  policyTypes: [Ingress]

---
# Allow only from specific namespace
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-from-frontend
spec:
  podSelector:
    matchLabels:
      app: api
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: frontend
        - podSelector:
            matchLabels:
              app: web
      ports:
        - port: 8080
          protocol: TCP
```

## 📐 Resource Management

```bash
# Resource quotas
kubectl get resourcequotas -A
kubectl describe resourcequota -n production

# LimitRange
kubectl get limitranges -A

# Top consumers
kubectl top pods -A --sort-by=cpu | head -20
kubectl top pods -A --sort-by=memory | head -20
kubectl top nodes
```

```yaml
# ResourceQuota
apiVersion: v1
kind: ResourceQuota
metadata:
  name: production-quota
  namespace: production
spec:
  hard:
    requests.cpu: "20"
    requests.memory: 40Gi
    limits.cpu: "40"
    limits.memory: 80Gi
    pods: "50"
    services: "20"
    persistentvolumeclaims: "10"

---
# LimitRange (per-pod defaults)
apiVersion: v1
kind: LimitRange
metadata:
  name: default-limits
  namespace: production
spec:
  limits:
    - type: Container
      default:
        cpu: "500m"
        memory: "256Mi"
      defaultRequest:
        cpu: "100m"
        memory: "128Mi"
```

## 🔧 Node Management

```bash
kubectl get nodes -o wide
kubectl describe node node-1
kubectl top nodes

# Cordon (no new pods)
kubectl cordon node-1
kubectl uncordon node-1

# Drain (evict all pods)
kubectl drain node-1 --ignore-daemonsets --delete-emptydir-data
kubectl drain node-1 --grace-period=60 --timeout=300s

# Taint & Tolerations
kubectl taint nodes node-1 dedicated=gpu:NoSchedule
kubectl taint nodes node-1 dedicated=gpu:NoSchedule-   # Remove taint

# Labels
kubectl label nodes node-1 disktype=ssd
kubectl get nodes -l disktype=ssd
```

## 🔄 Rollout Management

```bash
kubectl rollout status deployment/api -n production
kubectl rollout history deployment/api
kubectl rollout undo deployment/api                   # Rollback to previous
kubectl rollout undo deployment/api --to-revision=3   # Specific revision
kubectl rollout pause deployment/api                  # Pause rollout
kubectl rollout resume deployment/api                 # Resume rollout
kubectl rollout restart deployment/api                # Rolling restart

# Patch deployment
kubectl patch deployment api -p '{"spec":{"replicas":5}}'
kubectl set image deployment/api api=myapp:v2.0       # Update image
kubectl scale deployment api --replicas=10
```

## 🐛 Advanced Debugging

```bash
# Ephemeral debug containers (K8s 1.23+)
kubectl debug pod/mypod -it --image=nicolaka/netshoot --target=mycontainer
kubectl debug node/node-1 -it --image=ubuntu          # Debug node

# Copy files
kubectl cp production/mypod:/tmp/dump.sql ./dump.sql
kubectl cp ./config.yml production/mypod:/app/config.yml

# Port forwarding
kubectl port-forward pod/mypod 8080:8080
kubectl port-forward svc/myservice 8080:80
kubectl port-forward deployment/api 8080:8080

# Exec into pod
kubectl exec -it mypod -- /bin/sh
kubectl exec -it mypod -c sidecar -- /bin/bash        # Specific container

# Events
kubectl get events -n production --sort-by=.lastTimestamp | tail -20
kubectl get events --field-selector reason=FailedScheduling

# Resource diff
kubectl diff -f deployment.yaml                       # Preview changes
```

## 🎯 FAANG Interview Q&A

```
Q: How do you troubleshoot a pod stuck in Pending?
A: 1. kubectl describe pod → check Events section
   Common causes:
   - Insufficient resources → scale nodes or reduce requests
   - Node selector/affinity mismatch → check labels
   - PVC not bound → check storage class
   - Taint without toleration → add toleration

Q: How do you implement zero-downtime deployments?
A: 1. RollingUpdate strategy with maxSurge/maxUnavailable
   2. Readiness probes (don't route until ready)
   3. Liveness probes (restart unhealthy pods)
   4. PodDisruptionBudget (protect during drain)
   5. PreStop hook with sleep (allow LB to deregister)

Q: Explain the difference between Requests and Limits.
A: Requests: guaranteed minimum resources (used for scheduling).
   Limits: maximum resources (OOMKilled if exceeded for memory,
   throttled if exceeded for CPU). Set requests = limits for
   predictable performance (Guaranteed QoS class).
```

---

> 💡 **Power User Tip:** Master JSONPath and custom columns — they turn kubectl into a powerful query engine. Pipe output to `jq` for complex JSON manipulation.
