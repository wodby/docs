# Kubernetes Scalability

## Manual scaling

You can adjust the number of minimum nodes in the cluster for [managed Kubernetes](managed.md) clusters.

## Autoscaling

Usually, all cloud providers with [managed Kubernetes](managed.md) service deploy a cluster with autoscaler. You can set up maximum and minimum number of nodes in your cluster, and the autoscaler will automatically add or remove nodes based on the resource usage. This is a great way to ensure that your cluster is always running at optimal capacity, without having to manually manage the number of nodes.

However, the resources usage is not the real usage that a cluster receives from the metrics, it's rather a total amount of CPU and memory [resources requested](../apps/scalability.md#resources-management) by your app services and the total amount of said resources across the worker nodes. The requested resources together with pod autoscaling rules may increase the number of pod replicas running based on the actual metrics (e.g. average CPU load), this in its turn, will increase the total amount of requested resource which will trigger the cluster autoscaling if nodes do not pose enough of it. 

The downscaling works the similar way – once the CPU load is below the defined threshold, the number of pod replicas will be decreased, and if the total requested resources are below the minimum threshold, the cluster autoscaler will remove nodes from the cluster.
