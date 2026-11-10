# Choose a cluster option

Choose where your applications will run. On every option, Wodby creates or connects the cluster and keeps Kubernetes
and the [cluster infrastructure](infrastructure.md) up to date, so the choice is mostly about where the resources live
and how they are billed:

| Option | Runs where | Choose it when | What is left to you | Billing |
| --- | --- | --- | --- | --- |
| [Managed Kubernetes](managed.md) | Your cloud account | You want to keep resources in your own cloud account and use its Kubernetes service | Your cloud account and its quotas. The provider runs the Kubernetes control plane | Cloud provider charges plus Wodby platform usage |
| [K3S](k3s.md) | Your own server | You want the lowest cost on your own Linux server and don't need Kubernetes scaling | The server itself and its [operating system and kernel updates](k3s.md#operating-system-and-kernel-updates) | Server costs plus Wodby platform usage |
| [Wodby Cloud](wodby-cloud.md) | Wodby-hosted infrastructure | You don't want a cloud account or server of your own | Nothing: Wodby hosts the cluster | Wodby Cloud usage; requires a paid plan |
| [Demo](demo.md) | Temporary Wodby Cloud cluster | You need a short-lived environment to evaluate Wodby | Nothing: Wodby hosts the cluster | Free; deleted after 24 hours |

Demo clusters are deleted automatically after 24 hours. Applications deployed to them are deleted with them.

## Create or connect a cluster

- **Managed Kubernetes:** connect a supported [provider integration](../providers/kubernetes.md), then create the
  cluster from `Clusters`.
- **K3S:** open `Clusters > Connect server` and follow the [server setup instructions](k3s.md).
- **Wodby Cloud:** open `Clusters > New Wodby Cloud cluster`, or select Wodby Cloud in Step 2 of app creation.
- **Demo:** turn on the `Demo` switch when creating a Wodby Cloud cluster.

See [Clusters](index.md) for environment restrictions, updates, and monitoring.
