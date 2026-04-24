# Application Observability

## Monitoring

### Kubernetes resources monitoring

Wodby currently collects Kubernetes metrics at the node level. More detailed metrics for app instances are planned for a future release.

### Monitoring with third-party service

You can also monitor your app with third-party services. For example, you can attach a [New Relic integration](../providers/newrelic.md).

## Logging

### Live logs

For a successfully deployed app, you can stream live container logs from `Apps > [App] > Logs`.

If a service exposes more than one workload or container, you can select the target explicitly. Otherwise Wodby uses
the primary workload and its first container automatically.

Logs for deployments, builds, cron jobs, and actions are available in the related tasks.

### Persistent storage

Coming soon...

## Metrics

Service-level metrics are coming soon...
