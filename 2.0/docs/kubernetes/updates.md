# Kubernetes cluster updates

Cluster updates are managed from the dashboard at `Kubernetes > [Cluster] > Infrastructure`.

Wodby tracks two update states for each cluster:

- Wodby infrastructure version updates
- infrastructure app stack updates

The cluster can show that updates are available when either state is outdated. If both are outdated, update the Wodby
infrastructure version first. Wodby's automatic upgrade flow uses the same order.

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes
available and the cluster is marked as having outdated infrastructure apps. You can then upgrade the infrastructure app
stacks manually, or let Wodby upgrade them automatically when automatic infrastructure upgrades
are enabled.

Infrastructure app updates can include changes to platform services such as Envoy Gateway, monitoring, the FRPC proxy
tunnel, or provider-specific controller apps.

In the dashboard, open `Kubernetes`, select the cluster, and go to `Infrastructure > Operations`. The
`Infrastructure app stacks` card shows whether stack updates are available. When Wodby can identify the affected
infrastructure apps, the card lists each app and the current and target stack revision numbers.

The `Infrastructure Apps` tab lists the infrastructure apps installed on the cluster. Use it when you need to inspect
the app list or open an individual infrastructure app page.

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

In the dashboard, open `Kubernetes`, select the cluster, and go to `Infrastructure > Operations`. The
`Wodby infrastructure` card shows the current infrastructure version, the target version when an upgrade is available,
and a manual upgrade button. The manual button is disabled when no infrastructure version upgrade is available.

Manual infrastructure version upgrades and manual infrastructure app stack upgrades are not available for Wodby Cloud
clusters. Wodby Cloud infrastructure is operated by Wodby and can still be upgraded automatically by Wodby.

## Automatic infrastructure upgrades

Automatic infrastructure upgrades are configured per cluster with separate controls for two upgrade types:

| Control | Applies to |
| --- | --- |
| Infrastructure | Cluster-level infrastructure version upgrades |
| Infrastructure apps | Infrastructure app stack revision upgrades |

Each upgrade type has its own semver-only policy. Automatic infrastructure upgrades do not use revision or non-semver
matching. The policy controls whether automatic patch, minor, and major semver updates are allowed. By default, patch
and minor updates are allowed, and major updates are not.

Each upgrade type has its own `Auto upgrade` switch. Disabling both switches disables automatic infrastructure upgrades
for the cluster.

Version policy settings affect automatic upgrades only. You can still run a manual infrastructure or infrastructure app
upgrade when the dashboard offers one.

In the dashboard, auto-update settings are in the same two cards as the manual actions:

- `Infrastructure > Operations > Wodby infrastructure > Auto updates`
- `Infrastructure > Operations > Infrastructure app stacks > Auto updates`

Each section has an `Auto upgrade` switch and `Patch versions`, `Minor versions`, and `Major versions` policy
checkboxes. `Major versions` is visible but is not enabled by default.

### Defaults by cluster type

| Cluster type | Default |
| --- | --- |
| Wodby Cloud | Enabled and locked on. Major automatic upgrades are not allowed. |
| Managed Kubernetes in your cloud account | Enabled in the dashboard creation form. You can disable it during creation or later from `Infrastructure > Operations`. |
| K3S | Enabled in the dashboard creation form. You can disable it during creation or later from `Infrastructure > Operations`. |

Wodby Cloud clusters always keep automatic infrastructure upgrades enabled because Wodby operates the cluster
infrastructure. The dashboard shows these settings as managed by Wodby. Major automatic upgrades remain disabled for
Wodby Cloud.

### Notifications and tasks

Automatic infrastructure upgrades create tasks, the same as manual upgrades. Task history shows whether Wodby upgraded
the cluster infrastructure version or infrastructure app stacks.

Wodby sends email notifications when automatic infrastructure upgrades succeed or fail. You can manage these from
`User settings > Notifications`.

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Coming soon...
