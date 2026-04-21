# Kubernetes Scalability

## Manual scaling

For [managed Kubernetes](managed.md) clusters, you can adjust the minimum node count manually.

## Autoscaling

Managed Kubernetes providers usually support a cluster autoscaler. You configure the minimum and maximum number of worker nodes, and the autoscaler adds or removes nodes as needed.

In practice, cluster autoscaling reacts more to total scheduled demand than to raw node metrics alone. The key input is the total amount of CPU and memory [requested](../apps/scalability.md#resources-management) by your workloads compared with the capacity available on worker nodes.

This means app-level pod autoscaling and cluster autoscaling work together:

- pod autoscaling increases replicas based on workload metrics such as average CPU utilization
- more replicas increase total requested resources
- if the cluster no longer has enough capacity, the cluster autoscaler adds nodes

Downscaling follows the reverse pattern. When workload demand falls, pod autoscaling reduces replicas. If the remaining requested resources fit on fewer nodes, the cluster autoscaler can remove nodes again.
