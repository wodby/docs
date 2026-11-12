---
description: Collect traces, metrics and logs from your applications in one Wodby app with the Observability catalog stack, built on OpenTelemetry and Grafana.
---

# Observability

The Wodby Observability catalog stack collects traces, metrics, and logs from your applications in one app. The
OpenTelemetry Collector receives all three on one endpoint. Grafana Tempo stores traces, VictoriaMetrics stores metrics,
Grafana Loki stores logs, and Grafana shows them together. The current composition and defaults are in
[`wodby/stack-observability`](https://github.com/wodby/stack-observability).

Use this stack when you want all three signals in one place. To collect only one of them, use the
[Grafana Tempo](../tempo/index.md), [Grafana Loki](../loki/index.md), or
[VictoriaMetrics](../victoria-metrics/index.md) stack instead.

## Choose services when you create the app

Tempo, Loki, VictoriaMetrics, and the OpenTelemetry Collector are required. Grafana is enabled by default as the
stack's main interface. You can exclude Grafana when you query the data from another Grafana.

## Send telemetry from your applications

Applications send traces, metrics, and logs to the Collector over OTLP. The Collector's HTTP port has a public HTTPS
domain, listed under **Endpoints** for the app environment, so applications in other app environments, other clusters,
or outside Wodby can use it.

Every request needs the Collector's ingest token. Open the Collector app service's **Configuration > Tokens** tab and
reveal `ingest_token`. See [Tokens](../../../apps/tokens.md). Requests without the token are refused with `401`.

Set the standard OpenTelemetry SDK variables in the application that sends telemetry:

| Variable | Value |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `https://<Collector domain>`, without a path |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `Authorization=Bearer%20<ingest token>`, stored as a secret |
| `OTEL_SERVICE_NAME` | A name for the application, shown in Grafana |

The space after `Bearer` is written as `%20` because SDKs URL-decode header values. On Wodby, add the variables to the
sending app service. See [Environment variables](../../../apps/environment-variables.md).

The Collector sends traces to Tempo, metrics to VictoriaMetrics, and logs to Loki, so you don't need to turn off any
signal in the SDK. If your SDK or agent doesn't export metrics or logs by default, set `OTEL_METRICS_EXPORTER=otlp`
and `OTEL_LOGS_EXPORTER=otlp`.

Inside the same app environment, services can also send to `http://<Collector app service name>:4318`, or over gRPC to
port `4317`, with the same token.

Apps from the Wodby application stacks can instead forward telemetry through their own Collector: set its
**Upstream** link to this app's Collector, listed with the other apps you can link to. On the same cluster the data
stays on the private network. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## View telemetry in Grafana

Open the Grafana domain listed under **Endpoints**. Open the Grafana app service's **Configuration > Tokens** tab and
reveal `admin_username` (`admin`) and `admin_password`. Grafana applies them once, on the first start with an empty data
volume. See the [Grafana guide](../grafana/index.md).

Grafana has three data sources:

- **VictoriaMetrics**, the default, for metrics. VictoriaMetrics keeps OpenTelemetry attribute names, so queries quote
  them in label filters, for example `{"service.name"="api"}`.
- **Loki** for logs. Find them by the `service_name` label, for example `{service_name="api"}`.
- **Tempo** for traces. Search them with **Explore** or **Drilldown > Traces**.

The data sources are linked:

- From a span in Tempo, open **Logs for this span** to see the Loki logs of the same trace, from 5 minutes before the
  span to 5 minutes after it.
- A log line written during a trace shows a **View trace** link in its details that opens the trace in Tempo.

The links work when the application writes logs through the OpenTelemetry SDK while a trace is active, so each log
record carries the trace ID.

## Change configuration

The Collector config, Tempo config, and Grafana data sources are files under their app service's **Configuration >
Configs** tab. See [Configs tab](../../../apps/services.md#configs-tab). After a change, deploy the app service. Wodby
restarts it so the new file takes effect.

Common changes:

- **Send data to another backend as well.** Add an exporter to the Collector config, for example `otlp_http` with the
  backend's endpoint and headers. In each pipeline that should send to it, replace the exporter list
  `${env:OTLP_<SIGNAL>_EXPORTERS:-[nop]}` with both exporters, such as `[otlp_http/logs, otlp_http/<name>]`. Put the
  backend's key in a secret environment variable of the Collector and refer to it as `${env:NAME}` in the file.
- **Keep traces longer.** See [Grafana Tempo](../tempo/index.md#change-configuration).

Keep the token check on the Collector's receivers while its HTTP port has a public domain.

## Data

The stack creates a 20 GB data volume each for Tempo, Loki, and VictoriaMetrics. Grafana has its own 10 GB volume with
its dashboards, users, settings, and plugins. Tempo deletes traces after 7 days. Wodby sets no retention for
VictoriaMetrics, so it keeps the upstream default. Wodby defines no backups or imports for these services.

## Limits

- Tempo, Loki, and VictoriaMetrics each run as a single instance and are not scalable. The stack suits development
  environments and low to moderate volumes.
- Their ports are private: query them through Grafana or from another service in the app environment.
- The Collector can run several replicas with the default configuration.

## Check that the services are ready

- Tempo: `/ready` on port `3200`.
- Loki: `/ready` on port `3100`.
- VictoriaMetrics: `/-/ready` on port `8428`.
- Collector: port `13133` answers `200` when every pipeline has started.
- Send a test request to the Collector domain with the token: a `POST` of `{}` with `Content-Type: application/json` to
  `https://<Collector domain>/v1/traces`, `/v1/metrics`, or `/v1/logs` returns `200`.
