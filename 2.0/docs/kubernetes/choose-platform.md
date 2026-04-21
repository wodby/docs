# Choose a Kubernetes Option

Wodby supports four practical deployment paths:

- managed Kubernetes in your own cloud account
- self-hosted Kubernetes with K3S on your own server
- persistent Wodby Cloud clusters
- temporary Wodby Cloud demo clusters

## Quick recommendation

- Choose **Managed Kubernetes** when you want production-ready cloud infrastructure in your own provider account.
- Choose **K3S** when you want lower infrastructure cost and you are comfortable operating your own server.
- Choose **Wodby Cloud** when you want Wodby to handle cluster creation and operations for you.
- Choose **Demo** when you only need a short-lived test environment for up to 24 hours.

## Comparison

| Option | Runs where | Created from | Best for | Who manages infra | Billing model |
| --- | --- | --- | --- | --- | --- |
| Managed Kubernetes | Your cloud account | `Kubernetes` after connecting a provider integration | Production workloads with cloud-native flexibility | You and your cloud provider | Your cloud bill plus Wodby platform usage |
| K3S | Your own server | `Kubernetes > Connect server` | Cost-sensitive self-hosted setups | You | Your server costs plus Wodby platform usage |
| Wodby Cloud | Wodby-managed infrastructure | `Apps > New app > Step 2` | Teams that want less cluster ops work | Wodby | Wodby compute credits |
| Demo | Temporary Wodby Cloud cluster | `Apps > New app > Step 2 > Wodby Cloud > Demo` | Evaluation, prototypes, short-lived testing | Wodby | Free, deleted after 24 hours |

## When to choose Managed Kubernetes

Choose Managed Kubernetes when:

- you already operate in AWS, GCP, Azure, DigitalOcean, OVH, or another supported provider
- you want cluster resources to stay in your own cloud account
- you expect to scale infrastructure policies, networking, or compliance over time

## When to choose K3S

Choose K3S when:

- you control one or more Linux servers already
- you want Kubernetes without managed-cluster provider costs
- you are comfortable handling server lifecycle, networking, and host-level troubleshooting

## When to choose Wodby Cloud

Choose Wodby Cloud when:

- you want the fastest path to a persistent cluster
- you do not want to wire cloud credentials or bootstrap your own server
- you prefer Wodby-managed cluster operations

Persistent Wodby Cloud clusters require a paid plan.

## When to choose Demo

Choose Demo when:

- you want to try Wodby quickly
- you need a disposable cluster for testing
- you do not need the cluster or app to survive past the evaluation window

Demo clusters and their deployed applications are deleted automatically after 24 hours.

## Related pages

- [Kubernetes overview](index.md)
- [Managed Kubernetes](managed.md)
- [K3S](k3s.md)
- [Wodby Cloud](wodby-cloud.md)
- [Demo cluster](demo.md)
