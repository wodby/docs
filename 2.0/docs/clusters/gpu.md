# GPU node pools

A GPU node pool adds GPU nodes to a [managed Kubernetes](managed.md) cluster, next to its default node pool. Use it
for app services that need GPUs, such as model inference with vLLM, without making every node a GPU node.

GPU nodes run only the app services that request GPUs. Everything else stays on the default node pool.

## Supported clusters

GPU node pools are available for these managed Kubernetes clusters:

| Provider | GPU machine types | Minimum GPU nodes |
|---|---|---|
| [DigitalOcean (DOKS)](../providers/digitalocean.md#doks) | GPU optimized Droplets | `0` or more |
| [AWS (EKS)](../providers/aws.md#eks) | NVIDIA instance types, such as `g5`, `g6`, `g6e` and `p5` | `1` or more |
| [Google Cloud (GKE)](../providers/gcp.md#gke) | G2 (NVIDIA L4), A2 (NVIDIA A100) and A3 (NVIDIA H100/H200) | `0` or more |

GPU node pools are not available for AKS, OVH, serverless clusters, [single-node clusters](managed.md#single-node-clusters),
[K3S](k3s.md) clusters, [Wodby Cloud](wodby-cloud.md) or the [demo cluster](demo.md).

GPU nodes use images with NVIDIA drivers from the cloud provider, so you do not need to install drivers yourself.

!!! note "GPU quota"
    Most cloud accounts start with little or no GPU quota. Before you add a pool, make sure your account can create
    the GPU machine type in the cluster's region. For example, check the GPU limit on DigitalOcean, the
    `Running On-Demand G and VT instances` vCPU quota on AWS, or the GPU quota for the GPU model on Google Cloud.
    Request more from your cloud provider if needed.

## Add a GPU node pool

You can add a GPU node pool when you create a cluster, or later.

**When you create a cluster**, open the **GPU node pool (optional)** section of the cluster creation form, select
**Add a GPU node pool** and set:

- **GPU machine type**: only machine types with GPUs in the selected location are listed
- **Minimum # of GPU nodes**
- **Maximum # of GPU nodes**
- **GPU node disk size**, in GB, on providers where you choose the node disk size; at least `20`

**For an existing cluster**, go to `Clusters > [Cluster] > Infrastructure > Kubernetes`, and use **Add GPU node pool**
in the **GPU node pool** card. The cluster must be in the `OK` status. While Wodby creates the pool, the cluster status
is `Scaling`.

The cluster overview shows the pool's machine type and node counts in the **GPU node pool** row.

### Minimum and maximum nodes

- **DigitalOcean and Google Cloud**: a minimum of `0` lets the pool scale down when no app service requests GPUs, so you
  do not pay for idle GPU nodes. The cluster autoscaler adds GPU nodes when an app service needs them, up to the
  maximum.
- **AWS**: the pool always keeps its minimum number of nodes running, so the minimum is at least `1`.

On DigitalOcean, a new pool with a minimum of `0` starts with one node, and the autoscaler removes it when no app service
requests GPUs.

On Google Cloud, Wodby creates the GPU node pool in one zone of the cluster: the first of the cluster's zones that offers
the selected machine type.

## Change or remove the pool

Go to `Clusters > [Cluster] > Infrastructure > Kubernetes` and use the **GPU node pool** card:

- **Update GPU node pool** with the same machine type resizes the pool.
- **Update GPU node pool** with a different machine type creates a new pool first and removes the old pool after the new
  one is ready. You pay for both pools while the change runs.
- **Delete** removes the pool. Wodby refuses to remove it while app services on the cluster request GPUs. Remove the
  GPU request from those app services first, or delete them.

Changes to the pool can take several minutes, depending on the cloud provider. If a change fails, fix the cause, for
example GPU quota, and submit the change again.

## Run app services on GPU nodes

An app service runs on GPU nodes when its containers request GPUs. Some catalog services, such as vLLM, request a GPU
by default.

To request GPUs for an app service, set **GPU devices** in its [resources](../apps/scalability.md#resources-management):
the device name, such as `nvidia.com/gpu`, and the number of GPUs for each replica. A count of `0` turns off the GPU
request of the service's default configuration.

When the app service is deployed, Wodby schedules the pods that request GPUs on the GPU node pool. Pods that do not
request GPUs do not run on GPU nodes.

You can also manage the GPU node pool through the [Wodby API](../dev/api.md) and the [Wodby MCP server](../dev/mcp.md).
