# 🕸️ Istio Service Mesh Cheatsheet

> Traffic management, security (mTLS), observability — the service mesh powering Google's infrastructure.

---

## 📦 Installation

```bash
# istioctl
curl -L https://istio.io/downloadIstio | sh -
istioctl install --set profile=demo -y               # Demo (all features)
istioctl install --set profile=production -y          # Production (minimal)
istioctl verify-install

# Helm
helm repo add istio https://istio-release.storage.googleapis.com/charts
helm install istio-base istio/base -n istio-system --create-namespace
helm install istiod istio/istiod -n istio-system

# Enable sidecar injection
kubectl label namespace production istio-injection=enabled
kubectl get namespace -L istio-injection               # Verify
```

## 🔀 VirtualService (Traffic Routing)

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: api-routing
spec:
  hosts:
    - api.example.com
  gateways:
    - api-gateway
  http:
    # Canary: 90/10 traffic split
    - match:
        - uri:
            prefix: /api/v2
      route:
        - destination:
            host: api-service
            subset: v2
          weight: 10
        - destination:
            host: api-service
            subset: v1
          weight: 90

    # Header-based routing (internal testing)
    - match:
        - headers:
            x-canary:
              exact: "true"
      route:
        - destination:
            host: api-service
            subset: v2

    # Default route
    - route:
        - destination:
            host: api-service
            subset: v1

    # Timeout & retries
    timeout: 10s
    retries:
      attempts: 3
      perTryTimeout: 3s
      retryOn: 5xx,reset,connect-failure
```

## 🎯 DestinationRule

```yaml
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: api-service
spec:
  host: api-service
  trafficPolicy:
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        h2UpgradePolicy: DEFAULT
        http1MaxPendingRequests: 100
        http2MaxRequests: 1000

    # Circuit breaker
    outlierDetection:
      consecutive5xxErrors: 5
      interval: 30s
      baseEjectionTime: 60s
      maxEjectionPercent: 50

    # Load balancing
    loadBalancer:
      simple: LEAST_REQUEST               # ROUND_ROBIN, RANDOM, PASSTHROUGH

  # Version subsets
  subsets:
    - name: v1
      labels:
        version: v1
    - name: v2
      labels:
        version: v2
```

## 🌐 Gateway

```yaml
apiVersion: networking.istio.io/v1beta1
kind: Gateway
metadata:
  name: api-gateway
spec:
  selector:
    istio: ingressgateway
  servers:
    - port:
        number: 443
        name: https
        protocol: HTTPS
      tls:
        mode: SIMPLE
        credentialName: api-tls-cert
      hosts:
        - api.example.com
    - port:
        number: 80
        name: http
        protocol: HTTP
      hosts:
        - api.example.com
      tls:
        httpsRedirect: true
```

## 🔒 Security (mTLS)

```yaml
# Strict mTLS for namespace
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: production
spec:
  mtls:
    mode: STRICT                          # STRICT, PERMISSIVE, DISABLE

---
# Authorization Policy (who can call what)
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: api-auth
  namespace: production
spec:
  selector:
    matchLabels:
      app: api
  rules:
    - from:
        - source:
            principals: ["cluster.local/ns/production/sa/frontend"]
      to:
        - operation:
            methods: ["GET", "POST"]
            paths: ["/api/*"]
    - from:
        - source:
            namespaces: ["monitoring"]
      to:
        - operation:
            methods: ["GET"]
            paths: ["/health", "/metrics"]
```

## 📊 Observability

```bash
# Kiali (service mesh visualization)
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
istioctl dashboard kiali

# Jaeger (distributed tracing)
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/jaeger.yaml
istioctl dashboard jaeger

# Grafana (dashboards)
istioctl dashboard grafana

# Prometheus
istioctl dashboard prometheus

# Envoy proxy debugging
istioctl proxy-status                                 # Sync status
istioctl proxy-config routes <pod>                   # Route config
istioctl proxy-config clusters <pod>                 # Cluster config
istioctl proxy-config endpoints <pod>                # Endpoints
istioctl analyze -n production                       # Config analysis
```

## 🐞 Troubleshooting

```bash
istioctl analyze                                      # Find config issues
istioctl proxy-status                                 # Check sidecar sync
istioctl proxy-config log <pod> --level debug        # Enable debug logging
kubectl logs <pod> -c istio-proxy                    # Sidecar logs
istioctl experimental check-inject -n production     # Injection status
```

## 🎯 FAANG Interview Q&A

```
Q: What problem does a service mesh solve?
A: Offloads cross-cutting concerns from application code:
   mTLS (zero-trust security), traffic management (canary, retries),
   observability (metrics, traces, logs), circuit breaking.
   Without mesh: every service implements these independently.

Q: Sidecar proxy pattern explained?
A: Envoy proxy deployed alongside every pod (injected automatically).
   All traffic passes through Envoy → enables transparent security,
   routing, and observability without app code changes.
   Control plane (istiod) pushes config to all sidecars.

Q: How would you do a canary release with Istio?
A: 1. Deploy v2 pods with version: v2 label
   2. DestinationRule: define v1 and v2 subsets
   3. VirtualService: weight split (95/5 → 90/10 → 50/50 → 0/100)
   4. Monitor error rates and latency in Kiali/Grafana
   5. If errors spike: shift 100% back to v1 (instant rollback)
```

---

> 💡 **Production Rule:** Start with `PERMISSIVE` mTLS mode during migration, then switch to `STRICT` once all services have sidecars. Use `istioctl analyze` to catch config issues before they hit production.
