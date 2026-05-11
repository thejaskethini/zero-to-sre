# 🏗️ Helm Cheatsheet

> Essential Helm commands for managing Kubernetes applications.

---

## 📦 Repository Management

```bash
helm repo add stable https://charts.helm.sh/stable     # Add repo
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus https://prometheus-community.github.io/helm-charts
helm repo update                                         # Refresh repos
helm repo list                                           # List repos
helm search repo prometheus                              # Search
helm search hub ingress                                  # Search Artifact Hub
```

## 🚀 Install & Upgrade

```bash
helm install myapp ./chart                               # Install from local
helm install myapp bitnami/nginx                         # Install from repo
helm install myapp bitnami/nginx -n production --create-namespace

# With custom values
helm install myapp ./chart -f values-prod.yaml
helm install myapp ./chart --set image.tag=v2.0

# Upgrade
helm upgrade myapp ./chart -f values-prod.yaml
helm upgrade --install myapp ./chart                     # Install or upgrade

# Rollback
helm rollback myapp 1                                    # Rollback to revision 1
helm history myapp                                       # Show revision history
```

## 🔍 Inspect & Debug

```bash
helm list -A                                             # List all releases
helm status myapp                                        # Release status
helm get values myapp                                    # Current values
helm get manifest myapp                                  # Rendered manifests

# Dry run / debug
helm install myapp ./chart --dry-run --debug
helm template myapp ./chart                              # Render locally
helm template myapp ./chart --show-only templates/deployment.yaml
```

## 🗑️ Uninstall

```bash
helm uninstall myapp                                     # Remove release
helm uninstall myapp -n production                       # With namespace
helm uninstall myapp --keep-history                      # Keep history
```

## 📝 Chart Development

```bash
helm create mychart                                      # Scaffold new chart
helm lint ./mychart                                      # Validate chart
helm package ./mychart                                   # Package as .tgz
helm dependency update ./mychart                         # Update dependencies
helm dependency list ./mychart                           # List dependencies
```

## 🧪 Testing

```bash
helm test myapp                                          # Run chart tests
helm install myapp ./chart --dry-run                     # Dry run
```

---

> 💡 **Tips:** Always use `--dry-run` before real installs. Keep values files in version control. Use `helm diff` plugin to preview upgrades.
