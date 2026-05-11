#!/usr/bin/env python3
"""
=============================================================================
🔔 Alert Correlator — Intelligent Alert Grouping & Noise Reduction
=============================================================================
Description:
    Demonstrates alert correlation techniques:
    1. Temporal correlation (alerts within time window)
    2. Service topology correlation (dependency-aware)
    3. Deduplication

Usage:
    python alert_correlator.py

Author: Zero to SRE
License: MIT
=============================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from collections import defaultdict
import hashlib


@dataclass
class Alert:
    """Represents a raw alert from the monitoring system."""
    id: str
    timestamp: datetime
    service: str
    severity: str  # critical, warning, info
    title: str
    description: str
    labels: Dict[str, str] = field(default_factory=dict)


@dataclass
class Incident:
    """A correlated group of related alerts."""
    id: str
    title: str
    severity: str
    alerts: List[Alert] = field(default_factory=list)
    root_cause_service: Optional[str] = None
    created_at: Optional[datetime] = None

    @property
    def alert_count(self):
        return len(self.alerts)


# =============================================================================
# SERVICE DEPENDENCY MAP
# =============================================================================

SERVICE_DEPENDENCIES = {
    "frontend": ["api-gateway"],
    "api-gateway": ["auth-service", "payment-service", "order-service"],
    "auth-service": ["user-db", "redis-cache"],
    "payment-service": ["payment-db", "stripe-api"],
    "order-service": ["order-db", "inventory-service"],
    "inventory-service": ["inventory-db"],
}


def get_upstream_services(service: str) -> List[str]:
    """Get all services that depend on the given service."""
    upstream = []
    for svc, deps in SERVICE_DEPENDENCIES.items():
        if service in deps:
            upstream.append(svc)
    return upstream


def get_downstream_services(service: str) -> List[str]:
    """Get all services that the given service depends on."""
    return SERVICE_DEPENDENCIES.get(service, [])


# =============================================================================
# CORRELATION ENGINE
# =============================================================================

class AlertCorrelator:
    """Correlates alerts into incidents using multiple strategies."""

    def __init__(self, time_window_seconds: int = 300):
        self.time_window = timedelta(seconds=time_window_seconds)
        self.incidents: List[Incident] = []
        self.alert_to_incident: Dict[str, str] = {}

    def correlate(self, alerts: List[Alert]) -> List[Incident]:
        """Main correlation pipeline."""
        # Sort by timestamp
        sorted_alerts = sorted(alerts, key=lambda a: a.timestamp)

        # Step 1: Deduplicate
        deduped = self._deduplicate(sorted_alerts)
        print(f"  📋 After deduplication: {len(deduped)} alerts (removed {len(sorted_alerts) - len(deduped)} duplicates)")

        # Step 2: Temporal grouping
        temporal_groups = self._temporal_group(deduped)
        print(f"  ⏱️  Temporal groups: {len(temporal_groups)}")

        # Step 3: Topology-aware correlation
        incidents = self._topology_correlate(temporal_groups)
        print(f"  🔗 Final incidents: {len(incidents)}")

        self.incidents = incidents
        return incidents

    def _deduplicate(self, alerts: List[Alert]) -> List[Alert]:
        """Remove duplicate alerts (same service + title within time window)."""
        seen = {}
        deduped = []

        for alert in alerts:
            key = f"{alert.service}:{alert.title}"
            if key in seen:
                last_time = seen[key]
                if alert.timestamp - last_time < self.time_window:
                    continue  # Skip duplicate
            seen[key] = alert.timestamp
            deduped.append(alert)

        return deduped

    def _temporal_group(self, alerts: List[Alert]) -> List[List[Alert]]:
        """Group alerts that occur within the same time window."""
        if not alerts:
            return []

        groups = []
        current_group = [alerts[0]]

        for alert in alerts[1:]:
            if alert.timestamp - current_group[0].timestamp <= self.time_window:
                current_group.append(alert)
            else:
                groups.append(current_group)
                current_group = [alert]

        groups.append(current_group)
        return groups

    def _topology_correlate(self, groups: List[List[Alert]]) -> List[Incident]:
        """Correlate alerts within each temporal group using service topology."""
        incidents = []

        for i, group in enumerate(groups):
            # Find the root cause (deepest service in dependency chain)
            services_in_group = set(a.service for a in group)
            root_cause = self._find_root_cause(services_in_group)

            # Determine severity (highest in group)
            severity_order = {"critical": 3, "warning": 2, "info": 1}
            max_severity = max(group, key=lambda a: severity_order.get(a.severity, 0))

            incident_id = hashlib.md5(f"INC-{i}-{group[0].timestamp}".encode()).hexdigest()[:8]

            incident = Incident(
                id=f"INC-{incident_id}",
                title=f"{root_cause or group[0].service} — {group[0].title}",
                severity=max_severity.severity,
                alerts=group,
                root_cause_service=root_cause,
                created_at=group[0].timestamp,
            )
            incidents.append(incident)

        return incidents

    def _find_root_cause(self, services: set) -> Optional[str]:
        """Find the most likely root cause service based on dependency topology."""
        # Root cause = the service that is a dependency of others in the group
        for service in services:
            upstream = get_upstream_services(service)
            if any(u in services for u in upstream):
                return service  # This service has dependents that are also alerting

        # If no topology match, return the most critical service
        return list(services)[0] if services else None


# =============================================================================
# SAMPLE DATA
# =============================================================================

def generate_sample_alerts() -> List[Alert]:
    """Generate a realistic alert storm scenario."""
    base_time = datetime(2025, 1, 15, 14, 30, 0)

    return [
        # Scenario: payment-db goes down → cascading failures
        Alert("a1", base_time + timedelta(seconds=0), "payment-db", "critical",
              "Database connection refused", "PostgreSQL on payment-db is not accepting connections",
              {"instance": "payment-db-01", "port": "5432"}),
        Alert("a2", base_time + timedelta(seconds=15), "payment-service", "critical",
              "High error rate", "Error rate exceeded 10% threshold",
              {"error_type": "connection_refused"}),
        Alert("a3", base_time + timedelta(seconds=20), "payment-service", "warning",
              "Increased latency", "p95 latency > 5s",
              {"p95_ms": "5200"}),
        Alert("a4", base_time + timedelta(seconds=30), "api-gateway", "warning",
              "Upstream timeout", "payment-service responding with 504",
              {"upstream": "payment-service"}),
        Alert("a5", base_time + timedelta(seconds=35), "frontend", "warning",
              "Payment page errors", "Users seeing payment failures",
              {"page": "/checkout"}),
        # Duplicate alerts (should be deduped)
        Alert("a6", base_time + timedelta(seconds=45), "payment-service", "critical",
              "High error rate", "Error rate exceeded 10% threshold",
              {"error_type": "connection_refused"}),
        Alert("a7", base_time + timedelta(seconds=60), "payment-service", "critical",
              "High error rate", "Error rate exceeded 10% threshold",
              {"error_type": "connection_refused"}),

        # Separate incident 10 minutes later: redis cache issue
        Alert("b1", base_time + timedelta(minutes=10), "redis-cache", "warning",
              "High memory usage", "Redis memory usage > 90%",
              {"instance": "redis-01", "memory_pct": "92"}),
        Alert("b2", base_time + timedelta(minutes=10, seconds=30), "auth-service", "warning",
              "Cache miss rate high", "Cache hit ratio dropped below 50%",
              {"hit_ratio": "0.35"}),

        # Info alert (noise)
        Alert("c1", base_time + timedelta(minutes=20), "frontend", "info",
              "Deployment started", "New version v2.3.1 rolling out",
              {"version": "2.3.1"}),
    ]


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("=" * 60)
    print("🔔 Alert Correlator — Intelligent Noise Reduction")
    print("=" * 60)

    # Generate alerts
    alerts = generate_sample_alerts()
    print(f"\n📥 Received {len(alerts)} raw alerts\n")

    # Correlate
    print("🔄 Running correlation pipeline...")
    correlator = AlertCorrelator(time_window_seconds=300)
    incidents = correlator.correlate(alerts)

    # Report
    print("\n" + "=" * 60)
    print("📊 Correlation Results")
    print("=" * 60)
    print(f"\n  📥 Raw alerts:      {len(alerts)}")
    print(f"  📤 Incidents:       {len(incidents)}")
    print(f"  📉 Noise reduction: {(1 - len(incidents)/len(alerts))*100:.0f}%")

    for incident in incidents:
        severity_icon = {"critical": "🔴", "warning": "🟡", "info": "🔵"}.get(incident.severity, "⚪")
        print(f"\n  {severity_icon} {incident.id}: {incident.title}")
        print(f"     Severity: {incident.severity.upper()}")
        print(f"     Alerts:   {incident.alert_count}")
        print(f"     Root Cause: {incident.root_cause_service or 'Unknown'}")
        print(f"     Time: {incident.created_at}")
        for alert in incident.alerts:
            print(f"       └─ [{alert.severity:8s}] {alert.service}: {alert.title}")


if __name__ == "__main__":
    main()
