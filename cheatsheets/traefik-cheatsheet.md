# 🔀 Traefik Cheatsheet

> Cloud-native edge router — automatic service discovery, Docker/Kubernetes native, Let's Encrypt, and dynamic configuration.

---

## 📦 Installation

```bash
# Docker (most common)
docker run -d -p 80:80 -p 443:443 -p 8080:8080 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ./traefik.yml:/etc/traefik/traefik.yml \
  traefik:v3.0

# Helm (Kubernetes)
helm repo add traefik https://traefik.github.io/charts
helm install traefik traefik/traefik -n traefik --create-namespace

# Binary
wget https://github.com/traefik/traefik/releases/download/v3.0.0/traefik_v3.0.0_linux_amd64.tar.gz
tar xzf traefik_*.tar.gz && sudo mv traefik /usr/local/bin/
```

## ⚙️ Static vs Dynamic Config

```yaml
# traefik.yml (STATIC — requires restart)
api:
  dashboard: true
  insecure: true                        # Dashboard on :8080 (dev only!)

entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"

providers:
  docker:
    exposedByDefault: false             # Only route labeled containers
    network: traefik-net
  file:
    directory: /etc/traefik/dynamic     # Dynamic config files
    watch: true

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web

log:
  level: INFO
  format: json
accessLog:
  format: json
  fields:
    headers:
      defaultMode: keep
```

## 🐳 Docker Provider (Most Common)

```yaml
# docker-compose.yml
services:
  traefik:
    image: traefik:v3.0
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./traefik.yml:/etc/traefik/traefik.yml
      - letsencrypt:/letsencrypt
    networks:
      - traefik-net

  api:
    image: myapp:latest
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.example.com`)"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.services.api.loadbalancer.server.port=3000"
      # Middlewares
      - "traefik.http.routers.api.middlewares=rate-limit,headers"
      - "traefik.http.middlewares.rate-limit.ratelimit.average=100"
      - "traefik.http.middlewares.rate-limit.ratelimit.burst=50"
    networks:
      - traefik-net

networks:
  traefik-net:
    external: true

volumes:
  letsencrypt:
```

## ☸️ Kubernetes Ingress

```yaml
# IngressRoute CRD (Traefik-native)
apiVersion: traefik.io/v1alpha1
kind: IngressRoute
metadata:
  name: api-route
  namespace: production
spec:
  entryPoints:
    - websecure
  routes:
    - match: Host(`api.example.com`) && PathPrefix(`/v1`)
      kind: Rule
      services:
        - name: api-service
          port: 8080
      middlewares:
        - name: rate-limit
        - name: security-headers
  tls:
    certResolver: letsencrypt

---
# Middleware CRD
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: rate-limit
spec:
  rateLimit:
    average: 100
    burst: 50

---
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata:
  name: security-headers
spec:
  headers:
    stsSeconds: 31536000
    stsIncludeSubdomains: true
    frameDeny: true
    contentTypeNosniff: true
    browserXssFilter: true
```

## 🧩 Key Middlewares

```yaml
# Rate Limiting
- "traefik.http.middlewares.rl.ratelimit.average=100"
- "traefik.http.middlewares.rl.ratelimit.burst=50"
- "traefik.http.middlewares.rl.ratelimit.period=1s"

# Basic Auth
- "traefik.http.middlewares.auth.basicauth.users=admin:$$apr1$$hash"

# IP Whitelist
- "traefik.http.middlewares.ipwl.ipallowlist.sourcerange=10.0.0.0/8,172.16.0.0/12"

# Circuit Breaker
- "traefik.http.middlewares.cb.circuitbreaker.expression=LatencyAtQuantileMS(50.0) > 100"

# Retry
- "traefik.http.middlewares.retry.retry.attempts=4"
- "traefik.http.middlewares.retry.retry.initialinterval=100ms"

# Compress
- "traefik.http.middlewares.compress.compress=true"

# Strip Prefix
- "traefik.http.middlewares.strip.stripprefix.prefixes=/api"

# Headers
- "traefik.http.middlewares.sec.headers.stsSeconds=31536000"
- "traefik.http.middlewares.sec.headers.frameDeny=true"

# Redirect regex
- "traefik.http.middlewares.redir.redirectregex.regex=^https://old.example.com/(.*)"
- "traefik.http.middlewares.redir.redirectregex.replacement=https://new.example.com/$${1}"
```

## 📊 Routing Rules

```
Host(`example.com`)                    # Domain match
Host(`example.com`) && Path(`/api`)    # Domain + exact path
PathPrefix(`/api`)                     # Path prefix
Headers(`X-Custom`, `value`)           # Header match
Method(`GET`, `POST`)                  # HTTP method
ClientIP(`10.0.0.0/8`)               # Client IP range
Query(`token`, `abc123`)              # Query parameter
HostRegexp(`{subdomain:.+}.example.com`)  # Regex host
```

## 🔍 Debugging & Dashboard

```bash
# Dashboard at http://localhost:8080
# Shows: routers, services, middlewares, entrypoints

# CLI
traefik healthcheck                    # Health check
traefik version                        # Version info

# Docker debugging
docker logs traefik -f                 # Follow logs
docker exec traefik traefik healthcheck

# Check config
curl http://localhost:8080/api/rawdata | jq .  # Full config dump
curl http://localhost:8080/api/http/routers | jq .
curl http://localhost:8080/api/http/services | jq .
```

## 🎯 FAANG Interview Q&A

```
Q: Why Traefik over Nginx for microservices?
A: Traefik auto-discovers services from Docker/K8s labels — no manual
   config reload. Native service discovery is critical for dynamic
   container environments where services scale up/down frequently.

Q: How does Traefik handle SSL certificates?
A: Built-in ACME client auto-obtains & renews from Let's Encrypt.
   Supports HTTP-01, TLS-ALPN-01, and DNS-01 challenges.
   Stores certs in acme.json file or distributed KV stores.

Q: Traefik vs Istio for traffic management?
A: Traefik = edge router (north-south traffic, ingress).
   Istio = service mesh (east-west traffic, inter-service).
   They're complementary: Traefik at ingress, Istio inside cluster.

Q: How would you implement canary deployments with Traefik?
A: Use weighted round-robin in services:
   services: [{name: v1, weight: 90}, {name: v2, weight: 10}]
   Gradually shift weight to v2 while monitoring error rates.
```

---

> 💡 **Production Rule:** Always set `exposedByDefault: false` in Docker provider. Only containers with `traefik.enable=true` labels should be routed. Never expose the dashboard in production without auth.
