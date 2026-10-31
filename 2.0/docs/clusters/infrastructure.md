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

## Cluster components

To see the infrastructure software running on a cluster, open `Clusters > [Cluster] > Infrastructure > Components`. The
list shows each component's version, whether an update is available, where it runs, and how many pods or nodes run it.
It includes system pods and each node's Kubernetes agent, container runtime, operating system, and kernel. Your
applications are not included. Infrastructure apps are hidden because the `Apps` tab reports them; choose
`Infrastructure app` in the `Managed by` filter to show them.

A healthy cluster's list appears within a few minutes and refreshes about every six hours. The page shows when the
cluster was last checked. A cluster that isn't healthy keeps its last list until it recovers.

`Status` shows an update only when Wodby can apply it, and links to where to run it. A newer upstream release alone does
not count. On managed clusters, only Amazon EKS add-ons show updates. See
[component updates](updates.md#component-updates).

`Managed by` tells you how a component gets updated:

| Managed by | How it is updated |
| --- | --- |
| Wodby | An [infrastructure version upgrade](updates.md#infrastructure-version-upgrades) or a [component update](updates.md#component-updates). |
| Infrastructure app | An [infrastructure app upgrade](updates.md#infrastructure-updates). |
| k3s | Comes with the K3S release. A [Kubernetes version update](updates.md#kubernetes-version-updates) updates it. |
| Provider | Run by your Kubernetes provider. A [Kubernetes version update](updates.md#kubernetes-version-updates) can update it. On Amazon EKS, a [component update](updates.md#component-updates) can update add-ons. |
| Server | The operating system of your K3S server. You update it. |
| Other | Installed outside Wodby, or not recognized. Update it however it was installed. |

The version is the image tag or the version the node reports, exactly as published. It's empty for an image referenced
only by digest.

The list is also available through the API as `GET /v1/cluster-components/{id}`, using the cluster's ID, and the GraphQL
`clusterComponents` query.

## Cluster capability policy

A cluster capability policy records which published operator stack revisions are approved for the cluster.
It is separate from the infrastructure apps installed during cluster creation.

!!! warning "Policy storage only"

    Automatic operator installation and deployment dependency enforcement are not available yet. Saving
    `autoInstall: true` does not install operators or make a capability-dependent application ready to deploy.
    Leave it disabled for normal use.

New approvals must reference revisions you can access. Private stacks must match the cluster's organization
and ownership scope. Enabling the flag revalidates all retained approvals. Disabling it or removing stale approvals
does not require renewed access to those revisions.

### API fields

The REST cluster settings object `clusterCapabilities` contains:

- `autoInstall`: required boolean when submitting the object; disabled by default.
- `stackRevisionIds`: required array of up to 128 unique, positive integer IDs identifying approved, published stack
  revisions. These are revision IDs, not stack IDs.

Omitting `clusterCapabilities` preserves the existing policy. If the object is supplied, both fields must be present
and non-null. An explicit empty array clears the approved revisions; an explicit `false` disables the flag.

GraphQL uses `stackRevisionIDs` with string-valued IDs. MCP update input uses
`cluster_capabilities.auto_install` and `cluster_capabilities.stack_revision_ids`; its output uses the REST-style
`clusterCapabilities`, `autoInstall`, and `stackRevisionIds` names. See the
[API reference](https://wodby.com/docs/2.0/api/) for endpoints and schemas.

For service authors, see the [cluster capability declaration reference](../services/template.md#clustercapabilities).

## App environment network policies

When a regular app environment is deployed, Wodby creates or updates Kubernetes `NetworkPolicy` resources in the app
environment namespace. These policies provide namespace-level ingress isolation for app workloads.

Wodby installs app environment network policies on clusters where NetworkPolicy enforcement is supported in the Wodby
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

For each supported app environment namespace, Wodby manages these ingress policies:

| Policy | Effect |
| --- | --- |
| `wodby-deny-ingress` | Selects all pods in the app environment namespace and denies ingress unless another policy allows it. |
| `wodby-allow-same-namespace` | Allows ingress from other pods in the same app environment namespace. App services inside the same app environment can still communicate with each other. |
| `wodby-allow-edge` | Allows ingress from the `envoy-gateway` and `ingress-nginx` namespaces so Wodby's public edge components can reach app services. |

On self-hosted K3S and DigitalOcean Kubernetes clusters, Wodby also allows the cluster's own nodes to reach pods in
app environment namespaces. Without this, a node cannot reach an app pod that runs on another node, and an app that
mounts shared storage served from inside the cluster can stay in `ContainerCreating` on a cluster with several nodes.
App environments remain isolated from each other.

These policies affect ingress only. Wodby does not restrict egress with these policies, and does not generate per-service
or per-port NetworkPolicy rules from app links.

## Infrastructure versions

Infrastructure versions describe Wodby's cluster-level platform wiring. They are not the same thing as Kubernetes
versions or infrastructure app stack revisions.

Wodby marks a cluster as outdated only when there is an applicable infrastructure upgrade for that cluster type. For
example, version `3.0.0` is a K3S-specific networking upgrade. Managed Kubernetes clusters on version `2.0.0` are not
marked as outdated solely because `3.0.0` exists.

The latest version is `4.1.3`. Self-hosted K3S clusters are offered each version in order. Managed Kubernetes and Wodby
Cloud clusters are offered upgrades up to `4.0.0`, because later versions need no upgrade on them. They can show any
version from `4.0.0` to `4.1.3`, depending on when they were created.

Open `Clusters > [Cluster] > Infrastructure > Operations` to see a cluster's current version and any upgrade on offer.

### Changelog

#### 4.1.3

Version `4.1.3` updates Cilium on self-hosted K3S clusters to `1.19.10` and keeps your Cilium settings. Clusters must be
on `4.1.2` first. New K3S servers install this version directly. Managed Kubernetes clusters are not changed.

The new Cilium release includes these security fixes:

- [CVE-2026-56743](https://github.com/cilium/cilium/security/advisories/GHSA-fm8w-2m5w-9j7r): a Kubernetes NetworkPolicy
  can unexpectedly allow ingress from the local namespace.
- [CVE-2026-56742](https://github.com/cilium/cilium/security/advisories/GHSA-w7c2-w76w-5hmj): namespaced HTTPRoutes can
  redirect traffic to other namespaces. This affects Cilium's own Gateway API support. Wodby routes traffic through
  Envoy Gateway instead.
- Cilium no longer trusts the compromised eMudhra intermediate CA certificates.

Cilium restarts on each node during the upgrade, so run it during a maintenance window for production workloads. If the
upgrade fails, the cluster is marked as errored. Review the task logs, resolve the reported problem, and run the upgrade
again.

#### 4.1.2

Version `4.1.2` updates and verifies the host CA trust store on self-hosted K3S servers following the eMudhra
intermediate CA compromise. It restarts K3S to reload trust, including when the operating system has already applied
the CA fix. Run it during a maintenance window.

See the [K3S host CA security update](updates.md#k3s-host-ca-security-update-412) for upgrade steps, retry behavior,
and the separate updates needed for application CA bundles.

#### 4.1.1

Version `4.1.1` lets the nodes of a self-hosted K3S cluster reach app pods on other nodes. It fixes apps with shared
storage that could not start on K3S clusters with several nodes. The upgrade does not restart apps.

New K3S and DigitalOcean Kubernetes clusters are set up this way when they are created. Existing DigitalOcean
Kubernetes clusters get the same change with their next app deployment. Other managed Kubernetes clusters are not
changed by this version and need no upgrade.

#### 4.1.0

Version `4.1.0` enables Kubernetes Secret encryption at rest for new and existing self-hosted K3S clusters, improving
protection for Secret values stored in the cluster datastore.

#### 4.0.1

Version `4.0.1` strengthens network security for self-hosted K3S clusters.

#### 4.0.0

Version `4.0.0` separates HTTP routing deployment from app-service deployment.

Envoy Gateway remains the single public load-balancer entrypoint for the cluster. Wodby gives each regular app environment
its own routing release below that entrypoint. The routing release manages the app environment's Gateway API listeners,
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
- creates the app environment routing releases

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

The upgrade excludes paused app environments. A paused environment migrates automatically during its next full deployment
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
- redeploys user applications so app environment network policies are applied

For managed Kubernetes clusters, version `3.0.0` does not replace the provider's CNI. It records that the cluster uses
the current Wodby infrastructure model. This version does not introduce a required action for managed Kubernetes clusters
that already use version `2.0.0`.

#### 2.0.0

Ingress Nginx was replaced with Envoy Gateway for public HTTP, HTTPS, TCP, and UDP entrypoints.

#### 1.0.0

Introduced FRPC as the reverse proxy client used to connect to the Kubernetes API.

#### 0.1.0

The first version of the Kubernetes cluster infrastructure.
