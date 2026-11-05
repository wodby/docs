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
environment as your application and has no public domain. It forwards traces, metrics, and logs to an OTLP endpoint
you choose, such as the Collector of an [Observability](../stacks/catalog/observability/index.md),
[Grafana Tempo](../stacks/catalog/tempo/index.md), [Grafana Loki](../stacks/catalog/loki/index.md), or
[VictoriaMetrics](../stacks/catalog/victoria-metrics/index.md) app, or another OpenTelemetry backend.

### See your application's telemetry in Grafana

The Collector in your app only forwards data. To store and view it, send it to an app created from the
[Observability](../stacks/catalog/observability/index.md) stack, which has Grafana. One Observability app can collect
data from many apps and environments.

#### 1. Create the Observability app

1. Create an app from the Observability stack, on any cluster. See
   [Creating New Application](index.md#creating-new-application).
2. In its environment, open `Endpoints > Domains` and copy the domain of the `otel-collector` app service.
3. Open the `otel-collector` app service, then `Configuration > Tokens`, and reveal `ingest_token`. See
   [Tokens](tokens.md).

#### 2. Turn on the Collector in your app

1. In your app's environment, open the `otel-collector` app service. Under `Configuration > Settings`, set:
    - **Upstream OTLP endpoint**: `https://<Collector domain>` from step 1, without a path.
    - **Upstream Authorization header**: `Bearer <ingest token>` from step 1. It is stored as a secret.
2. Under `Configuration > General`, enable the service. You can also enable it and set its settings when you create the
   app.
3. Deploy the app environment, so your application gets the variables described below.

Repeat these steps in each environment you want to see. The Collector does not start until the upstream endpoint is set.
Environments created before the stack included the Collector get it with a [stack upgrade](stack.md#upgrade).

#### 3. Instrument your application

Wodby sets the variables, but your code must send the data. Add an OpenTelemetry SDK or agent for your language and set
`OTEL_SERVICE_NAME`, for example to the app and environment name. See
[What your application gets](#what-your-application-gets) and, for PHP, [PHP applications](#php-applications). Build
and deploy the application.

#### 4. Open Grafana

1. In the Observability app's environment, open `Endpoints > Domains` and open the `grafana` domain.
2. Sign in with `admin_username` and `admin_password` from the `grafana` app service's `Configuration > Tokens` tab.
3. Open `Explore`. Choose the Tempo data source for traces, Loki for logs, or VictoriaMetrics for metrics, and filter by
   your service name. See
   [View telemetry in Grafana](../stacks/catalog/observability/index.md#view-telemetry-in-grafana).

You can also send data to another OpenTelemetry backend. Set its OTLP/HTTP base URL and the `Authorization` header it
expects in the same two settings.

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

### Choose what to forward

The Collector forwards traces, metrics, and logs to the same endpoint. The Collector of a Wodby Observability app
accepts all three. The Collector of a Wodby Grafana Tempo app accepts only traces, Grafana Loki only logs, and
VictoriaMetrics only metrics. Data the upstream refuses is dropped, and the Collector logs `Exporting failed`. Either
turn off the other signals in your application, for example `OTEL_METRICS_EXPORTER=none` and
`OTEL_LOGS_EXPORTER=none` when forwarding to Tempo, or edit the **Collector config** under `Configuration > Configs` to
remove pipelines or add an exporter per destination. Deploy the service after a config change. See
[Configs tab](services.md#configs-tab).
