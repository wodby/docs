---
description: Create managed Kubernetes clusters on GKE, EKS, AKS, DigitalOcean or OVH from Wodby. Supported versions and GPU node pools.
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

The minimum Kubernetes version for new managed clusters is 1.35. Versions below 1.35 are not shown during cluster
creation and cannot be selected for a new cluster.

Kubernetes 1.36 is the default version for new managed clusters and Wodby Cloud. When a provider publishes full patch
or build versions, Wodby selects the latest available release in the 1.36 series. When a provider accepts only a minor
version such as `1.36`, the provider selects and maintains the patch release.

Newer Kubernetes versions remain available when the cloud provider offers them, but Wodby does not select them by
default. If a provider does not offer Kubernetes 1.36, Wodby selects its newest available supported version below 1.36,
but never a version below the 1.35 minimum.

Existing clusters use a provider-specific upgrade plan based on their current version. A legacy cluster below the
current creation minimum may need to install a provider-approved patch before it can upgrade to the next minor version.

In the cluster creation form, choose an `Owner`:

- `Organization <organization>` creates an organization-owned cluster
- `Project <project>` creates a project-owned cluster

Automatic infrastructure upgrades are enabled by default during cluster creation for managed Kubernetes clusters. You can
disable them during creation or change them later from `Clusters > [Cluster] > Infrastructure > Operations`.

[Automatic Kubernetes upgrades](updates.md#automatic-kubernetes-upgrades), which also apply component updates, are off
by default for managed clusters. Every Kubernetes upgrade of a managed cluster replaces all of its nodes, even for a
patch, so every pod restarts and a single-node cluster is unavailable for a few minutes. To create the cluster with
them, select `Auto upgrade Kubernetes and components`. You can change them later from
`Clusters > [Cluster] > Infrastructure > Kubernetes`.

Use the cluster `Ownership` page later if other projects need `Read/Use` or `Modify/Delete` access.

When you delete a managed cluster from Wodby, Wodby also deletes it in the cloud provider account.

## GPU node pools

DOKS, EKS and GKE clusters can have an optional [GPU node pool](gpu.md) next to the default node pool, for app
services that need GPUs.

## Single-node clusters

New single-node clusters are no longer available. To run a small cluster, create one with a minimum and maximum of one
node; it can grow later.

Existing single-node clusters keep running with one fixed node and no cloud provider load balancer. Public app traffic
goes directly to the node's IP, shown in the cluster overview as `Public IPs`. You can't scale them or recycle their
nodes.

!!! warning "The public IP changes when the node is replaced"
    A Kubernetes version upgrade replaces the cluster's only node, and the new node gets a new public IP. Wodby does not
    move your domains to the new IP, so the apps on the cluster stop being reachable. Before you upgrade Kubernetes on
    a single-node cluster, move its apps to a cluster with a minimum and maximum node count.

!!! warning "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
