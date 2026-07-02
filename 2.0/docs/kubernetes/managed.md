# Managed Kubernetes cluster

Wodby can deploy your applications to managed Kubernetes clusters in supported cloud providers such as:

- [Google Kubernetes Engine (GKE)](../providers/gcp.md#gke)
- [AWS Elastic Kubernetes Service (EKS)](../providers/aws.md#eks)
- [Azure Kubernetes Service (AKS)](../providers/azure.md#aks)
- [DigitalOcean Kubernetes (DOKS)](../providers/digitalocean.md#doks)
- [OVH Kubernetes](../providers/ovh.md#kubernetes)

To create a managed cluster, first connect your cloud account to Wodby by creating an integration of type `Kubernetes`.

In the cluster creation form, choose an `Owner`:

- `Organization <organization>` creates an organization-owned cluster
- `Project <project>` creates a project-owned cluster

Automatic infrastructure upgrades are enabled by default during cluster creation for managed Kubernetes clusters. You can
disable them during creation or change them later from `Kubernetes > [Cluster] > Infrastructure > Operations`.

Use the cluster `Sharing` page later if other projects need `Read/Use` or `Modify/Delete` access.

When you delete a managed cluster from Wodby, Wodby also deletes it in the cloud provider account.

## Single-node clusters

Some managed Kubernetes providers expose a `Single-node cluster` option in Wodby's cluster creation form. The option is available only for standard, non-serverless clusters after you select a supported Kubernetes integration.

When enabled, Wodby creates a fixed one-node cluster:

- minimum node count is fixed to `1`
- maximum node count is fixed to `1`
- cluster scaling is unavailable from `Infrastructure > Kubernetes`
- Wodby does not create a cloud provider load balancer
- public app traffic is routed directly to the node IP

Use this mode for small clusters where reducing infrastructure cost matters more than high availability or scaling.

Endpoint values are still shown in the cluster overview as `Public IPs` or `Hostname`.

Single-node clusters are currently available for DigitalOcean-backed Kubernetes clusters.

!!! warning "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
