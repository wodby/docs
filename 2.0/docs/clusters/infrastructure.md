# Cluster infrastructure

Wodby provides core cluster capabilities through infrastructure apps deployed during cluster creation.

These infrastructure apps can include:

- Envoy Gateway
- Monitoring
- FRPC proxy tunnel for secure connection to the Kubernetes API
- Additional controller applications (e.g. AWS Load Balancer controller for EKS cluster)

Infrastructure apps follow the same general stack-and-version model as regular apps, so they can be upgraded and
configured. Their configuration surface is narrower than a normal user application.

Wodby tracks two separate kinds of cluster infrastructure updates:

- infrastructure app stack revisions, for updates to the apps that provide platform capabilities
- infrastructure versions, for cluster-level platform wiring changes such as networking or routing behavior

See [Kubernetes cluster updates](updates.md) for manual and automatic infrastructure upgrade behavior.

New clusters use Envoy Gateway for public HTTP and HTTPS entrypoints. TCP and UDP entrypoints are also available when the
cluster's Gateway API bundle includes the corresponding experimental route types. New self-hosted K3S clusters include
those route types and also use Cilium for Kubernetes networking and NetworkPolicy enforcement.

Older clusters may still run Ingress Nginx, or may run K3S with the default flannel networking and kube-router network
policy controller, until their cluster infrastructure is upgraded.

## App instance network policies

When a regular app instance is deployed, Wodby creates or updates Kubernetes `NetworkPolicy` resources in the app
instance namespace. These policies provide namespace-level ingress isolation for app workloads.

Wodby installs app instance network policies on clusters where NetworkPolicy enforcement is supported in the Wodby
cluster setup:

- self-hosted K3S clusters on infrastructure version `3.0.0` or newer
- AWS EKS clusters
- Azure AKS clusters created by Wodby with Azure CNI Overlay and the AKS-managed Cilium dataplane
- DigitalOcean Kubernetes clusters, including single-node clusters
- Google Kubernetes Engine clusters
- OVH Managed Kubernetes clusters

Wodby does not install these policies for:

- cluster and infrastructure apps
- self-hosted K3S clusters with infrastructure version older than `3.0.0`
- legacy or imported Azure AKS clusters whose NetworkPolicy capability is not tracked by Wodby
- clusters where the provider or NetworkPolicy enforcement capability is unknown

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

#### 4.1.0

Version `4.1.0` enables Kubernetes Secret encryption at rest for self-hosted K3S clusters. New K3S clusters use the
`secretbox` provider from their first server start. Existing supported K3S clusters use a staged infrastructure upgrade
that restarts K3S, rotates the encryption key, and rewrites the current version of every Secret with `secretbox` before
the version is recorded as complete.

Managed Kubernetes providers own control-plane datastore encryption. Version `4.1.0` does not change provider-managed
control-plane settings or restart managed cluster nodes.

See [K3S Secret encryption at rest](k3s.md#secret-encryption-at-rest) for compatibility, verification, backup, and
datastore-history details.

#### 4.0.1

Version `4.0.1` strengthens network security for self-hosted K3S clusters.

#### 4.0.0

Version `4.0.0` separates HTTP routing deployment from app-service deployment.

Envoy Gateway remains the single public load-balancer entrypoint for the cluster. Wodby gives each regular app instance
its own routing release below that entrypoint. The routing release manages the app instance's Gateway API listeners,
HTTP routes, TLS certificates, HTTP authentication, and route policies. App-service releases continue to manage
application workloads and their internal Kubernetes Services.

During an upgrade from an older infrastructure version, Wodby:

- checks the Envoy Gateway infrastructure app and upgrades it to the required stack revision when necessary; this is
  included in the infrastructure version upgrade, so you do not need to upgrade infrastructure app stacks separately
  first
- reconciles the cluster entrypoint and verifies the stable Gateway API ListenerSet resources needed for the new routing
  model; Envoy Gateway `1.8.0` or newer is required
- keeps compatible provider-managed Standard Gateway API resources in place; on DigitalOcean Kubernetes, Wodby can use
  the provider's supported ownership handoff when the managed resources are too old
- records whether TCP and UDP route types are available on the cluster
- reconciles existing app-service releases to remove their legacy routing resources without rebuilding or redeploying
  application workloads
- creates the app-instance routing releases

##### Gateway API compatibility

Wodby checks the Gateway API resources actually installed on the cluster instead of assuming their capabilities from
the Kubernetes provider or a version label. A compatible provider-managed bundle remains under the provider's control;
Wodby does not replace it merely to take ownership. A Wodby-managed bundle is upgraded together with the Envoy Gateway
infrastructure app.

Provider handling during the `4.0.0` upgrade is:

| Existing Gateway API management | Upgrade behavior |
| --- | --- |
| DigitalOcean Kubernetes | A compatible provider-managed bundle is retained. If it is too old, Wodby uses DigitalOcean's supported handoff to stop provider management before upgrading it. |
| GKE or AKS provider integration | A compatible provider-managed bundle is retained. An incompatible bundle is not overwritten; upgrade the cluster or its provider-managed Gateway API integration, then retry. |
| Wodby-managed bundle, normally used on Wodby-created EKS, OVH, and K3S clusters | Wodby upgrades the bundle. |
| Other externally managed bundle | A compatible bundle is retained. Its external owner must upgrade an incompatible bundle before the infrastructure upgrade can continue. |

Imported or customized clusters can differ from their provider's usual setup, so the live ownership and capability
check is authoritative.

TCP and UDP route types are optional because they are not part of the Gateway API Standard channel. A cluster can use
infrastructure `4.0.0` for HTTP and HTTPS while showing TCP or UDP port publishing as unavailable. Availability is
tracked separately for each protocol. The upgrade stops before changing routing ownership if an existing published port
depends on an unavailable route type; unpublish that port or make the corresponding Gateway API route type available
before retrying.

Open `Infrastructure > Overview` on the cluster to see the detected CRD channel and management, Envoy Gateway
controller version, HTTP/HTTPS and ListenerSet readiness, and TCP and UDP availability in a dedicated Gateway API
section. Port pages explain unavailable protocols and prevent new ports of those protocols from being published. HTTP
and HTTPS routing is unaffected when only TCP or UDP support is unavailable.

The upgrade excludes paused app instances. A paused instance migrates automatically during its next full deployment
after it is resumed. Infrastructure apps are also excluded because the cluster-wide entrypoint remains part of the
infrastructure release.

After migration, route, route-setting, authentication, and certificate changes can be deployed without rebuilding or
redeploying application services. See [routing deployments](../apps/deploys.md#routing-deployments).

#### 3.0.0

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
