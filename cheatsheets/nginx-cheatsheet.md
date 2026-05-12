# 🌐 Nginx Cheatsheet

> Production-grade Nginx configuration — reverse proxy, load balancing, SSL, caching, and security hardening.

---

## 📦 Installation & Service Management

```bash
# Install
sudo apt update && sudo apt install -y nginx         # Debian/Ubuntu
sudo yum install -y epel-release && sudo yum install -y nginx  # CentOS/RHEL
brew install nginx                                     # macOS

# Service management
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx
sudo systemctl reload nginx                            # Graceful reload (no downtime)
sudo systemctl enable nginx                            # Start on boot
sudo systemctl status nginx

# Test configuration before reload (ALWAYS do this)
sudo nginx -t
sudo nginx -T                                          # Test + dump full config
```

## 📂 Config Structure

```
/etc/nginx/
├── nginx.conf                    # Main config
├── conf.d/                       # Additional configs (auto-included)
│   ├── default.conf
│   └── myapp.conf
├── sites-available/              # Available vhosts (Debian-style)
├── sites-enabled/                # Symlinked active vhosts
├── snippets/                     # Reusable config fragments
├── mime.types                    # MIME type mappings
└── modules-enabled/              # Dynamic modules
```

```bash
# Enable/disable sites (Debian/Ubuntu)
sudo ln -s /etc/nginx/sites-available/myapp /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/myapp                 # Disable
```

## 🔄 Reverse Proxy (Most Common Pattern)

```nginx
# Basic reverse proxy — forward traffic to a backend app
upstream backend {
    server 127.0.0.1:3000;
}

server {
    listen 80;
    server_name myapp.example.com;

    location / {
        proxy_pass http://backend;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## ⚖️ Load Balancing

```nginx
# Round Robin (default)
upstream api_cluster {
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
    server 10.0.1.12:8080;
}

# Weighted distribution
upstream api_weighted {
    server 10.0.1.10:8080 weight=5;       # Gets 5x traffic
    server 10.0.1.11:8080 weight=3;
    server 10.0.1.12:8080 weight=2;
}

# Least connections (best for varying request times)
upstream api_least {
    least_conn;
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
}

# IP Hash (sticky sessions)
upstream api_sticky {
    ip_hash;
    server 10.0.1.10:8080;
    server 10.0.1.11:8080;
}

# Health checks & failover
upstream api_resilient {
    server 10.0.1.10:8080 max_fails=3 fail_timeout=30s;
    server 10.0.1.11:8080 max_fails=3 fail_timeout=30s;
    server 10.0.1.12:8080 backup;         # Only used when others are down
}
```

## 🔒 SSL/TLS Configuration (Production)

```nginx
server {
    listen 443 ssl http2;
    server_name myapp.example.com;

    # Certificates
    ssl_certificate /etc/letsencrypt/live/myapp.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.example.com/privkey.pem;

    # Modern TLS (FAANG-grade)
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # HSTS (1 year)
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
}

# HTTP → HTTPS redirect
server {
    listen 80;
    server_name myapp.example.com;
    return 301 https://$host$request_uri;
}
```

```bash
# Let's Encrypt with Certbot
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d myapp.example.com
sudo certbot renew --dry-run                          # Test renewal
```

## 🚦 Rate Limiting & Connection Control

```nginx
# Define rate limit zones
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;
limit_req_zone $binary_remote_addr zone=login_limit:10m rate=1r/s;
limit_conn_zone $binary_remote_addr zone=conn_limit:10m;

server {
    # API rate limiting with burst
    location /api/ {
        limit_req zone=api_limit burst=20 nodelay;
        limit_req_status 429;
        proxy_pass http://backend;
    }

    # Strict login rate limiting
    location /api/auth/login {
        limit_req zone=login_limit burst=5;
        limit_req_status 429;
        proxy_pass http://backend;
    }

    # Connection limits
    location /downloads/ {
        limit_conn conn_limit 5;                     # Max 5 connections per IP
        limit_rate 1m;                               # 1MB/s per connection
    }
}
```

## ⚡ Caching & Performance

```nginx
# Proxy cache
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=app_cache:10m
                 max_size=1g inactive=60m use_temp_path=off;

server {
    location /api/ {
        proxy_cache app_cache;
        proxy_cache_valid 200 10m;
        proxy_cache_valid 404 1m;
        proxy_cache_use_stale error timeout http_500 http_502 http_503;
        proxy_cache_lock on;
        add_header X-Cache-Status $upstream_cache_status;
        proxy_pass http://backend;
    }

    # Static file caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_comp_level 5;
    gzip_types text/plain text/css application/json application/javascript
               text/xml application/xml text/javascript image/svg+xml;
}
```

## 🛡️ Security Hardening

```nginx
server {
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self'" always;
    add_header Permissions-Policy "camera=(), microphone=(), geolocation=()" always;

    # Hide Nginx version
    server_tokens off;

    # Block common exploits
    location ~ /\. { deny all; }                     # Hidden files
    location ~* \.(env|git|htaccess|htpasswd)$ { deny all; }
    location = /wp-admin { deny all; }               # Block WordPress scanners

    # IP whitelisting (admin panel)
    location /admin/ {
        allow 10.0.0.0/8;
        allow 172.16.0.0/12;
        deny all;
        proxy_pass http://backend;
    }

    # Request size limits
    client_max_body_size 10m;
    client_body_timeout 10s;
    client_header_timeout 10s;
}
```

## 📊 Logging & Monitoring

```nginx
# Custom log format (JSON for ELK/Datadog)
log_format json_combined escape=json
  '{'
    '"time":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"request":"$request",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_response_time":"$upstream_response_time",'
    '"http_user_agent":"$http_user_agent",'
    '"http_referer":"$http_referer"'
  '}';

access_log /var/log/nginx/access.log json_combined;
error_log /var/log/nginx/error.log warn;

# Stub status (for Prometheus nginx-exporter)
server {
    listen 8080;
    location /nginx_status {
        stub_status;
        allow 127.0.0.1;
        deny all;
    }
}
```

## 🐞 Debugging

```bash
# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo tail -100 /var/log/nginx/error.log | grep "500\|502\|503"

# Test configuration
sudo nginx -t                                         # Syntax check
sudo nginx -T                                         # Full config dump
sudo nginx -T 2>&1 | grep "server_name"              # Find all server blocks

# Check what's listening
sudo ss -tlnp | grep nginx
sudo lsof -i :80
sudo lsof -i :443

# Check worker processes
ps aux | grep nginx
cat /proc/$(cat /run/nginx.pid)/limits                # Worker limits

# Connection debugging
curl -I https://myapp.example.com                      # Response headers
curl -vk https://myapp.example.com 2>&1 | grep "SSL"  # SSL handshake
```

## 🎯 WebSocket Proxy

```nginx
# WebSocket support (common for real-time apps)
location /ws/ {
    proxy_pass http://backend;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_read_timeout 86400s;                        # Keep alive for 24h
    proxy_send_timeout 86400s;
}
```

---

> 💡 **Production Rule:** Always run `nginx -t` before `systemctl reload nginx`. A bad config will take down your entire ingress layer.
