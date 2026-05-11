# 📋 kubectl Cheatsheet

> Quick reference for the most commonly used Kubernetes commands.

---

## 🔍 Cluster Info

```bash
kubectl cluster-info                     # Cluster endpoint info
kubectl get nodes -o wide                # List nodes with details
kubectl top nodes                        # Node resource usage
kubectl api-resources                    # All available resource types
kubectl explain deployment.spec          # Docs for any resource field
```

## 📦 Pods

```bash
kubectl get pods                         # List pods (current namespace)
kubectl get pods -A                      # List pods (all namespaces)
kubectl get pods -o wide                 # With IP and node info
kubectl get pods --sort-by=.status.startTime  # Sort by start time
kubectl describe pod <name>              # Detailed pod info
kubectl logs <pod>                       # Pod logs
kubectl logs <pod> -c <container>        # Specific container logs
kubectl logs <pod> -f                    # Follow/stream logs
kubectl logs <pod> --previous            # Logs from crashed container
kubectl exec -it <pod> -- sh            # Shell into pod
kubectl port-forward <pod> 8080:3000     # Port forward
kubectl cp <pod>:/path/file ./local      # Copy from pod
kubectl delete pod <name>               # Delete pod
kubectl top pods                        # Pod resource usage
```

## 🚀 Deployments

```bash
kubectl get deployments                  # List deployments
kubectl describe deployment <name>      # Details
kubectl scale deployment <name> --replicas=5    # Scale
kubectl set image deployment/<name> app=img:v2  # Update image
kubectl rollout status deployment/<name>        # Rollout progress
kubectl rollout history deployment/<name>       # History
kubectl rollout undo deployment/<name>          # Rollback
kubectl rollout undo deployment/<name> --to-revision=2  # Specific
kubectl rollout restart deployment/<name>       # Restart all pods
```

## 🌐 Services & Networking

```bash
kubectl get svc                          # List services
kubectl get endpoints                    # Service endpoints
kubectl get ingress                      # List ingress rules
kubectl port-forward svc/<name> 8080:80  # Forward service port
kubectl get networkpolicies              # Network policies
```

## 🔧 ConfigMaps & Secrets

```bash
kubectl get configmaps                   # List configmaps
kubectl get secrets                      # List secrets
kubectl create secret generic my-secret --from-literal=key=value
kubectl create configmap my-config --from-file=config.yml
kubectl get secret <name> -o jsonpath='{.data.password}' | base64 -d
```

## 📋 Namespaces

```bash
kubectl get namespaces                   # List namespaces
kubectl create namespace staging         # Create namespace
kubectl config set-context --current --namespace=staging  # Switch
```

## 🔎 Debugging

```bash
kubectl get events --sort-by='.lastTimestamp'  # Recent events
kubectl get pods --field-selector=status.phase=Failed  # Failed pods
kubectl describe node <name> | grep -A 5 Conditions  # Node health
kubectl run debug --image=busybox -it --rm -- sh  # Debug pod
kubectl auth can-i create deployments    # Permission check
```

## 🏷️ Labels & Selectors

```bash
kubectl get pods -l app=myapp            # Filter by label
kubectl get pods -l 'env in (prod,staging)'  # Multiple values
kubectl label pod <name> version=v2      # Add label
kubectl label pod <name> version-        # Remove label
```

## 📊 Output Formatting

```bash
kubectl get pods -o json                 # JSON output
kubectl get pods -o yaml                 # YAML output
kubectl get pods -o name                 # Just names
kubectl get pods -o jsonpath='{.items[*].metadata.name}'  # JSONPath
kubectl get pods --no-headers            # Skip headers (for scripts)
```

---

> 💡 **Tip:** Install [kubectx + kubens](https://github.com/ahmetb/kubectx) for fast context/namespace switching, and [k9s](https://k9scli.io/) for a terminal UI.
