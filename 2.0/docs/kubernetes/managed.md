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

Use the cluster `Sharing` page later if other projects need `Read/Use` or `Modify/Delete` access.

When you delete a managed cluster from Wodby, Wodby also deletes it in the cloud provider account.

!!! warning "Do not modify your cluster from cloud provider panel"
    Clusters created from Wodby should not be modified directly from the cloud provider control panel. Doing so can lead to drift and unexpected errors.
