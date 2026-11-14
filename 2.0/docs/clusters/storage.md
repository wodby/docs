---
description: See every persistent volume on a Kubernetes cluster with its size, usage, storage class and owner, and the storage classes the cluster offers, in the Wodby dashboard.
---

# Cluster storage

The `Storage` tab of a cluster shows where the cluster's disk space goes: every persistent volume, how full it is, which
app service uses it, and how much each storage class holds. Open it from `Clusters > [Cluster] > Storage`.

The tab is available on [managed Kubernetes](managed.md) and [K3s](k3s.md) clusters. [Wodby Cloud](wodby-cloud.md)
and serverless clusters don't have it. The tab only shows information; to change a volume, open its app service.

## Volumes

`Storage > Volumes` starts with an overview of the whole cluster:

- number of volumes
- requested space of the volumes that have a disk
- used space, and how many volumes reported it
- volumes that are 85% full or more
- volumes with a disk that no running pod mounts

Below it, the volumes are listed by app environment. Each app environment is shown once for all of its volumes.

| Column | What it shows |
| --- | --- |
| App environment | The app environment the volume belongs to. Volumes outside app environments show `Infrastructure` for Wodby's cluster components such as monitoring, `System` for Kubernetes system volumes, or `Other`, including a volume whose app service no longer exists |
| App service | The app service and its volume. Open it to see the volume in the app service's `Volumes` tab |
| Volume | The volume claim's name and its Kubernetes namespace |
| Class | The volume's [storage class](../apps/storage.md#choose-a-storage-class) and where it comes from |
| Size | The volume's size |
| Used | Used space and the share of the volume it takes |
| Pods | How many running pods mount the volume, or why none does |

Use the filters above the list to show only one storage class, app, app environment or owner, or only volumes that are
85% full or more or not mounted. Sort by volume, size, used space or pods to see the whole cluster in that order.

### Volumes that aren't mounted

When no running pod mounts a volume, the `Pods` column says why:

| Tag | What it means |
| --- | --- |
| `Environment paused` | The volume's app environment is paused. Resume it to use the volume again |
| `Service disabled` | The volume's app service is disabled. Its data is kept for when you enable the service again |
| `No disk yet` | No disk has been created for the volume. Some storage classes create the disk only for the first pod that uses the volume. It takes no space and isn't counted in the requested space |
| `Not mounted` | Nothing explains why the volume isn't used. It may be left behind after its app service was removed |

Volumes that are paused, disabled or not mounted still take up disk space. A disabled service's volume can also show
`Service disabled` while it has no disk yet; it then takes no space either.

### Usage that isn't reported

Usage comes from the cluster's [metrics](observability.md). A volume shows `Not reported` when its storage doesn't
report usage, for example NFS volumes, or when the cluster was created without `Enable monitoring`. Its size, storage
class and owner still show.

Local volumes on [K3s](k3s.md) clusters are folders on their server's disk. Their used space is measured every few
minutes and shown as a share of the volume's size. All of them share the server's disk, so also check how full the disk
is in the cluster's [metrics](observability.md). If they show `Not reported`, apply the available
[infrastructure app updates](updates.md#infrastructure-updates) to the cluster.

### Volumes of other app environments

The list includes every volume on the cluster and the overview counts all of them. A volume of an app environment you
can't open shows `Not visible to you` instead of its app environment and app service.

## Storage classes

`Storage > Storage classes` lists the storage classes the cluster offers for new volumes, with:

- provisioner
- reclaim policy: `Delete` removes the disk when its volume is deleted, `Retain` keeps the disk until you delete it in
  your cloud account or on the server
- binding mode
- whether volumes can be expanded
- how many volumes use the class, and their requested and used space

The cluster's default class is marked `Default`. A class that volumes use but that isn't offered for new volumes is
marked `Not offered`. Volumes without a storage class are grouped in their own row.

An icon next to a class shows where it comes from:

- the icon of the [storage service](../services/types.md#storage), such as NFS, that provides the class
- on [managed Kubernetes](managed.md) clusters, the icon of the cluster's integration for the cloud provider's block
  storage

K3s local storage has no icon. Neither does a storage service in an app environment you can't open.

To choose a class for a new volume, see [Application persistent storage](../apps/storage.md).
