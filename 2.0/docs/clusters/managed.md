---
description: Create managed Kubernetes clusters on GKE, EKS, AKS, DigitalOcean or OVH from Wodby. Supported versions, GPU node pools and single-node clusters.
---

# Managed Kubernetes cluster

Wodby can deploy your applications to managed Kubernetes clusters in supported cloud providers such as:

- [Google Kubernetes Engine (GKE)](../providers/gcp.md#gke)
- [AWS Elastic Kubernetes Service (EKS)](../providers/aws.md#eks)
- [Azure Kubernetes Service (AKS)](../providers/azure.md#aks)
- [DigitalOcean Kubernetes (DOKS)](../providers/digitalocean.md#doks)
- [OVH Kubernetes](../providers/ovh.md#kubernetes)

To create a managed cluster, first connect your cloud account to Wodby by creating an integration of type `Kubernetes`.

## Kubernetes versions

The cluster creation form lists the Kubernetes versions the cloud provider offers for the selected location, starting
from the oldest version Wodby supports, with the recommended version selected. A new version appears as soon as the
provider offers it. When a provider publishes full patch or build versions, Wodby selects the latest available release
of the recommended version. When a provider accepts only a minor version, the provider selects and maintains the patch
release.

Existing clusters use a provider-specific upgrade plan based on their current version. A cluster on a version that new
clusters can no longer use may need to install a provider-approved patch before it can upgrade to the next minor
version.

In the cluster creation form, choose an `Owner`:

- `Organization <organization>` creates an organization-owned cluster
- `Project <project>` creates a project-owned cluster

Automatic infrastructure upgrades are enabled by default during cluster creation for managed Kubernetes clusters. You can
disable them during creation or change them later from `Clusters > [Cluster] > Infrastructure > Updates`.

[Automatic Kubernetes upgrades](updates.md#automatic-kubernetes-upgrades), which also apply component updates, are off
by default for managed clusters. Every Kubernetes upgrade of a managed cluster replaces all of its nodes, even for a
patch, so every pod restarts and a single-node cluster is unavailable for a few minutes. To create the cluster with
them, select `Auto upgrade Kubernetes and components`. You can change them later from
`Clusters > [Cluster] > Kubernetes > Updates`.

Use the cluster `Ownership` page later if other projects need `Read/Use` or `Modify/Delete` access.

When you delete a managed cluster from Wodby, Wodby also deletes it in the cloud provider account.

## Nodes

`Clusters > [Cluster] > Nodes` lists the cluster's nodes as Kubernetes reports them. For each node you see its status,
machine type, zone, Kubernetes version, CPU, memory, disk, private and public IP, and when it was created. When the
cluster has a [GPU node pool](gpu.md), the list also shows each node's pool and its GPUs.

A node marked `Cordoned` takes no new pods, for example while the provider replaces it during an upgrade.

The cloud provider adds, replaces and removes the nodes, so you can't add or remove a node from the list. To change how
many nodes the cluster has, see [Cluster scalability](scalability.md).

## GPU node pools

DOKS, EKS and GKE clusters can have an optional [GPU node pool](gpu.md) next to the default node pool, for app
services that need GPUs.

## Single-node clusters

Some managed Kubernetes providers expose a `Single-node cluster` option in Wodby's cluster creation form. The option is available only for standard, non-serverless clusters after you select a supported Kubernetes integration.

When enabled, Wodby creates a fixed one-node cluster:

- minimum node count is fixed to `1`
- maximum node count is fixed to `1`
- cluster scaling is unavailable from `Kubernetes > Operations`
- Wodby does not create a cloud provider load balancer
- public app traffic is routed directly to the node IP

Use this mode for small clusters where reducing infrastructure cost matters more than high availability or scaling.

Endpoint values are still shown in the cluster overview as `Public IPs` or `Hostname`.

Single-node clusters are currently available for DigitalOcean-backed Kubernetes clusters.

!!! warning "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
