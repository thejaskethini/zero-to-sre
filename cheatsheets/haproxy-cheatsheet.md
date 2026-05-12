# ⚖️ HAProxy Cheatsheet

> The industry-standard TCP/HTTP load balancer — used by GitHub, Stack Overflow, Reddit for ultra-high-throughput traffic management.

---

## 📦 Installation & Service

```bash
sudo apt install -y haproxy                           # Debian/Ubuntu
sudo yum install -y haproxy                           # CentOS/RHEL
brew install haproxy                                  # macOS

sudo systemctl start haproxy
sudo systemctl reload haproxy                         # Graceful reload
sudo systemctl enable haproxy
haproxy -c -f /etc/haproxy/haproxy.cfg               # Validate config
```

## ⚙️ Config Structure

```haproxy
# /etc/haproxy/haproxy.cfg

#── GLOBAL ──────────────────────────────────
global
    log /dev/log local0
    log /dev/log local1 notice
    maxconn 50000
    user haproxy
    group haproxy
    daemon
    stats socket /run/haproxy/admin.sock mode 660 level admin
    tune.ssl.default-dh-param 2048

#── DEFAULTS ────────────────────────────────
defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    option  forwardfor
    timeout connect 5s
    timeout client  30s
    timeout server  30s
    timeout http-request 10s
    timeout http-keep-alive 10s
    errorfile 503 /etc/haproxy/errors/503.http

#── FRONTEND (receives traffic) ─────────────
frontend http_front
    bind *:80
    bind *:443 ssl crt /etc/haproxy/certs/combined.pem alpn h2,http/1.1
    http-request redirect scheme https unless { ssl_fc }

    # ACL-based routing
    acl is_api path_beg /api
    acl is_admin path_beg /admin
    acl is_websocket hdr(Upgrade) -i websocket

    use_backend api_servers if is_api
    use_backend admin_servers if is_admin
    use_backend ws_servers if is_websocket
    default_backend web_servers

#── BACKEND (sends traffic to) ──────────────
backend web_servers
    balance roundrobin
    option httpchk GET /health
    http-check expect status 200
    server web1 10.0.1.10:8080 check inter 5s fall 3 rise 2
    server web2 10.0.1.11:8080 check inter 5s fall 3 rise 2
    server web3 10.0.1.12:8080 check inter 5s fall 3 rise 2 backup

backend api_servers
    balance leastconn
    option httpchk GET /api/health
    server api1 10.0.2.10:3000 check weight 5
    server api2 10.0.2.11:3000 check weight 3
    server api3 10.0.2.12:3000 check weight 2

backend admin_servers
    balance roundrobin
    server admin1 10.0.3.10:4000 check

backend ws_servers
    balance source
    timeout tunnel 1h
    server ws1 10.0.4.10:9000 check
    server ws2 10.0.4.11:9000 check
```

## ⚖️ Load Balancing Algorithms

```
roundrobin    → Equal distribution, most common
leastconn     → Fewest active connections (best for varying request times)
source        → IP hash (sticky sessions, good for WebSocket)
uri           → Hash the URI (good for caching layers)
hdr(name)     → Hash a header value (e.g., X-User-ID)
random(2)     → Power-of-two random choice
first         → Fill first server before moving to next
```

## 🩺 Health Checks

```haproxy
backend api_servers
    option httpchk GET /health HTTP/1.1\r\nHost:\ api.internal
    http-check expect status 200
    http-check expect string "ok"

    # Health check parameters
    server api1 10.0.1.10:8080 check inter 3s fall 3 rise 2 weight 100
    # check    → Enable health checks
    # inter 3s → Check every 3 seconds
    # fall 3   → Mark DOWN after 3 consecutive failures
    # rise 2   → Mark UP after 2 consecutive successes
    # weight   → Relative traffic weight

    # Slow start (gradually ramp traffic after recovery)
    server api2 10.0.1.11:8080 check slowstart 30s
```

## 🔒 SSL/TLS

```haproxy
frontend https_front
    bind *:443 ssl crt /etc/haproxy/certs/ alpn h2,http/1.1
    # Loads all .pem files from the directory

    # Modern TLS
    ssl-default-bind-ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256
    ssl-default-bind-ciphersuites TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384
    ssl-default-bind-options ssl-min-ver TLSv1.2

    # HSTS
    http-response set-header Strict-Transport-Security "max-age=31536000; includeSubDomains"
```

## 📊 Stats Page (Monitoring)

```haproxy
listen stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
    stats admin if TRUE                # Enable admin actions
    stats auth admin:SecurePassword    # Basic auth
    stats show-legends
```

## 🔧 ACLs & Traffic Control

```haproxy
frontend http_front
    # IP-based blocking
    acl blocked_ips src 1.2.3.4 5.6.7.0/24
    http-request deny if blocked_ips

    # Rate limiting (stick tables)
    stick-table type ip size 200k expire 30s store http_req_rate(10s)
    http-request track-sc0 src
    http-request deny deny_status 429 if { sc_http_req_rate(0) gt 100 }

    # Maintenance mode
    acl maintenance always_false       # Change to always_true to enable
    http-request redirect location /maintenance.html if maintenance

    # Header-based routing
    acl is_mobile hdr_sub(User-Agent) -i mobile
    use_backend mobile_servers if is_mobile
```

## 🐞 Debugging

```bash
# Check config
haproxy -c -f /etc/haproxy/haproxy.cfg

# Runtime management via socket
echo "show stat" | socat stdio /run/haproxy/admin.sock
echo "show info" | socat stdio /run/haproxy/admin.sock
echo "show servers state" | socat stdio /run/haproxy/admin.sock

# Drain a server (graceful removal)
echo "set server api_servers/api1 state drain" | socat stdio /run/haproxy/admin.sock

# Disable/enable server
echo "set server api_servers/api1 state maint" | socat stdio /run/haproxy/admin.sock
echo "set server api_servers/api1 state ready" | socat stdio /run/haproxy/admin.sock

# Change weight
echo "set server api_servers/api1 weight 50%" | socat stdio /run/haproxy/admin.sock
```

## 🎯 FAANG Interview Q&A

```
Q: HAProxy vs Nginx as a load balancer?
A: HAProxy: purpose-built LB, better health checks, stick tables,
   runtime API, superior for pure TCP/HTTP load balancing.
   Nginx: also serves static content, reverse proxy, more versatile.
   HAProxy wins at high-concurrency L4/L7 load balancing.

Q: How does HAProxy handle session persistence?
A: Three methods:
   1. source — IP-hash (simple, breaks with NAT)
   2. cookie — Insert/prefix cookie with server ID (best for HTTP)
   3. stick-table — Store session mapping in shared table

Q: How to do zero-downtime deployments with HAProxy?
A: 1. Deploy new version to new servers
   2. Add new servers to backend with "check"
   3. Wait for health checks to pass
   4. Drain old servers: "set server state drain"
   5. Wait for connections to finish
   6. Remove old servers from config

Q: What's a stick table?
A: In-memory key-value store for tracking per-client state:
   connection rates, error rates, bytes transferred.
   Used for rate limiting, abuse detection, session persistence.
   Can be replicated between HAProxy peers for HA.
```

---

> 💡 **Production Rule:** HAProxy's stats page and runtime socket API are incredibly powerful for debugging. Always enable them (behind auth). Use `drain` state before removing servers — never hard-remove.
