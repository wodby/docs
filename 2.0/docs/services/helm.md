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
- `autoscaling`
- `image.repository`, `image.tag`, `image.registry`
- `command`
- `args`

If a chart uses different paths, define them explicitly in the service manifest. This is common for charts that manage
multiple workloads, where each workload may have its own image values.

## Backend-managed value mappings

Wodby injects several values that control the app service itself. The optional `helm.valueMappings` object maps those
settings to paths exposed by the chart. Existing service manifests remain compatible because every omitted mapping
uses the legacy default:

| App-service setting | Default Helm value path |
| --- | --- |
| Replica count | Both `replicas` and `replicaCount` |
| Full resource-name override | `fullnameOverride` |
| Kubernetes service account name | `serviceAccountName` |
| Autoscaling enabled | `autoscaling.enabled` |
| Autoscaling minimum replicas | `autoscaling.minReplicas` |
| Autoscaling maximum replicas | `autoscaling.maxReplicas` |
| Autoscaling target CPU utilization | `autoscaling.targetCPUUtilizationPercentage` |

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
    autoscaling:
      enabled: workload.autoscaling.enabled
      minReplicas: workload.autoscaling.minReplicas
      maxReplicas: workload.autoscaling.maxReplicas
      targetCPUUtilizationPercentage: workload.autoscaling.targetCPU
```

An explicit `replicas` mapping replaces both legacy replica aliases with the configured path. Each other property is
resolved independently, so a partial `valueMappings` object continues to use the defaults for omitted properties.

Wodby supplies the effective replica count on every deployment, including `0` while an app service is disabled or its
app instance is paused. A chart should therefore render `spec.replicas` from the mapped value for Deployments and
StatefulSets. Chart-managed autoscaling should default to disabled and should omit `spec.replicas` only when Wodby
explicitly enables autoscaling.

Service-level `helm.values` are applied after the backend-managed defaults. Do not set the same paths there unless the
service intentionally replaces the backend-managed value. Replica overrides and explicit service-account mappings
that break the rendered workload contract are rejected by import validation.

When a chart keeps the full image path inside one repository value and does not expose a separate registry field, set
`workloads[].containers[].helm.image.registry: ""`. This disables separate registry injection and makes Wodby write the
full repository path into the configured `repository` value instead.

## Import validation

During service import, Wodby validates explicit Helm value paths against the chart's merged values and schema when they
are available. It also renders the chart with the same backend-managed values used during deployment.

For the primary Deployment or StatefulSet, Wodby renders replica counts `0`, `1`, and `2` and verifies that the
matching workload has the same `spec.replicas` value. This semantic check detects charts that accept a Helm value but
do not use it, including charts that omit `spec.replicas` because autoscaling is enabled by default. DaemonSets do not
have a replica-count check.

When `helm.valueMappings.serviceAccountName` is explicit, Wodby also renders a sentinel service account and verifies
that it reaches `spec.template.spec.serviceAccountName`. A chart-rendering failure during these checks fails the service
import instead of skipping validation.

If you're creating a custom Helm chart, we recommend starting from one of the existing
[charts by Wodby](https://github.com/wodby/charts) or [by Bitnami](https://github.com/bitnami/charts). The
[`wodby/charts`](https://github.com/wodby/charts) repository contains public Wodby Helm charts and boilerplates for
stateful and stateless charts.

Helm chart information and default Helm values are defined under the [`helm` section](template.md#helm) in a service
template.

To generate a service manifest from an existing chart, see
[Create from a Helm chart](create.md#create-from-a-helm-chart).
