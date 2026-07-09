# Get Started

Wodby helps developers deploy and manage scalable web applications on Kubernetes with a workflow centered around
stacks, integrations, and application instances.

Start here if you are deciding where your app should run, how Wodby's app model is structured, or which core terms the dashboard is using.

To deploy your first [application](apps/index.md), choose one of the following cluster options:

- [Managed Kubernetes](clusters/managed.md) in your own cloud account
- [Self-hosted Kubernetes with K3S](clusters/k3s.md) on your own server
- [Wodby Cloud](clusters/wodby-cloud.md), where Wodby creates and manages the cluster for you
- [Demo](clusters/demo.md), which is a temporary Wodby Cloud cluster for testing

For managed Kubernetes, connect an account from a supported cloud provider that offers a managed Kubernetes service, such as:

- [Google Cloud Platform GKE](providers/gcp.md#gke)
- [Amazon Web Services EKS](providers/aws.md#eks)
- [Azure AKS](providers/azure.md#aks)
- [DigitalOcean DOKS](providers/digitalocean.md#doks)
- [OVH Kubernetes](providers/ovh.md#kubernetes)

Typical first steps:

1. Create or choose an [organization](org.md) and a [project](projects.md)
2. Choose a cluster option:
   - connect a managed Kubernetes provider via [integrations](integrations/index.md)
   - connect your own server with [K3S](clusters/k3s.md)
   - create a [Wodby Cloud](clusters/wodby-cloud.md) cluster from the Clusters page or choose Wodby Cloud in the new application flow
3. Create your first application from a [stack](stacks/index.md). Use a catalog stack, or [create a custom stack](stacks/create.md) when you need your own service composition.
4. Configure the first [instance](apps/instances.md) and deploy it

If the catalog does not include the component you need, [create or import a service](services/create.md), add it to a stack, and then create an application from that stack.

If you use managed Kubernetes, create an [integration](integrations/index.md) from the _Integrations_ tab and then create a cluster from the _Clusters_ tab. Wodby will provision the cluster in the selected cloud account for you.

If you use Wodby Cloud, create a cluster from _Clusters > New Wodby Cloud cluster_ or select _Wodby Cloud_ in Step 2 of the new application form. For testing, you can enable [Demo](clusters/demo.md); demo clusters are deleted automatically after 24 hours, and applications deployed to them are deleted with them.

## Decision guides

- [Choose a cluster option](clusters/choose-platform.md)
- [App vs app instance vs app service](apps/app-vs-instance-vs-service.md)
- [Provider vs integration](integrations/providers-vs-integrations.md)
- [Glossary](glossary.md)

Key concepts:

- [Applications](apps/index.md) and [Instances](apps/instances.md)
- [Stacks](stacks/index.md) and [Services](services/index.md)
- [Clusters](clusters/index.md)
- [CI/CD](cicd/index.md)
- [Databases](databases/index.md)
- [Integrations](integrations/index.md)

Organize your resources:

- [Organization](org.md)
- [Projects](projects.md)
- [Teams](teams.md)

How to:

- [Create your first application](apps/index.md#creating-new-application)
- [Create your cluster](clusters/index.md)
- [Create or import a service](services/create.md)
- [Create or import a stack](stacks/create.md)
