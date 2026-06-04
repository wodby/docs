# Kubernetes cluster infrastructure

Wodby provides core cluster capabilities through infrastructure apps deployed during cluster creation.

These infrastructure apps can include:

- Envoy Gateway
- Monitoring
- FRPC proxy tunnel for secure connection to the Kubernetes API
- Additional controller applications (e.g. AWS Load Balancer controller for EKS cluster)

Infrastructure apps follow the same general stack-and-version model as regular apps, so they can be upgraded and configured. Their configuration surface is narrower than a normal user application.

New clusters use Envoy Gateway for public HTTP, HTTPS, TCP, and UDP entrypoints. New self-hosted K3S clusters also use
Cilium for Kubernetes networking and NetworkPolicy enforcement.

Older clusters may still run Ingress Nginx, or may run K3S with the default flannel networking and kube-router network
policy controller, until their cluster infrastructure is upgraded.

## App instance network policies

When a regular app instance is deployed, Wodby creates or updates Kubernetes `NetworkPolicy` resources in the app
instance namespace. These policies provide namespace-level ingress isolation for app workloads.

Wodby installs app instance network policies on clusters where NetworkPolicy enforcement is supported in the Wodby
cluster setup:

- self-hosted K3S clusters on infrastructure version `3.0.0` or newer
- AWS EKS clusters
- DigitalOcean Kubernetes clusters
- Google Kubernetes Engine clusters
- OVH Managed Kubernetes clusters

Wodby does not install these policies for:

- cluster and infrastructure apps
- clusters with infrastructure version older than `3.0.0`
- Azure AKS clusters, because NetworkPolicy enforcement is not enabled in the current Wodby AKS template
- clusters where the provider or NetworkPolicy enforcement capability is unknown
- single-node managed clusters that use node-direct gateway routing, because the gateway uses host networking

For each supported app instance namespace, Wodby manages these ingress policies:

| Policy | Effect |
| --- | --- |
| `wodby-deny-ingress` | Selects all pods in the app instance namespace and denies ingress unless another policy allows it. |
| `wodby-allow-same-namespace` | Allows ingress from other pods in the same app instance namespace. App services inside the same app instance can still communicate with each other. |
| `wodby-allow-edge` | Allows ingress from the `envoy-gateway` and `ingress-nginx` namespaces so Wodby's public edge components can reach app services. |

These policies affect ingress only. Wodby does not restrict egress with these policies, and does not generate per-service
or per-port NetworkPolicy rules from app links.

## Infrastructure versions

Infrastructure versions describe Wodby's cluster-level platform wiring. They are not the same thing as Kubernetes
versions or infrastructure app stack revisions.

Wodby marks a cluster as outdated only when there is an applicable infrastructure upgrade for that cluster type. For
example, version `3.0.0` is a K3S-specific networking upgrade. Managed Kubernetes clusters on version `2.0.0` are not
marked as outdated solely because `3.0.0` exists.

### Changelog

#### 3.0.0

This is the current infrastructure version for new clusters.

For K3S clusters, version `3.0.0` means Cilium is used for pod networking and NetworkPolicy enforcement.

For new K3S clusters, the bootstrap script installs K3S with flannel disabled and the built-in K3S network policy
controller disabled, then installs Cilium.

For existing K3S clusters on version `2.0.0`, the infrastructure upgrade:

- hardens public access to the K3S API endpoint
- disables K3S flannel networking
- disables the built-in K3S network policy controller
- removes stale kube-router network policy rules from the host
- installs Cilium
- redeploys user applications so app instance network policies are applied

For managed Kubernetes clusters, version `3.0.0` does not replace the provider's CNI. It records that the cluster uses
the current Wodby infrastructure model. This version does not introduce a required action for managed Kubernetes clusters
that already use version `2.0.0`.

#### 2.0.0

Ingress Nginx was replaced with Envoy Gateway for public HTTP, HTTPS, TCP, and UDP entrypoints.

#### 1.0.0

Introduced FRPC as the reverse proxy client used to connect to the Kubernetes API.

#### 0.1.0

The first version of the Kubernetes cluster infrastructure.
