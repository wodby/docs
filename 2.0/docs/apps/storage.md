---
description: Choose and change storage classes for the persistent volumes of your app services on managed Kubernetes and K3s clusters in Wodby.
---

# Application persistent storage

Persistent storage options depend on the type of cluster you run: [managed Kubernetes](../clusters/managed.md) or [K3s](../clusters/k3s.md).

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

When an app and its cluster are created together, the volume uses the cluster's default storage class once the cluster
is ready. The dashboard reports this in the disabled selector until the cluster is provisioned.

When you copy settings from another app environment, Wodby copies a volume's class only when that class is selectable on
the destination cluster. Otherwise the dashboard uses the destination cluster's sole selectable default or requires a
new explicit choice.

## Current storage class

Open an app environment, select an app service, and open its `Volumes` tab. The `Storage class` column shows the
class used by the volume and warns if it differs from your selection or cannot be verified.

| State | Meaning |
| --- | --- |
| Mismatch | The effective class differs from the configured class |
| Mixed | Claims associated with the volume use more than one class |
| Unknown | The claim, class inventory, or Kubernetes state could not be determined |
| Unavailable | The effective class is no longer present in the cluster |

Refresh the app-service volume state after provisioning or a cluster storage change if the result is temporarily
unknown.

To see every volume on a cluster with its usage and owner, open the cluster's [Storage tab](../clusters/storage.md).

## Changing a storage class

You can choose a class for a new volume during app creation or when adding an omitted optional volume later, but the
class of an existing volume cannot be changed. Updating an app or upgrading its stack does not move existing volume data
to another class.

Moving existing data to another class on the same cluster requires a separate migration: provision replacement storage,
copy or restore the data, verify the new workload, and only then remove the old claim. Wodby does not currently automate
an in-place storage-class migration.

When moving the entire app environment to another cluster, Wodby's
[app environment cluster migration](migration.md) restores supported root-volume data onto the storage classes selected
for the target cluster.

When a stack upgrade introduces a new volume, Wodby uses the class that the environment's existing volumes share when
possible. Otherwise it uses the cluster's single default class. The upgrade stops before making changes if Wodby cannot
read the cluster's storage classes or the choice is ambiguous.

## Storage types

### Block storage

Block storage is available on managed Kubernetes clusters. It is usually provided by the cloud platform and exposed
through one or more storage classes configured in the cluster.

Block storage is typically single-writer and attached to one node at a time.

### Local storage

Local storage is typical for K3s clusters. By default, persistent volume claims use storage from the server where the
app service is running. New app creation, deployments that can create persistent volume claims, app-service backups,
and imports perform a
[storage-capacity preflight](../clusters/k3s.md#disk-capacity-and-persistent-volumes) before storage work begins.

For a new app on an existing K3s cluster, Wodby checks that the requested sizes of the new local volumes fit in the
server's free disk space while keeping 10% of the disk in reserve. It also compares the combined size of existing and
requested local volumes with the disk's usable capacity. Shared volumes, volumes that reuse another volume, disabled
services, and unselected optional volumes are not counted. Wodby repeats the check before a deployment creates volumes,
including after an optional volume is added to an existing app service.

When the requested volumes do not fit in free space after the reserve, or Kubernetes reports `DiskPressure`, Wodby
stops creation or deployment with an error. If only the combined volume sizes exceed usable capacity, Wodby warns and
continues, because volume sizes are maximums rather than current disk usage. If the disk capacity cannot be determined,
Wodby also warns and continues.

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
