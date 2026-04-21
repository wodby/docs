# Self-hosted Kubernetes cluster with K3S

If you want to keep infrastructure under your control and avoid managed Kubernetes costs, you can connect your own server to Wodby as a K3S cluster.

!!! info "Why use K3S instead of Managed Kubernetes?"
    Learn more about the <a href="https://wodby.com/blog/affordable-kubernetes-with-k3s" target="_blank">benefits of K3S</a> in our blog

[K3S](https://k3s.io/) is a certified lightweight distribution of Kubernetes.

## Requirements

- A server with at least 2 GB of RAM and 2 CPUs
- A server with dedicated, non-shared CPU
- Supported OS: Ubuntu/Debian, Fedora/CentOS, OpenSUSE
- Currently only `amd64` machines are supported
- At least 20 GB of disk space

For more details, see the official [K3S installation requirements](https://docs.k3s.io/installation/requirements).

## Connect server flow

1. Open `Kubernetes > Connect server` in the dashboard.
2. Select the project where the cluster should live.
3. Enter the cluster name and title.
4. Decide whether to leave `Enable monitoring` turned on. It is enabled by default.
5. Create the cluster.

New K3S clusters are created in the `Awaiting` state. This means Wodby is waiting for you to run the generated installation command on your server.

## Installation command

After creation, Wodby redirects you to the cluster page and shows a one-time installation command.

- Run the command on the target server as `root` or with `sudo`
- The download token inside that command expires after 15 minutes
- If it expires, reload the cluster page to generate a fresh command

The generated script performs the current bootstrap flow for you. It:

- disables swap
- installs required NFS client packages
- installs K3S
- installs Helm
- prepares local kubeconfig on the server
- installs Wodby's proxy client so the cluster can securely connect back to Wodby
- sends the final initialization request to Wodby

## What happens next

After the script completes successfully, Wodby initializes the cluster and deploys the required infrastructure components.

- Ingress Nginx is deployed for HTTP routing
- Monitoring components are deployed if you left monitoring enabled
- The cluster moves out of `Awaiting` and eventually becomes ready for app deployments

Once the cluster is ready, create new apps and choose that cluster from `My clusters`.

## Troubleshooting

- If the command has expired, reload the cluster page and use the new command.
- If the cluster stays in `Awaiting`, the bootstrap script likely never completed the final initialization step.
- If the script fails, fix the server issue first and then rerun a fresh command from the cluster page.
- Make sure the server can reach the public internet and the Wodby API endpoints during installation.
