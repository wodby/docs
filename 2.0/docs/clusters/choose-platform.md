# Choose a cluster option

Choose where your applications will run and who will manage the cluster:

| Option | Runs where | Choose it when | Who manages infrastructure | Billing |
| --- | --- | --- | --- | --- |
| [Managed Kubernetes](managed.md) | Your cloud account | You want to keep resources in your own cloud account and use its Kubernetes service | You and your cloud provider | Cloud provider charges plus Wodby platform usage |
| [K3S](k3s.md) | Your own server | You want to use your own Linux server and can manage its lifecycle, networking, and troubleshooting | You | Server costs plus Wodby platform usage |
| [Wodby Cloud](wodby-cloud.md) | Wodby-managed infrastructure | You want Wodby to create and operate the cluster | Wodby | Wodby Cloud usage; requires a paid plan |
| [Demo](demo.md) | Temporary Wodby Cloud cluster | You need a short-lived environment to evaluate Wodby | Wodby | Free; deleted after 24 hours |

Demo clusters are deleted automatically after 24 hours. Applications deployed to them are deleted with them.

## Create or connect a cluster

- **Managed Kubernetes:** connect a supported [provider integration](../providers/kubernetes.md), then create the
  cluster from `Clusters`.
- **K3S:** open `Clusters > Connect server` and follow the [server setup instructions](k3s.md).
- **Wodby Cloud:** open `Clusters > New Wodby Cloud cluster`, or select Wodby Cloud in Step 2 of app creation.
- **Demo:** turn on the `Demo` switch when creating a Wodby Cloud cluster.

See [Clusters](index.md) for environment restrictions, updates, and monitoring.
