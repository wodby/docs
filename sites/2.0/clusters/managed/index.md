Source: https://wodby.com/docs/2.0/clusters/managed/

# Managed Kubernetes cluster

Wodby can deploy your applications to managed Kubernetes clusters in supported cloud providers such as:

- [Google Kubernetes Engine (GKE)](https://wodby.com/docs/2.0/providers/gcp/#gke)
- [AWS Elastic Kubernetes Service (EKS)](https://wodby.com/docs/2.0/providers/aws/#eks)
- [Azure Kubernetes Service (AKS)](https://wodby.com/docs/2.0/providers/azure/#aks)
- [DigitalOcean Kubernetes (DOKS)](https://wodby.com/docs/2.0/providers/digitalocean/#doks)
- [OVH Kubernetes](https://wodby.com/docs/2.0/providers/ovh/#kubernetes)
- [UpCloud Managed Kubernetes](https://wodby.com/docs/2.0/providers/upcloud/#kubernetes)

To create a managed cluster, first connect your cloud account to Wodby by creating an integration of type `Kubernetes`.

## Kubernetes versions

The cluster creation form lists the Kubernetes versions your cloud provider offers. See
[Kubernetes versions for new clusters](https://wodby.com/docs/2.0/clusters/kubernetes/#kubernetes-versions-for-new-clusters).

In the cluster creation form, choose an `Owner`:

- `Organization <organization>` creates an organization-owned cluster
- `Project <project>` creates a project-owned cluster

Automatic infrastructure upgrades are enabled by default during cluster creation for managed Kubernetes clusters. You can
disable them during creation or change them later from `Clusters > [Cluster] > Infrastructure > Updates`.

[Automatic Kubernetes upgrades](https://wodby.com/docs/2.0/clusters/kubernetes/#automatic-kubernetes-upgrades), which also apply component updates, are off
by default for managed clusters. Every Kubernetes upgrade of a managed cluster replaces all of its nodes, even for a
patch, so every pod restarts and a single-node cluster is unavailable for a few minutes. To create the cluster with
them, select `Auto upgrade Kubernetes and components`. You can change them later from
`Clusters > [Cluster] > Kubernetes > Updates`.

Use the cluster `Ownership` page later if other projects need `Read/Use` or `Modify/Delete` access.

When you delete a managed cluster from Wodby, Wodby also deletes it in the cloud provider account.

## Nodes

`Clusters > [Cluster] > Nodes` lists the cluster's nodes as Kubernetes reports them. For each node you see its status,
machine type, zone, Kubernetes version, CPU, memory, disk, private and public IP, and when it was created. When the
cluster has a [GPU node pool](https://wodby.com/docs/2.0/clusters/gpu/), the list also shows each node's pool and its GPUs.

A node marked `Cordoned` takes no new pods, for example while the provider replaces it during an upgrade.

The cloud provider adds, replaces and removes the nodes, so you can't add or remove a node from the list. To change how
many nodes the cluster has or replace its nodes, use `Nodes > Operations`. See [Cluster scalability](https://wodby.com/docs/2.0/clusters/scalability/) and
[Worker node updates](https://wodby.com/docs/2.0/clusters/kubernetes/#worker-node-updates).

## GPU node pools

DOKS, EKS and GKE clusters can have an optional [GPU node pool](https://wodby.com/docs/2.0/clusters/gpu/) next to the default node pool, for app
services that need GPUs.

## Single-node clusters

Some managed Kubernetes providers expose a `Single-node cluster` option in Wodby's cluster creation form. The option is available only for standard, non-serverless clusters after you select a supported Kubernetes integration.

When enabled, Wodby creates a fixed one-node cluster:

- minimum node count is fixed to `1`
- maximum node count is fixed to `1`
- cluster scaling is unavailable from `Nodes > Operations`
- Wodby does not create a cloud provider load balancer
- public app traffic is routed directly to the node IP

Use this mode for small clusters where reducing infrastructure cost matters more than high availability or scaling.

Endpoint values are still shown in the cluster overview as `Public IPs` or `Hostname`.

Single-node clusters are currently available for DigitalOcean-backed Kubernetes clusters.

Do not modify your cluster from cloud provider panel

Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
