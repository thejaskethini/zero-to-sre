# 📝 Blameless Postmortem Template

> Schedule this meeting within 48 hours of incident resolution. Focus on systems, not people.

---

## Incident Metadata

| Field | Details |
|-------|---------|
| **Incident ID** | INC-YYYY-MM-DD-NNN |
| **Postmortem Date** | YYYY-MM-DD |
| **Postmortem Author** | @name |
| **Severity** | SEV-1 / SEV-2 / SEV-3 |
| **Duration** | X hours Y minutes |
| **Incident Commander** | @name |

---

## Executive Summary

_2-3 sentences describing what happened, the impact, and the resolution._

**Example:** On January 15, 2025, the payment service experienced a complete outage for 47 minutes due to a database connection pool exhaustion. Approximately 12,000 users were unable to complete purchases, resulting in an estimated $45,000 in lost revenue. The issue was mitigated by increasing connection pool size and resolved permanently by fixing a connection leak in the checkout service.

---

## Impact

| Metric | Value |
|--------|-------|
| **Duration** | X hours Y minutes |
| **Users Affected** | Number or percentage |
| **Revenue Impact** | $X estimated |
| **SLO Impact** | Error budget consumed: X% |
| **Support Tickets** | N tickets created |

---

## Timeline

| Time (UTC) | Event |
|-----------|-------|
| HH:MM | _Leading event or change that contributed_ |
| HH:MM | 🔔 First alert fired |
| HH:MM | 📢 Incident declared |
| HH:MM | 🔍 Initial investigation |
| HH:MM | 💡 Root cause identified |
| HH:MM | 🔧 Mitigation applied |
| HH:MM | ✅ Service fully restored |
| HH:MM | 📝 Monitoring confirms stability |

---

## Root Cause Analysis

### What happened?

_Detailed technical explanation of the root cause._

### Why did it happen?

_Use the "5 Whys" technique:_

1. **Why** did the service go down? → Connection pool exhausted
2. **Why** was the pool exhausted? → Connections were not being returned
3. **Why** weren't connections returned? → A code path didn't close connections on error
4. **Why** wasn't this caught? → No unit test for error path, no pool monitoring
5. **Why** was there no monitoring? → Pool metrics were not exposed

### Contributing Factors

- [ ] Code change (specify PR/commit)
- [ ] Configuration change
- [ ] Infrastructure change
- [ ] Traffic spike
- [ ] Dependency failure
- [ ] Missing monitoring
- [ ] Missing documentation
- [ ] Other: ___

---

## What Went Well

_Acknowledge what worked during the response:_

- ✅ Detection was fast (MTTD: X minutes)
- ✅ On-call responded within Y minutes
- ✅ Communication was clear and timely
- ✅ Runbook was available and accurate

## What Went Poorly

_Be honest about what didn't work:_

- ❌ Took too long to identify root cause
- ❌ Runbook was outdated
- ❌ No monitoring for this failure mode
- ❌ Rollback was not tested

## Where We Got Lucky

_Things that could have been worse:_

- 🍀 Happened during low traffic hours
- 🍀 Only one region was affected
- 🍀 Database had recent backup

---

## Action Items

> Every action item must have an **owner** and a **deadline**. If it doesn't, it won't happen.

| # | Action | Priority | Owner | Deadline | Ticket |
|---|--------|----------|-------|----------|--------|
| 1 | Fix connection leak in checkout service | 🔴 P0 | @dev1 | YYYY-MM-DD | JIRA-123 |
| 2 | Add connection pool monitoring | 🟠 P1 | @dev2 | YYYY-MM-DD | JIRA-124 |
| 3 | Add alert for pool saturation > 80% | 🟠 P1 | @sre1 | YYYY-MM-DD | JIRA-125 |
| 4 | Write unit test for error path | 🟡 P2 | @dev1 | YYYY-MM-DD | JIRA-126 |
| 5 | Update runbook with pool debugging steps | 🟡 P2 | @sre2 | YYYY-MM-DD | JIRA-127 |

---

## Lessons Learned

1. _Key lesson 1_
2. _Key lesson 2_
3. _Key lesson 3_

---

## Attendees

| Name | Role |
|------|------|
| @name | Incident Commander |
| @name | Operations Lead |
| @name | Engineering Manager |

---

> 📌 **Remember:** Postmortems are about learning, not blaming. "We don't have a people problem; we have a systems problem."
