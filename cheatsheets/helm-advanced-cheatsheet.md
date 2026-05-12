# 🏗️ Helm Advanced Cheatsheet

> Chart development, templating, hooks, library charts, OCI registries, and production best practices.

---

## 📁 Chart Structure

```
mychart/
├── Chart.yaml                    # Chart metadata
├── Chart.lock                    # Dependency lock file
├── values.yaml                   # Default values
├── values-staging.yaml           # Environment overrides
├── values-production.yaml
├── templates/
│   ├── _helpers.tpl              # Template helpers/partials
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   ├── hpa.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   ├── serviceaccount.yaml
│   ├── NOTES.txt                 # Post-install message
│   └── tests/
│       └── test-connection.yaml
├── charts/                       # Dependency charts
└── .helmignore
```

## 📐 Templating Deep Dive

```yaml
# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "mychart.fullname" . }}
  labels:
    {{- include "mychart.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  selector:
    matchLabels:
      {{- include "mychart.selectorLabels" . | nindent 6 }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          ports:
            - containerPort: {{ .Values.service.port }}
          {{- with .Values.resources }}
          resources:
            {{- toYaml . | nindent 12 }}
          {{- end }}
          {{- if .Values.env }}
          env:
            {{- range $key, $value := .Values.env }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
          {{- end }}
```

## 🧩 Helpers (_helpers.tpl)

```yaml
# templates/_helpers.tpl
{{- define "mychart.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name .Chart.Name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "mychart.labels" -}}
helm.sh/chart: {{ .Chart.Name }}-{{ .Chart.Version }}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{- define "mychart.selectorLabels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}
```

## 🪝 Hooks

```yaml
# Pre-install database migration
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "mychart.fullname" . }}-migrate
  annotations:
    "helm.sh/hook": pre-install,pre-upgrade
    "helm.sh/hook-weight": "-5"              # Lower runs first
    "helm.sh/hook-delete-policy": before-hook-creation,hook-succeeded
spec:
  template:
    spec:
      restartPolicy: Never
      containers:
        - name: migrate
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
          command: ["npm", "run", "migrate"]

# Hook types:
# pre-install, post-install
# pre-delete, post-delete
# pre-upgrade, post-upgrade
# pre-rollback, post-rollback
# test
```

## 📦 OCI Registry

```bash
# Push to OCI registry
helm package mychart/
helm push mychart-1.0.0.tgz oci://ghcr.io/myorg/charts
helm push mychart-1.0.0.tgz oci://registry.example.com/charts

# Pull from OCI
helm pull oci://ghcr.io/myorg/charts/mychart --version 1.0.0
helm install myapp oci://ghcr.io/myorg/charts/mychart --version 1.0.0

# Login to registry
helm registry login ghcr.io -u USERNAME -p TOKEN
```

## 🔌 Helm Diff Plugin

```bash
# Install
helm plugin install https://github.com/databus23/helm-diff

# Preview changes before upgrade
helm diff upgrade myapp ./mychart -f values-production.yaml
helm diff upgrade myapp ./mychart --set image.tag=v2.0
helm diff revision myapp 3 4                         # Diff between revisions
helm diff rollback myapp 3                           # Preview rollback
```

## 🔐 Secrets Management

```yaml
# Using external secrets (recommended)
# helm-secrets plugin
helm plugin install https://github.com/jkroepke/helm-secrets

# Encrypt values file with sops
sops -e values-secrets.yaml > values-secrets.enc.yaml
helm secrets install myapp ./mychart -f values-secrets.enc.yaml

# Or use Sealed Secrets / External Secrets Operator
# templates/external-secret.yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: {{ include "mychart.fullname" . }}-secrets
spec:
  secretStoreRef:
    name: aws-secrets-manager
    kind: ClusterSecretStore
  target:
    name: {{ include "mychart.fullname" . }}-secrets
  data:
    - secretKey: db-password
      remoteRef:
        key: production/db-password
```

## 🏗️ Production values.yaml Pattern

```yaml
# values.yaml
replicaCount: 3

image:
  repository: ghcr.io/myorg/api
  tag: ""                                  # Override via CI/CD
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 8080

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

resources:
  requests:
    cpu: 250m
    memory: 256Mi
  limits:
    cpu: 500m
    memory: 512Mi

autoscaling:
  enabled: true
  minReplicas: 3
  maxReplicas: 20
  targetCPUUtilization: 70

probes:
  liveness:
    path: /health
    initialDelaySeconds: 15
  readiness:
    path: /ready
    initialDelaySeconds: 5
```

## 🎯 FAANG Interview Q&A

```
Q: Helm vs Kustomize?
A: Helm: full templating engine, versioned packages, dependency mgmt,
   hooks, rollback. Best for shared/reusable charts.
   Kustomize: overlay-based patching, no templating, built into kubectl.
   Best for simple env-specific customization. Many teams use both.

Q: How do you handle Helm chart versioning?
A: Semantic versioning (SemVer). Chart version in Chart.yaml tracks
   chart changes. AppVersion tracks the application version.
   Store charts in OCI registry or Helm repo. Pin versions in
   production. Use helm diff before every upgrade.

Q: How would you implement canary releases with Helm?
A: 1. Deploy canary as separate release: helm install api-canary ./chart
   2. Use Ingress annotations for traffic splitting (10% canary)
   3. Monitor metrics, errors, latency
   4. If healthy: promote canary image to main release
   5. Delete canary release
   Or use Argo Rollouts for automated canary analysis.
```

---

> 💡 **Production Rule:** Always use `helm diff` before `helm upgrade`. Always pin chart versions. Never store secrets in values.yaml. Use `--atomic` flag for automatic rollback on failure.
