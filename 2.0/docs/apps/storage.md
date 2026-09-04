# Application Persistent Storage

Persistent storage options depend on the type of cluster you run: [managed Kubernetes](../clusters/managed.md) or [K3S](../clusters/k3s.md).

## Choose a storage class

When you create an app, or add a previously omitted optional volume to an existing app service, each eligible
persistent volume can use one of the selectable storage classes reported by the target cluster. A storage class
determines which Kubernetes provisioner creates the volume and can affect performance, availability, expansion
support, topology, and cost.

After selecting the destination cluster, open the `Volumes` section on the `Settings` step. Each eligible volume has a
`Storage class` selector. The selector shows the class name and provisioner, and marks the cluster default. Classes that
belong to another app or are otherwise private are not shown.

If the cluster has exactly one selectable default, the dashboard selects it automatically. You can keep it or choose
another class. If the cluster has no unambiguous selectable default, you must select a class explicitly before
continuing. Changing the destination cluster revalidates every selection and replaces a class that is not available on
the new cluster with its sole selectable default, when one exists.

Storage-class selection is not available for every volume:

- shared volumes inherit the class provided by their linked storage service
- volumes that reuse another volume inherit the source claim's class
- older or custom service revisions must implement the
  [storage-class selection contract](../services/template.md#storage-class-selection-contract)

For a service-owned volume that cannot expose selection, the dashboard shows the same storage-class selector in a
disabled state with the one safe cluster default selected. App creation stops before submission when such a required
volume does not have exactly one selectable cluster default.

A shared volume shows its linked storage service, such as an NFS service, in a disabled `Storage service` selector. The
linked service's own volume settings control the underlying storage class. A volume that reuses another volume does not
expose an independent storage-class choice.

For an existing app service, open its `Volumes` tab and select `Add volume` on an omitted optional volume. The same
storage-class rules apply. Adding the volume marks the app service and environment for redeploy; Kubernetes storage is
provisioned by the subsequent deployment. Once added, the volume cannot be resized, removed, or moved to another class
from app-service settings.

When an app and its cluster are created together, the cluster inventory is not available yet. Wodby leaves the class
unset so Kubernetes can apply the cluster default after the cluster becomes ready. The dashboard reports this in the
disabled selector until the cluster is provisioned.

When you copy settings from another app environment, Wodby copies a volume's class only when that class is selectable on
the destination cluster. Otherwise the dashboard uses the destination cluster's sole selectable default or requires a
new explicit choice.

## Current storage class

Wodby keeps the configured class separately from the class observed on live Kubernetes PVCs and PVs. The dashboard can
therefore distinguish them. Open an app environment, select an app service, and open its `Volumes` tab. The `Storage class`
column shows:

- the effective class currently observed on the Kubernetes claim when the volume is healthy
- the selected and effective classes when they differ or cannot be verified
- a warning status only when the state needs attention

An optional volume that has not been added shows empty size and storage-class values with no diagnostic status. Its
absence is valid and does not affect configuration health.

Healthy volumes show the class once; the dashboard does not repeat matching values or display a `Current` badge.
Diagnostic statuses are:

| State | Meaning |
| --- | --- |
| Mismatch | The effective class differs from the configured class |
| Mixed | Claims associated with the volume use more than one class |
| Unknown | The claim, class inventory, or Kubernetes state could not be determined |
| Unavailable | The effective class is no longer present in the cluster |

Refresh the app-service volume state after provisioning or a cluster storage change if the result is temporarily
unknown.

After this feature is enabled, Wodby reconciles existing apps in the background. It records a configured class only
when every labeled claim for a volume resolves to the same class and that class is still selectable. Shared or reused
volumes, unlabeled claims, claims without an effective class, mixed claims, and private or removed classes remain
unconfigured and continue to show their live state when it can be observed. This reconciliation does not modify or
move any PVC data.

## Changing a storage class

You can choose a class for a new volume during app creation or when adding an omitted optional volume later, but
Kubernetes does not allow changing `storageClassName` on an existing bound PVC. Updating an app or upgrading its stack
therefore does not move existing volume data to another class.

Moving existing data to another class on the same cluster requires a separate migration: provision replacement storage,
copy or restore the data, verify the new workload, and only then remove the old claim. Wodby does not currently automate
an in-place storage-class migration.

When moving the entire app environment to another cluster, Wodby's
[app environment cluster migration](migration.md) restores supported root-volume data onto the storage classes selected
for the target cluster.

When a stack upgrade introduces a new volume, Wodby reuses one class already configured consistently across existing
owned volumes when possible. Otherwise it uses the cluster's one selectable default. The upgrade stops before making
changes if the live storage-class inventory cannot be refreshed or the choice is ambiguous.

## Storage types

### Block storage

Block storage is available on managed Kubernetes clusters. It is usually provided by the cloud platform and exposed
through one or more storage classes configured in the cluster.

Block storage is typically single-writer and attached to one node at a time.

### Local storage

Local storage is typical for K3S clusters. By default, persistent volume claims use storage from the server where the
app service is running. New app creation, deployments that can create persistent volume claims, app-service backups,
and imports perform a
[storage-capacity preflight](../clusters/k3s.md#disk-capacity-and-persistent-volumes) before storage work begins.

For a new app on an existing K3S cluster, Wodby adds the requested sizes of enabled, physical local-path volumes and
checks them against measured free space after keeping a 10% host-disk safety reserve. It also compares the combined
size claimed by existing and requested local-path volumes with usable host capacity. Shared volumes, volumes that reuse
another claim, disabled services, and unselected optional volumes do not add another allocation. Wodby repeats the
check in a deployment task immediately before it can create claims, including after an optional volume is added to an
existing app service; retries exclude claims that already exist.

When the requested allocation does not fit in measured free space after the safety reserve, or Kubernetes reports
`DiskPressure`, Wodby stops creation or deployment with an error. If only the combined claimed volume sizes exceed
usable capacity, Wodby warns and continues because claims are maximum sizes rather than current disk usage. If K3S
cannot report authoritative host-filesystem capacity, or a selected storage class uses a provisioner without a
capacity resolver, Wodby also warns and continues instead of treating unknown capacity as zero.

### Distributed storage

#### Container-based

Some workloads need shared storage with multiple writers, especially in scaled or highly available setups. For those cases, Wodby provides [storage services](../services/types.md#storage).

The simplest container-based option is an NFS server. It is easy to use, but it is not highly available on its own. In this setup, the NFS server stores its data on local or block storage, depending on the cluster type, and then exposes a storage class for other services to use.

Services that require distributed storage have [volumes](../services/configuration.md#volumes) defined with a mandatory link to reference a storage service.

#### Managed

You can also use a third-party distributed storage system such as AWS EFS when your infrastructure supports it.

### Storage classes from infrastructure apps

Infrastructure apps can install additional provisioners and storage classes, including distributed systems such as
Rook. A cluster-scoped class appears as an app-volume choice only when it is public for selection. Infrastructure app
authors can mark a `StorageClass` explicitly:

```yaml
metadata:
  annotations:
    app.wodby.com/storage-class-selectable: "true"
```

Do not add this annotation to a class intended for only one app or one internal component.
