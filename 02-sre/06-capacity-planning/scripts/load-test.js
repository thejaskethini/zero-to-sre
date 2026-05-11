// =============================================================================
// 📈 k6 Load Test Script — Production-Ready
// =============================================================================
// Description:
//   Load test script for validating API performance under various conditions.
//   Tests: smoke, load, stress, and spike scenarios.
//
// Prerequisites:
//   brew install k6  (macOS)
//   choco install k6  (Windows)
//   snap install k6  (Linux)
//
// Usage:
//   # Smoke test (quick validation)
//   k6 run --env SCENARIO=smoke load-test.js
//
//   # Full load test
//   k6 run --env SCENARIO=load load-test.js
//
//   # Stress test (find breaking point)
//   k6 run --env SCENARIO=stress load-test.js
//
//   # With HTML report
//   k6 run --out json=results.json load-test.js
//
// Reference: https://k6.io/docs/
// =============================================================================

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// ─── Custom Metrics ────────────────────────────────────────────────────────
const errorRate = new Rate('errors');
const apiDuration = new Trend('api_duration', true);
const requestCount = new Counter('total_requests');

// ─── Configuration ─────────────────────────────────────────────────────────
const BASE_URL = __ENV.BASE_URL || 'http://localhost:3000';

// ─── Test Scenarios ────────────────────────────────────────────────────────
// Choose scenario via: k6 run --env SCENARIO=load load-test.js

const scenarios = {
  // Smoke Test — Quick validation (1-2 min)
  smoke: {
    executor: 'constant-vus',
    vus: 1,
    duration: '1m',
  },

  // Load Test — Normal expected load (10 min)
  load: {
    executor: 'ramping-vus',
    stages: [
      { duration: '2m', target: 50 },   // Ramp up to 50 users
      { duration: '5m', target: 50 },   // Stay at 50 users
      { duration: '2m', target: 100 },  // Ramp up to 100 users
      { duration: '3m', target: 100 },  // Stay at 100 users
      { duration: '2m', target: 0 },    // Ramp down
    ],
  },

  // Stress Test — Beyond normal capacity (15 min)
  stress: {
    executor: 'ramping-vus',
    stages: [
      { duration: '2m', target: 100 },
      { duration: '3m', target: 200 },
      { duration: '3m', target: 300 },  // Push limits
      { duration: '3m', target: 400 },  // Breaking point?
      { duration: '2m', target: 0 },
    ],
  },

  // Spike Test — Sudden burst (5 min)
  spike: {
    executor: 'ramping-vus',
    stages: [
      { duration: '30s', target: 10 },
      { duration: '30s', target: 500 },  // Sudden spike!
      { duration: '1m', target: 500 },
      { duration: '30s', target: 10 },   // Sudden drop
      { duration: '1m', target: 10 },
    ],
  },
};

// Select scenario from environment variable
const selectedScenario = __ENV.SCENARIO || 'smoke';

export const options = {
  scenarios: {
    default: scenarios[selectedScenario] || scenarios.smoke,
  },

  // SLO Thresholds — Test FAILS if these are breached
  thresholds: {
    http_req_duration: [
      'p(95) < 500',   // 95% of requests under 500ms
      'p(99) < 2000',  // 99% of requests under 2s
    ],
    http_req_failed: ['rate < 0.05'],  // Error rate < 5%
    errors: ['rate < 0.1'],
  },
};

// ─── Test Functions ────────────────────────────────────────────────────────

export default function () {
  // Group: Health Check
  group('Health Check', function () {
    const res = http.get(`${BASE_URL}/health`);
    check(res, {
      'health status is 200': (r) => r.status === 200,
      'health response time < 100ms': (r) => r.timings.duration < 100,
    });
    errorRate.add(res.status !== 200);
    requestCount.add(1);
  });

  // Group: API Endpoints
  group('API Endpoints', function () {
    // GET — List resources
    const listRes = http.get(`${BASE_URL}/api/v1/items`, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${__ENV.API_TOKEN || 'test-token'}`,
      },
    });
    check(listRes, {
      'list status is 200': (r) => r.status === 200,
      'list has items': (r) => {
        try {
          return JSON.parse(r.body).length > 0;
        } catch {
          return false;
        }
      },
    });
    apiDuration.add(listRes.timings.duration);
    errorRate.add(listRes.status !== 200);
    requestCount.add(1);

    // POST — Create resource
    const payload = JSON.stringify({
      name: `load-test-${Date.now()}`,
      value: Math.random() * 100,
    });

    const createRes = http.post(`${BASE_URL}/api/v1/items`, payload, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${__ENV.API_TOKEN || 'test-token'}`,
      },
    });
    check(createRes, {
      'create status is 201 or 200': (r) => [200, 201].includes(r.status),
      'create response time < 500ms': (r) => r.timings.duration < 500,
    });
    apiDuration.add(createRes.timings.duration);
    errorRate.add(![200, 201].includes(createRes.status));
    requestCount.add(1);
  });

  // Think time — simulate real user behavior
  sleep(Math.random() * 2 + 1); // 1-3 seconds between requests
}

// ─── Summary Report ────────────────────────────────────────────────────────

export function handleSummary(data) {
  const summary = {
    scenario: selectedScenario,
    timestamp: new Date().toISOString(),
    total_requests: data.metrics.total_requests ? data.metrics.total_requests.values.count : 0,
    avg_duration_ms: data.metrics.http_req_duration ? data.metrics.http_req_duration.values.avg.toFixed(2) : 0,
    p95_duration_ms: data.metrics.http_req_duration ? data.metrics.http_req_duration.values['p(95)'].toFixed(2) : 0,
    p99_duration_ms: data.metrics.http_req_duration ? data.metrics.http_req_duration.values['p(99)'].toFixed(2) : 0,
    error_rate: data.metrics.http_req_failed ? (data.metrics.http_req_failed.values.rate * 100).toFixed(2) + '%' : '0%',
  };

  console.log('\n' + '='.repeat(60));
  console.log('📊 Load Test Summary');
  console.log('='.repeat(60));
  console.log(JSON.stringify(summary, null, 2));
  console.log('='.repeat(60));

  return {
    stdout: JSON.stringify(summary, null, 2),
  };
}
