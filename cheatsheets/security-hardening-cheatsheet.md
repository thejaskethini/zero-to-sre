# 🛡️ Security & Hardening Cheatsheet

> Production security practices — the checklist Google, AWS, and FAANG teams follow before going live.

---

## 🔐 Server Hardening (Linux)

```bash
# SSH hardening (/etc/ssh/sshd_config)
PermitRootLogin no                                    # Never allow root SSH
PasswordAuthentication no                             # Keys only
PubkeyAuthentication yes
MaxAuthTries 3
AllowUsers deploy admin                               # Whitelist users
Port 2222                                             # Non-standard port (minor)

# After changes
sudo systemctl restart sshd

# Firewall (UFW)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 2222/tcp                               # SSH
sudo ufw allow 80/tcp                                 # HTTP
sudo ufw allow 443/tcp                                # HTTPS
sudo ufw enable
sudo ufw status verbose

# Firewall (iptables)
sudo iptables -A INPUT -p tcp --dport 22 -s 10.0.0.0/8 -j ACCEPT
sudo iptables -A INPUT -p tcp --dport 22 -j DROP
sudo iptables -L -n -v                               # List rules

# Auto security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure unattended-upgrades

# Audit & monitoring
sudo apt install -y fail2ban auditd
sudo systemctl enable fail2ban
sudo systemctl enable auditd
```

## 🐳 Container Security

```bash
# Image scanning
trivy image myapp:latest                              # Vulnerability scan
trivy image --severity HIGH,CRITICAL myapp:latest     # Only high/critical
docker scout cves myapp:latest                        # Docker Scout scan
grype myapp:latest                                    # Anchore Grype scan

# Dockerfile best practices
# ✅ DO:
FROM node:20-alpine AS builder                        # Use minimal base
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser                                          # Never run as root
COPY --chown=appuser:appgroup . .
HEALTHCHECK CMD curl -f http://localhost:3000/health

# ❌ DON'T:
# FROM ubuntu:latest                                  # Too large, too many CVEs
# RUN apt-get install -y curl wget vim                # Don't install debug tools
# USER root                                           # Never run as root
# COPY . .                                            # Use .dockerignore
```

```yaml
# Kubernetes Pod Security
apiVersion: v1
kind: Pod
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 2000
  containers:
    - name: app
      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop: ["ALL"]
      resources:
        limits:
          cpu: "500m"
          memory: "256Mi"
```

## 🔑 Secrets Management

```bash
# NEVER do this:
export DB_PASSWORD="hunter2"                          # In shell history
echo "password123" > config.yaml                      # In version control

# DO this instead:
# AWS Secrets Manager
aws secretsmanager create-secret --name prod/db/password --secret-string "..."
aws secretsmanager get-secret-value --secret-id prod/db/password

# HashiCorp Vault
vault kv put secret/prod/db password="..."
vault kv get -field=password secret/prod/db

# Kubernetes Secrets (base64 is NOT encryption)
kubectl create secret generic db-creds \
  --from-literal=password='...' \
  -n production

# Sealed Secrets (encrypted, safe for git)
kubeseal --format=yaml < secret.yaml > sealed-secret.yaml

# SOPS (encrypted files in git)
sops --encrypt --age $(cat ~/.sops/key.txt) secrets.yaml > secrets.enc.yaml
```

## 🌐 API Security

```
AUTHENTICATION:
  JWT Tokens    → Stateless, include expiry (short-lived: 15min)
  OAuth 2.0     → Delegation framework (PKCE for SPAs)
  API Keys      → Simple, but no user context (rate limit per key)
  mTLS          → Mutual TLS for service-to-service

AUTHORIZATION:
  RBAC          → Role-Based Access Control (K8s, cloud IAM)
  ABAC          → Attribute-Based (flexible but complex)
  OPA           → Open Policy Agent (policy as code)

SECURITY HEADERS:
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=()

INPUT VALIDATION:
  - Validate all input server-side (never trust client)
  - Use parameterized queries (prevent SQL injection)
  - Sanitize HTML output (prevent XSS)
  - Rate limit all public endpoints
  - Implement request size limits
```

## 📋 Security Audit Checklist

```
PRE-PRODUCTION SECURITY REVIEW:
──────────────────────────────────────────
[ ] No secrets in source code or Docker images
[ ] Container runs as non-root user
[ ] All dependencies scanned for CVEs
[ ] TLS 1.2+ enforced, weak ciphers disabled
[ ] CORS configured (not wildcard *)
[ ] Rate limiting on all public endpoints
[ ] Input validation on all user inputs
[ ] SQL injection protection (parameterized queries)
[ ] Authentication on all non-public endpoints
[ ] RBAC configured with least privilege
[ ] Logging does NOT contain sensitive data (PII, passwords)
[ ] Health check endpoint does NOT leak system info
[ ] Error responses do NOT leak stack traces
[ ] Database connections use TLS
[ ] Backups encrypted at rest
[ ] Network policies restrict pod-to-pod traffic
```

## 🔍 Security Scanning in CI/CD

```yaml
# GitHub Actions security pipeline
- name: SAST (Static Analysis)
  uses: github/codeql-action/analyze@v3

- name: Dependency Scan
  run: npm audit --audit-level=high

- name: Container Scan
  run: trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE

- name: Secret Detection
  uses: trufflesecurity/trufflehog@main
  with:
    extra_args: --only-verified

- name: IaC Security (Terraform)
  run: tfsec .
```

---

> 💡 **FAANG Rule:** Security is not a feature — it's a constraint on every feature. Every PR should be reviewed for security implications. Defense in depth: assume every layer will be breached.
