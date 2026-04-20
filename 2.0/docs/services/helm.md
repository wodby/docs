# Service Helm integration

We use [Helm](https://helm.sh/) to deploy non-external services to Kubernetes.

A service's [`helm` section](template.md#helm) defines the chart source, chart name, version, and the value paths Wodby
uses to inject Kubernetes-specific configuration such as:

- annotations
- labels
- environment variables
- resources
- sidecars
- volumes
- bind mounts

Services can also define default Helm values in the template. Those values become part of the deployed configuration
and can be overridden later at stack or app level when needed.

On top of that we expect the Helm chart to support the following values:

- `replicas` or `replicaCount` for scalability
- `fullnameOverride` to override hostnames
- `pullPolicy`
- `autoscaling`
- `image.repository`, `image.tag`, `image.registry`, `image.pullSecrets`
- `command`
- `args`

If you're creating a custom Helm chart, we recommend starting from one of the existing
[charts by Wodby](https://github.com/wodby/charts) or [by Bitnami](https://github.com/bitnami/charts).

Helm chart information and default Helm values are defined under the [`helm` section](template.md#helm) in a service
template.
