# Kubernetes cluster monitoring

As the part of our [infrastructure apps](infrastructure.md) we deploy service to collect metrics from cluster nodes and kubernetes resources.

You can find the live metrics from our Dashboard: _"[Kubernetes cluster] > Metrics"_ page.

We track the following metrics:

- CPU usage
- Memory usage
- CPU capacity (total amount of [requested CPU](../apps/scalability.md#resources-management))
- Memory capacity (total amount of [requested memory](../apps/scalability.md#resources-management))
- Limit of pods per node
- Node's disk usage
- Node's inodes usage
