# Kubernetes

Wodby supports four practical deployment choices for Kubernetes-backed applications.

Use these pages when you are deciding where your app should run or when you need to connect or create a cluster.

## Quick comparison

| Option | Best when | Created from |
| --- | --- | --- |
| Managed Kubernetes | You want cloud-native infrastructure in your own provider account | `Kubernetes` |
| K3S | You want self-hosted Kubernetes on your own server | `Kubernetes > Connect server` |
| Wodby Cloud | You want Wodby to create and manage the cluster | `Apps > New app > Step 2` |
| Demo | You want a temporary test cluster for 24 hours | `Apps > New app > Step 2 > Wodby Cloud > Demo` |

See [Choose a Kubernetes option](choose-platform.md) for the full decision guide.

## 1. [Managed Kubernetes](managed.md)

Ready-to-run, scalable clusters created in your own cloud account through [integrations](../integrations/index.md) such as GCP, AWS, Azure, DigitalOcean, and OVH.

If you plan to scale your cluster and need more flexibility, we recommend this approach.

Create these clusters from the `Kubernetes` section after connecting the corresponding provider integration.

## 2. [Self-hosted Kubernetes with K3S](k3s.md)

If you want to save money and have more control over your cluster, you can deploy a self-hosted Kubernetes cluster using K3S.

Connect your server from the `Kubernetes` section using the `Connect server` flow.

## 3. [Wodby Cloud](wodby-cloud.md)

If you want Wodby to create and manage the cluster for you, choose `Wodby Cloud` in Step 2 of the new application form.
Persistent Wodby Cloud clusters require a paid plan.

## Demo

[Demo](demo.md) is the temporary Wodby Cloud option for testing. Enable the `Demo` switch in the same Step 2 flow.
Demo clusters and their applications are deleted automatically after 24 hours.

## Related pages

- [Choose a Kubernetes option](choose-platform.md)
- [Wodby Cloud](wodby-cloud.md)
- [K3S](k3s.md)
