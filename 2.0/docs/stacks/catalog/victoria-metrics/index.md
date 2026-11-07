# VictoriaMetrics

The Wodby VictoriaMetrics catalog stack runs single-node VictoriaMetrics with Grafana as its interface. The current
composition and defaults are in [`wodby/stack-victoria-metrics`](https://github.com/wodby/stack-victoria-metrics).

To collect traces, metrics, and logs in one app, with links between them in Grafana, use the
[Observability](../observability/index.md) stack.

## Choose services when you create the app

VictoriaMetrics is required. Grafana is enabled by default and is the stack's public interface. Its VictoriaMetrics
data source is provisioned for you. The OpenTelemetry Collector is enabled by default as the public endpoint that
applications send metrics to. You can exclude it when only services in the same app environment write metrics.

## Sign in to Grafana

Open the Grafana app service's **Configuration > Tokens** tab and reveal `admin_username` (`admin`) and
`admin_password`. Grafana applies them once, on the first start with an empty data volume. Changing the tokens later does
not change the existing account. See [Tokens](../../../apps/tokens.md) and the [Grafana guide](../grafana/index.md).

## Send metrics from your applications

Applications send metrics to the OpenTelemetry Collector over OTLP. The Collector's HTTP port has a public HTTPS domain,
listed under **Endpoints** for the app environment, so applications in other app environments, other clusters, or
outside Wodby can use it. Every request needs the Collector's ingest token: open the Collector app service's
**Configuration > Tokens** tab and reveal `ingest_token`. See [Tokens](../../../apps/tokens.md).

Set the standard OpenTelemetry SDK variables in the application that sends metrics:

| Variable | Value |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `https://<Collector domain>`, without a path |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `Authorization=Bearer%20<ingest token>`, stored as a secret |
| `OTEL_SERVICE_NAME` | A name for the application |
| `OTEL_METRICS_EXPORTER` | `otlp` |
| `OTEL_TRACES_EXPORTER`, `OTEL_LOGS_EXPORTER` | `none`, because this Collector accepts metrics only |

The Collector forwards metrics to VictoriaMetrics. VictoriaMetrics keeps OpenTelemetry attribute names, so queries
quote them in label filters, for example `{"service.name"="api"}`. To change what the
Collector does, edit its **Collector config** under **Configuration > Configs** and deploy the service. See
[Configs tab](../../../apps/services.md#configs-tab).

Apps from the Wodby application stacks can instead forward metrics through their own Collector: set its **Metrics**
link to this app's Collector, listed with the other apps you can link to. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## Send and query metrics

VictoriaMetrics listens on port `8428`. The port is private, so Wodby creates no public route for it. Other services in
the app environment reach it at `http://<VictoriaMetrics app service name>:8428`. No authentication is configured.

The same port serves:

- the Prometheus-compatible query API (`/api/v1/query`, `/api/v1/query_range`), which Grafana uses
- Prometheus remote write (`/api/v1/write`)
- the built-in interface (`/vmui`)

Wodby sets no scrape configuration. Metrics arrive only when something writes them: the Collector, or a service in the
same app environment.

## Limits

- Retention is the upstream default. Wodby sets none.
- VictoriaMetrics has no settings, links, or config files in Wodby. Environment variables are not read as flags, so you
  cannot change its flags this way.
- It is not scalable.

## Data

The stack creates a 20 GB **VictoriaMetrics data** volume, mounted at `/victoria-metrics-data`. Grafana has its own
10 GB volume. Wodby defines no backups or imports for these services.

## Check that it is ready

`/-/ready` and `/-/healthy` on port `8428` are the readiness and liveness endpoints.
