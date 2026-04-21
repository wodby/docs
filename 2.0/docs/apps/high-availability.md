# Application High Availability

High availability depends on more than one layer. To make an app highly available, look at the cluster, the app services themselves, and the storage they depend on.

## [Kubernetes cluster high availability](../kubernetes/high-availability.md)

Start with the cluster. A common baseline is:

- at least two worker nodes
- nodes spread across at least two availability zones when the provider supports that
- a highly available control plane, which is often included by default or offered as an option

## Stateless app services

Stateless app services are usually the easiest part of HA. In practice, you normally want at least two replicas so one pod can continue serving traffic if another fails.

## Stateful app services

Stateful services need service-specific HA support. Single-node and highly available deployments often differ significantly in architecture, operational complexity, and required resources.

For some stateful components, it can be simpler to rely on managed services such as [managed databases](../databases/managed.md).

## Distributed storage

Not every distributed storage system is highly available by itself. If your app depends on shared storage, make sure the storage layer also meets your HA requirements.

In some cases, a managed distributed-storage service such as AWS EFS is a better HA fit than a container-based storage service inside the cluster.
