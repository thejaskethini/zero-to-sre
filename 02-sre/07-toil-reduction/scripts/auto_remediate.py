#!/usr/bin/env python3
"""
🤖 Auto-Remediation Engine — Self-Healing Infrastructure

Monitors system health and automatically takes corrective actions
based on predefined rules. Demonstrates the auto-remediation pattern
used at Netflix, Google, and Amazon.

Usage: python auto_remediate.py
Author: Zero to SRE | License: MIT
"""
import time
import random
import subprocess
from dataclasses import dataclass
from typing import Callable, Optional, List
from datetime import datetime

@dataclass
class HealthCheck:
    name: str
    check_fn: Callable[[], dict]
    remediate_fn: Callable[[], bool]
    threshold: float
    cooldown_seconds: int = 300
    last_remediated: Optional[datetime] = None

class AutoRemediator:
    """Monitors health checks and auto-remediates failures."""

    def __init__(self):
        self.checks: List[HealthCheck] = []
        self.history: list = []

    def register(self, check: HealthCheck):
        self.checks.append(check)

    def run_once(self):
        """Run all health checks once."""
        for check in self.checks:
            result = check.check_fn()
            status = "✅" if result["healthy"] else "❌"
            print(f"  {status} {check.name}: {result.get('message', '')}")

            if not result["healthy"]:
                # Check cooldown
                if check.last_remediated:
                    elapsed = (datetime.now() - check.last_remediated).seconds
                    if elapsed < check.cooldown_seconds:
                        print(f"    ⏳ Cooldown active ({check.cooldown_seconds - elapsed}s remaining)")
                        continue

                print(f"    🔧 Auto-remediating...")
                success = check.remediate_fn()
                check.last_remediated = datetime.now()
                self.history.append({
                    "time": datetime.now().isoformat(),
                    "check": check.name,
                    "action": "remediated",
                    "success": success,
                })
                icon = "✅" if success else "❌"
                print(f"    {icon} Remediation {'succeeded' if success else 'FAILED'}")

    def run_loop(self, interval: int = 30, max_iterations: int = 5):
        """Run health checks in a loop."""
        print("=" * 55)
        print("🤖 Auto-Remediation Engine — Running")
        print("=" * 55)
        for i in range(max_iterations):
            print(f"\n🔄 Check #{i+1} at {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 40)
            self.run_once()
            if i < max_iterations - 1:
                print(f"\n  ⏱️  Next check in {interval}s...")
                time.sleep(interval)

        print(f"\n{'='*55}")
        print(f"📊 Remediation History: {len(self.history)} actions taken")
        for h in self.history:
            print(f"  [{h['time'][:19]}] {h['check']}: {'✅' if h['success'] else '❌'}")


# ─── SIMULATED HEALTH CHECKS ─────────────────────────────────

def check_disk_space() -> dict:
    """Simulate disk space check."""
    usage = random.uniform(60, 95)
    return {
        "healthy": usage < 85,
        "value": usage,
        "message": f"Disk usage: {usage:.1f}%"
    }

def remediate_disk_space() -> bool:
    """Simulate disk cleanup."""
    print("    📂 Cleaning old logs and temp files...")
    print("    📂 Running: find /var/log -name '*.gz' -mtime +7 -delete")
    print("    📂 Running: docker system prune -f")
    return random.random() > 0.1  # 90% success rate

def check_pod_health() -> dict:
    """Simulate K8s pod health check."""
    healthy_pods = random.randint(1, 3)
    desired = 3
    return {
        "healthy": healthy_pods == desired,
        "value": healthy_pods,
        "message": f"Pods: {healthy_pods}/{desired} healthy"
    }

def remediate_pods() -> bool:
    """Simulate pod restart."""
    print("    ☸️  Running: kubectl rollout restart deployment/myapp")
    print("    ☸️  Waiting for pods to become ready...")
    return random.random() > 0.05  # 95% success rate

def check_certificate() -> dict:
    """Simulate certificate expiry check."""
    days_left = random.randint(1, 90)
    return {
        "healthy": days_left > 14,
        "value": days_left,
        "message": f"Certificate expires in {days_left} days"
    }

def remediate_certificate() -> bool:
    """Simulate certificate renewal."""
    print("    🔒 Running: certbot renew --quiet")
    print("    🔒 Reloading nginx...")
    return random.random() > 0.1

# ─── MAIN ─────────────────────────────────────────────────────

def main():
    engine = AutoRemediator()

    engine.register(HealthCheck(
        name="Disk Space",
        check_fn=check_disk_space,
        remediate_fn=remediate_disk_space,
        threshold=85, cooldown_seconds=60,
    ))
    engine.register(HealthCheck(
        name="Pod Health",
        check_fn=check_pod_health,
        remediate_fn=remediate_pods,
        threshold=3, cooldown_seconds=120,
    ))
    engine.register(HealthCheck(
        name="TLS Certificate",
        check_fn=check_certificate,
        remediate_fn=remediate_certificate,
        threshold=14, cooldown_seconds=300,
    ))

    engine.run_loop(interval=5, max_iterations=4)

if __name__ == "__main__":
    main()
