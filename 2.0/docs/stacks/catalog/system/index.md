---
description: The Kubernetes system stacks that Wodby deploys as infrastructure apps to operate a cluster. Which ones run depends on the provider and features.
---

# Kubernetes system stacks

Wodby deploys these stacks as [infrastructure apps](../../../clusters/infrastructure.md) that operate a cluster. You
don't create apps from them. Which ones a cluster runs depends on its provider and selected infrastructure features.

| Stack | What it does | Source |
| --- | --- | --- |
| Envoy Gateway | Provides the Kubernetes Gateway API and ingress control plane for clusters that use Envoy Gateway | [stack-envoy-gateway](https://github.com/wodby/stack-envoy-gateway) |
| Monitoring | Provides node, workload and Kubernetes object telemetry for cluster observability | [stack-monitoring](https://github.com/wodby/stack-monitoring) |
| Metrics | Provides Kubernetes resource and object-state metrics for cluster operations | [stack-metrics](https://github.com/wodby/stack-metrics) |
| AWS LB Controller | Connects clusters that need it to AWS load balancers | [stack-aws-lb-controller](https://github.com/wodby/stack-aws-lb-controller) |
| FRPC | Provides tunneling for cluster networking configurations that need an FRP client | [stack-frpc](https://github.com/wodby/stack-frpc) |

To update them, see [Kubernetes cluster updates](../../../clusters/updates.md). To view the metrics they collect, see
[cluster observability](../../../clusters/observability.md).

The FRPC stack is separate from the [FRP Server](../frps/index.md) application stack, which you deploy yourself for
workloads outside the cluster.
