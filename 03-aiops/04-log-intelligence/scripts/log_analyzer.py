#!/usr/bin/env python3
"""
=============================================================================
📝 Log Pattern Analyzer — Automated Log Clustering & Anomaly Detection
=============================================================================
Description:
    Analyzes log files to:
    1. Parse and structure unstructured logs
    2. Cluster similar log patterns (reduce noise)
    3. Detect anomalous log patterns
    4. Generate summary statistics

Usage:
    pip install pandas numpy
    python log_analyzer.py [--file /path/to/logfile]
    python log_analyzer.py  # Uses built-in sample data

Author: Zero to SRE
License: MIT
=============================================================================
"""

import re
import sys
import argparse
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import hashlib


# =============================================================================
# LOG PARSER — Extracts structure from unstructured log lines
# =============================================================================

# Common log format patterns
LOG_PATTERNS = {
    'timestamp': r'(\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?)',
    'level': r'\b(DEBUG|INFO|WARN(?:ING)?|ERROR|FATAL|CRITICAL)\b',
    'ip': r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',
    'status_code': r'\b([1-5]\d{2})\b',
    'duration_ms': r'(\d+(?:\.\d+)?)\s*(?:ms|milliseconds)',
    'duration_s': r'(\d+(?:\.\d+)?)\s*(?:s|seconds)',
    'uuid': r'([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})',
    'path': r'(?:GET|POST|PUT|DELETE|PATCH)\s+(/\S+)',
}


def parse_log_line(line: str) -> Dict:
    """Parse a single log line and extract structured fields."""
    parsed = {'raw': line.strip()}

    for field, pattern in LOG_PATTERNS.items():
        match = re.search(pattern, line, re.IGNORECASE)
        if match:
            parsed[field] = match.group(1)

    return parsed


def create_log_template(line: str) -> str:
    """
    Create a template from a log line by replacing variable parts with placeholders.
    This is a simplified version of log parsing algorithms like Drain3.
    """
    template = line.strip()

    # Replace common variable patterns with placeholders
    replacements = [
        (r'\d{4}[-/]\d{2}[-/]\d{2}[\sT]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:?\d{2})?', '<TIMESTAMP>'),
        (r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<UUID>'),
        (r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', '<IP>'),
        (r'(?<=[\s=:"])\d+(?:\.\d+)?(?=[\s,;"\]]|$)', '<NUM>'),
        (r'"[^"]*"', '<STR>'),
    ]

    for pattern, placeholder in replacements:
        template = re.sub(pattern, placeholder, template)

    return template


# =============================================================================
# LOG CLUSTERING — Group similar log lines
# =============================================================================

def cluster_logs(lines: List[str]) -> Dict[str, List[int]]:
    """
    Cluster log lines by their template pattern.
    Returns: {template: [line_indices]}
    """
    clusters = defaultdict(list)

    for i, line in enumerate(lines):
        template = create_log_template(line)
        # Create a hash for efficient grouping
        template_hash = hashlib.md5(template.encode()).hexdigest()[:8]
        clusters[f"{template_hash}|{template}"] = clusters.get(
            f"{template_hash}|{template}", []
        )
        clusters[f"{template_hash}|{template}"].append(i)

    return clusters


# =============================================================================
# ANOMALY DETECTION — Find unusual log patterns
# =============================================================================

def detect_log_anomalies(
    lines: List[str],
    window_minutes: int = 5
) -> Dict:
    """
    Detect anomalies in log data:
    1. Error burst detection (sudden spike in errors)
    2. New pattern detection (patterns never seen before)
    3. Volume anomaly (unusual number of logs)
    """
    anomalies = {
        'error_bursts': [],
        'new_patterns': [],
        'volume_anomalies': [],
    }

    # Parse all lines
    parsed_lines = [parse_log_line(line) for line in lines]

    # --- Error Burst Detection ---
    error_counts = Counter()
    for parsed in parsed_lines:
        level = parsed.get('level', '').upper()
        if level in ('ERROR', 'FATAL', 'CRITICAL'):
            ts = parsed.get('timestamp', '')
            if ts:
                # Group by minute
                minute_key = ts[:16]  # YYYY-MM-DD HH:MM
                error_counts[minute_key] += 1

    if error_counts:
        avg_errors = sum(error_counts.values()) / max(len(error_counts), 1)
        for minute, count in error_counts.items():
            if count > avg_errors * 3:  # 3x average = anomaly
                anomalies['error_bursts'].append({
                    'time': minute,
                    'error_count': count,
                    'avg_count': round(avg_errors, 1),
                    'severity': 'HIGH' if count > avg_errors * 5 else 'MEDIUM'
                })

    # --- Level Distribution ---
    level_counts = Counter()
    for parsed in parsed_lines:
        level = parsed.get('level', 'UNKNOWN')
        level_counts[level.upper()] += 1

    # --- Status Code Distribution ---
    status_counts = Counter()
    for parsed in parsed_lines:
        code = parsed.get('status_code', '')
        if code:
            status_counts[code] += 1

    return anomalies, level_counts, status_counts


# =============================================================================
# SAMPLE LOG DATA — For demonstration
# =============================================================================

SAMPLE_LOGS = """2025-01-15T10:30:01Z INFO  [api] GET /health - 200 - 2ms - req_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890
2025-01-15T10:30:02Z INFO  [api] GET /api/v1/users - 200 - 45ms - ip=10.0.1.52
2025-01-15T10:30:02Z INFO  [api] POST /api/v1/orders - 201 - 120ms - ip=10.0.1.53
2025-01-15T10:30:03Z DEBUG [db] Query executed: SELECT * FROM users WHERE id = 12345 - 12ms
2025-01-15T10:30:03Z INFO  [api] GET /api/v1/products - 200 - 35ms - ip=10.0.1.54
2025-01-15T10:30:04Z WARN  [cache] Cache miss for key: user:12345 - falling back to database
2025-01-15T10:30:05Z INFO  [api] GET /api/v1/users - 200 - 42ms - ip=10.0.1.55
2025-01-15T10:30:06Z ERROR [api] POST /api/v1/payments - 500 - 5032ms - ip=10.0.1.56 - err="connection timeout to payment-gateway:443"
2025-01-15T10:30:06Z ERROR [payment] Payment processing failed for order ord-789 - timeout after 5000ms
2025-01-15T10:30:07Z ERROR [api] POST /api/v1/payments - 500 - 5001ms - ip=10.0.1.57 - err="connection timeout to payment-gateway:443"
2025-01-15T10:30:07Z ERROR [payment] Payment processing failed for order ord-790 - timeout after 5000ms
2025-01-15T10:30:08Z ERROR [api] POST /api/v1/payments - 503 - 100ms - ip=10.0.1.58 - err="circuit breaker OPEN for payment-gateway"
2025-01-15T10:30:08Z WARN  [circuit-breaker] Circuit breaker opened for payment-gateway - 5 failures in 10s
2025-01-15T10:30:09Z INFO  [api] GET /health - 200 - 1ms
2025-01-15T10:30:10Z INFO  [api] GET /api/v1/users - 200 - 38ms - ip=10.0.1.59
2025-01-15T10:30:11Z ERROR [api] POST /api/v1/payments - 503 - 5ms - ip=10.0.1.60 - err="circuit breaker OPEN for payment-gateway"
2025-01-15T10:30:12Z WARN  [retry] Retry attempt 1/3 for payment-gateway connection
2025-01-15T10:30:15Z WARN  [retry] Retry attempt 2/3 for payment-gateway connection
2025-01-15T10:30:20Z INFO  [retry] Retry attempt 3/3 for payment-gateway connection - SUCCESS
2025-01-15T10:30:20Z INFO  [circuit-breaker] Circuit breaker half-open for payment-gateway - testing with probe request
2025-01-15T10:30:21Z INFO  [circuit-breaker] Circuit breaker closed for payment-gateway - service recovered
2025-01-15T10:30:22Z INFO  [api] POST /api/v1/payments - 201 - 250ms - ip=10.0.1.61
2025-01-15T10:30:23Z INFO  [api] GET /api/v1/orders/ord-789 - 200 - 30ms - ip=10.0.1.56""".strip()


# =============================================================================
# MAIN — Run analysis
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='📝 Log Pattern Analyzer')
    parser.add_argument('--file', '-f', help='Path to log file (uses sample data if not provided)')
    args = parser.parse_args()

    print("=" * 60)
    print("📝 Log Pattern Analyzer")
    print("=" * 60)

    # Load log data
    if args.file:
        try:
            with open(args.file, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
            print(f"\n📂 Loaded {len(lines)} lines from {args.file}")
        except FileNotFoundError:
            print(f"\n❌ File not found: {args.file}")
            sys.exit(1)
    else:
        lines = SAMPLE_LOGS.split('\n')
        print(f"\n📊 Using sample data ({len(lines)} log lines)")

    # --- Step 1: Parse & Cluster ---
    print("\n" + "-" * 60)
    print("🔗 Step 1: Log Pattern Clustering")
    print("-" * 60)

    clusters = cluster_logs(lines)
    sorted_clusters = sorted(clusters.items(), key=lambda x: len(x[1]), reverse=True)

    print(f"\n📊 Found {len(clusters)} unique log patterns:\n")
    for key, indices in sorted_clusters[:10]:  # Top 10 patterns
        template = key.split('|', 1)[1] if '|' in key else key
        count = len(indices)
        pct = count / len(lines) * 100
        # Truncate long templates
        display = template[:80] + "..." if len(template) > 80 else template
        print(f"  [{count:4d}x] ({pct:5.1f}%) {display}")

    # --- Step 2: Anomaly Detection ---
    print("\n" + "-" * 60)
    print("📉 Step 2: Anomaly Detection")
    print("-" * 60)

    anomalies, level_counts, status_counts = detect_log_anomalies(lines)

    # Level distribution
    print("\n📊 Log Level Distribution:")
    total = sum(level_counts.values())
    for level, count in sorted(level_counts.items(), key=lambda x: -x[1]):
        bar = "█" * int(count / total * 40)
        icon = {"ERROR": "🔴", "WARN": "🟡", "WARNING": "🟡", "INFO": "🟢", "DEBUG": "⚪", "FATAL": "💀"}.get(level, "⚪")
        print(f"  {icon} {level:8s}: {count:4d} ({count/total*100:5.1f}%) {bar}")

    # Status code distribution
    if status_counts:
        print("\n📊 HTTP Status Code Distribution:")
        for code, count in sorted(status_counts.items()):
            icon = "🟢" if code.startswith('2') else "🟡" if code.startswith('3') else "🟠" if code.startswith('4') else "🔴"
            print(f"  {icon} {code}: {count}")

    # Error bursts
    if anomalies['error_bursts']:
        print(f"\n🚨 Error Bursts Detected ({len(anomalies['error_bursts'])}):")
        for burst in anomalies['error_bursts']:
            print(f"  ⚠️  [{burst['severity']}] {burst['time']}: {burst['error_count']} errors (avg: {burst['avg_count']})")
    else:
        print("\n✅ No error bursts detected")

    # --- Step 3: Key Insights ---
    print("\n" + "-" * 60)
    print("💡 Step 3: Key Insights")
    print("-" * 60)

    error_lines = [l for l in lines if re.search(r'\bERROR\b', l, re.IGNORECASE)]
    if error_lines:
        print(f"\n🔴 Top Errors ({len(error_lines)} total):")
        error_messages = Counter()
        for line in error_lines:
            # Extract error message
            err_match = re.search(r'err="([^"]+)"', line)
            if err_match:
                error_messages[err_match.group(1)] += 1
            else:
                # Use the last part of the line as error description
                parts = line.split(' - ')
                if len(parts) > 1:
                    error_messages[parts[-1].strip()] += 1

        for msg, count in error_messages.most_common(5):
            print(f"  [{count}x] {msg}")

    print("\n✅ Analysis complete!")


if __name__ == "__main__":
    main()
