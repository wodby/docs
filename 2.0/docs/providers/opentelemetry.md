# OpenTelemetry

OpenTelemetry is available in Wodby as a `variable` provider. Use it to send traces, metrics, and logs from your
applications to an OpenTelemetry Collector or an observability vendor. The integration sets the standard OpenTelemetry
SDK variables, so applications instrumented with OpenTelemetry need no Wodby-specific code.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| OTLP endpoint | Yes | `OTEL_EXPORTER_OTLP_ENDPOINT` |
| Protocol | Yes | `OTEL_EXPORTER_OTLP_PROTOCOL` |
| Headers | No | `OTEL_EXPORTER_OTLP_HEADERS` |

- **OTLP endpoint**: the base URL, without a path such as `/v1/traces`. SDKs add the path for each signal.
- **Protocol**: `http/protobuf` or `grpc`. Use `http/protobuf` unless your destination needs gRPC.
- **Headers**: comma-separated `key=value` pairs with URL-encoded values. Wodby stores them as a secret.

To change the endpoint of an existing integration, enter the headers again. They usually hold a token, so a new
endpoint can't reuse them without you entering them.

## Send to a Wodby OpenTelemetry Collector

The [Grafana Tempo](../stacks/catalog/tempo/index.md), [Grafana Loki](../stacks/catalog/loki/index.md), and
[VictoriaMetrics](../stacks/catalog/victoria-metrics/index.md) stacks include an OpenTelemetry Collector with a public
HTTPS domain and a generated ingest token.

| Field | Value |
| --- | --- |
| OTLP endpoint | `https://<Collector domain>`, listed under **Endpoints** for the stack's app environment |
| Protocol | `http/protobuf` |
| Headers | `Authorization=Bearer%20<ingest token>`, revealed on the Collector app service's **Configuration > Tokens** tab |

Each of these Collectors accepts one signal: traces for Tempo, logs for Loki, and metrics for VictoriaMetrics. Turn off
the signals your destination doesn't accept in the application, for example with `OTEL_METRICS_EXPORTER=none` and
`OTEL_LOGS_EXPORTER=none` when sending to the Tempo stack.

## Send to a vendor

Use the OTLP endpoint and headers from your vendor's documentation, such as Grafana Cloud, Honeycomb, Datadog, or
New Relic. Most vendors accept `http/protobuf`.

## Usage

After you create an OpenTelemetry integration and attach it to an app service or stack, Wodby injects the variables
into the container. Set `OTEL_SERVICE_NAME` on each app service to name it in your traces and metrics. See
[Environment variables](../apps/environment-variables.md).

The application must be instrumented with an OpenTelemetry SDK or agent, such as the OpenTelemetry Java agent or
`opentelemetry-instrument` for Python. Without instrumentation, the variables have no effect.
