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
- per app environment as an override

### Resources management

App services can define resource requests and limits, following the same model as [Kubernetes container resources](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

Resource limits help contain bursty workloads so they do not affect other workloads on the same cluster. Resource requests help Kubernetes schedule pods correctly and also matter for both pod autoscaling and [cluster autoscaling](../clusters/scalability.md).

CPU requests and limits are specified in millicores, where `1000` millicores equals 1 CPU core. Memory requests and limits are specified in mebibytes, where `1024` MiB is roughly 1 GiB.

You can define resources at:

- service level, as defaults in the service manifest
- stack level
- app-service level

A container uses its service defaults unless its stack service or app service sets resources for it. Resources set
for a container replace the service defaults as a whole: if you set only a memory request, the container gets no CPU
request and no limits.

App services can also request GPUs with **GPU devices**: a device name, such as `nvidia.com/gpu`, and the number of
GPUs for each replica. A count of `0` turns off the GPU request of the service's default configuration. App services
that request GPUs run on the cluster's [GPU node pool](../clusters/gpu.md).

#### Resource presets

A resource preset is a named set of CPU and memory values. Instead of typing the values, pick a preset from **Preset**
in the resources dialog when you create an app, or on the **Resources** tab of an app service or a stack service.
Picking a preset fills in its values and clears the ones it doesn't set. You can still change any value afterwards.
The **Preset** column shows which preset a container's values match.

Choosing a preset copies its values. Wodby doesn't keep a link to the preset, so changing or deleting a preset later
doesn't change any service that used it.

Wodby provides these presets. They set requests only, so containers can use spare CPU and memory on the node:

| Preset    | Requested CPU | Requested memory |
|-----------|---------------|------------------|
| `nano`    | 10m           | 32 MiB           |
| `micro`   | 20m           | 64 MiB           |
| `small`   | 50m           | 128 MiB          |
| `medium`  | 100m          | 256 MiB          |
| `large`   | 250m          | 512 MiB          |
| `xlarge`  | 500m          | 1024 MiB         |
| `2xlarge` | 1000m         | 2048 MiB         |

Wodby's presets never change. A new size gets a new name.

Your organization can add its own presets in **Resource presets** in the organization menu. Every member can view them
and use them. Organization owners and admins create, edit and delete them. A custom preset can set any of the four
values: requested CPU and memory, and CPU and memory limits. CPU values are multiples of `10` millicores and memory
values are multiples of `16` MiB. For example, a preset for Java services can add a memory limit, because the JVM sizes
its memory from the limit. A custom preset can't use the name of a Wodby preset.

Service and stack manifests can name a Wodby preset in `resources.preset`, and override any of its values:

```yaml
resources:
  preset: medium
  limit:
    memory: 1024
```

See the
[service template](../services/template.md#resources-object) and the
[stack template](../stacks/template.md). The API, the [CLI](../dev/cli.md) and the
[MCP tools](../dev/mcp/tools.md) accept the name of a Wodby preset or of a custom preset of your organization.

#### Clearing resources when creating an app

When you create an app, the icons under `TOTAL` in the services table reset all services to the stack's defaults or
clear their resources. You can also clear the values of one service in its resources dialog.

A cleared service reserves nothing and has no limit. It is the first to suffer when a node runs short of memory or CPU.
Clearing all services also turns off their autoscaling, because autoscaling needs a CPU request.

### Cluster capacity

When you create an app or an app environment on an existing cluster, Wodby adds up the resource requests of its enabled
services and compares them with what the cluster can offer: the capacity free now, plus any nodes it can still add.

- **It can't fit:** Wodby refuses to create the environment and shows both amounts. This also applies when one replica
  of a service is larger than a node. Lower the resources, choose a larger cluster, or
  [scale the cluster](../clusters/scalability.md).
- **It may not fit:** you see a warning and can continue. This happens when the environment fits only if the cluster adds
  nodes, or when Wodby can't read the cluster's current usage. The deployment fails if there is no room for it.

The same refusal applies when you create an environment through the API, the CLI, or an agent.

A check that passes doesn't guarantee a deployment:

- Services that define no resource requests count as nothing, even though they use resources.
- Enough capacity in total can still be split across nodes so that a replica doesn't fit on any one of them.
- Only creating an environment is checked. Enabling a service or raising its resources later isn't.

## Autoscaling rules

Autoscaling requires an active paid subscription. Manual replica scaling remains available on all active plans. If
your current subscription does not include autoscaling, you cannot enable or increase a rule, but you can turn an
existing rule off.

When creating an app, you can define autoscaling rules for supported services. You can change the rule later from
**Apps > your app > your environment > Stack > App services > your service > Configuration > General**.

Turn **Autoscaling** on to reveal:

- **Requested CPU** for the primary container, in millicores
- **Minimum replicas**
- **Maximum replicas**
- **Avg. CPU utilization**, as a percentage of requested CPU

**Requested CPU** must be at least `100` millicores. If the primary container already has a CPU request, the field is
pre-filled with that value. Changing it here updates the same app-service resource override shown on the
**Resources** tab before Wodby enables the autoscaling rule.

While autoscaling is on, the manual **Replicas** field is disabled. Wodby controls the replica count between the
configured minimum and maximum, using the minimum as the baseline. Turn **Autoscaling** off to clear the saved rule
and manage **Replicas** manually again.

The dashboard offers new autoscaling configuration only for eligible top-level, non-external services whose service
revision supports horizontal scaling. If an existing rule becomes ineligible, its configuration remains visible so
you can turn it off, but its settings cannot be increased. The API rejects enabling autoscaling for other services.

The current autoscaling signal is average CPU utilization. The target is expressed as a percentage of the configured
CPU request. For example, if a service has a CPU request of `2000` millicores and an autoscaling target of `50%`,
scaling starts when average CPU usage reaches `1000` millicores.

The replica range works as follows:

- the minimum replica count is the baseline when CPU usage stays below the target
- the maximum replica count is the upper limit autoscaling can grow to

The autoscaling controls remain available when the app service is disabled. Disabling an app service preserves its
autoscaling rule for a future re-enable; it does not turn autoscaling off or remove the service as a
[subscription downgrade](../pricing.md#downgrading-a-paid-subscription) blocker. To remove the rule, open the disabled
service's **Configuration > General** page, turn **Autoscaling** off, and select **Update**.

## Vertical scaling

Wodby does not currently configure automatic vertical pod autoscaling. Adjust CPU and memory requests and limits
manually at the stack or app-service level, then deploy the updated configuration. Use metrics to review actual usage
before changing requests or limits.
