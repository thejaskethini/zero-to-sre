# 🔄 ArgoCD Cheatsheet

> GitOps continuous delivery for Kubernetes — Application CRD, sync strategies, app-of-apps, and production workflows.

---

## 📦 Installation

```bash
# Namespace install
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Helm install
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -n argocd --create-namespace

# CLI
brew install argocd                                   # macOS
curl -sSL -o argocd https://github.com/argoproj/argo-cd/releases/latest/download/argocd-linux-amd64

# Login
argocd login argocd.example.com --grpc-web
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

## 📋 Application CRD

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: api-production
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-manifests.git
    targetRevision: main
    path: apps/api/overlays/production

  destination:
    server: https://kubernetes.default.svc
    namespace: production

  syncPolicy:
    automated:
      prune: true                        # Delete resources removed from git
      selfHeal: true                     # Auto-fix drift
      allowEmpty: false                  # Don't sync if source is empty
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        maxDuration: 3m
        factor: 2

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas               # Ignore HPA-managed replicas
```

## 🏗️ App-of-Apps Pattern

```yaml
# root-app.yaml — manages all other apps
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/k8s-manifests.git
    targetRevision: main
    path: apps                           # Contains Application YAMLs
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated:
      selfHeal: true
      prune: true
```

```
# Repository structure for app-of-apps
k8s-manifests/
├── apps/                              # Root app watches this
│   ├── api.yaml                       # Application CRD for API
│   ├── frontend.yaml                  # Application CRD for frontend
│   ├── monitoring.yaml                # Application CRD for Prometheus
│   └── ingress.yaml                   # Application CRD for nginx-ingress
├── base/
│   ├── api/
│   ├── frontend/
│   └── monitoring/
└── overlays/
    ├── staging/
    └── production/
```

## 📋 ApplicationSet (Dynamic App Generation)

```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: microservices
  namespace: argocd
spec:
  generators:
    - git:
        repoURL: https://github.com/myorg/k8s-manifests.git
        revision: main
        directories:
          - path: apps/*
  template:
    metadata:
      name: '{{path.basename}}'
    spec:
      project: default
      source:
        repoURL: https://github.com/myorg/k8s-manifests.git
        targetRevision: main
        path: '{{path}}'
      destination:
        server: https://kubernetes.default.svc
        namespace: '{{path.basename}}'
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
        syncOptions:
          - CreateNamespace=true
```

## 🔧 CLI Commands

```bash
# App management
argocd app list
argocd app get api-production
argocd app sync api-production                        # Manual sync
argocd app sync api-production --prune                # Sync + remove orphans
argocd app wait api-production                        # Wait for sync
argocd app diff api-production                        # Preview changes

# Rollback
argocd app history api-production
argocd app rollback api-production <revision>

# App actions
argocd app set api-production --sync-policy automated
argocd app set api-production -p image.tag=v2.0       # Set parameter
argocd app delete api-production --cascade             # Delete app + resources

# Repo & cluster management
argocd repo add https://github.com/myorg/repo.git --username user --password token
argocd cluster add my-cluster-context
argocd cluster list

# Projects
argocd proj list
argocd proj create team-a -d https://kubernetes.default.svc,production \
  -s https://github.com/myorg/*
```

## 🔐 RBAC & SSO

```yaml
# argocd-rbac-cm ConfigMap
apiVersion: v1
kind: ConfigMap
metadata:
  name: argocd-rbac-cm
  namespace: argocd
data:
  policy.csv: |
    # Role definitions
    p, role:staging-admin, applications, *, staging-*/*, allow
    p, role:production-viewer, applications, get, production-*/*, allow
    p, role:production-deployer, applications, sync, production-*/*, allow

    # Group bindings (from SSO)
    g, dev-team, role:staging-admin
    g, sre-team, role:production-deployer
    g, managers, role:production-viewer

  policy.default: role:readonly
```

## 🎯 FAANG Interview Q&A

```
Q: What is GitOps and why ArgoCD?
A: GitOps: Git as single source of truth for infrastructure.
   ArgoCD: K8s-native GitOps controller that continuously
   reconciles cluster state with Git. Benefits: audit trail,
   declarative, self-healing, rollback = git revert.

Q: ArgoCD vs FluxCD?
A: ArgoCD: UI dashboard, app-of-apps pattern, multi-cluster,
   ApplicationSet, RBAC. FluxCD: more lightweight, better
   Helm controller, native OCI support, no UI (by design).
   ArgoCD for teams needing visibility, FluxCD for GitOps purists.

Q: How do you handle secrets in GitOps?
A: Never store plaintext secrets in Git. Options:
   1. Sealed Secrets (encrypt in git, decrypt in cluster)
   2. External Secrets Operator (pull from Vault/AWS SM)
   3. SOPS + ArgoCD plugin (encrypted values files)
   4. Vault Agent Injector (inject at pod level)

Q: What's the app-of-apps pattern?
A: A root Application that manages other Application CRDs.
   Single entry point for the entire cluster's applications.
   Add a new service = add an Application YAML to git.
   ArgoCD auto-discovers and deploys it.
```

---

> 💡 **GitOps Rule:** The cluster should NEVER be modified directly (kubectl apply). Everything goes through Git. ArgoCD's selfHeal ensures any manual drift is automatically corrected.
