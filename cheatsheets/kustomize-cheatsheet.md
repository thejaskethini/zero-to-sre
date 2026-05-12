# 📐 Kustomize Cheatsheet

> Kubernetes native configuration management — bases, overlays, patches, and multi-environment setups without templating.

---

## 📁 Directory Structure

```
k8s/
├── base/                              # Shared base resources
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── configmap.yaml
│   └── hpa.yaml
├── overlays/
│   ├── development/
│   │   ├── kustomization.yaml
│   │   └── replica-patch.yaml
│   ├── staging/
│   │   ├── kustomization.yaml
│   │   ├── replica-patch.yaml
│   │   └── env-patch.yaml
│   └── production/
│       ├── kustomization.yaml
│       ├── replica-patch.yaml
│       ├── resource-patch.yaml
│       └── ingress.yaml
```

## 📋 Base kustomization.yaml

```yaml
# base/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml

commonLabels:
  app: myapi
  managed-by: kustomize

commonAnnotations:
  team: platform

images:
  - name: myapi
    newName: ghcr.io/myorg/api
    newTag: latest
```

## 🔧 Overlay (Production)

```yaml
# overlays/production/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

namespace: production
namePrefix: prod-
nameSuffix: ""

resources:
  - ../../base
  - ingress.yaml                         # Production-only resources

patches:
  - path: replica-patch.yaml
  - path: resource-patch.yaml

images:
  - name: myapi
    newName: ghcr.io/myorg/api
    newTag: v2.0.0                        # Pin to specific version

configMapGenerator:
  - name: app-config
    behavior: merge
    literals:
      - NODE_ENV=production
      - LOG_LEVEL=warn

secretGenerator:
  - name: db-credentials
    literals:
      - DB_HOST=prod-db.internal
      - DB_NAME=production
    type: Opaque

replicas:
  - name: myapi
    count: 5
```

## 📝 Patch Types

```yaml
# Strategic Merge Patch (most common)
# overlays/production/replica-patch.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapi
spec:
  replicas: 5
  template:
    spec:
      containers:
        - name: myapi
          resources:
            requests:
              cpu: 500m
              memory: 512Mi
            limits:
              cpu: "1"
              memory: 1Gi
          env:
            - name: NODE_ENV
              value: production
```

```yaml
# JSON Patch (precise operations)
# overlays/production/kustomization.yaml
patches:
  - target:
      kind: Deployment
      name: myapi
    patch: |-
      - op: replace
        path: /spec/replicas
        value: 5
      - op: add
        path: /spec/template/spec/containers/0/env/-
        value:
          name: LOG_LEVEL
          value: warn
```

```yaml
# Inline patches
patches:
  - target:
      kind: Deployment
      name: myapi
    patch: |-
      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: myapi
      spec:
        replicas: 10
```

## ⚡ Generators

```yaml
# ConfigMap from file
configMapGenerator:
  - name: nginx-config
    files:
      - nginx.conf
      - configs/app.properties
  - name: app-env
    envs:
      - .env.production
  - name: app-config
    literals:
      - API_URL=https://api.example.com
      - LOG_LEVEL=info

# Secret generator
secretGenerator:
  - name: tls-certs
    files:
      - tls.crt=certs/server.crt
      - tls.key=certs/server.key
    type: kubernetes.io/tls
  - name: db-secret
    literals:
      - password=supersecret
    options:
      disableNameSuffixHash: true         # Don't append hash
```

## 🔧 CLI Commands

```bash
# Build (preview output)
kubectl kustomize overlays/production
kustomize build overlays/production

# Apply
kubectl apply -k overlays/production
kubectl apply -k overlays/staging

# Diff before applying
kubectl diff -k overlays/production

# Delete
kubectl delete -k overlays/production

# View resources
kubectl kustomize overlays/production | kubectl get -f - -o name
```

## 🏗️ Advanced Features

```yaml
# Components (reusable optional features)
# components/monitoring/kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1alpha1
kind: Component
resources:
  - service-monitor.yaml
patches:
  - target:
      kind: Deployment
    patch: |-
      - op: add
        path: /spec/template/metadata/annotations/prometheus.io~1scrape
        value: "true"

# Use component in overlay
# overlays/production/kustomization.yaml
components:
  - ../../components/monitoring
```

```yaml
# Replacement transformers (rename references)
replacements:
  - source:
      kind: ConfigMap
      name: app-config
      fieldPath: metadata.name
    targets:
      - select:
          kind: Deployment
        fieldPaths:
          - spec.template.spec.containers.[name=myapi].envFrom.[configMapRef].name
```

## 🆚 Kustomize vs Helm

```
Feature              Kustomize              Helm
─────────────────────────────────────────────────
Templating           No (patches)           Yes (Go templates)
Learning curve       Low                    Medium-High
Package management   No                     Yes (charts, repos)
Versioning           No                     Yes (SemVer)
Rollback             No (use git)           Yes (helm rollback)
Hooks                No                     Yes (pre/post hooks)
Dependencies         No                     Yes (subcharts)
Built into kubectl   Yes                    No (separate tool)
Best for             Simple env diffs       Reusable packages
```

## 🎯 FAANG Interview Q&A

```
Q: When would you use Kustomize over Helm?
A: Kustomize: when you manage YOUR OWN manifests across envs
   (dev/staging/prod) and don't need templating or packaging.
   Helm: when you need reusable charts, versioning, or are
   deploying third-party software (nginx, prometheus, etc.).
   Many teams use both: Helm for third-party, Kustomize for internal.

Q: How does Kustomize handle config drift between environments?
A: Base contains shared config. Overlays add/modify only what differs.
   Strategic merge patches layer env-specific changes cleanly.
   You can see exactly what's different in each environment by
   reading the overlay — no template variable hunting.

Q: What's the configMapGenerator hash suffix?
A: Kustomize appends a hash of the content to ConfigMap/Secret names.
   When content changes, the name changes, which triggers a
   Deployment rollout (new pod spec → rolling update).
   This solves the "config changed but pods didn't restart" problem.
```

---

> 💡 **Production Pattern:** Use Kustomize for internal services (base + overlays), Helm for third-party charts. Combine them: `helmCharts` in kustomization.yaml can render Helm charts with Kustomize overlays.
