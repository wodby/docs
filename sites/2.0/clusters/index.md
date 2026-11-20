Source: https://wodby.com/docs/2.0/clusters/

# Clusters

Manage your clusters from `Clusters` in the dashboard. To create or connect your first cluster,
see [Choose a cluster option](https://wodby.com/docs/2.0/clusters/choose-platform/).

## Cluster environments

Every cluster has an [environment type](https://wodby.com/docs/2.0/apps/environment-types/). This is a visual classification for the cluster itself; it does not
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

- [Monitor cluster health and resource usage](https://wodby.com/docs/2.0/clusters/observability/).
- See the cluster's nodes and their resources: [managed clusters](https://wodby.com/docs/2.0/clusters/managed/#nodes), [K3s](https://wodby.com/docs/2.0/clusters/k3s/#worker-nodes).
- [See the cluster's volumes and storage classes](https://wodby.com/docs/2.0/clusters/storage/).
- [Scale cluster capacity](https://wodby.com/docs/2.0/clusters/scalability/).
- [Update infrastructure and infrastructure apps](https://wodby.com/docs/2.0/clusters/updates/).
- [Update the Kubernetes version, cluster components and worker nodes](https://wodby.com/docs/2.0/clusters/kubernetes/).
- [Plan for high availability](https://wodby.com/docs/2.0/clusters/high-availability/).

## Related pages

- [Choose a cluster option](https://wodby.com/docs/2.0/clusters/choose-platform/)
- [Wodby Cloud](https://wodby.com/docs/2.0/clusters/wodby-cloud/)
- [K3s](https://wodby.com/docs/2.0/clusters/k3s/)
- [Cluster updates](https://wodby.com/docs/2.0/clusters/updates/)
- [Kubernetes updates and node operations](https://wodby.com/docs/2.0/clusters/kubernetes/)
- [App environments](https://wodby.com/docs/2.0/apps/environments/)
- [Environment types](https://wodby.com/docs/2.0/apps/environment-types/)
