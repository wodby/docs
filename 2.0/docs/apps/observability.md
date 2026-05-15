# Application Observability

## Monitoring

### Kubernetes resources monitoring

When cluster monitoring is enabled, Wodby collects metrics at several levels:

- Kubernetes cluster and node metrics
- Kubernetes namespace metrics
- app instance runtime metrics
- app service runtime metrics
- pod and container runtime metrics

Cluster-level metrics are shown from `Kubernetes > [Cluster] > Metrics`.

That page also includes namespace-level usage details, including namespace type, related app instance, pod and
container counts, restart totals, and CPU and memory usage per namespace.

### Monitoring with third-party service

You can also monitor your app with third-party services. For example, you can attach a [New Relic integration](../providers/newrelic.md).

## Logging

### Live logs

For a successfully deployed app instance, you can stream live container logs from `Apps > [App] > [Instance] > Logs`.

You choose the app service first. If that service exposes more than one workload or container, you can select the
target explicitly. Otherwise Wodby uses the primary workload and its first container automatically.

Logs for deployments, builds, cron jobs, and actions are available in the related tasks.

### Persistent storage

Coming soon...

## Metrics

App instance metrics are available from `Apps > [App] > [Instance] > Metrics`.

That page shows:

- CPU and memory usage
- CPU and memory requests and limits
- pod and container readiness
- restart counts
- Kubernetes workload summaries for the instance

App service metrics are available from `Apps > [App] > [Instance] > Services > [Service] > Metrics`.

That page shows:

- aggregated CPU and memory usage for the service
- pod readiness
- per-pod and per-container metrics such as requests, limits, restarts, node placement, and lifecycle timestamps

If cluster monitoring is disabled, app-instance and app-service metrics pages are not available.
