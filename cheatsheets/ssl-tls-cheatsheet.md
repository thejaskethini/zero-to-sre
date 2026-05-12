# 🔐 SSL/TLS Cheatsheet

> TLS handshake, certificates, openssl commands, Let's Encrypt, mTLS, and debugging.

---

## 🤝 TLS Handshake Explained

```
CLIENT HELLO ──────────────────────────────────────→ SERVER
  "I support TLS 1.2/1.3, these ciphers, SNI=example.com"

CLIENT ←────────────────────────────────── SERVER HELLO
  "Let's use TLS 1.3, this cipher, here's my certificate"

CLIENT verifies certificate:
  1. Is cert signed by trusted CA?
  2. Is cert expired?
  3. Does cert match the hostname (SNI)?
  4. Is cert revoked? (OCSP/CRL check)

CLIENT ──────── Key Exchange (ECDHE) ──────→ SERVER
  Both derive shared session key

CLIENT ──────── Encrypted Application Data ──→ SERVER
  All traffic encrypted with session key

TLS 1.3 improvements over 1.2:
  - 1-RTT handshake (vs 2-RTT in TLS 1.2)
  - 0-RTT resumption (at cost of replay risk)
  - Removed weak ciphers (RC4, 3DES, SHA-1)
  - Forward secrecy mandatory (ECDHE only)
```

## 🔧 OpenSSL Commands

```bash
# Generate private key
openssl genrsa -out server.key 4096                   # RSA 4096-bit
openssl ecparam -genkey -name prime256v1 -out server.key  # ECDSA (faster)

# Generate CSR (Certificate Signing Request)
openssl req -new -key server.key -out server.csr \
  -subj "/CN=api.example.com/O=MyOrg/C=US"

# Generate self-signed cert (testing only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -sha256 -days 365 -nodes -subj "/CN=localhost"

# Generate with SAN (Subject Alternative Names)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem \
  -sha256 -days 365 -nodes \
  -subj "/CN=example.com" \
  -addext "subjectAltName=DNS:example.com,DNS:*.example.com,IP:10.0.1.10"

# View certificate details
openssl x509 -in cert.pem -noout -text
openssl x509 -in cert.pem -noout -dates              # Expiry dates
openssl x509 -in cert.pem -noout -subject -issuer    # Subject + issuer
openssl x509 -in cert.pem -noout -fingerprint -sha256

# Verify cert matches key
openssl x509 -noout -modulus -in cert.pem | md5sum
openssl rsa -noout -modulus -in key.pem | md5sum
# Both must match!

# Verify certificate chain
openssl verify -CAfile ca-bundle.crt server.crt

# Convert formats
openssl pkcs12 -export -out cert.pfx -inkey key.pem -in cert.pem  # PEM → PKCS12
openssl pkcs12 -in cert.pfx -out cert.pem -nodes                   # PKCS12 → PEM
openssl x509 -in cert.der -inform DER -out cert.pem                # DER → PEM
```

## 🔍 Debug Remote SSL

```bash
# Check remote certificate
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | \
  openssl x509 -noout -dates -subject -issuer

# Full chain inspection
openssl s_client -connect example.com:443 -showcerts </dev/null 2>/dev/null

# Check TLS version and cipher
openssl s_client -connect example.com:443 </dev/null 2>/dev/null | \
  grep -E "Protocol|Cipher"

# Test specific TLS versions
openssl s_client -connect example.com:443 -tls1_2 </dev/null
openssl s_client -connect example.com:443 -tls1_3 </dev/null

# OCSP stapling check
openssl s_client -connect example.com:443 -status </dev/null 2>/dev/null | \
  grep "OCSP Response Status"

# Certificate expiry monitoring (script)
check_cert_expiry() {
  local host="$1" days
  days=$(echo | openssl s_client -connect "${host}:443" -servername "$host" 2>/dev/null | \
    openssl x509 -noout -enddate | cut -d= -f2)
  expiry=$(date -d "$days" +%s)
  now=$(date +%s)
  remaining=$(( (expiry - now) / 86400 ))
  echo "${host}: ${remaining} days remaining"
}
```

## 🔒 Let's Encrypt / Certbot

```bash
# Install
sudo apt install -y certbot python3-certbot-nginx

# Obtain cert (Nginx)
sudo certbot --nginx -d example.com -d www.example.com

# Obtain cert (standalone)
sudo certbot certonly --standalone -d example.com

# Obtain cert (DNS challenge — wildcard)
sudo certbot certonly --manual --preferred-challenges dns -d "*.example.com"

# Renew
sudo certbot renew --dry-run                          # Test renewal
sudo certbot renew                                    # Actually renew

# Auto-renewal (cron)
echo "0 0 1 * * root certbot renew --quiet --post-hook 'systemctl reload nginx'" | \
  sudo tee /etc/cron.d/certbot-renewal

# Certificate location
# /etc/letsencrypt/live/example.com/fullchain.pem
# /etc/letsencrypt/live/example.com/privkey.pem
```

## 🔄 Mutual TLS (mTLS)

```
STANDARD TLS:
  Client verifies Server's certificate (one-way)

MUTUAL TLS (mTLS):
  Client verifies Server's certificate
  Server verifies Client's certificate (two-way)
  Used for: service-to-service communication (zero trust)

HOW IT WORKS:
  1. Both services have their own cert signed by internal CA
  2. Server requires client cert in TLS config
  3. Both sides verify each other's certificates
  4. Connection established only if both are trusted
```

```bash
# Generate CA
openssl req -x509 -newkey rsa:4096 -keyout ca.key -out ca.crt -sha256 -days 3650 -nodes -subj "/CN=Internal CA"

# Generate server cert signed by CA
openssl req -newkey rsa:2048 -keyout server.key -out server.csr -nodes -subj "/CN=api.internal"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Generate client cert signed by CA
openssl req -newkey rsa:2048 -keyout client.key -out client.csr -nodes -subj "/CN=frontend"
openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365

# Test mTLS connection
curl --cert client.crt --key client.key --cacert ca.crt https://api.internal:443/health
```

## 🎯 FAANG Interview Q&A

```
Q: How does TLS 1.3 improve over 1.2?
A: 1-RTT handshake (vs 2-RTT), mandatory forward secrecy (ECDHE),
   removed weak algorithms, encrypted handshake metadata,
   0-RTT resumption for returning clients.

Q: What is forward secrecy and why does it matter?
A: Each session uses ephemeral keys (ECDHE). Compromising the
   server's private key doesn't decrypt past traffic.
   Without FS: attacker records traffic, later steals key, decrypts all.

Q: How would you implement certificate rotation with zero downtime?
A: 1. Generate new cert before old one expires (30 days ahead)
   2. Deploy new cert to all servers
   3. Nginx/HAProxy support hot-reload without connection drops
   4. Automate with cert-manager (K8s) or certbot + cron

Q: Explain certificate pinning.
A: Client hardcodes expected cert/public key hash.
   Prevents MITM even with compromised CA.
   Risk: cert rotation requires client update.
   Used in mobile apps, not recommended for web browsers.
```

---

> 💡 **Production Rule:** Automate certificate management. Manual cert renewal is the #1 cause of preventable outages. Use cert-manager in K8s, certbot with cron for VMs. Monitor expiry with alerts at 30/14/7 days.
