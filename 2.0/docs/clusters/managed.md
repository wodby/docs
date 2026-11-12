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

The cluster creation form lists the Kubernetes versions Wodby supports for the selected provider and location, with the
recommended version selected. A version the cloud provider offers is not listed until Wodby supports it. When a
provider publishes full patch or build versions, Wodby selects the latest available release of the recommended
version. When a provider accepts only a minor version, the provider selects and maintains the patch release.

Existing clusters use a provider-specific upgrade plan based on their current version. A cluster on a version that new
clusters can no longer use may need to install a provider-approved patch before it can upgrade to the next minor
version.

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

Some managed Kubernetes providers expose a `Single-node cluster` option in Wodby's cluster creation form. The option is available only for standard, non-serverless clusters after you select a supported Kubernetes integration.

When enabled, Wodby creates a fixed one-node cluster:

- minimum node count is fixed to `1`
- maximum node count is fixed to `1`
- cluster scaling is unavailable from `Infrastructure > Kubernetes`
- Wodby does not create a cloud provider load balancer
- public app traffic is routed directly to the node IP

Use single-node clusters for development environments that use only technical domains. For production, create a
scalable cluster, even with one node: its load balancer keeps the cluster's public IP when nodes are replaced.

Endpoint values are still shown in the cluster overview as `Public IPs` or `Hostname`.

Single-node clusters are currently available for DigitalOcean-backed Kubernetes clusters.

### Public IP changes

A single-node cluster has no load balancer, so its public IP is its node's IP. The node, and with it the IP, is
replaced when:

- the cluster's [Kubernetes version is upgraded](updates.md#kubernetes-version-updates)
- you [recycle its node](updates.md#recycle-a-single-node-cluster)
- the provider replaces a failed node

When the IP changes:

- Wodby points the cluster's technical domains at the new IP within a few minutes.
- Wodby emails the organization's owners and admins the old and the new IP, with the cluster's custom domains that
  still resolve to the old IP. See [Cluster public IP changes](../user/notifications.md#cluster-public-ip-changes).
- Custom domains with a DNS A record that points to the old IP stop working until you change the record to the new
  IP. The cluster overview shows the new IP under `Public IPs`.

Because each upgrade changes the IP, [automatic Kubernetes upgrades](updates.md#automatic-kubernetes-upgrades) aren't
available for a single-node cluster with custom domains. Upgrade it manually during a maintenance window, then update
the custom domains' DNS records.

!!! warning "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
