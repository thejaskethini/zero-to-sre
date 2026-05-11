#!/usr/bin/env python3
"""
🤖 Toil Tracker — Measure and prioritize automation opportunities.

Tracks manual, repetitive tasks (toil) and calculates ROI for automating them.
Helps SRE teams prioritize which tasks to automate first.

Usage: python toil_tracker.py
Author: Zero to SRE | License: MIT
"""
from dataclasses import dataclass
from typing import List

@dataclass
class ToilTask:
    name: str
    frequency_per_week: float
    time_minutes: float
    engineer_count: int  # engineers who do this
    error_prone: bool
    automatable: bool
    automation_hours: float  # estimated hours to automate

def calculate_roi(task: ToilTask) -> dict:
    """Calculate automation ROI for a toil task."""
    weekly_mins = task.frequency_per_week * task.time_minutes * task.engineer_count
    yearly_hours = (weekly_mins * 52) / 60
    yearly_cost = yearly_hours * 75  # ~$75/hr engineer cost
    automation_cost = task.automation_hours * 75
    payback_weeks = (task.automation_hours * 60) / weekly_mins if weekly_mins > 0 else 999
    yearly_savings = yearly_cost - automation_cost

    return {
        "name": task.name,
        "weekly_hours": round(weekly_mins / 60, 1),
        "yearly_hours": round(yearly_hours, 0),
        "yearly_cost": round(yearly_cost),
        "automation_cost": round(automation_cost),
        "payback_weeks": round(payback_weeks, 1),
        "yearly_savings": round(yearly_savings),
        "priority": "HIGH" if payback_weeks < 8 else "MEDIUM" if payback_weeks < 20 else "LOW",
    }

# Sample toil tasks
TASKS = [
    ToilTask("SSL Certificate Renewal", 0.5, 45, 2, True, True, 16),
    ToilTask("Database Backup Verification", 5, 15, 1, False, True, 8),
    ToilTask("Log Rotation & Cleanup", 3, 10, 1, False, True, 4),
    ToilTask("Incident Report Writing", 2, 60, 3, False, True, 40),
    ToilTask("Access Provisioning", 10, 20, 2, True, True, 24),
    ToilTask("Deployment Rollback", 1, 30, 2, True, True, 20),
    ToilTask("Capacity Rightsizing Review", 0.25, 120, 1, False, True, 30),
    ToilTask("Dependency Updates (CVEs)", 2, 45, 2, True, True, 32),
]

def main():
    print("=" * 60)
    print("🤖 Toil Tracker — Automation ROI Calculator")
    print("=" * 60)

    results = [calculate_roi(t) for t in TASKS]
    results.sort(key=lambda x: x["payback_weeks"])

    total_yearly_hours = sum(r["yearly_hours"] for r in results)
    total_savings = sum(r["yearly_savings"] for r in results)

    print(f"\n📊 Tracking {len(TASKS)} toil tasks")
    print(f"   Total toil: {total_yearly_hours:.0f} engineer-hours/year")
    print(f"   Potential savings: ${total_savings:,.0f}/year\n")

    print(f"{'Task':<30} {'Weekly':<8} {'Yearly':<8} {'Payback':<10} {'Savings':<12} {'Priority'}")
    print("-" * 88)
    for r in results:
        icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}[r["priority"]]
        print(f"{r['name']:<30} {r['weekly_hours']:<8} {r['yearly_hours']:<8.0f} "
              f"{r['payback_weeks']:<10} ${r['yearly_savings']:<11,} {icon} {r['priority']}")

    print(f"\n💡 Automate HIGH priority items first (payback < 8 weeks)")

if __name__ == "__main__":
    main()
