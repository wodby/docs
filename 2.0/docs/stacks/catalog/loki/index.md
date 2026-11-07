# Grafana Loki

The Wodby Grafana Loki catalog stack runs Loki with Grafana as its interface. The current composition and defaults are
in [`wodby/stack-loki`](https://github.com/wodby/stack-loki).

To collect traces, metrics, and logs in one app, with links between them in Grafana, use the
[Observability](../observability/index.md) stack.

## Choose services when you create the app

Loki is required. Grafana is enabled by default as the stack's main interface, with Loki provisioned as its default
data source. The OpenTelemetry Collector is enabled by default as the public endpoint that applications send logs to.
You can exclude Grafana when you need only the Loki API, and the Collector when only services in the same app
environment write to Loki.

## Sign in to Grafana

Open the Grafana app service's **Configuration > Tokens** tab and reveal `admin_username` (`admin`) and
`admin_password`. Grafana applies them once, on the first start with an empty data volume. Changing the tokens later does
not change the existing account. See [Tokens](../../../apps/tokens.md) and the [Grafana guide](../grafana/index.md).

## Send logs from your applications

Applications send logs to the OpenTelemetry Collector over OTLP. The Collector's HTTP port has a public HTTPS domain,
listed under **Endpoints** for the app environment, so applications in other app environments, other clusters, or
outside Wodby can use it. Every request needs the Collector's ingest token: open the Collector app service's
**Configuration > Tokens** tab and reveal `ingest_token`. See [Tokens](../../../apps/tokens.md).

Set the standard OpenTelemetry SDK variables in the application that sends logs:

| Variable | Value |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `https://<Collector domain>`, without a path |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `Authorization=Bearer%20<ingest token>`, stored as a secret |
| `OTEL_SERVICE_NAME` | A name for the application |
| `OTEL_LOGS_EXPORTER` | `otlp` |
| `OTEL_TRACES_EXPORTER`, `OTEL_METRICS_EXPORTER` | `none`, because this Collector accepts logs only |

The Collector forwards logs to Loki. In Grafana, find them by the `service_name` label, for example
`{service_name="api"}`. To change what the Collector does, edit its **Collector config** under
**Configuration > Configs** and deploy the service. See [Configs tab](../../../apps/services.md#configs-tab) and the
[Grafana Tempo guide](../tempo/index.md#change-configuration) for the same Collector used for traces.

Apps from the Wodby application stacks can instead forward logs through their own Collector: set its **Logs**
link to this app's Collector, listed with the other apps you can link to. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## Connect to Loki

Loki runs as a single instance and listens on port `3100`. The port is private, so Wodby creates no public route for
it. Other services in the app environment reach it at `http://<Loki app service name>:3100`.

Authentication is off, and Loki stores chunks, index, and rules on the local filesystem.

## Data

The stack creates a 20 GB **Loki data** volume, mounted at `/loki`. Grafana has its own 10 GB volume. Wodby defines no
backups or imports for these services.

## Limits

- Loki has no settings, links, or config files in Wodby. Its configuration file is part of the image and is not on a
  volume, so do not edit it in the container.
- Loki is not scalable.

## Check that Loki is ready

`/ready` on port `3100` answers when Loki can accept requests.
