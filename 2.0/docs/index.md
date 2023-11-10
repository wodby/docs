# Getting started

Wodby was designed to help developers deploy and manage scalable web application in the most simple fashion. To deploy your first application you would need a kubernetes cluster, Wodby does not provide Kubernetes cluster out of the box (we're not a hosting provider) with an exception to the Demo cluster for testing purposes, so it is required for you to connect an account from your preferred cloud provider that provides managed Kubernetes service, such as:

- [Google Cloud Platform GKE](integrations/gcp.md#gke)
- [Amazone Web Service EKS](integrations/aws.md#eks)
- [Azure AKZ](integrations/azure.md#aks)
- [DigitalOcean DOKS](integrations/digitalocean.md#doks)
- [OVH Kubernetes](integrations/ovh.md#kubernetes)
- [Linode LKE](integrations/linode.md#lke) or others.

You can connect your account by creating an integration from _Integrations_ tab of Wodby dashboard. After you create an integration that provides Kubernetes integration you can create a Kubernetes cluster from _Kubernetes_ tab – Wodby will create a new kubernetes cluster under you account.

If you're using Demo cluster please note that all applications deployed to our demo server will be automatically deleted after 12 hours.

Key concepts:

* [Application Instances](apps/instances.md)
* [Clusters](clusters/index.md)
* [Stacks](stacks/index.md)

How to:

* [Create your first application](apps/new.md)
* [Create your Kubernetes cluster](clusters/new.md)
