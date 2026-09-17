# Clusters

Manage your clusters from `Clusters` in the dashboard. To create or connect your first cluster,
see [Choose a cluster option](choose-platform.md).

## Cluster environments

Every cluster has an [environment type](../apps/environment-types.md). This is a visual classification for the cluster itself; it does not
change Kubernetes configuration or automatically move workloads. Production clusters are marked in the Clusters list,
and you can filter the list by environment type.

When you create or edit a cluster, choose how app environments may use it:

- `Any environment type` allows non-infrastructure app environments of every type.
- `Restricted` allows only the environment types you select. The cluster's own type must be included.

Restrictions use the same fixed environment types used by app environments, integrations, databases, and backup
presets. Infrastructure apps that operate the cluster are not restricted by this setting. Wodby rejects a restriction
change if an existing app environment on the cluster would become disallowed.

Existing clusters are initially unrestricted. Their visual type is classified as `prod` when at least one
non-infrastructure `prod` app environment is deployed there; otherwise it is classified as `dev`.

## Manage a cluster

- [Monitor cluster health and resource usage](observability.md).
- [Scale cluster capacity](scalability.md).
- [Update infrastructure and infrastructure apps](updates.md).
- [Plan for high availability](high-availability.md).

## Related pages

- [Choose a cluster option](choose-platform.md)
- [Wodby Cloud](wodby-cloud.md)
- [K3S](k3s.md)
- [Cluster updates](updates.md)
- [App environments](../apps/environments.md)
- [Environment types](../apps/environment-types.md)
