# Kubernetes cluster updates

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes
available and the cluster is marked as having outdated infrastructure apps. You can then upgrade the infrastructure app
instance to that stack revision manually, or let Wodby upgrade it automatically when automatic infrastructure upgrades
are enabled.

Infrastructure app updates can include changes to platform services such as Envoy Gateway, monitoring, the FRPC proxy
tunnel, or provider-specific controller apps.

## Infrastructure version upgrades

Some changes affect the cluster-level infrastructure version rather than only an infrastructure app stack revision.
These upgrades can change how Wodby wires cluster networking, routing, or platform controllers.

See [Kubernetes cluster infrastructure](infrastructure.md#infrastructure-versions) for infrastructure version details,
the changelog, current versions, and cluster-type-specific upgrade behavior.

Run K3S infrastructure version upgrades during a maintenance window for production workloads, because pod networking can
be briefly interrupted while K3S restarts and Cilium takes over.

If both an infrastructure version upgrade and infrastructure app stack upgrade are pending, Wodby handles the
infrastructure version upgrade first. Infrastructure app upgrades are checked again after the cluster is no longer
outdated at the infrastructure version level.

## Automatic infrastructure upgrades

Automatic infrastructure upgrades are configured per cluster. The setting has one master switch and separate controls
for two upgrade types:

| Control | Applies to |
| --- | --- |
| Infrastructure | Cluster-level infrastructure version upgrades |
| Infrastructure apps | Infrastructure app stack revision upgrades |

Each upgrade type has its own semver-only policy. Automatic infrastructure upgrades do not use revision or non-semver
matching. The policy controls whether automatic patch, minor, and major semver updates are allowed. By default, patch
and minor updates are allowed, and major updates are not.

Version policy settings affect automatic upgrades only. You can still run a manual infrastructure or infrastructure app
upgrade when the dashboard offers one.

### Defaults by cluster type

| Cluster type | Default |
| --- | --- |
| Wodby Cloud | Enabled and locked on. Major automatic upgrades are not allowed. |
| Managed Kubernetes in your cloud account | Disabled unless enabled during cluster creation or later from cluster settings. |
| K3S | Disabled unless enabled during cluster creation or later from cluster settings. |

Wodby Cloud clusters always keep automatic infrastructure upgrades enabled because Wodby operates the cluster
infrastructure. Major automatic upgrades remain disabled for Wodby Cloud even if cluster settings are changed later.

### Notifications and tasks

Automatic infrastructure upgrades create tasks, the same as manual upgrades. Task history shows whether Wodby upgraded
the cluster infrastructure version or infrastructure app stacks.

Wodby sends email notifications when automatic infrastructure upgrades succeed or fail. You can manage these from
`User settings > Notifications`.

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Coming soon...
