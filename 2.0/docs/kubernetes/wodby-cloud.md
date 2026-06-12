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
- minimum number of nodes and maximum number of nodes for scalable clusters

You can also create a persistent Wodby Cloud cluster with the `Single-node cluster` checkbox. In this mode Wodby creates one fixed node, disables cluster scaling, and does not provision a cloud load balancer. Public app traffic is routed directly to the node IP. Public endpoint data is still shown in the cluster overview as `Public IPs` or `Hostname`.

Single-node Wodby Cloud clusters cannot be changed into scalable clusters later. If you need node scaling after creation, create a regular Wodby Cloud cluster and move the application there.

Use single-node Wodby Cloud only when a small non-high-availability cluster is acceptable.

Wodby then creates the cluster and deploys the application to it.

## Demo

Demo is the temporary Wodby Cloud mode for testing.

- free of charge
- created as a single-node cluster
- created from the same Step 2 flow
- automatically deleted after 24 hours together with deployed applications

## Billing

Wodby Cloud is billed in dollars as Wodby compute usage. See the live pricing page for current rates:
https://wodby.com/pricing

Compute usage is driven by:

- selected cluster machine type
- node count
- additional cluster fee for scalable clusters
- provisioned persistent storage for apps deployed to the cluster

Single-node Wodby Cloud clusters do not include the additional scalable-cluster fee.

Wodby Cloud is available in two regions: US and EU.

Paid plans include $24 of Wodby compute per month.
