# Service Helm integration

We use [Helm](https://helm.sh/) to deploy non-external services to Kubernetes. Such services must provide basic Helm configuration specifying repository source, chart name, chart version. Additionally, a service must provide Helm configuration that specifies yaml path to Helm values that will allow addition of Kubernetes configuration such as:

- annotations
- labels
- environment variables
- resources
- sidecars
- volumes
- bind mounts

On top of that we expect the Helm chart to support the following values:

- `replicas` or `replicaCount` for scalability
- `fullnameOverride` to override hostnames
- `pullPolicy`
- `autoscaling`
- `image.repository`, `image.tag`, `image.registry`, `image.pullSecrets`
- `command`
- `args`

If you're creating a custom Helm chart we recommend to fork one of existing [charts by Wodby](https://github.com/wodby/charts) or [by Bitnami](https://github.com/bitnami/charts)
