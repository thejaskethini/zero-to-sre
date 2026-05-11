# 🚨 Runbook: SSL/TLS Certificate Expiry

## 📋 Overview

| Field | Value |
|-------|-------|
| **Alert Name** | `CertificateExpiringSoon` |
| **Severity** | P1 — Critical (if < 7 days), P2 (if < 30 days) |
| **Service** | Ingress / Load Balancer |
| **Symptom** | Users see "connection not secure" warnings, TLS handshake failures |
| **Impact** | Total loss of HTTPS traffic, broken API calls, loss of user trust |

---

## 🔍 Diagnosis Steps

### Step 1: Check Certificate Expiry

```bash
# Check certificate expiry from outside
echo | openssl s_client -servername api.example.com -connect api.example.com:443 2>/dev/null | openssl x509 -noout -dates

# Check all K8s TLS secrets
kubectl get secrets -A -o json | jq -r '.items[] | select(.type=="kubernetes.io/tls") | .metadata.namespace + "/" + .metadata.name'

# Check specific secret
kubectl get secret myapp-tls -n production -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -noout -dates

# Check cert-manager certificates
kubectl get certificates -A
kubectl describe certificate myapp-tls -n production
```

### Step 2: Check cert-manager (if using)

```bash
# Check cert-manager pods
kubectl get pods -n cert-manager

# Check certificate status
kubectl get orders -A
kubectl get challenges -A

# Check cert-manager logs
kubectl logs -l app=cert-manager -n cert-manager --tail=50
```

---

## 🔧 Mitigation

### If Using cert-manager (Auto-Renewal)

```bash
# Force renewal
kubectl delete secret myapp-tls -n production
# cert-manager will detect missing secret and re-issue

# Or trigger renewal via annotation
kubectl annotate certificate myapp-tls -n production cert-manager.io/renew-before="720h" --overwrite

# Check renewal progress
kubectl describe certificate myapp-tls -n production
kubectl get events -n production --sort-by='.lastTimestamp' | grep cert
```

### If Manual Certificate

```bash
# 1. Generate new certificate (Let's Encrypt via certbot)
certbot certonly --dns-route53 -d api.example.com

# 2. Update K8s secret
kubectl create secret tls myapp-tls \
  --cert=/etc/letsencrypt/live/api.example.com/fullchain.pem \
  --key=/etc/letsencrypt/live/api.example.com/privkey.pem \
  -n production --dry-run=client -o yaml | kubectl apply -f -

# 3. Restart ingress controller to pick up new cert
kubectl rollout restart deployment ingress-nginx-controller -n ingress-nginx
```

### Prevention

1. **Use cert-manager** for automatic renewal
2. **Set alerts** for certificates expiring in < 30 days:
   ```promql
   # Prometheus query (if using cert-manager exporter)
   certmanager_certificate_expiration_timestamp_seconds - time() < 30 * 24 * 3600
   ```
3. **Monitor with external tools:** UptimeRobot, Datadog Synthetics

---

## ✅ Resolution Verification

```bash
# Verify new certificate
echo | openssl s_client -servername api.example.com -connect api.example.com:443 2>/dev/null | openssl x509 -noout -text | grep -A 2 "Validity"

# Test from browser
curl -vI https://api.example.com 2>&1 | grep -E "expire|subject|issuer"

# Verify no TLS errors in logs
kubectl logs -l app.kubernetes.io/name=ingress-nginx -n ingress-nginx --tail=20 | grep -i "ssl\|tls\|cert"
```
