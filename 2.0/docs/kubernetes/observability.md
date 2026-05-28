# Kubernetes Cluster Monitoring

As part of the cluster [infrastructure apps](infrastructure.md), Wodby deploys components that collect metrics from cluster nodes and Kubernetes resources.

You can view live metrics from `[Kubernetes cluster] > Metrics` in the dashboard.

Tracked metrics include:

- CPU usage
- Memory usage
- CPU capacity (total amount of [requested CPU](../apps/scalability.md#resources-management))
- Memory capacity (total amount of [requested memory](../apps/scalability.md#resources-management))
- persistent volume storage usage and capacity per namespace
- pod limit per node
- node disk usage
- node inode usage

Namespace metrics include CPU, memory, pod and container readiness, restart totals, and PVC storage usage where
Kubernetes exposes kubelet volume stats for matching persistent volume claims.
