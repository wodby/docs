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

### Persistent storage

Coming soon...

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
