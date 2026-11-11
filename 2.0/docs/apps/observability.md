---
description: Monitor Wodby applications with metrics for clusters, environments, services and pods, view logs, and add an OpenTelemetry Collector to a stack.
---

# Application Observability

## Monitoring

### Kubernetes resources monitoring

When cluster monitoring is enabled, Wodby collects metrics at several levels:

- Kubernetes cluster and node metrics
- Kubernetes namespace metrics
- app environment runtime metrics
- app service runtime metrics
- pod and container runtime metrics

Cluster-level metrics are shown from `Clusters > [Cluster] > Metrics`.

That page also includes namespace-level usage details, including namespace type, related app environment, pod and
container counts, restart totals, CPU and memory usage, and persistent volume storage usage per namespace.

### Monitoring with third-party service

You can also monitor your app with third-party services. For example, you can attach a [New Relic integration](../providers/newrelic.md).

## Logging

### Live logs

For a deployed app environment, you can stream live container logs from `Apps > [App] > [Environment] > Logs`. Live logs
remain available while a deployment is in progress, including as pods are added or replaced during a rollout.

You choose the app service first. If that service exposes more than one workload or container, you can select the
target explicitly. Otherwise Wodby uses the primary workload and its first container automatically.

Live logs follow the selected container across all current replicas by default, including replicas added while the
stream is open. When a workload has multiple pods, you can keep **All replicas** selected or narrow the stream to one
pod. All-replica streams prefix every line with its pod name so interleaved messages remain attributable to the replica
that produced them. A stream narrowed to one pod does not add that prefix.

If a selected pod is replaced, its stream stops instead of silently switching to the replacement pod. Choose the new
pod or switch back to **All replicas** to continue following the workload through scaling and rolling updates.

Logs for deployments, builds, cron jobs, and actions are available in the related tasks.

### Persistent log storage

Wodby streams container logs but does not retain them as searchable historical application logs. Use a logging service
or cluster-level log collector when you need long-term retention, search, or alerting for container output.

Task-step logs are stored separately and remain available from the related deployment, build, cron, action, or other
task. Task logs are an operation history; they are not a persistent copy of the application's container logs.

## Metrics

App environment metrics are available from `Apps > [App] > [Environment] > Metrics`.

That page shows:

- CPU and memory usage
- CPU and memory requests and limits
- persistent volume storage usage and capacity for the app environment namespace
- pod and container readiness
- restart counts
- Kubernetes workload summaries for the environment, including service-level storage usage where available

App service metrics are available from `Apps > [App] > [Environment] > Stack > App services > [Service] > Metrics`.

That page shows:

- aggregated CPU and memory usage for the service
- persistent volume storage usage and capacity for volumes associated with the service
- pod readiness
- per-pod and per-container metrics such as requests, limits, restarts, node placement, and lifecycle timestamps

Storage metrics come from Kubernetes PVC stats. They are available at app environment, app service, and namespace levels.
Per-pod and per-container tables do not show separate storage usage because PVC usage is reported for volumes rather
than individual containers.

If cluster monitoring is disabled, app environment and app-service metrics pages are not available.

## OpenTelemetry Collector in application stacks

The catalog stacks for application runtimes include an OpenTelemetry Collector, disabled by default: ASP.NET Core,
Astro, Django, Drupal, FastAPI, Flask, Go, Java, Kotlin, Laravel, Next.js, Node.js, Nuxt, PHP, Python, Rails, Ruby,
Rust, Spring Boot, Strapi, SvelteKit, Symfony, TanStack Start, and WordPress. The Collector runs in the same app
environment as your application and has no public domain. It forwards traces, metrics, and logs to the destinations
its links name: usually the Collector of an [Observability](../stacks/catalog/observability/index.md) app, or a hosted
OpenTelemetry backend.

### See your application's telemetry in Grafana

The Collector in your app only forwards data. To store and view it, send it to an app created from the
[Observability](../stacks/catalog/observability/index.md) stack, which has Grafana. One Observability app can collect
data from many apps and environments.

1. Create an app from the Observability stack. See [Creating New Application](index.md#creating-new-application). On
   the same cluster as your app, data stays on the cluster's private network; on another cluster it goes to the
   Observability Collector's public domain.
2. In your app's environment, open the `otel-collector` app service, then `Connections > Links`. Set **Upstream** to
   the Collector of the Observability app, listed with the other apps you can link to. See
   [Links tab](services.md#links-tab).
3. Under `Configuration > General`, enable the service, then deploy the app environment so your application gets the
   variables below.
4. Add an OpenTelemetry SDK or agent to your code and set `OTEL_SERVICE_NAME`, for example to the app and environment
   name. See [What your application gets](#what-your-application-gets).
5. Open the Observability app's Grafana and find the data in `Explore`. See
   [View telemetry in Grafana](../stacks/catalog/observability/index.md#view-telemetry-in-grafana).

Repeat steps 2 and 3 in each environment you want to see. Environments created before the stack included the Collector
get it with a [stack upgrade](stack.md#upgrade).

### Destinations

The Collector has four links. At least one must be set before the Collector can be enabled, so set its links first.

| Link | Sends | Can point at |
| --- | --- | --- |
| **Upstream** | Every signal, unless one of the links below is set | A Collector, or a custom target |
| **Traces** | Traces | A Collector, Grafana Tempo, or a custom target |
| **Metrics** | Metrics | A Collector, VictoriaMetrics, or a custom target |
| **Logs** | Logs | A Collector, Grafana Loki, or a custom target |

A signal with no destination is dropped. For a hosted backend, choose **Custom** and enter its OTLP/HTTP base URL,
without a path, and the `Authorization` header it expects, for example `Bearer <key>`. Backends that need another
header name are not supported by these fields; edit the **Collector config** under `Configuration > Configs` instead.

Use **Traces**, **Metrics**, or **Logs** to split signals, for example traces to a hosted backend and logs to your
Observability app. The Collector of a [Grafana Tempo](../stacks/catalog/tempo/index.md),
[Grafana Loki](../stacks/catalog/loki/index.md), or [VictoriaMetrics](../stacks/catalog/victoria-metrics/index.md) app
accepts only its own signal, so link it with the matching link, not with **Upstream**.

### What your application gets

While the Collector is enabled, the application service, and worker services such as Celery or Sidekiq, get the standard
OpenTelemetry SDK variables:

| Variable | Value |
| --- | --- |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://otel-collector:4318` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | `http/protobuf` |
| `OTEL_EXPORTER_OTLP_HEADERS` | The Collector's ingest token, as a secret |

Wodby does not instrument your code. Add an OpenTelemetry SDK or agent for your language that reads these variables,
and set `OTEL_SERVICE_NAME` to name the application in traces. While the Collector is disabled, the variables are
absent, so start the instrumentation only when `OTEL_EXPORTER_OTLP_ENDPOINT` is set.

### PHP applications

In the PHP, Laravel, Symfony, WordPress, and Drupal stacks, the PHP service also gets `OTEL_PHP_AUTOLOAD_ENABLED=true`
while the Collector is enabled. The OpenTelemetry PHP extension is already in the image. Add the SDK, the OTLP
exporter, and an HTTP client to your project with Composer:

```bash
composer require open-telemetry/sdk open-telemetry/exporter-otlp php-http/guzzle7-adapter
```

The SDK then sets itself up from the variables when your application loads Composer's autoloader, with no code
changes. Add instrumentation packages for what you want to trace, for example
`open-telemetry/opentelemetry-auto-laravel`, `open-telemetry/opentelemetry-auto-symfony`,
`open-telemetry/opentelemetry-auto-wordpress`, or `open-telemetry/opentelemetry-auto-pdo` for database queries.
While the Collector is disabled, the variables are absent and the SDK stays off.
