# Kubernetes cluster updates

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes available and the cluster is marked as outdated. You can then upgrade the infrastructure app instance to that stack revision manually.

Infrastructure auto-updates are not available today.

## Infrastructure version upgrades

Some changes affect the cluster-level infrastructure version rather than only an infrastructure app stack revision.
These upgrades can change how Wodby wires cluster networking, routing, or platform controllers.

Wodby marks a cluster as outdated only when there is an applicable upgrade for that cluster type. For example,
infrastructure version `3.0.0` is a K3S-specific upgrade that replaces the default K3S flannel/kube-router networking
setup with Cilium. Managed Kubernetes clusters on version `2.0.0` are not marked as outdated just because `3.0.0`
exists.

For K3S clusters, the upgrade from `2.0.0` to `3.0.0`:

- hardens public access to the K3S API endpoint
- restarts K3S with flannel disabled
- disables the built-in K3S network policy controller
- installs Cilium
- redeploys user applications so app instance network policies are applied

Run K3S infrastructure version upgrades during a maintenance window for production workloads, because pod networking can
be briefly interrupted while K3S restarts and Cilium takes over.

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Coming soon...
