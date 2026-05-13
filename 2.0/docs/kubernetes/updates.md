# Kubernetes cluster updates

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes available and the cluster is marked as outdated. You can then upgrade the infrastructure app instance to that stack revision manually.

Infrastructure auto-updates are not available today.

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Coming soon...
