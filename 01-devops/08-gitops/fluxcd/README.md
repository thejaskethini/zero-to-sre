# 🔄 FluxCD — GitOps Toolkit

> **FluxCD is a CNCF graduated GitOps operator that keeps your Kubernetes clusters in sync with Git.**

## ArgoCD vs FluxCD

| Feature | ArgoCD | FluxCD |
|---------|--------|--------|
| UI | Rich web UI | No UI (CLI + Grafana) |
| Architecture | Centralized server | Distributed controllers |
| Multi-cluster | Application sets | Kustomization |
| Helm support | Native | Helm Controller |
| OCI support | Limited | Native (OCI artifacts) |
| Best for | Teams wanting UI | GitOps purists, multi-tenant |

## Quick Start

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap (GitHub)
flux bootstrap github \
  --owner=myorg \
  --repository=fleet-infra \
  --path=clusters/production \
  --personal

# Check status
flux get all

# Create a source
flux create source git myapp \
  --url=https://github.com/myorg/myapp \
  --branch=main \
  --interval=1m

# Create a kustomization
flux create kustomization myapp \
  --source=myapp \
  --path="./k8s" \
  --prune=true \
  --interval=5m
```

## Core Components

| Component | Purpose |
|-----------|---------|
| **Source Controller** | Fetches manifests from Git, Helm, OCI |
| **Kustomize Controller** | Applies Kustomize overlays |
| **Helm Controller** | Manages Helm releases |
| **Notification Controller** | Sends alerts (Slack, Teams, webhooks) |
| **Image Automation** | Auto-updates image tags in Git |

## Further Reading

- [FluxCD Docs](https://fluxcd.io/docs/)
- [FluxCD vs ArgoCD](https://fluxcd.io/blog/2023/12/flux-vs-argocd/)
