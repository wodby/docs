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
- `image.pullSecrets`
- `image.pullPolicy`
- `autoscaling`
- `image.repository`, `image.tag`, `image.registry`
- `command`
- `args`

If a chart uses different paths, define them explicitly in the service manifest. This is common for charts that manage
multiple workloads, where each workload may have its own image values.

When a chart keeps the full image path inside one repository value and does not expose a separate registry field, set
`workloads[].containers[].helm.image.registry: ""`. This disables separate registry injection and makes Wodby write the
full repository path into the configured `repository` value instead.

During service import, Wodby validates explicit Helm value paths against the chart's merged values and schema when they
are available.

If you're creating a custom Helm chart, we recommend starting from one of the existing
[charts by Wodby](https://github.com/wodby/charts) or [by Bitnami](https://github.com/bitnami/charts).

Helm chart information and default Helm values are defined under the [`helm` section](template.md#helm) in a service
template.
