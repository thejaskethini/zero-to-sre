# 🔭 OpenTelemetry Cheatsheet

> The vendor-neutral observability standard — traces, metrics, logs, SDK, Collector, and instrumentation.

---

## 🏗️ Architecture

```
Your App (SDK) → OTel Collector → Backend (Jaeger/Prometheus/Loki)

Components:
  SDK        → Instrument your code (auto or manual)
  Collector  → Receive, process, export telemetry data
  Exporters  → Send to backends (Jaeger, Prometheus, Datadog, etc.)

Three Signals:
  Traces   → Request flow across services (spans)
  Metrics  → Numeric measurements (counters, gauges, histograms)
  Logs     → Structured event records
```

## 📦 Collector Setup

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318
  prometheus:
    config:
      scrape_configs:
        - job_name: 'otel-collector'
          scrape_interval: 15s
          static_configs:
            - targets: ['localhost:8888']

processors:
  batch:
    timeout: 5s
    send_batch_size: 1024
  memory_limiter:
    check_interval: 1s
    limit_mib: 512
  attributes:
    actions:
      - key: environment
        value: production
        action: upsert
  tail_sampling:
    decision_wait: 10s
    policies:
      - name: errors
        type: status_code
        status_code: { status_codes: [ERROR] }
      - name: slow-requests
        type: latency
        latency: { threshold_ms: 1000 }
      - name: sample-rest
        type: probabilistic
        probabilistic: { sampling_percentage: 10 }

exporters:
  otlp/jaeger:
    endpoint: jaeger:4317
    tls:
      insecure: true
  prometheus:
    endpoint: 0.0.0.0:8889
  loki:
    endpoint: http://loki:3100/loki/api/v1/push

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp/jaeger]
    metrics:
      receivers: [otlp, prometheus]
      processors: [memory_limiter, batch]
      exporters: [prometheus]
    logs:
      receivers: [otlp]
      processors: [memory_limiter, batch, attributes]
      exporters: [loki]
```

## 🟢 Node.js Auto-Instrumentation

```javascript
// tracing.js — load BEFORE your app
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { getNodeAutoInstrumentations } = require('@opentelemetry/auto-instrumentations-node');
const { OTLPTraceExporter } = require('@opentelemetry/exporter-trace-otlp-grpc');
const { OTLPMetricExporter } = require('@opentelemetry/exporter-metrics-otlp-grpc');
const { PeriodicExportingMetricReader } = require('@opentelemetry/sdk-metrics');

const sdk = new NodeSDK({
  serviceName: 'api-server',
  traceExporter: new OTLPTraceExporter({
    url: 'http://otel-collector:4317',
  }),
  metricReader: new PeriodicExportingMetricReader({
    exporter: new OTLPMetricExporter({
      url: 'http://otel-collector:4317',
    }),
    exportIntervalMillis: 15000,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
});

sdk.start();
```

```bash
# Run with auto-instrumentation
node --require ./tracing.js server.js

# Or via environment variables
OTEL_SERVICE_NAME=api-server \
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317 \
OTEL_TRACES_SAMPLER=parentbased_traceidratio \
OTEL_TRACES_SAMPLER_ARG=0.1 \
node --require @opentelemetry/auto-instrumentations-node/register server.js
```

## 🐍 Python Auto-Instrumentation

```bash
pip install opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install  # Auto-install instrumentations

OTEL_SERVICE_NAME=api \
OTEL_EXPORTER_OTLP_ENDPOINT=http://collector:4317 \
opentelemetry-instrument python app.py
```

## 📐 Manual Instrumentation

```javascript
// Custom spans (when auto-instrumentation isn't enough)
const { trace } = require('@opentelemetry/api');
const tracer = trace.getTracer('payment-service');

async function processPayment(order) {
  return tracer.startActiveSpan('process-payment', async (span) => {
    try {
      span.setAttribute('order.id', order.id);
      span.setAttribute('order.amount', order.amount);
      span.setAttribute('payment.method', order.paymentMethod);

      const result = await chargeCard(order);

      span.setAttribute('payment.status', 'success');
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      span.recordException(error);
      throw error;
    } finally {
      span.end();
    }
  });
}
```

## ☸️ Kubernetes Deployment

```yaml
# OTel Collector as DaemonSet
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: otel-collector
spec:
  selector:
    matchLabels:
      app: otel-collector
  template:
    spec:
      containers:
        - name: collector
          image: otel/opentelemetry-collector-contrib:latest
          ports:
            - containerPort: 4317   # OTLP gRPC
            - containerPort: 4318   # OTLP HTTP
            - containerPort: 8889   # Prometheus metrics
          volumeMounts:
            - name: config
              mountPath: /etc/otelcol-contrib
      volumes:
        - name: config
          configMap:
            name: otel-collector-config
```

## 🎯 FAANG Interview Q&A

```
Q: Why OpenTelemetry over vendor-specific agents?
A: Vendor-neutral — instrument once, export to any backend.
   Switch from Jaeger to Datadog without code changes.
   CNCF-backed standard, merges OpenTracing + OpenCensus.
   Reduces vendor lock-in, future-proofs observability.

Q: What's the difference between auto and manual instrumentation?
A: Auto: SDK automatically instruments HTTP, DB, cache libraries
   (zero code changes). Manual: custom spans for business logic,
   custom attributes. Best practice: auto for infrastructure,
   manual for business-critical paths.

Q: Explain sampling strategies.
A: Head-based: decide at trace start (simple, may miss errors).
   Tail-based: decide after trace completes (captures errors/slow).
   Always sample errors + slow requests, probabilistic for rest.
   Production: tail-sampling in Collector, 100% for errors, 10% rest.

Q: How does context propagation work?
A: Trace context (trace_id, span_id) is injected into request headers
   (W3C Traceparent or B3). Each service extracts context and creates
   child spans. This links spans across services into one trace.
```

---

> 💡 **Production Rule:** Always use the OTel Collector as a middleman — never export directly from apps to backends. The Collector handles batching, retries, sampling, and format conversion.
