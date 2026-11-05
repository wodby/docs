# Grafana Tempo

The Wodby Grafana Tempo catalog stack collects and stores distributed traces from your applications. The OpenTelemetry
Collector receives traces, Grafana Tempo stores them, and Grafana shows them. The current composition and defaults are
in [`wodby/stack-tempo`](https://github.com/wodby/stack-tempo).

## Choose services when you create the app

Tempo and the OpenTelemetry Collector are required. Grafana is enabled by default as the stack's main interface, with
Tempo provisioned as its default data source. You can exclude Grafana when you query Tempo from another Grafana.

## Send traces from your applications

Applications send traces to the Collector over OTLP. The Collector's HTTP port has a public HTTPS domain, listed under
**Endpoints** for the app environment, so applications in other app environments, other clusters, or outside Wodby can
use it.

Every request needs the Collector's ingest token. Open the Collector app service's **Configuration > Tokens** tab and
reveal `ingest_token`. See [Tokens](../../../apps/tokens.md). Requests without the token are refused with `401`.

Set the standard OpenTelemetry SDK variables in the application that sends traces:

| Variable | Value |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `https://<Collector domain>`, without a path |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_HEADERS` | `Authorization=Bearer%20<ingest token>` |
| `OTEL_SERVICE_NAME` | A name for the application, shown in Grafana |

Store `OTEL_EXPORTER_OTLP_HEADERS` as a secret variable. The space after `Bearer` is written as `%20` because SDKs
URL-decode header values. On Wodby, add the variables to the sending app service. See
[Environment variables](../../../apps/environment-variables.md).

The Collector accepts traces only. Set `OTEL_METRICS_EXPORTER=none` and `OTEL_LOGS_EXPORTER=none` for SDKs and agents
that also export metrics or logs by default, such as the OpenTelemetry Java agent; otherwise those exports fail.

Inside the same app environment, services can also send to `http://<Collector app service name>:4318`, or over gRPC to
port `4317`, with the same token.

Apps from the Wodby application stacks can instead forward traces through their own Collector, set to this
Collector's domain and token. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## View traces in Grafana

Open the Grafana domain listed under **Endpoints**. Open the Grafana app service's **Configuration > Tokens** tab and
reveal `admin_username` (`admin`) and `admin_password`. Grafana applies them once, on the first start with an empty data
volume. See the [Grafana guide](../grafana/index.md).

Search traces with **Explore** and the Tempo data source, or with **Drilldown > Traces**. A trace can be opened by ID
as soon as it arrives; it appears in search results a few seconds later.

## Change configuration

The Collector and Tempo each have a config file under their app service's **Configuration > Configs** tab: **Collector
config** and **Tempo config**. See [Configs tab](../../../apps/services.md#configs-tab). After a change, deploy the app
service. Wodby restarts it so the new file takes effect.

Common changes:

- **Send traces to another backend as well.** Add an exporter to the Collector config, for example `otlp_http` with the
  backend's endpoint and headers, and list it in the traces pipeline. Put the backend's key in a secret environment
  variable of the Collector and refer to it as `${env:NAME}` in the file.
- **Keep traces longer.** Tempo deletes traces after 7 days. Change
  `overrides.defaults.compaction.block_retention` in the Tempo config, for example to `336h` for 14 days, and increase
  the Tempo data volume to match.

Keep the token check on the Collector's receivers while its HTTP port has a public domain, and keep Tempo's listen ports
and storage paths unchanged.

## Data

The stack creates a 20 GB **Tempo data** volume for traces. Grafana has its own 10 GB volume with its dashboards, users,
settings, and plugins. Wodby defines no backups or imports for these services.

## Limits

- Tempo runs as a single instance and is not scalable. It suits development environments and low to moderate trace
  volumes.
- Tempo's ports are private: query Tempo through Grafana or from another service in the app environment.
- The Collector can run several replicas with the default configuration. A tail-sampling configuration needs all spans
  of a trace on one replica, so keep one replica with it.

## Check that the services are ready

- Tempo: `/ready` on port `3200` answers when Tempo can accept requests.
- Collector: port `13133` answers `200` when every pipeline has started.
- Send a test request to the Collector domain with the token: a `POST` of `{}` with `Content-Type: application/json` to
  `https://<Collector domain>/v1/traces` returns `200`.
