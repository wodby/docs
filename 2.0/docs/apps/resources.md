# Resources management

App services may have resources request and limits (the [same way as in Kubernetes](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/)).

Although it's not mandatory to set up resources for your app services, we recommend to do so. Resources limits are useful to limit burstable workloads and their effect on other resources on the same cluster. Resources request help your cluster to schedule and distribute workloads across the nodes by [autoscaling](scalability.md) pods and also [scale the Kubernetes cluster](../kubernetes/scalability.md). 

CPU request and limits specified in milicores where 1000 milicores equal to 1 CPU core. Memory requests and limits specified in mebibytes where 1024 mebibytes equal to 1 GB.

Resources request and usage can be done on different levels:

- Stack level (via template or UI)
- App service level
