---
description: Scale the worker capacity of a managed Kubernetes cluster in Wodby with minimum and maximum node counts and autoscaling.
---

# Cluster scalability

## Manual scaling

For [managed Kubernetes](managed.md) clusters, you can scale worker capacity manually from
`Clusters > [Cluster] > Infrastructure > Kubernetes`.

You can set:

- minimum node count
- maximum node count

A [GPU node pool](gpu.md) has its own minimum and maximum node counts, set on the same page.

Existing [single-node clusters](managed.md#single-node-clusters) cannot be scaled or changed into scalable clusters.
They always have one node, and the dashboard does not show scaling controls for them. New single-node clusters are no
longer available; create a cluster with minimum and maximum node counts instead.

## Autoscaling

Managed Kubernetes providers usually support a cluster autoscaler. You configure the minimum and maximum number of worker nodes, and the autoscaler adds or removes nodes as needed.

In practice, cluster autoscaling reacts more to total scheduled demand than to raw node metrics alone. The key input is the total amount of CPU and memory [requested](../apps/scalability.md#resources-management) by your workloads compared with the capacity available on worker nodes.

This means app-level pod autoscaling and cluster autoscaling work together:

- pod autoscaling increases replicas based on workload metrics such as average CPU utilization
- more replicas increase total requested resources
- if the cluster no longer has enough capacity, the cluster autoscaler adds nodes

Downscaling follows the reverse pattern. When workload demand falls, pod autoscaling reduces replicas. If the remaining requested resources fit on fewer nodes, the cluster autoscaler can remove nodes again.
