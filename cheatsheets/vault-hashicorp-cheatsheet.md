# 🔐 HashiCorp Vault Cheatsheet

> Secrets management, dynamic secrets, PKI, K8s integration, and production HA setup.

---

## 📦 Installation & Init

```bash
# Install
brew install vault                                    # macOS
sudo apt install -y vault                             # Debian/Ubuntu (HashiCorp repo)

# Dev server (testing only)
vault server -dev
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root-token'

# Initialize production server
vault operator init -key-shares=5 -key-threshold=3   # 5 keys, need 3 to unseal
# SAVE THE ROOT TOKEN AND UNSEAL KEYS SECURELY!

# Unseal
vault operator unseal <key1>
vault operator unseal <key2>
vault operator unseal <key3>
vault status
```

## 🔧 Secrets Engine: KV (Key-Value)

```bash
# Enable KV v2
vault secrets enable -path=secret kv-v2

# Write secrets
vault kv put secret/production/db password="SuperSecret" host="db.internal" port=5432
vault kv put secret/production/api-key value="sk_live_abc123"

# Read secrets
vault kv get secret/production/db
vault kv get -field=password secret/production/db     # Single field
vault kv get -format=json secret/production/db        # JSON output

# List secrets
vault kv list secret/production/

# Version management
vault kv get -version=2 secret/production/db          # Specific version
vault kv rollback -version=1 secret/production/db     # Rollback
vault kv destroy -versions=3 secret/production/db     # Destroy version
vault kv metadata delete secret/production/db         # Delete all versions
```

## 🔄 Dynamic Secrets: Database

```bash
# Enable database engine
vault secrets enable database

# Configure PostgreSQL
vault write database/config/production-db \
  plugin_name=postgresql-database-plugin \
  connection_url="postgresql://{{username}}:{{password}}@db.internal:5432/production" \
  allowed_roles="readonly,readwrite" \
  username="vault_admin" \
  password="admin_password"

# Create role (generates temporary credentials)
vault write database/roles/readonly \
  db_name=production-db \
  creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
  default_ttl="1h" \
  max_ttl="24h"

# Get dynamic credentials
vault read database/creds/readonly
# Returns: username=v-token-readonly-abc123, password=random, lease_id, lease_duration

# Revoke credentials
vault lease revoke database/creds/readonly/lease-id
```

## 📜 PKI (Certificate Authority)

```bash
# Enable PKI engine
vault secrets enable pki
vault secrets tune -max-lease-ttl=87600h pki

# Generate root CA
vault write pki/root/generate/internal \
  common_name="Internal Root CA" \
  ttl=87600h

# Create intermediate CA
vault secrets enable -path=pki_int pki
vault write pki_int/intermediate/generate/internal \
  common_name="Internal Intermediate CA"

# Configure roles
vault write pki_int/roles/server-cert \
  allowed_domains="internal,example.com" \
  allow_subdomains=true \
  max_ttl=720h

# Issue certificate
vault write pki_int/issue/server-cert \
  common_name="api.internal" \
  alt_names="api.internal,api.example.com" \
  ttl=24h
```

## 🔐 Auth Methods

```bash
# AppRole (for applications)
vault auth enable approle
vault write auth/approle/role/api-server \
  secret_id_ttl=10m \
  token_ttl=20m \
  token_max_ttl=30m \
  policies="api-policy"

role_id=$(vault read -field=role_id auth/approle/role/api-server/role-id)
secret_id=$(vault write -f -field=secret_id auth/approle/role/api-server/secret-id)
vault write auth/approle/login role_id="$role_id" secret_id="$secret_id"

# Kubernetes auth
vault auth enable kubernetes
vault write auth/kubernetes/config \
  kubernetes_host="https://kubernetes.default.svc"

vault write auth/kubernetes/role/api-server \
  bound_service_account_names=api-sa \
  bound_service_account_namespaces=production \
  policies=api-policy \
  ttl=1h
```

## 📋 Policies

```hcl
# api-policy.hcl
path "secret/data/production/*" {
  capabilities = ["read", "list"]
}

path "database/creds/readonly" {
  capabilities = ["read"]
}

path "pki_int/issue/server-cert" {
  capabilities = ["create", "update"]
}

# Deny access to admin paths
path "sys/*" {
  capabilities = ["deny"]
}
```

```bash
vault policy write api-policy api-policy.hcl
vault policy list
vault policy read api-policy
```

## ☸️ Kubernetes Integration

```yaml
# Vault Agent Injector (sidecar)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/role: "api-server"
        vault.hashicorp.com/agent-inject-secret-db: "secret/data/production/db"
        vault.hashicorp.com/agent-inject-template-db: |
          {{- with secret "secret/data/production/db" -}}
          DB_HOST={{ .Data.data.host }}
          DB_PASSWORD={{ .Data.data.password }}
          {{- end -}}
    spec:
      serviceAccountName: api-sa
      containers:
        - name: api
          command: ["sh", "-c", "source /vault/secrets/db && node server.js"]
```

## 🎯 FAANG Interview Q&A

```
Q: Why Vault over AWS Secrets Manager?
A: Vault: multi-cloud, dynamic secrets, PKI, transit encryption,
   fine-grained policies, self-hosted. AWS SM: simpler, managed,
   tight AWS integration. Use Vault for multi-cloud or advanced
   features. Use AWS SM for AWS-only simple secret storage.

Q: What are dynamic secrets and why do they matter?
A: Vault generates unique, short-lived credentials on-demand.
   Each app gets its own DB credentials that auto-expire.
   Benefits: no shared credentials, automatic rotation,
   revocation on breach, full audit trail.

Q: How does Vault seal/unseal work?
A: Vault encrypts all data with a master key. Master key is
   split into shares (Shamir's Secret Sharing). Need threshold
   of shares to reconstruct and unseal. Prevents single person
   from accessing all secrets. Auto-unseal with cloud KMS available.
```

---

> 💡 **Production Rule:** Never use the root token in production. Use short-lived tokens with minimal policies. Enable audit logging. Use auto-unseal with cloud KMS. Rotate secrets regularly.
