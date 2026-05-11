#!/usr/bin/env python3
"""
=============================================================================
📊 SLO Tracker — Error Budget Calculator & Dashboard
=============================================================================
Description:
    Calculates error budget consumption, burn rate, and projections for your
    services. Simulates real SLO tracking used at Google, Netflix, etc.

Usage:
    python slo_tracker.py

Author: Zero to SRE
License: MIT
=============================================================================
"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict
import random
import math


@dataclass
class SLODefinition:
    """Defines a Service Level Objective."""
    name: str
    sli_description: str
    target: float  # e.g., 99.9
    window_days: int  # Rolling window (usually 30)


@dataclass
class SLIDataPoint:
    """A single SLI measurement."""
    timestamp: datetime
    total_requests: int
    successful_requests: int
    p50_latency_ms: float
    p95_latency_ms: float
    p99_latency_ms: float


def generate_sample_data(days: int = 30) -> List[SLIDataPoint]:
    """Generate realistic SLI data with some degradation events."""
    random.seed(42)
    data = []
    start = datetime.now() - timedelta(days=days)

    for day in range(days):
        for hour in range(24):
            ts = start + timedelta(days=day, hours=hour)

            # Base traffic pattern (higher during business hours)
            hour_factor = 1.0 + 0.5 * math.sin(2 * math.pi * (hour - 6) / 24)
            total = int(10000 * hour_factor + random.gauss(0, 500))
            total = max(total, 100)

            # Success rate (usually > 99.9%, with occasional dips)
            base_success_rate = 0.9995

            # Simulate incidents
            if day == 10 and 14 <= hour <= 16:  # Incident on day 10
                base_success_rate = 0.98  # 2% error rate
            elif day == 22 and 9 <= hour <= 10:  # Minor incident on day 22
                base_success_rate = 0.995

            successful = int(total * (base_success_rate + random.gauss(0, 0.0005)))
            successful = min(successful, total)

            # Latency
            base_latency = 50  # ms
            if day == 10 and 14 <= hour <= 16:
                base_latency = 800  # Slow during incident
            elif day == 22 and 9 <= hour <= 10:
                base_latency = 200

            data.append(SLIDataPoint(
                timestamp=ts,
                total_requests=total,
                successful_requests=successful,
                p50_latency_ms=base_latency * 0.5 + random.gauss(0, 5),
                p95_latency_ms=base_latency * 1.5 + random.gauss(0, 10),
                p99_latency_ms=base_latency * 3.0 + random.gauss(0, 20),
            ))

    return data


def calculate_error_budget(
    slo: SLODefinition,
    data: List[SLIDataPoint]
) -> Dict:
    """Calculate error budget consumption and burn rate."""
    total_requests = sum(d.total_requests for d in data)
    successful_requests = sum(d.successful_requests for d in data)
    failed_requests = total_requests - successful_requests

    # Current SLI
    current_sli = (successful_requests / total_requests) * 100 if total_requests > 0 else 100

    # Error budget
    error_budget_total = total_requests * (1 - slo.target / 100)
    error_budget_consumed = failed_requests
    error_budget_remaining = max(error_budget_total - error_budget_consumed, 0)
    error_budget_consumed_pct = (error_budget_consumed / error_budget_total * 100) if error_budget_total > 0 else 0

    # Burn rate (current rate / expected rate)
    # Expected rate = error_budget_total / window_days
    days_elapsed = len(data) / 24  # hourly data
    expected_budget_consumed = error_budget_total * (days_elapsed / slo.window_days)
    burn_rate = error_budget_consumed / expected_budget_consumed if expected_budget_consumed > 0 else 0

    # Time until budget exhaustion
    if burn_rate > 1 and error_budget_remaining > 0:
        remaining_hours = error_budget_remaining / (error_budget_consumed / len(data))
        time_to_exhaustion = timedelta(hours=remaining_hours)
    elif burn_rate <= 1:
        time_to_exhaustion = None  # Won't exhaust at current rate
    else:
        time_to_exhaustion = timedelta(hours=0)

    # SLO compliance windows
    hourly_compliance = []
    for d in data:
        rate = d.successful_requests / d.total_requests * 100 if d.total_requests > 0 else 100
        hourly_compliance.append(rate >= slo.target)

    compliance_pct = sum(hourly_compliance) / len(hourly_compliance) * 100

    return {
        'slo_name': slo.name,
        'slo_target': slo.target,
        'current_sli': round(current_sli, 4),
        'slo_met': current_sli >= slo.target,
        'total_requests': total_requests,
        'failed_requests': failed_requests,
        'error_budget_total': round(error_budget_total),
        'error_budget_consumed': round(error_budget_consumed),
        'error_budget_remaining': round(error_budget_remaining),
        'error_budget_consumed_pct': round(error_budget_consumed_pct, 1),
        'burn_rate': round(burn_rate, 2),
        'time_to_exhaustion': str(time_to_exhaustion) if time_to_exhaustion else 'N/A (safe)',
        'compliance_pct': round(compliance_pct, 1),
    }


def display_report(result: Dict):
    """Display a formatted SLO report."""
    slo_met = result['slo_met']
    status_icon = "✅" if slo_met else "❌"
    burn_icon = "🟢" if result['burn_rate'] < 1 else "🟡" if result['burn_rate'] < 2 else "🔴"

    print("\n" + "=" * 60)
    print(f"📊 SLO Report: {result['slo_name']}")
    print("=" * 60)

    print(f"\n  {status_icon} SLO Target:        {result['slo_target']}%")
    print(f"  📏 Current SLI:       {result['current_sli']}%")
    print(f"  📋 SLO Met:           {'Yes ✅' if slo_met else 'NO ❌'}")
    print(f"  📈 Compliance:        {result['compliance_pct']}% of hours")

    print(f"\n  📊 Total Requests:    {result['total_requests']:,}")
    print(f"  ❌ Failed Requests:   {result['failed_requests']:,}")

    # Error budget visualization
    consumed_pct = result['error_budget_consumed_pct']
    bar_length = 40
    filled = int(bar_length * min(consumed_pct, 100) / 100)
    bar = "█" * filled + "░" * (bar_length - filled)
    color = "🟢" if consumed_pct < 50 else "🟡" if consumed_pct < 80 else "🔴"

    print(f"\n  💰 Error Budget:")
    print(f"     Total:     {result['error_budget_total']:,} allowed failures")
    print(f"     Consumed:  {result['error_budget_consumed']:,} ({consumed_pct}%)")
    print(f"     Remaining: {result['error_budget_remaining']:,}")
    print(f"     {color} [{bar}] {consumed_pct}%")

    print(f"\n  {burn_icon} Burn Rate:         {result['burn_rate']}x")
    print(f"  ⏰ Time to Exhaust:  {result['time_to_exhaustion']}")

    # Recommendation
    print("\n  📋 Recommendation:")
    if result['burn_rate'] < 0.5:
        print("     🟢 Excellent! Plenty of error budget. Ship features confidently.")
    elif result['burn_rate'] < 1.0:
        print("     🟢 Healthy. Error budget on track. Normal operations.")
    elif result['burn_rate'] < 2.0:
        print("     🟡 Warning. Burning budget faster than planned. Review recent changes.")
    elif result['burn_rate'] < 5.0:
        print("     🟠 Elevated. Consider slowing down deployments. Investigate errors.")
    else:
        print("     🔴 CRITICAL. Freeze feature releases. Focus on reliability immediately.")


def main():
    print("=" * 60)
    print("📊 SLO Tracker — Error Budget Calculator")
    print("=" * 60)

    # Define SLOs
    availability_slo = SLODefinition(
        name="API Availability",
        sli_description="Proportion of successful HTTP requests (non-5xx)",
        target=99.9,
        window_days=30,
    )

    # Generate sample data
    print("\n📊 Generating 30 days of sample SLI data...")
    data = generate_sample_data(days=30)
    print(f"   Generated {len(data)} hourly data points")
    print(f"   Period: {data[0].timestamp.strftime('%Y-%m-%d')} to {data[-1].timestamp.strftime('%Y-%m-%d')}")

    # Calculate and display
    result = calculate_error_budget(availability_slo, data)
    display_report(result)

    # Also show latency SLO
    print("\n" + "=" * 60)
    print("📊 Latency SLO Report")
    print("=" * 60)

    # Check how many hours had p95 > 300ms
    total_hours = len(data)
    hours_within_slo = sum(1 for d in data if d.p95_latency_ms < 300)
    latency_compliance = hours_within_slo / total_hours * 100

    print(f"\n  🎯 SLO: p95 latency < 300ms, 99.5% of the time")
    print(f"  📏 Current: {latency_compliance:.1f}% of hours within target")
    print(f"  {'✅ SLO Met' if latency_compliance >= 99.5 else '❌ SLO Breached'}")

    # Find worst hours
    worst = sorted(data, key=lambda d: d.p95_latency_ms, reverse=True)[:5]
    print(f"\n  🔴 Top 5 worst latency hours:")
    for d in worst:
        print(f"     {d.timestamp.strftime('%Y-%m-%d %H:00')} — p50: {d.p50_latency_ms:.0f}ms, p95: {d.p95_latency_ms:.0f}ms, p99: {d.p99_latency_ms:.0f}ms")


if __name__ == "__main__":
    main()
