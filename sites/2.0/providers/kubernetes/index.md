Source: https://wodby.com/docs/2.0/providers/kubernetes/

# Kubernetes providers

Kubernetes providers are third-party services whose integrations expose the `kubernetes` type. Use this group when you want Wodby to create and manage a managed Kubernetes cluster inside your cloud account.

Machine name: `kubernetes`

Use a Kubernetes provider when:

- you want Wodby to provision a managed Kubernetes cluster in your own cloud account
- you want cluster lifecycle operations to stay tied to a provider-backed integration
- you want to deploy apps to managed Kubernetes rather than to Wodby Cloud or K3s

## Where it is used in Wodby

Kubernetes integrations are used for:

- creating managed Kubernetes clusters
- choosing a provider-backed cluster destination for apps
- managing cluster settings such as region, machine type, node count, and high availability through the supported provider workflow

## Supported providers

| Provider | Managed service |
| --- | --- |
| [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#eks) | EKS |
| [Azure](https://wodby.com/docs/2.0/providers/azure/#aks) | AKS |
| [Google Cloud Platform](https://wodby.com/docs/2.0/providers/gcp/#gke) | GKE |
| [DigitalOcean](https://wodby.com/docs/2.0/providers/digitalocean/#doks) | DOKS |
| [OVH EU, OVH CA, OVH US](https://wodby.com/docs/2.0/providers/ovh/#kubernetes) | Managed Kubernetes |
| [UpCloud](https://wodby.com/docs/2.0/providers/upcloud/#kubernetes) | Managed Kubernetes |

- Use [Wodby Cloud](https://wodby.com/docs/2.0/clusters/wodby-cloud/) or [Demo Cluster](https://wodby.com/docs/2.0/clusters/demo/) when you do not want to bring your own cloud account.
- Use [K3s](https://wodby.com/docs/2.0/clusters/k3s/) when you want to connect your own server instead of provisioning a managed Kubernetes service.

## Related pages

- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
- [Choose deployment option](https://wodby.com/docs/2.0/clusters/choose-platform/)
