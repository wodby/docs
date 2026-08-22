# Deployment configuration

Deployment configuration controls how Kubernetes replaces pods during an update, how long a new pod must stay ready,
and how long a terminating pod has to shut down. Service authors can provide defaults, stack authors can override them
for every app created from a stack, and app operators can tune one app service without changing the stack.

Wodby passes only configured deployment settings to Helm. If a setting is not configured at any level, the chart keeps
its own default. Deployment configuration is not available for external services.

## Configure deployment behavior

For a stack service, open
`Stack > Stack services > [Service] > Configuration > Deployment`. Changes are saved to the stack draft and take effect
after the draft is published and an app is created or upgraded to that stack revision.

For one app service, open
`Apps > [App] > [Instance] > Stack > App services > [Service] > Configuration > Deployment`. Saving an override marks
the app instance as needing redeploy.

Use `All workloads` for service-wide settings. Services with multiple workloads also show a card for each workload, so
a setting can be overridden only for the workload that needs different behavior. Leaving a field empty inherits the
next applicable value; if no inherited value exists, the chart default is used.

## Inheritance and precedence

Each field is resolved independently. From lowest to highest precedence, the sources are:

1. service manifest `deployment`
2. service manifest `workloads[].deployment`
3. stack service `deployment`
4. stack service `workloads[].deployment`
5. app service `deployment`
6. app service workload override

For example, an app-level shutdown grace period can coexist with a workload-specific rolling-update limit inherited
from the service manifest.

## Settings

| Setting | Purpose | Supported workload kinds |
| --- | --- | --- |
| `strategy` | Selects how Kubernetes updates the workload | Deployment, StatefulSet, DaemonSet |
| `maxUnavailable` | Maximum unavailable pods during a rolling update | Deployment, StatefulSet, DaemonSet |
| `maxSurge` | Maximum extra pods during a rolling update | Deployment, DaemonSet |
| `minReady` | Time a pod must remain ready before it is considered available | Deployment, StatefulSet, DaemonSet |
| `progressDeadline` | Maximum time a Deployment rollout may make no progress | Deployment |
| `shutdownGracePeriod` | Time Kubernetes gives containers to stop before forcefully terminating them | Deployment, StatefulSet, DaemonSet |

`maxUnavailable` and `maxSurge` accept a non-negative integer or a percentage from `0%` through `100%`. They apply only
to a rolling strategy and cannot both be zero. StatefulSets do not support `maxSurge`.

Durations use Go duration syntax, for example `10s`, `5m`, or `10m30s`, and must resolve to whole seconds.
`progressDeadline` must be greater than zero and, when `minReady` is also configured, greater than `minReady`.

### Strategies

| Manifest value | Kubernetes behavior | Supported workload kinds |
| --- | --- | --- |
| `rolling` | Gradually replaces old pods with new pods | Deployment, StatefulSet, DaemonSet |
| `recreate` | Stops all old pods before creating new pods | Deployment |
| `onDelete` | Replaces pods only when they are deleted manually | StatefulSet, DaemonSet |

## Service manifest defaults

Set defaults for a single-workload service at the top level:

```yaml
deployment:
  strategy: rolling
  maxUnavailable: 0
  maxSurge: 1
  minReady: 10s
  progressDeadline: 15m
  shutdownGracePeriod: 11m
```

For a service with multiple workloads, put workload-specific behavior under each workload:

```yaml
workloads:
  - name: web
    kind: deployment
    deployment:
      maxUnavailable: 0
      maxSurge: 1
      shutdownGracePeriod: 11m
  - name: worker
    kind: deployment
    deployment:
      shutdownGracePeriod: 2m
```

Stack manifests use the same fields under `services[].deployment` and `services[].workloads[].deployment`. See the
[stack template reference](../stacks/template.md#servicesdeployment).

## Helm chart integration

For a service with one workload, Wodby uses these default Helm paths:

| Setting | Deployment | StatefulSet | DaemonSet |
| --- | --- | --- | --- |
| `strategy` | `strategy` | `updateStrategy` | `updateStrategy` |
| `minReady` | `minReadySeconds` | `minReadySeconds` | `minReadySeconds` |
| `progressDeadline` | `progressDeadlineSeconds` | Not supported | Not supported |
| `shutdownGracePeriod` | `terminationGracePeriodSeconds` | `terminationGracePeriodSeconds` | `terminationGracePeriodSeconds` |

`maxUnavailable` and `maxSurge` are written below the mapped strategy path as `rollingUpdate.maxUnavailable` and
`rollingUpdate.maxSurge`.

Charts with different paths can override `helm.valueMappings.strategy`, `minReady`, `progressDeadline`, and
`shutdownGracePeriod`. Charts with multiple workloads must define the corresponding mappings under each
`workloads[].helm` object. See [Service Helm Integration](helm.md#deployment-value-mappings) for examples.
