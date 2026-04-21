# Kubernetes providers

Kubernetes providers are third-party services whose integrations expose the `kubernetes` type. Use this group when you want Wodby to create and manage a managed Kubernetes cluster inside your cloud account.

Machine name: `kubernetes`

Use a Kubernetes provider when:

- you want Wodby to provision a managed Kubernetes cluster in your own cloud account
- you want cluster lifecycle operations to stay tied to a provider-backed integration
- you want to deploy apps to managed Kubernetes rather than to Wodby Cloud or K3S

## Where it is used in Wodby

Kubernetes integrations are used for:

- creating managed Kubernetes clusters
- choosing a provider-backed cluster destination for apps
- managing cluster settings such as region, machine type, node count, and high availability through the supported provider workflow

## Supported providers

| Provider | Managed service |
| --- | --- |
| [Amazon Web Services](aws.md#eks) | EKS |
| [Azure](azure.md#aks) | AKS |
| [Google Cloud Platform](gcp.md#gke) | GKE |
| [DigitalOcean](digitalocean.md#doks) | DOKS |
| [OVH](ovh.md#kubernetes) | Managed Kubernetes |

- Use [Wodby Cloud](../kubernetes/wodby-cloud.md) or [Demo Cluster](../kubernetes/demo.md) when you do not want to bring your own cloud account.
- Use [K3S](../kubernetes/k3s.md) when you want to connect your own server instead of provisioning a managed Kubernetes service.

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [Choose deployment option](../kubernetes/choose-platform.md)
