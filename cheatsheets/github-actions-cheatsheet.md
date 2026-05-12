# 🔄 GitHub Actions Cheatsheet

> Workflow syntax, triggers, matrix builds, caching, secrets, reusable workflows, and production CI/CD patterns.

---

## 📝 Workflow Syntax

```yaml
name: CI/CD Pipeline
on:
  push:
    branches: [main, develop]
    paths-ignore: ['docs/**', '**.md']
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * 1'                              # Weekly Monday 6 AM
  workflow_dispatch:                                   # Manual trigger
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        type: choice
        options: [staging, production]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true                            # Cancel stale runs

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}
```

## 🏗️ Jobs & Steps

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        node-version: [18, 20, 22]
        os: [ubuntu-latest]
      fail-fast: false                                # Don't cancel other matrix jobs
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports: ['5432:5432']
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test -- --coverage
        env:
          DATABASE_URL: postgresql://postgres:test@localhost:5432/testdb
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: coverage-${{ matrix.node-version }}
          path: coverage/
          retention-days: 7

  build:
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      - id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha
            type=ref,event=branch
            type=semver,pattern={{version}}
      - uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## 🔐 Secrets & OIDC

```yaml
# Using secrets
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
  API_KEY: ${{ secrets.API_KEY }}

# OIDC for AWS (no long-lived credentials!)
deploy-aws:
  permissions:
    id-token: write
    contents: read
  steps:
    - uses: aws-actions/configure-aws-credentials@v4
      with:
        role-to-assume: arn:aws:iam::123456789:role/github-actions
        aws-region: us-east-1
    - run: aws ecs update-service --cluster prod --service api --force-new-deployment
```

## ♻️ Reusable Workflows

```yaml
# .github/workflows/deploy.yml (reusable)
on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      image-tag:
        required: true
        type: string
    secrets:
      KUBECONFIG:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - run: |
          echo "${{ secrets.KUBECONFIG }}" > kubeconfig
          kubectl --kubeconfig=kubeconfig set image deployment/api \
            api=${{ inputs.image-tag }} -n ${{ inputs.environment }}

# Caller workflow
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy.yml
    with:
      environment: staging
      image-tag: ${{ needs.build.outputs.image-tag }}
    secrets:
      KUBECONFIG: ${{ secrets.STAGING_KUBECONFIG }}
```

## ⚡ Caching

```yaml
# npm cache
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'

# Docker layer cache
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max

# Custom cache
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pip
      node_modules
    key: ${{ runner.os }}-deps-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-deps-
```

## 🎯 FAANG Interview Q&A

```
Q: How do you secure GitHub Actions?
A: 1. Pin actions to SHA (not tags): actions/checkout@abc123
   2. Use OIDC for cloud auth (no stored credentials)
   3. Limit GITHUB_TOKEN permissions (least privilege)
   4. Use environments with required reviewers for prod
   5. Dependabot for action version updates
   6. Never echo secrets in logs

Q: How do you optimize CI/CD pipeline speed?
A: 1. Parallel jobs (lint, test, build concurrently)
   2. Caching (npm, Docker layers, custom)
   3. Matrix builds for multi-version testing
   4. cancel-in-progress for stale runs
   5. Minimal base images for runners
   6. Skip unnecessary runs (paths-ignore)
```

---

> 💡 **Production Rule:** Always use `concurrency` to cancel stale runs. Always use OIDC over stored cloud credentials. Pin action versions to SHA hashes for supply chain security.
