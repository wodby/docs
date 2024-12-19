# Getting started

!!! warning "Beta Version"
    
    Wodby 2.0 is currently in Beta, do not use it for production.<br>
    This documentation is not complete and actively updated. 

Wodby was designed to help developers deploy and manage scalable web application in the most simple fashion. To deploy your first [application](apps/index.md) you would need a [kubernetes cluster](kubernetes/index.md), Wodby does not currently provide Kubernetes cluster out of the box with an exception to the [Demo cluster](kubernetes/demo.md) for testing purposes, so it is required for you to connect an account from your preferred cloud provider that provides managed Kubernetes service, such as:

- [Google Cloud Platform GKE](integrations/gcp.md#gke)
- [Amazon Web Service EKS](integrations/aws.md#eks)
- [Azure AKZ](integrations/azure.md#aks)
- [DigitalOcean DOKS](integrations/digitalocean.md#doks)
- [OVH Kubernetes](integrations/ovh.md#kubernetes) or others.

You can connect your account by creating an [integration](integrations/index.md) from _Integrations_ tab in Wodby dashboard. After creating a Kubernetes integration you can now create a Kubernetes cluster from _Kubernetes_ tab – Wodby will deploy a new kubernetes cluster in the selected cloud provider under you account.

Key concepts:

- [Applications](apps/index.md) and [Instances](apps/instances.md)
- [CI/CD](cicd/index.md)
- [Kubernetes clusters](kubernetes/index.md)
- [Databases](databases/index.md)
- [Stacks](stacks/index.md)
- [Services](services/index.md)
- [Integrations](integrations/index.md)

Organize your resources:

- [Organization](org.md)
- [Projects](projects.md)
- [Teams](teams.md)

How to:

- [Create your first application](apps/index.md#creating-new-application)
- [Create your Kubernetes cluster](kubernetes/index.md)
