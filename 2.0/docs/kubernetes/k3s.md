# Self-hosted Kubernetes cluster with K3S

If you want to save money and have more control over your cluster, you can deploy a self-hosted Kubernetes cluster using K3S.

!!! info "Why use K3S instead of Managed Kubernetes?"
    Learn about <a href="https://wodby.com/blog/affordable-kubernetes-with-k3s" target="_blank">benefits of K3S</a> from our blog

[K3S](https://k3s.io/) is a certified lightweight distribution of Kubernetes.

## Requirements

* A server with at least 2GB of RAM and 2 CPUs
* A server with dedicated (non-shared) CPU
* Supported OS: Ubuntu/Debian, Fedora/CentOS, OpenSUSE
* Currently, we support only amd64 machines
* At least 20GB of disk space

For more see [k3s requirements](https://docs.k3s.io/installation/requirements) from the official documentation.

## Installation

- Click "new k3s cluster" from "Kubernetes" page in Wodby dashboard
- Enter cluster name
- You will be redirected to the cluster page where you can find the command that you need to execute with root privileges on the server
- The command will install k3s, kubectl, helm chart for our proxy client to security connect to the Kubernetes API
- After all installation complete the command will initiate connection with Wodby, if successful Wodby will start deploying infrastructure applications such as Ingress Nginx and Monitoring
- Once the cluster is ready you can start deploying your applications
