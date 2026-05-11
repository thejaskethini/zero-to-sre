#!/usr/bin/env python3
"""
🤖 Incident Summarizer — LLM-Powered Incident Summary Generator

Demonstrates how LLMs can auto-generate incident summaries.
Uses template-based generation (no API keys needed).
In production, replace with an LLM API call (OpenAI, Ollama, etc).

Usage: python incident_summarizer.py
Author: Zero to SRE | License: MIT
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict

@dataclass
class AlertEvent:
    timestamp: datetime
    service: str
    severity: str
    message: str

@dataclass
class IncidentData:
    incident_id: str
    title: str
    severity: str
    start_time: datetime
    end_time: datetime
    duration_minutes: int
    affected_services: List[str]
    alerts: List[AlertEvent]
    metrics: Dict[str, str]
    actions_taken: List[str]
    root_cause: str
    resolution: str
    customer_impact: str

def generate_summary(incident: IncidentData) -> str:
    """Generate incident summary. Replace with LLM call in production."""
    alerts_tl = "\n".join([
        f"  {a.timestamp.strftime('%H:%M:%S')} [{a.severity.upper():8s}] {a.service}: {a.message}"
        for a in sorted(incident.alerts, key=lambda x: x.timestamp)
    ])
    actions = "\n".join([f"  {i+1}. {a}" for i, a in enumerate(incident.actions_taken)])
    svcs = ", ".join(incident.affected_services)
    metrics_str = "\n".join([f"  {k}: {v}" for k, v in incident.metrics.items()])

    return f"""
{'='*60}
INCIDENT SUMMARY — {incident.incident_id}
{'='*60}
Title:     {incident.title}
Severity:  {incident.severity.upper()} | Duration: {incident.duration_minutes}m
Services:  {svcs}
Impact:    {incident.customer_impact}

TIMELINE:
{alerts_tl}

METRICS:
{metrics_str}

ACTIONS:
{actions}

ROOT CAUSE: {incident.root_cause}
RESOLUTION: {incident.resolution}

ACTION ITEMS:
  1. [P1] Add automated failover for {incident.affected_services[0]}
  2. [P2] Improve monitoring for early detection
  3. [P2] Update runbook with resolution steps
  4. [P3] Chaos experiment to validate fix
{'='*60}
"""

def main():
    start = datetime(2025, 1, 15, 14, 30, 0)
    incident = IncidentData(
        incident_id="INC-2025-0115-001",
        title="Payment Service Outage — DB Connection Pool Exhaustion",
        severity="critical", start_time=start,
        end_time=start + timedelta(minutes=47), duration_minutes=47,
        affected_services=["payment-service", "payment-db", "api-gateway"],
        alerts=[
            AlertEvent(start, "payment-db", "critical", "Connection pool exhausted"),
            AlertEvent(start+timedelta(seconds=15), "payment-service", "critical", "Error rate > 10%"),
            AlertEvent(start+timedelta(seconds=30), "api-gateway", "warning", "Upstream timeout"),
            AlertEvent(start+timedelta(minutes=5), "payment-service", "critical", "Circuit breaker OPEN"),
            AlertEvent(start+timedelta(minutes=45), "payment-service", "info", "Error rate normalized"),
        ],
        metrics={"Error Rate (peak)": "45.2%", "p95 Latency": "12,400ms",
                 "Failed Transactions": "847", "Error Budget Consumed": "18.5%"},
        actions_taken=[
            "14:31 — Alert acknowledged by on-call",
            "14:35 — Identified connection pool exhaustion",
            "14:38 — Increased max_connections 100 -> 200",
            "14:42 — Found root cause: missing connection.close() in retry logic",
            "14:50 — Deployed hotfix PR #4521",
            "15:17 — All metrics normalized, incident resolved",
        ],
        root_cause="Connection leak in retry logic caused pool exhaustion under traffic spike",
        resolution="Deployed hotfix with proper connection cleanup in finally block",
        customer_impact="~2,300 users experienced payment failures over 47 minutes",
    )
    print(generate_summary(incident))

if __name__ == "__main__":
    main()
