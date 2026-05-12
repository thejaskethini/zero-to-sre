# 🦊 GitLab CI Cheatsheet

> .gitlab-ci.yml syntax, stages, rules, includes, runners, caching, and production pipelines.

---

## 📝 Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_ENV: test
  DOCKER_TLS_CERTDIR: ""

lint:
  stage: lint
  image: node:20-alpine
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths: [node_modules/]
  script:
    - npm ci
    - npm run lint
    - npm run type-check

test:
  stage: test
  image: node:20-alpine
  services:
    - postgres:16
  variables:
    POSTGRES_DB: test
    POSTGRES_PASSWORD: test
    DATABASE_URL: postgresql://postgres:test@postgres:5432/test
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths: [node_modules/]
    policy: pull
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/All files.*\|.*\s+([\d.]+)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml
    when: always
    expire_in: 7 days

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-staging:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/api api=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-production:
  stage: deploy
  image: bitnami/kubectl:latest
  environment:
    name: production
    url: https://api.example.com
  script:
    - kubectl set image deployment/api api=$CI_REGISTRY_IMAGE:$CI_COMMIT_SHA -n production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual                                    # Require manual approval
  allow_failure: false
```

## 🔧 Rules (Modern Workflow Control)

```yaml
# Rules replace only/except (deprecated)
job:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == "main"
    - if: $CI_COMMIT_TAG                              # On tags
    - if: $CI_COMMIT_BRANCH =~ /^feature\//           # Regex match
    - changes:                                         # Path-based
        - src/**/*
        - package.json
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual                                    # Manual approval
      allow_failure: false
    - when: never                                     # Default: skip
```

## 📦 Includes & Templates

```yaml
# Include shared templates
include:
  - template: Security/SAST.gitlab-ci.yml            # GitLab templates
  - template: Security/Container-Scanning.gitlab-ci.yml
  - project: 'platform/ci-templates'                  # From another project
    ref: main
    file: '/templates/docker-build.yml'
  - local: '/.gitlab/ci/deploy.yml'                   # Local file
  - remote: 'https://example.com/ci-template.yml'     # Remote URL

# Reusable job template
.deploy-template: &deploy
  image: bitnami/kubectl:latest
  before_script:
    - echo "$KUBECONFIG_DATA" > kubeconfig
    - export KUBECONFIG=kubeconfig
  script:
    - kubectl set image deployment/$APP api=$IMAGE -n $NAMESPACE

deploy-staging:
  <<: *deploy
  variables:
    NAMESPACE: staging
    APP: api
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == "develop"

deploy-production:
  <<: *deploy
  variables:
    NAMESPACE: production
    APP: api
  environment:
    name: production
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      when: manual
```

## ⚡ Caching & Artifacts

```yaml
# Global cache
cache:
  key:
    files: [package-lock.json]                        # Cache key from file hash
  paths:
    - node_modules/
  policy: pull-push                                   # pull | push | pull-push

# Per-job cache
test:
  cache:
    key: ${CI_COMMIT_REF_SLUG}-test
    paths: [node_modules/, .cache/]
    policy: pull                                      # Only read, don't update

# Artifacts (pass between jobs)
build:
  artifacts:
    paths:
      - dist/
    expire_in: 1 hour

deploy:
  needs: [build]                                      # Uses build artifacts
```

## 🔐 Variables & Secrets

```yaml
variables:
  # Pipeline variables
  APP_VERSION: "2.0.0"
  DEPLOY_ENV: staging

# Protected variables: Settings → CI/CD → Variables
# $CI_REGISTRY_PASSWORD, $AWS_ACCESS_KEY_ID, etc.

# Predefined variables
# $CI_COMMIT_SHA          → Full commit hash
# $CI_COMMIT_SHORT_SHA    → Short commit hash
# $CI_COMMIT_BRANCH       → Branch name
# $CI_COMMIT_TAG          → Tag name
# $CI_PIPELINE_ID         → Pipeline ID
# $CI_PROJECT_NAME        → Project name
# $CI_REGISTRY_IMAGE      → Container registry image path
# $CI_ENVIRONMENT_NAME    → Environment name
```

## 🏃 Runners

```bash
# Register runner
gitlab-runner register \
  --url https://gitlab.example.com \
  --registration-token TOKEN \
  --executor docker \
  --docker-image "alpine:latest" \
  --tag-list "docker,linux" \
  --run-untagged=true

# Runner config (/etc/gitlab-runner/config.toml)
[[runners]]
  name = "docker-runner"
  executor = "docker"
  [runners.docker]
    image = "alpine:latest"
    privileged = true                                 # For DinD
    volumes = ["/cache", "/var/run/docker.sock:/var/run/docker.sock"]
```

## 🔒 Security Scanning

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Secret-Detection.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml

# Results appear in MR Security tab automatically
```

## 🎯 FAANG Interview Q&A

```
Q: GitLab CI vs GitHub Actions?
A: GitLab: built-in container registry, security scanning,
   environments, review apps, single platform (code + CI + registry).
   GitHub Actions: larger marketplace, better community actions,
   simpler YAML syntax, matrix builds. GitLab is more opinionated
   and complete; GitHub Actions is more flexible.

Q: How do you implement review apps in GitLab?
A: Use dynamic environments with MR-based naming:
   environment: { name: review/$CI_MERGE_REQUEST_IID }
   Deploy a temporary instance per MR, auto-stop on merge.
   Great for QA review before merging.

Q: needs vs dependencies?
A: needs: DAG keyword — job starts as soon as needed jobs finish
   (doesn't wait for entire stage). dependencies: controls which
   artifacts are downloaded. Use needs for speed, dependencies for
   artifact control.
```

---

> 💡 **Production Rule:** Use `rules` instead of `only/except`. Use `needs` for DAG pipelines (faster). Pin runner versions. Use `include` for shared templates across projects.
