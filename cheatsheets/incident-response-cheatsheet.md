# 📟 Incident Response Cheatsheet

> The on-call playbook — structured incident management from detection to postmortem, following Google SRE practices.

---

## 🚨 Incident Severity Levels

```
SEV1 (Critical):
  → Complete service outage / data loss / security breach
  → Response: All-hands, exec notification, war room
  → Target resolution: < 1 hour
  → Example: Production database down, payment processing failed

SEV2 (High):
  → Major feature degraded, significant user impact
  → Response: On-call engineer + backup, team lead notified
  → Target resolution: < 4 hours
  → Example: Search returning errors for 30% of users

SEV3 (Medium):
  → Minor feature issue, limited user impact
  → Response: On-call engineer, next business day OK
  → Target resolution: < 24 hours
  → Example: Email notifications delayed by 30 minutes

SEV4 (Low):
  → Cosmetic issue, no user-facing impact
  → Response: Ticket created, sprint backlog
  → Target resolution: < 1 week
  → Example: Internal dashboard showing stale data
```

## 📋 Incident Response Steps

```
1. DETECT & ALERT (0-5 min)
   └── Alert fires → Acknowledge → Assess severity

2. TRIAGE (5-10 min)
   ├── What is the user impact?
   ├── How many users affected?
   ├── Is it getting worse?
   └── Assign severity level

3. COMMUNICATE (10-15 min)
   ├── Update status page
   ├── Notify stakeholders (Slack channel, email)
   └── Start incident doc (who, what, when, impact)

4. MITIGATE (15-60 min)
   ├── Rollback last deployment
   ├── Scale up resources
   ├── Failover to backup
   ├── Enable feature flag kill switch
   └── GOAL: Restore service, NOT find root cause

5. RESOLVE
   ├── Confirm service restored
   ├── Monitor for recurrence (30 min minimum)
   └── Update status page: "Resolved"

6. POSTMORTEM (within 48 hours)
   ├── Timeline of events
   ├── Root cause analysis
   ├── What went well / what didn't
   ├── Action items with owners and deadlines
   └── BLAMELESS — focus on systems, not people
```

## 🔧 Quick Mitigation Commands

```bash
# Rollback deployment (Kubernetes)
kubectl rollout undo deployment/api -n production
kubectl rollout status deployment/api -n production

# Scale up
kubectl scale deployment/api --replicas=10 -n production

# Kill switch (feature flag)
curl -X PUT https://flags.internal/api/v1/flags/new-checkout \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"enabled": false}'

# Block bad traffic
# Nginx
echo 'deny 1.2.3.4;' >> /etc/nginx/conf.d/blocklist.conf
sudo nginx -t && sudo nginx -s reload

# Drain a bad node
kubectl drain node-3 --ignore-daemonsets --delete-emptydir-data

# Emergency DB query kill
psql -c "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE state = 'active' AND query_start < now() - interval '5 minutes';"
```

## 📝 Postmortem Template

```markdown
# Incident Postmortem: [Title]

**Date:** YYYY-MM-DD
**Duration:** X hours Y minutes
**Severity:** SEV-X
**Impact:** [Number of affected users / requests]
**Authors:** [Names]

## Summary
One-paragraph description of what happened.

## Timeline (all times UTC)
| Time  | Event |
|-------|-------|
| 14:00 | Alert fired: API error rate > 5% |
| 14:05 | On-call acknowledged, began investigation |
| 14:15 | Identified: bad config deployed at 13:45 |
| 14:20 | Rollback initiated |
| 14:25 | Service restored, monitoring |
| 14:55 | Confirmed stable, incident closed |

## Root Cause
Detailed technical explanation.

## What Went Well
- Alert fired within 2 minutes
- Rollback process was smooth

## What Went Wrong
- No config validation in CI pipeline
- Runbook was outdated

## Action Items
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| Add config validation to CI | @engineer | 2026-02-01 | TODO |
| Update runbook for this scenario | @sre | 2026-01-25 | TODO |
| Add canary deployment step | @platform | 2026-02-15 | TODO |
```

## 📡 Communication Templates

```
STATUS PAGE UPDATE (Initial):
"We are investigating elevated error rates on [service].
Some users may experience [symptom]. We are actively
working on resolution. Next update in 30 minutes."

STATUS PAGE UPDATE (Mitigating):
"We have identified the cause of [issue] and are
implementing a fix. [Service] functionality is being
restored. Next update in 15 minutes."

STATUS PAGE UPDATE (Resolved):
"The issue affecting [service] has been resolved.
All systems are operating normally. A full postmortem
will be published within 48 hours."
```

---

> 💡 **Google SRE Principle:** "Hope is not a strategy." Every service needs runbooks, every alert needs a response plan, and every incident needs a blameless postmortem.
