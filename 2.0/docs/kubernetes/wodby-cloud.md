# Wodby Cloud

If you do not want to bring your own cloud account or server, you can use Wodby Cloud.

Wodby Cloud is Wodby's managed Kubernetes infrastructure. Wodby creates and operates the cluster for you.

## Creating a Wodby Cloud cluster

Wodby Cloud clusters are created from the new application flow:

1. Start creating a new application
2. In Step 2 choose `Wodby Cloud`
3. Either enable `Demo` or configure a persistent cluster
4. Complete the app creation flow

Unlike managed Kubernetes and K3S, Wodby Cloud clusters are not created from the _Kubernetes_ page.

## Persistent Wodby Cloud clusters

Persistent Wodby Cloud clusters require a paid subscription.

When creating one, you choose:

- region
- CPU type
- machine type
- minimum number of nodes
- maximum number of nodes

Wodby then creates the cluster and deploys the application to it.

## Demo

Demo is the temporary Wodby Cloud mode for testing.

- free of charge
- created from the same Step 2 flow
- automatically deleted after 24 hours together with deployed applications

## Billing

Wodby Cloud is billed in compute credits. See the live pricing page for current rates:
https://wodby.com/pricing

Compute-credit usage is driven by:

- cluster base cost, which mostly covers shared infrastructure such as the load balancer
- shared CPU on cluster nodes
- dedicated CPU on cluster nodes
- cluster node RAM
- persistent block storage used by apps deployed to the cluster

Wodby Cloud is available in two regions: US and EU.

Paid plans include 1000 compute credits per month.
