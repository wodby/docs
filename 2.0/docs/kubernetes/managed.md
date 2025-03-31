# Managed Kubernetes cluster

Wodby 2.0 allows to deploy your applications to Kubernetes clusters. You can connect your Kubernetes cluster from a cloud provider that offers managed Kubernetes services like:

- [Google Kubernetes Engine (GKE)](../integrations/gcp.md#gke)
- [AWS Elastic Kubernetes Service (EKS)](../integrations/aws.md#eks)
- [Azure Kubernetes Service (AKS)](../integrations/azure.md#aks)
- [DigitalOcean Kubernetes (DOKS)](../integrations/digitalocean.md#doks)
- [OVH Kubernetes](../integrations/ovh.md#kubernetes)

To create a cluster you should first connect your account from appropriate cloud provider to Wodby by creating a new integration with _kubernetes_ type.

When you delete a cluster from Wodby we will also delete it from your cloud provider.

!!! warning "Do not modify your cluster from cloud provider panel"
Clusters created from Wodby should not be modified directly from a cloud provider panel. This will lead to unexpected errors.
