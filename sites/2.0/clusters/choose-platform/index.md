Source: https://wodby.com/docs/2.0/clusters/choose-platform/

# Choose a cluster option

Choose where your applications will run and who will manage the cluster:

| Option | Runs where | Choose it when | Who manages infrastructure | Billing |
| --- | --- | --- | --- | --- |
| [Managed Kubernetes](https://wodby.com/docs/2.0/clusters/managed/) | Your cloud account | You want to keep resources in your own cloud account and use its Kubernetes service | You and your cloud provider | Cloud provider charges plus Wodby platform usage |
| [K3s](https://wodby.com/docs/2.0/clusters/k3s/) | Your own server | You want to use your own Linux server and can manage its lifecycle, networking, and troubleshooting | You | Server costs plus Wodby platform usage |
| [Wodby Cloud](https://wodby.com/docs/2.0/clusters/wodby-cloud/) | Wodby-managed infrastructure | You want Wodby to create and operate the cluster | Wodby | Wodby Cloud usage; requires a paid plan |
| [Demo](https://wodby.com/docs/2.0/clusters/demo/) | Temporary Wodby Cloud cluster | You need a short-lived environment to evaluate Wodby | Wodby | Free; deleted after 24 hours |

Demo clusters are deleted automatically after 24 hours. Applications deployed to them are deleted with them.

## Create or connect a cluster

- **Managed Kubernetes:** connect a supported [provider integration](https://wodby.com/docs/2.0/providers/kubernetes/), then create the
  cluster from `Clusters`.
- **K3s:** open `Clusters > Connect server` and follow the [server setup instructions](https://wodby.com/docs/2.0/clusters/k3s/).
- **Wodby Cloud:** open `Clusters > New Wodby Cloud cluster`, or select Wodby Cloud in Step 2 of app creation.
- **Demo:** turn on the `Demo` switch when creating a Wodby Cloud cluster.

See [Clusters](https://wodby.com/docs/2.0/clusters/) for environment restrictions, updates, and monitoring.
