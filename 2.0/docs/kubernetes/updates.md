# Kubernetes cluster updates

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes available and the cluster is marked as outdated. You can then upgrade the infrastructure app instance to that stack revision manually.

Infrastructure auto-updates are not available today.

## Infrastructure version upgrades

Some changes affect the cluster-level infrastructure version rather than only an infrastructure app stack revision.
These upgrades can change how Wodby wires cluster networking, routing, or platform controllers.

See [Kubernetes cluster infrastructure](infrastructure.md#infrastructure-versions) for infrastructure version details,
the changelog, current versions, and cluster-type-specific upgrade behavior.

Run K3S infrastructure version upgrades during a maintenance window for production workloads, because pod networking can
be briefly interrupted while K3S restarts and Cilium takes over.

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Coming soon...
