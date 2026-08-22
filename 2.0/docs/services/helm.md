# Service Helm Integration

We use [Helm](https://helm.sh/) to deploy non-external services to Kubernetes.

A service's [`helm` section](template.md#helm) defines the chart source, chart name, version, and service-level Helm
paths such as image pull secrets. Workload- and container-specific Helm paths live under
[`workloads`](template.md#workloads). Together they tell Wodby where to inject Kubernetes-specific configuration such
as:

- annotations
- labels
- environment variables
- resources
- container images
- sidecars
- volumes
- bind mounts

Services can also define default Helm values in the template. Those values become part of the deployed configuration
and can be overridden later at stack or app level when needed.

`helm.values[].value` can use [built-in runtime tokens](../apps/tokens.md) and service-defined tokens.

For chart-managed configuration files, prefer using [`configs`](template.md#configs) with `configs[].helm` so Wodby
passes the resolved file content into the chart and the chart keeps ownership of the ConfigMap mount and rollout
logic. Use `configs[].filename` only when the chart explicitly expects the name of an existing ConfigMap instead of the
content itself. If the config needs Wodby tokens, enable `configs[].processTokens` explicitly.

Wodby works best with charts that expose common values such as:

- `replicas` or `replicaCount` for scalability
- `fullnameOverride` to override hostnames
- `serviceAccountName` or another value that sets `spec.template.spec.serviceAccountName`
- `image.pullSecrets`
- `image.pullPolicy`
- `strategy` or `updateStrategy`
- `minReadySeconds`
- `progressDeadlineSeconds`
- `terminationGracePeriodSeconds`
- `autoscaling`
- `image.repository`, `image.tag`, `image.registry`
- `command`
- `args`

If a chart uses different paths, define them explicitly in the service manifest. This is common for charts that manage
multiple workloads, where each workload may have its own image values.

## Backend-managed value mappings

Wodby injects several values that control the app service itself. The optional `helm.valueMappings` object maps those
settings to paths exposed by the chart. Existing service manifests remain compatible because every omitted mapping
uses its documented compatibility default:

| App-service setting | Default Helm value path |
| --- | --- |
| Replica count | Both `replicas` and `replicaCount` |
| Full resource-name override | `fullnameOverride` |
| Kubernetes service account name | `serviceAccountName` |
| Disable chart-owned service account creation | No default; configure `serviceAccountCreate` when needed |
| Rollout strategy | `strategy` for Deployments; `updateStrategy` for StatefulSets and DaemonSets |
| Minimum ready duration | `minReadySeconds` |
| Deployment progress deadline | `progressDeadlineSeconds` |
| Pod shutdown grace period | `terminationGracePeriodSeconds` |

Override only the paths that differ from these defaults. For example, a chart that nests its deployment values can
define:

```yaml
helm:
  name: example
  source: oci://registry.example.com/example
  chart: oci://registry.example.com/example
  version: 1.2.3
  valueMappings:
    replicas: workload.replicaCount
    fullnameOverride: workload.fullnameOverride
    serviceAccountName: serviceAccount.name
    serviceAccountCreate: serviceAccount.create
    strategy: workload.strategy
    minReady: workload.minReadySeconds
    progressDeadline: workload.progressDeadlineSeconds
    shutdownGracePeriod: workload.terminationGracePeriodSeconds
```

An explicit `replicas` mapping replaces both legacy replica aliases with the configured path. Each other property is
resolved independently, so a partial `valueMappings` object continues to use the defaults for omitted properties.
`serviceAccountCreate` has no default because not every chart creates a service account. When configured, Wodby sets it
to `false` whenever it supplies an annotated service account and points the workload at that account.

When an external database connection requires workload identity, `serviceAccountName` must be mapped explicitly in the
selected service revision. Wodby stops the deployment with a user-facing compatibility error before running Helm if
that mapping is absent. If assigning the mapped name makes the chart render its own ServiceAccount, the chart must also
map `serviceAccountCreate` so Wodby can disable that duplicate resource.

Wodby supplies the effective replica count on every deployment, including `0` while an app service is disabled or its
app instance is paused. A chart should therefore render `spec.replicas` from the mapped value for Deployments and
StatefulSets. Wodby does not enable chart autoscaling values. When autoscaling is configured, Wodby creates and
reconciles the HorizontalPodAutoscaler while the chart continues to render its ordinary replica value. A chart-owned
autoscaler must therefore remain disabled with the service manifest's Helm values. Wodby-maintained charts always
render `spec.replicas` and do not expose chart-owned autoscaling values.

Service-level `helm.values` are applied after the backend-managed defaults. Do not set the same paths there unless the
service intentionally replaces the backend-managed value. Replica overrides and explicit service-account mappings
that break the rendered workload contract are rejected by import validation.

When a chart keeps the full image path inside one repository value and does not expose a separate registry field, set
`workloads[].containers[].helm.image.registry: ""`. This disables separate registry injection and makes Wodby write the
full repository path into the configured `repository` value instead.

## Deployment value mappings

Deployment configuration is optional. Wodby writes only the fields configured by the service, stack, or app service;
an unset field remains absent from the generated Helm values so the chart can apply its own default.

For a service with one workload, the compatibility defaults are:

| Mapping | Deployment | StatefulSet | DaemonSet |
| --- | --- | --- | --- |
| `strategy` | `strategy` | `updateStrategy` | `updateStrategy` |
| `minReady` | `minReadySeconds` | `minReadySeconds` | `minReadySeconds` |
| `progressDeadline` | `progressDeadlineSeconds` | Not supported | Not supported |
| `shutdownGracePeriod` | `terminationGracePeriodSeconds` | `terminationGracePeriodSeconds` | `terminationGracePeriodSeconds` |

The configured `maxUnavailable` and `maxSurge` values are written below the strategy path as
`rollingUpdate.maxUnavailable` and `rollingUpdate.maxSurge`.

Override only paths that differ from these defaults:

```yaml
helm:
  valueMappings:
    strategy: controller.updateStrategy
    minReady: controller.minReadySeconds
    progressDeadline: controller.progressDeadlineSeconds
    shutdownGracePeriod: controller.terminationGracePeriodSeconds
```

Service-level deployment mappings are resolved only for a service with one workload. A chart that renders multiple
workloads must define each workload's paths explicitly:

```yaml
workloads:
  - name: server
    kind: deployment
    helm:
      strategy: server.strategy
      minReady: server.minReadySeconds
      progressDeadline: server.progressDeadlineSeconds
      shutdownGracePeriod: server.terminationGracePeriodSeconds
```

See [Deployment configuration](deployment.md) for the supported settings, strategies, workload kinds, and inheritance
rules.

## Import validation

During service import, Wodby validates explicit Helm value paths against the chart's merged values and schema when they
are available. It also renders the chart with the same backend-managed values used during deployment.

For the primary Deployment or StatefulSet, Wodby renders replica counts `0` and `1` and verifies that the matching
workload has the same `spec.replicas` value. Services marked as scalable are also rendered with `2` replicas and must
preserve that exact count. Fixed services may normalize values above one to a singleton. This semantic check detects
charts that accept a Helm value but do not use it, including charts that omit `spec.replicas` because autoscaling is
enabled by default. DaemonSets do not have a replica-count check.

Validation rejects any HorizontalPodAutoscaler rendered with the service manifest's Helm values. A chart may expose a
dormant autoscaling option, but Wodby does not enable it because app-service autoscaling is managed by the backend.

When `helm.valueMappings.serviceAccountName` is explicit, Wodby also renders a sentinel service account and verifies
that it reaches `spec.template.spec.serviceAccountName`. If `serviceAccountCreate` is configured, validation also
checks that setting it to `false` prevents the chart from rendering the backend-managed account. Build-image workloads
must similarly render the configured image pull secret; services without build-image workloads do not need that
capability. A chart-rendering failure during these checks fails the service import instead of skipping validation.

If you're creating a custom Helm chart, we recommend starting from one of the existing
[charts by Wodby](https://github.com/wodby/charts) or [by Bitnami](https://github.com/bitnami/charts). The
[`wodby/charts`](https://github.com/wodby/charts) repository contains public Wodby Helm charts and boilerplates for
stateful and stateless charts.

Helm chart information and default Helm values are defined under the [`helm` section](template.md#helm) in a service
template.

To generate a service manifest from an existing chart, see
[Create from a Helm chart](create.md#create-from-a-helm-chart).
