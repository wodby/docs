# UpCloud

## Auth

UpCloud integrations use an API token.

1. In the UpCloud Control Panel, open **Account** → **API tokens** and create a token.
2. Leave **Allowed IP ranges** open. Wodby calls the UpCloud API from its own servers.
3. Copy the token. It starts with `ucat_` and is shown only once.
4. In Wodby, create an UpCloud integration and paste the token.

UpCloud tokens can't be limited to Kubernetes: a token can manage everything in the account or workspace that owns it.
A token is valid for at most a year. Update the integration with a new token before it expires, or Wodby can no longer
create, scale or delete your clusters.

## Kubernetes

Wodby creates clusters in UpCloud Managed Kubernetes.

- Wodby creates a private network for each cluster and deletes it with the cluster.
- Nodes have public IP addresses.
- UpCloud does not add or remove nodes automatically. A cluster has a fixed number of nodes, which you set when you
  create it and can change later from the cluster's settings.
- Single-node clusters are supported. Their gateway listens on the node's public IP address, so they need no load
  balancer.
- Node disk size comes with the selected machine type and cannot be changed.
- Wodby deploys Metrics Server for basic Kubernetes monitoring.
- Wodby deploys Envoy Gateway behind one UpCloud load balancer per cluster for public app entrypoints. The load balancer
  passes the visitor's IP address to your apps.
- UDP ports can be published only on single-node clusters. UpCloud's load balancer forwards TCP only.
- Kubernetes version upgrades and node recycling are not available for UpCloud clusters yet.

### Billing options

Choose one when you create a cluster:

| Option | Control plane | Load balancer |
| --- | --- | --- |
| Development | One API server, free | One server, free |
| Production | Three API servers, highly available | Two servers, highly available |

UpCloud bills the Production control plane and load balancer, the worker nodes, and the disks. An UpCloud account can
have five free load balancers. When they are used up, a new Development cluster gets UpCloud's cheapest paid load
balancer instead. See [UpCloud's pricing](https://upcloud.com/pricing/) for current prices.

### Storage

Persistent storage uses UpCloud Block Storage. Wodby adds three storage classes to every UpCloud cluster:

| Storage class | Tier |
| --- | --- |
| `wodby-maxiops` (default) | MaxIOPS |
| `wodby-standard` | Standard |
| `wodby-hdd` | HDD |

Disks are encrypted at rest and deleted together with their volume. UpCloud's own storage classes keep a disk after its
volume is deleted, so Wodby hides them from volume selection.

### Deleting a cluster

UpCloud keeps a cluster's load balancers and disks after the cluster is deleted and continues to bill for them. When
you delete an UpCloud cluster in Wodby, Wodby also deletes the cluster's load balancers, its disks and its private
network. If one of them can't be deleted, the task shows a warning: delete it in the UpCloud Control Panel.
