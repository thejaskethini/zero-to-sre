# 🔄 CI/CD Pipeline Cheatsheet

> Production-grade CI/CD patterns — GitHub Actions, GitLab CI, Jenkins, and deployment strategies used at scale.

---

## 🏗️ GitHub Actions (Most Popular)

```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm test -- --coverage
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - run: |
          kubectl set image deployment/api \
            api=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n staging

  deploy-production:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production  # Requires approval
    steps:
      - run: |
          kubectl set image deployment/api \
            api=ghcr.io/${{ github.repository }}:${{ github.sha }} \
            -n production
```

## 🚀 Deployment Strategies

```
ROLLING UPDATE (Default K8s):
  ├── Replace instances one by one
  ├── Zero downtime
  ├── Slow rollback (redeploy old version)
  └── Risk: mixed versions during rollout

BLUE-GREEN:
  ├── Two identical environments (blue=current, green=new)
  ├── Switch traffic instantly (DNS/LB)
  ├── Instant rollback (switch back)
  └── Cost: 2x infrastructure during deploy

CANARY:
  ├── Route 5% traffic to new version → monitor → increase
  ├── Gradual risk exposure
  ├── Fast rollback (route 100% back to old)
  └── Requires: traffic splitting (Istio, ALB)

A/B TESTING:
  ├── Route by user segment (not random)
  ├── Feature-flag driven
  └── Measure business metrics, not just errors

FEATURE FLAGS:
  ├── Deploy code without enabling features
  ├── Decouple deploy from release
  ├── Tools: LaunchDarkly, Flagsmith, Unleash
  └── Pattern: if (featureFlag.isEnabled('new-checkout')) { ... }
```

## 🔐 Secrets Management in CI/CD

```bash
# GitHub Actions Secrets
${{ secrets.AWS_ACCESS_KEY_ID }}
${{ secrets.DATABASE_URL }}

# Vault integration
vault kv get -field=password secret/db/production

# AWS Secrets Manager
aws secretsmanager get-secret-value --secret-id prod/db/password

# SOPS (encrypted files in git)
sops -d secrets.enc.yaml > secrets.yaml
```

## 🧪 Testing Pyramid in CI

```
                    ┌──────────┐
                    │   E2E    │  ← Few, slow, expensive
                    │  Tests   │    (Cypress, Playwright)
                   ┌┴──────────┴┐
                   │ Integration │  ← Some, medium speed
                   │   Tests     │    (API tests, DB tests)
                  ┌┴─────────────┴┐
                  │  Unit Tests    │  ← Many, fast, cheap
                  │                │    (Jest, pytest, Go test)
                  └────────────────┘

CI PIPELINE ORDER:
  1. Lint & Format Check (fast fail)
  2. Unit Tests (parallel)
  3. Build (Docker image)
  4. Integration Tests (against test DB)
  5. Security Scan (Snyk, Trivy)
  6. E2E Tests (staging environment)
  7. Deploy
```

## 📊 Pipeline Metrics (DORA)

```
DORA METRICS (Google's DevOps Research):
──────────────────────────────────────────
                     Elite    High    Medium   Low
Deployment Freq      On-demand Weekly Monthly  Monthly+
Lead Time           <1 day   1-7d    1-6mo    6mo+
Change Fail Rate    <5%      5-10%   10-15%   >15%
Recovery Time       <1 hour  <1 day  <1 week  1week+

TRACK THESE:
  - Build time (target: < 10 min)
  - Test pass rate (target: > 98%)
  - Deploy frequency (target: daily)
  - Mean time to recovery (target: < 1 hour)
```

---

> 💡 **FAANG Rule:** The best CI/CD pipeline is one that developers trust. If people skip it or override it, the pipeline is too slow or too flaky. Fix that first.
