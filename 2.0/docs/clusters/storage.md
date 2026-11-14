---
description: See every persistent volume on a Kubernetes cluster with its size, usage, storage class and owner, and the storage classes the cluster offers, in the Wodby dashboard.
---

# Cluster storage

The `Storage` tab of a cluster shows where the cluster's disk space goes: every persistent volume, how full it is, which
app service uses it, and how much each storage class holds. Open it from `Clusters > [Cluster] > Storage`.

The tab is available on [managed Kubernetes](managed.md) and [K3S](k3s.md) clusters. [Wodby Cloud](wodby-cloud.md)
and serverless clusters don't have it. The tab only shows information; to change a volume, open its app service.

## Volumes

`Storage > Volumes` starts with an overview of the whole cluster:

- number of volumes
- requested space
- used space, and how many volumes reported it
- volumes that are 85% full or more
- volumes that no running pod mounts

Below it, each volume shows:

| Column | What it shows |
| --- | --- |
| Volume | The volume claim's name and its Kubernetes namespace |
| App environment | The app environment the volume belongs to |
| App service | The app service and its volume. Open it to see the volume in the app service's `Volumes` tab |
| Owner | `App service`, `Infrastructure` for Wodby's cluster components such as monitoring, `System` for Kubernetes system volumes, or `Other`, including a volume whose app service no longer exists |
| Class | The volume's [storage class](../apps/storage.md#choose-a-storage-class) |
| Size | The volume's size |
| Used | Used space and the share of the volume's filesystem it takes |
| Pods | How many running pods mount the volume, or `Not mounted` |

Use the filters above the list to show only one storage class, app, app environment or owner, or only volumes that are
85% full or more or not mounted.

A volume that isn't mounted still takes up disk space. It can be a volume of a stopped or paused app service, or one
left behind after its app service was removed.

### Usage that isn't reported

Usage comes from the cluster's [metrics](observability.md). A volume shows `Not reported` when its storage doesn't
report usage, for example NFS volumes, or when the cluster was created without `Enable monitoring`. Its size, storage
class and owner still show.

Local volumes on [K3S](k3s.md) clusters show used space without a percentage. They share their server's disk, so they
have no filesystem size of their own and don't count toward `85% full or more`. To see how full the server's disk is,
open the cluster's [metrics](observability.md). If they show `Not reported`, apply the available
[infrastructure app updates](updates.md#infrastructure-updates) to the cluster. Used space is measured every few
minutes.

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

To choose a class for a new volume, see [Application persistent storage](../apps/storage.md).
