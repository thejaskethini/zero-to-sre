# 🔒 Caddy Cheatsheet

> The modern web server with **automatic HTTPS** — zero-config TLS, reverse proxy, static files, and more.

---

## 📦 Installation

```bash
# Debian/Ubuntu
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update && sudo apt install caddy

# macOS
brew install caddy

# Docker
docker run -d -p 80:80 -p 443:443 -v caddy_data:/data caddy

# Service management
sudo systemctl start caddy
sudo systemctl reload caddy                           # Apply config changes
sudo systemctl status caddy
caddy validate --config /etc/caddy/Caddyfile          # Validate before reload
caddy fmt --overwrite /etc/caddy/Caddyfile            # Auto-format config
```

## 📝 Caddyfile Syntax

```caddyfile
# Minimal static file server
localhost {
    root * /var/www/html
    file_server
}

# Reverse proxy (most common pattern)
api.example.com {
    reverse_proxy localhost:3000
}

# Multiple sites in one file
app.example.com {
    reverse_proxy localhost:3000
}
admin.example.com {
    reverse_proxy localhost:4000
}
```

## 🔒 Automatic HTTPS (Killer Feature)

```caddyfile
# Just use a domain name — Caddy handles EVERYTHING:
# ✅ Obtains certificate from Let's Encrypt
# ✅ Redirects HTTP → HTTPS
# ✅ Renews certificates automatically
# ✅ Enables OCSP stapling
# ✅ Uses modern TLS 1.2/1.3

myapp.example.com {
    reverse_proxy localhost:3000
}
# That's it. No certbot. No cron. No renewal scripts.

# Internal/staging with self-signed cert
staging.internal:443 {
    tls internal
    reverse_proxy localhost:3000
}

# Custom cert
secure.example.com {
    tls /path/to/cert.pem /path/to/key.pem
}
```

## 🔄 Reverse Proxy Patterns

```caddyfile
# Basic reverse proxy with headers
api.example.com {
    reverse_proxy localhost:8080 {
        header_up Host {upstream_hostport}
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
    }
}

# Load balancing
api.example.com {
    reverse_proxy 10.0.1.10:8080 10.0.1.11:8080 10.0.1.12:8080 {
        lb_policy round_robin          # or least_conn, ip_hash, random
        health_uri /health
        health_interval 10s
        health_timeout 5s
        fail_duration 30s
    }
}

# Path-based routing
example.com {
    handle /api/* {
        reverse_proxy localhost:3000
    }
    handle /admin/* {
        reverse_proxy localhost:4000
    }
    handle {
        root * /var/www/frontend
        file_server
        try_files {path} /index.html   # SPA support
    }
}

# WebSocket proxy
example.com {
    reverse_proxy /ws/* localhost:3000
}
```

## 🛡️ Security & Headers

```caddyfile
example.com {
    header {
        Strict-Transport-Security "max-age=31536000; includeSubDomains"
        X-Content-Type-Options "nosniff"
        X-Frame-Options "DENY"
        Referrer-Policy "strict-origin-when-cross-origin"
        Content-Security-Policy "default-src 'self'"
        -Server                        # Remove server header
    }

    # Rate limiting
    rate_limit {remote.ip} 10r/s

    # IP restriction
    @blocked remote_ip 1.2.3.4 5.6.7.0/24
    respond @blocked 403

    # Basic auth
    basicauth /admin/* {
        admin $2a$14$hash...           # caddy hash-password
    }
}
```

## ⚡ Performance & Caching

```caddyfile
example.com {
    encode gzip zstd                    # Compression (zstd is faster)

    @static path *.js *.css *.png *.jpg *.svg *.woff2
    header @static Cache-Control "public, max-age=31536000, immutable"

    reverse_proxy localhost:3000
}
```

## 📊 Logging

```caddyfile
example.com {
    log {
        output file /var/log/caddy/access.log {
            roll_size 100mb
            roll_keep 10
            roll_keep_for 720h          # 30 days
        }
        format json
        level INFO
    }
}
```

## 🆚 Caddy vs Nginx

```
Feature              Caddy                    Nginx
────────────────────────────────────────────────────────
Auto HTTPS           ✅ Built-in              ❌ Need Certbot
Config format        Caddyfile (simple)       nginx.conf (complex)
Hot reload           ✅ Zero-downtime API     ✅ nginx -s reload
HTTP/3               ✅ Built-in              ❌ Experimental
Performance          Good                     Excellent (C-based)
Ecosystem            Growing                  Massive
Memory usage         Higher (Go runtime)      Lower
Plugin system        Go modules               C modules
Use case             Small-medium apps        Everything
```

## 🎯 FAANG Interview Q&A

```
Q: When would you choose Caddy over Nginx?
A: Caddy for automatic TLS, simple configs, and small-medium deployments.
   Nginx for high-throughput, complex routing, and established ecosystems.
   Key: Caddy eliminates certificate management entirely.

Q: How does Caddy's automatic HTTPS work?
A: Caddy uses the ACME protocol to obtain certs from Let's Encrypt.
   It handles HTTP-01 or TLS-ALPN-01 challenges automatically,
   stores certs in its data directory, and renews before expiry.

Q: Caddy vs Traefik for Kubernetes?
A: Traefik is better for K8s — native CRD support, service discovery.
   Caddy is better for VM-based deployments with simple configs.
```

---

> 💡 **Production Tip:** Caddy's killer feature is zero-config HTTPS. If you're deploying anything web-facing and don't need Nginx-level performance tuning, Caddy will save you hours of certificate management.
