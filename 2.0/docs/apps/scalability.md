# Applications Scalability

Before scaling your application, make sure you have a [Kubernetes cluster](../kubernetes/index.md) that is capable of [scaling](../kubernetes/scalability.md). The most flexible scalability offered by a [managed Kubernetes cluster](../kubernetes/managed.md) that is capable of scaling nodes dynamically using cluster autoscaler. If you are using a [K3S cluster](../kubernetes/k3s.md), you will be limited by the number of nodes you connect to your K3S cluster.

## Manual scaling

You can manually scale number of replicas of your app services. All stateless services can be scaled up and down, but stateful services need to support scalability (usually achieved by increasing read replicas). You can set up number of replicas in your stack configuration or do it individually per app instance.

### Resources management

App services may have resources request and limits (the [same way as in Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)).

Although it's not mandatory to set up resources for your app services, we recommend to do so. Resources limits are useful to limit burstable workloads and their effect on other resources on the same cluster. Resources request help your cluster to schedule and distribute workloads across the nodes by [autoscaling](scalability.md) pods and also [scale the Kubernetes cluster](../kubernetes/scalability.md).

CPU request and limits specified in milicores where 1000 milicores equal to 1 CPU core. Memory requests and limits specified in mebibytes where 1024 mebibytes equal to 1 GB.

Resources request and usage can be done on different levels:

- Stack level (via template or UI)
- App service level

## Autoscaling rules

To enable autoscaling for your app, you need to define autoscaling rules when you create an app. Currently, the only autoscaling option is for average CPU consumption (hence it requires specifying [CPU request](resources.md)), when average CPU utilization reaches % of specified request, the number of pod replicas will be increased by 1, e.g. if you specified `2000 milicores` (2 CPUs) with average utilization of `50%`, then the scaling will happen when the CPU utilization for the service reaches `1000 milicores`. 

You can specify minimum and maximum number of replicas for autoscaling. The minimum number of replicas is the number of replicas that will be used when the CPU consumption is below the defined threshold. The maximum number of replicas is the number of replicas that will be used when the CPU consumption is above the defined threshold.

## Vertical scaling

Coming soon...
