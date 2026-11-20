Source: https://wodby.com/docs/2.0/stacks/catalog/system/

# Kubernetes system stacks

Wodby deploys these stacks as [infrastructure apps](https://wodby.com/docs/2.0/clusters/infrastructure/) that operate a cluster. You
don't create apps from them. Which ones a cluster runs depends on its provider and selected infrastructure features.

| Stack | What it does | Source |
| --- | --- | --- |
| Envoy Gateway | Provides the Kubernetes Gateway API and ingress control plane for clusters that use Envoy Gateway | [stack-envoy-gateway](https://github.com/wodby/stack-envoy-gateway) |
| Monitoring | Provides node, workload and Kubernetes object telemetry for cluster observability | [stack-monitoring](https://github.com/wodby/stack-monitoring) |
| Metrics | Provides Kubernetes resource and object-state metrics for cluster operations | [stack-metrics](https://github.com/wodby/stack-metrics) |
| AWS LB Controller | Connects clusters that need it to AWS load balancers | [stack-aws-lb-controller](https://github.com/wodby/stack-aws-lb-controller) |
| FRPC | Provides tunneling for cluster networking configurations that need an FRP client | [stack-frpc](https://github.com/wodby/stack-frpc) |

To update them, see [Cluster updates](https://wodby.com/docs/2.0/clusters/updates/). To view the metrics they collect, see
[cluster observability](https://wodby.com/docs/2.0/clusters/observability/).

The FRPC stack is separate from the [FRP Server](https://wodby.com/docs/2.0/stacks/catalog/frps/) application stack, which you deploy yourself for
workloads outside the cluster.
