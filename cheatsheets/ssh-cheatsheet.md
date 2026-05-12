# 🔑 SSH Cheatsheet

> Key management, tunneling, config, hardening, bastion patterns, and SSH certificates.

---

## 🔐 Key Generation & Management

```bash
# Generate keys
ssh-keygen -t ed25519 -C "user@example.com"           # Ed25519 (recommended)
ssh-keygen -t rsa -b 4096 -C "user@example.com"       # RSA 4096

# Copy public key to server
ssh-copy-id -i ~/.ssh/id_ed25519.pub user@server
cat ~/.ssh/id_ed25519.pub | ssh user@server 'cat >> ~/.ssh/authorized_keys'

# Agent management
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
ssh-add -l                                             # List loaded keys
ssh-add -D                                             # Remove all keys

# Key fingerprint
ssh-keygen -lf ~/.ssh/id_ed25519.pub
ssh-keygen -lf ~/.ssh/id_ed25519.pub -E md5            # MD5 format
```

## ⚙️ SSH Config (~/.ssh/config)

```
# Default settings
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
    IdentitiesOnly yes

# Production servers
Host prod-*
    User deploy
    IdentityFile ~/.ssh/prod_ed25519
    ForwardAgent no

Host prod-web1
    HostName 10.0.1.10

Host prod-web2
    HostName 10.0.1.11

# Jump through bastion
Host prod-internal-*
    User deploy
    ProxyJump bastion
    IdentityFile ~/.ssh/prod_ed25519

Host bastion
    HostName bastion.example.com
    User admin
    IdentityFile ~/.ssh/bastion_ed25519
    ForwardAgent no

# Tunnel to database through bastion
Host db-tunnel
    HostName db.internal
    User deploy
    ProxyJump bastion
    LocalForward 5432 db.internal:5432
```

```bash
# Usage
ssh prod-web1                                         # Uses config settings
ssh prod-internal-db                                   # Auto-jumps through bastion
ssh db-tunnel                                          # Opens DB tunnel
```

## 🔗 Tunneling (Port Forwarding)

```bash
# Local Forward — access remote service locally
ssh -L 5432:db.internal:5432 bastion
# Now: psql -h localhost -p 5432 (connects to db.internal via bastion)

# Remote Forward — expose local service to remote
ssh -R 8080:localhost:3000 server
# Now: server:8080 → your localhost:3000

# Dynamic (SOCKS proxy)
ssh -D 1080 bastion
# Configure browser: SOCKS5 proxy → localhost:1080
# All browser traffic goes through bastion

# Background tunnel
ssh -fNL 5432:db.internal:5432 bastion
# -f = background, -N = no command, -L = local forward

# Multiple forwards
ssh -L 5432:db1:5432 -L 6379:redis1:6379 -L 9200:elastic:9200 bastion
```

## 🛡️ sshd_config Hardening

```bash
# /etc/ssh/sshd_config (server-side)
Port 2222                              # Non-standard port
Protocol 2                             # SSH2 only
PermitRootLogin no                     # NEVER allow root
PasswordAuthentication no              # Keys only
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
ChallengeResponseAuthentication no
UsePAM yes
MaxAuthTries 3
MaxSessions 5
LoginGraceTime 30
ClientAliveInterval 300
ClientAliveCountMax 2
AllowUsers deploy admin                # Whitelist users
AllowGroups ssh-users                  # Or whitelist groups

# Restrict ciphers
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com
KexAlgorithms curve25519-sha256,diffie-hellman-group16-sha512

# After changes
sudo sshd -t                          # Test config
sudo systemctl restart sshd
```

## 📜 SSH Certificates (vs Keys)

```bash
# WHY: Certificates expire, are centrally managed, and don't need
# authorized_keys on every server. Used at Google, Facebook, Netflix.

# Generate CA key pair
ssh-keygen -t ed25519 -f ca_key -C "SSH CA"

# Sign a user key (valid 24 hours)
ssh-keygen -s ca_key -I "user@example.com" -n deploy -V +24h user_key.pub

# Sign a host key
ssh-keygen -s ca_key -I "prod-web1.example.com" -h -n prod-web1.example.com host_key.pub

# Server trusts CA (in sshd_config)
TrustedUserCAKeys /etc/ssh/ca_key.pub

# Client trusts host CA (in known_hosts)
@cert-authority *.example.com ssh-ed25519 AAAA...ca_public_key
```

## 🏰 Bastion Host Pattern

```
INTERNET → [Bastion/Jump Host] → [Private Servers]

Architecture:
  Bastion: in public subnet, minimal attack surface
  Internal: in private subnet, no public IP

Best practices:
  ✅ Use ProxyJump (not agent forwarding)
  ✅ Enable session logging on bastion
  ✅ Rotate bastion access frequently
  ✅ Use MFA on bastion login
  ✅ Limit bastion to specific source IPs
  ❌ Don't store any data on bastion
  ❌ Don't use agent forwarding (key theft risk)
```

```bash
# ProxyJump (modern, secure)
ssh -J bastion internal-server

# Or in config
Host internal-*
    ProxyJump bastion

# AWS SSM (no bastion needed!)
aws ssm start-session --target i-0abc123
```

## 📂 SCP & Rsync

```bash
# SCP (simple copy)
scp file.tar.gz user@server:/tmp/
scp -r ./dir user@server:/opt/app/
scp user@server:/var/log/app.log ./

# Rsync (better — incremental, resumable)
rsync -avz --progress ./dist/ user@server:/opt/app/
rsync -avz --delete ./dist/ user@server:/opt/app/    # Mirror (delete extras)
rsync -avz -e "ssh -p 2222" ./dir user@server:/opt/  # Custom SSH port
rsync -avz --exclude='node_modules' --exclude='.git' ./ user@server:/opt/app/
```

## 🎯 FAANG Interview Q&A

```
Q: SSH keys vs SSH certificates?
A: Keys: static, must distribute to every server's authorized_keys.
   Certificates: signed by CA, expire automatically, centrally managed.
   Certificates scale better — no authorized_keys management.
   Used at Google, Netflix, Facebook for SSH access.

Q: Why is SSH agent forwarding dangerous?
A: If bastion is compromised, attacker can use your forwarded key
   to connect to any server you can access. Use ProxyJump instead —
   it proxies the TCP connection, not the key.

Q: How would you audit SSH access in production?
A: 1. SSH certificates with short TTL (8-24 hours)
   2. Centralized logging (send auth.log to SIEM)
   3. Use AWS SSM Session Manager (full session recording)
   4. IP-based restrictions + MFA on bastion
   5. Periodic access reviews + key rotation
```

---

> 💡 **FAANG Practice:** Use SSH certificates over keys, SSM over bastion hosts, and ProxyJump over agent forwarding. The goal is zero standing SSH access — just-in-time, audited, and expiring.
