# Application Scalability

Before you scale an app, make sure the underlying [Kubernetes cluster](../clusters/index.md) can scale with it.

[Managed Kubernetes clusters](../clusters/managed.md) give you the most flexibility because they can scale worker nodes dynamically through a cluster autoscaler. With [K3S](../clusters/k3s.md), app scaling is limited by the number of servers you connect to the cluster.

## Manual scaling

You can scale the replica count of app services manually when the selected service revision supports horizontal
scaling. The service overview shows whether horizontal scaling is supported.

Stateless services can usually be scaled up and down directly. Stateful services need service-specific support for
scaling, for example through read replicas. A fixed service can be scaled to zero or run as a single replica, but it
cannot be configured with multiple replicas.

You can set replica counts:

- in the stack configuration as the default
- per app instance as an override

### Resources management

App services can define resource requests and limits, following the same model as [Kubernetes container resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

Resource limits help contain bursty workloads so they do not affect other workloads on the same cluster. Resource requests help Kubernetes schedule pods correctly and also matter for both pod autoscaling and [cluster autoscaling](../clusters/scalability.md).

CPU requests and limits are specified in millicores, where `1000` millicores equals 1 CPU core. Memory requests and limits are specified in mebibytes, where `1024` MiB is roughly 1 GiB.

You can define resources at:

- stack level
- app-service level

## Autoscaling rules

Autoscaling requires an active paid subscription. Manual replica scaling remains available on all active plans.

When creating an app, you can define autoscaling rules for supported services. You can change the rule later from
**Apps > your app > your instance > Services > your service > Configure**. Turn **Autoscaling** on to edit the CPU
target and replica range, or turn it off to clear the saved rule. The controls remain available when the app service is
disabled, so you do not need to re-enable or delete a service just to remove its autoscaling configuration.

The dashboard does not show autoscaling controls for fixed services, and the API rejects autoscaling settings for them.

The current autoscaling signal is average CPU utilization, so you must define a [CPU request](#resources-management) first.

The target is expressed as a percentage of the configured CPU request. For example, if a service has a CPU request of `2000` millicores and an autoscaling target of `50%`, scaling starts when average CPU usage reaches `1000` millicores.

You can also define minimum and maximum replica counts:

- the minimum replica count is the baseline when CPU usage stays below the target
- the maximum replica count is the upper limit autoscaling can grow to

Disabling an app service preserves its autoscaling rule for a future re-enable. It does not turn autoscaling off or
remove the service as a [subscription downgrade](../pricing.md#downgrading-a-paid-subscription) blocker. To remove the
rule, open the disabled service's **Configure** page, turn **Autoscaling** off, and select **Update**.

## Vertical scaling

Coming soon...
