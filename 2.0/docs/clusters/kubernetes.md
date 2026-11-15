---
description: Upgrade a cluster's Kubernetes version in Wodby, turn on automatic upgrades, update cluster components, scale the cluster and recycle worker nodes.
---

# Kubernetes updates and node operations

Manage a cluster's Kubernetes version, its components and its worker nodes at `Clusters > [Cluster] > Kubernetes`:

- `Updates`: [upgrade the Kubernetes version](#kubernetes-version-updates), set up
  [automatic Kubernetes upgrades](#automatic-kubernetes-upgrades) and run [component updates](#component-updates).
- `Operations`, on managed Kubernetes clusters: [scale the cluster](#scale-the-cluster) and
  [recycle worker nodes](#worker-node-updates).

Wodby infrastructure version and infrastructure app updates are separate. See [Cluster updates](updates.md).

## Kubernetes versions for new clusters

The creation form of a [managed Kubernetes](managed.md) cluster lists the Kubernetes versions the cloud provider
offers for the selected location, starting from the oldest version Wodby supports, with the recommended version
selected. A new version appears as soon as the provider offers it. When a provider publishes full patch or build versions, Wodby selects the latest available release
of the recommended version. When a provider accepts only a minor version, the provider selects and maintains the patch
release.

Existing clusters use a provider-specific upgrade plan based on their current version. A cluster on a version that new
clusters can no longer use may need to install a provider-approved patch before it can upgrade to the next minor
version.

## Kubernetes version updates

Kubernetes version updates are separate from Wodby infrastructure version and infrastructure app updates. Wodby reads
the current cluster state and asks the provider for direct upgrade targets each time you open the `Kubernetes > Updates`
tab. The plan is cluster-specific rather than a generic list of Kubernetes releases.

Wodby supports this workflow for:

- Amazon EKS
- Azure AKS
- Google GKE Standard clusters
- DigitalOcean Kubernetes
- OVH Managed Kubernetes
- self-hosted K3s clusters

GKE Autopilot and other serverless clusters do not use this workflow. Kubernetes versions for Wodby Cloud clusters are
managed by Wodby and cannot be changed manually.

### Upgrade policy

Wodby filters the provider's direct targets to keep upgrades incremental and recoverable:

- If a newer patch is available in the current Kubernetes minor, only the newest available patch is offered first. On
  DigitalOcean Kubernetes and Google GKE, this includes a newer provider build of the same Kubernetes version, such as
  `1.36.5-do.1` to `1.36.5-do.2`, because providers can ship security fixes that way.
- After the current minor is patched, you can move to the immediately following minor version. On K3s, it is offered only
  after your current minor version reaches end of life. On managed clusters you can choose it earlier, but it shows as
  an update only after end of life.
  The dashboard labels this step `Major`, because a new Kubernetes minor version can remove APIs your workloads use.
- On K3s, a minor version the cluster's Cilium doesn't support yet is not offered, and the plan names the Cilium version
  to update to first. Patches of your current minor version are still offered.
- Skipping a minor or changing the Kubernetes major version is not offered as a direct upgrade.
- Preview Kubernetes versions are excluded.

The plan shows provider warnings and blockers before an upgrade starts. An upgrade is blocked when the cluster is not
in `OK` status, when the provider integration is unavailable, or when the version reported by the provider does not
match the version observed through the Kubernetes API. Resolve the reported condition and load the plan again.

### Known vulnerabilities

The known vulnerabilities of your cluster's Kubernetes version are listed with the cluster's other vulnerabilities on
`Clusters > [Cluster] > Infrastructure > Security`. See [Cluster security](security.md#kubernetes-version). A row with a
fixed version links to `Update Kubernetes`, which opens `Kubernetes > Updates`.

The same list for Kubernetes alone is available through the [MCP tool](../dev/mcp/tools.md)
`list_cluster_kubernetes_vulnerabilities`.

### Run an upgrade

Open `Clusters`, select the cluster, and go to `Kubernetes > Updates`. In the `Kubernetes version` card, select
one of the available direct targets, and start the upgrade. Run production upgrades during a maintenance window: on a
managed cluster the provider replaces every worker node, even for a patch, and the Kubernetes API can be temporarily
unavailable. The confirmation dialog of a managed cluster warns that all nodes will be replaced. See
[How upgrades affect your apps](#how-upgrades-affect-your-apps).

The upgrade runs as a task and puts the cluster into `Upgrading` status. Wodby:

1. Records the source and target versions in the task and lists your nodes.
2. Starts or resumes the provider upgrade.
3. Waits for the provider operation to complete.
4. Verifies that the Kubernetes API reports the target and that every node is `Ready`.
5. Records the observed version and returns the cluster to normal operation.
6. Lists your nodes again and [shows what changed](#check-what-changed-on-your-nodes).

Open the task to follow progress and review provider details. If an upgrade fails after the provider has applied it to
the control plane or some node pools, repeat the failed task. The retry detects the partially applied target and resumes
the remaining stages instead of trying to start an unrelated transition.

### How upgrades affect your apps

A Kubernetes version update, including a patch version, can restart your apps:

- **Managed Kubernetes:** providers update worker nodes by replacing them, even for a patch or a newer provider build
  of the same version, such as `1.36.5-do.2` to `1.36.5-do.3`. Kubernetes moves your pods from each old node to its
  replacement, so every pod restarts once. An app that keeps a volume can take longer, because the volume has to detach
  from the old node and attach to the new one.
- **DigitalOcean Kubernetes:** before the upgrade, Wodby turns on surge upgrades for the cluster. DigitalOcean then
  starts a replacement node before it removes an old one, so your pods have somewhere to move. The extra node is billed
  while it runs, and your DigitalOcean account needs room for one more Droplet.
- **K3s:** Wodby updates K3s in place. The server node isn't drained, so apps on it keep running, and the Kubernetes API
  is unavailable for a short time while K3s restarts. In clusters with agent nodes, Wodby drains each agent node in
  turn, so pods on agent nodes restart once.

On a single-node cluster, an app with one replica is unavailable while its pod restarts. On a single-node managed
cluster, all apps are unavailable for a few minutes, because the only node is replaced. To keep an app available during
upgrades, run the cluster with at least two nodes and the app with at least two replicas.

### Amazon EKS add-ons

On Amazon EKS, the upgrade also updates the vpc-cni, kube-proxy, CoreDNS, and EBS CSI driver add-ons after the nodes. Each
moves to the version AWS marks as the default for the target Kubernetes version. Add-ons that are already newer are not
downgraded, and add-ons several releases behind move one minor version at a time. Settings Wodby applied when it created
the cluster are kept.

EKS installs kube-proxy and CoreDNS as self-managed workloads when a cluster is created. The first upgrade replaces them
with EKS-managed add-ons, which restarts their pods. Changes you made directly to those workloads, such as a custom CoreDNS
configuration, can be overwritten.

If this stage fails, repeat the failed task. The retry leaves the control plane and nodes as they are and resumes the
add-on updates. An EKS cluster without the EKS-managed vpc-cni or EBS CSI driver add-on keeps those components unchanged.

### Automatic Kubernetes upgrades

Wodby can upgrade a cluster's Kubernetes version and apply its [component updates](#component-updates) for you during
a time window you choose. An automatic upgrade is the same upgrade you can start from the `Kubernetes version` card, and
it follows the same [upgrade policy](#upgrade-policy).

Automatic Kubernetes upgrades are on by default for K3s clusters, for patch versions only. Wodby upgrades K3s in place,
so apps on the server node keep running. To create a K3s cluster without them, clear
`Auto upgrade Kubernetes and components` in the cluster creation form.

On managed Kubernetes clusters, automatic Kubernetes upgrades are off by default. Every upgrade of a managed cluster
replaces all of its nodes, even for a patch, so every pod restarts and a single-node cluster is unavailable for a few
minutes. See [How upgrades affect your apps](#how-upgrades-affect-your-apps). Turn them on only if your apps can be
unavailable for a few minutes during the time window, for example on a cluster with at least two nodes and apps with at
least two replicas. To create a managed cluster with them, select `Auto upgrade Kubernetes and components` in the
cluster creation form. Managed clusters that already had them on were switched off when this default changed; turn them
on again in the `Kubernetes auto upgrade settings` card if you want them.

Wodby Cloud clusters and serverless clusters such as GKE Autopilot don't have them.

To change them:

1. Open `Clusters > [Cluster] > Kubernetes > Updates`.
2. In the `Kubernetes auto upgrade settings` card, turn `Auto upgrade` on or off.
3. Under `Version changes`, choose which upgrades Wodby can start. Select at least one:
    - `Patch versions`: a newer patch of the current minor version, such as `1.36.4` to `1.36.5`. This includes a newer
      provider build of the same version, such as `1.36.5-do.1` to `1.36.5-do.2`.
    - `Minor versions`: the next minor version, such as `1.36` to `1.37`. With
      `Only after the current minor reaches end of life` selected, Wodby waits until your current minor version reaches
      end of life. While its end-of-life date is unknown, Wodby doesn't start the upgrade.
4. Under `Components`, keep `Include component updates` selected to let Wodby also apply
   [component updates](#component-updates), or clear it to run them yourself. It's selected by default.
5. Set the [time window](../automation-time-windows.md) and save.

When component updates are included, the same `Version changes` apply to them:

- `Patch versions` allows a component update that stays within the component's minor version, such as Cilium `1.19.9`
  to `1.19.10`.
- `Minor versions` allows larger component updates, such as Cilium `1.18` to `1.19`. On Amazon EKS, it also allows
  replacing an add-on copy that EKS installed with an EKS-managed add-on, which can overwrite a custom configuration.
  `Only after the current minor reaches end of life` applies only to the Kubernetes version.

By default only `Patch versions` is selected. Patch versions bring security and bug fixes and keep your cluster on the
same minor version. A new minor version can remove Kubernetes APIs your workloads use, so check your workloads before
you allow minor upgrades.

New clusters get a `02:00` to `04:00` window in your organization's time zone. Clusters created before automatic
Kubernetes upgrades were available get the same hours in `UTC` unless you've changed the setting, so check the window
and its time zone. With `Time window` turned off, an upgrade can start at any time.

If you don't want Wodby to upgrade a cluster's Kubernetes version automatically, turn `Auto upgrade` off. Your choice is
kept.

#### When an upgrade starts

Wodby checks every 30 minutes. It starts an upgrade when the time window is open, the cluster is in `OK` status, no
other upgrade or [blocking app activity](updates.md#app-activity-during-infrastructure-upgrades) is running, and the
policy allows the next version.

The Kubernetes version comes first. When there's no version upgrade to start, Wodby applies the next component update
the policy allows instead. On K3s, a new Kubernetes minor version waits until the cluster runs a Cilium version that
supports it, so a Cilium update can come before that upgrade. Without `Include component updates`, that upgrade
waits until you update Cilium yourself. On Amazon EKS, a Kubernetes version upgrade already
updates the add-ons.

An automatic upgrade affects your apps the same way as a manual one. See
[How upgrades affect your apps](#how-upgrades-affect-your-apps).

Wodby runs one automatic upgrade or component update on a cluster at a time. If an infrastructure version upgrade is
pending and [automatic infrastructure upgrades](updates.md#automatic-infrastructure-upgrades) will apply it, Wodby runs
it first, during its own time window. The Kubernetes upgrade starts after it. Pending infrastructure app upgrades wait for the
Kubernetes upgrade.

Some providers keep clusters up to date on their own, so automatic patch upgrades often have nothing left to do:

- OVH Managed Kubernetes clusters created by Wodby update themselves.
- Google upgrades GKE clusters enrolled in a release channel.
- Amazon EKS applies control plane patches itself.

#### Tasks and failures

An automatic upgrade or component update runs as a task, the same as a manual one. Task history shows it as started by
Wodby.

If an automatic upgrade fails before the provider starts changing the cluster, the cluster returns to `OK`. Wodby
doesn't try the same version again automatically for 24 hours. If it fails after the provider has started, the cluster
stays in an error state and Wodby stops automatic upgrades for it. Open the failed task, resolve the reported problem,
and repeat the task. See [Run an upgrade](#run-an-upgrade).

If an automatic component update fails, the cluster returns to `OK` and the update stays available. Wodby doesn't try
the same update again automatically for 24 hours. You can run it yourself from the `Component updates` card.

Wodby sends email notifications when an automatic Kubernetes version upgrade succeeds or fails. You can manage these
from `User settings > Notifications`. Automatic Kubernetes upgrades also appear in the weekly organization report.
Automatic component updates don't send notifications, so check the cluster's task history for them.

## Component updates

Some cluster components can be updated on their own, without a Kubernetes or infrastructure upgrade. When an update is
available, the `Component updates` card appears under the `Kubernetes version` card at
`Clusters > [Cluster] > Kubernetes > Updates`. Choose `Update` and confirm to run it as a task.

[Automatic Kubernetes upgrades](#automatic-kubernetes-upgrades) also apply component updates. They're on by default for
K3s clusters, so with the default settings you don't need to run K3s patch updates yourself. On managed clusters they're
off by default, so you run component updates yourself unless you turn automatic Kubernetes upgrades on. To run them only
yourself, clear `Include component updates` in the `Kubernetes auto upgrade settings` card.

| Cluster | Components |
| --- | --- |
| K3s | Cilium, once the cluster's Wodby infrastructure version is up to date. |
| Amazon EKS | The VPC CNI, kube-proxy, CoreDNS, and EBS CSI driver add-ons. The update moves them to the AWS default for the cluster's Kubernetes version. |

Other cluster types don't offer component updates, because the provider manages these components. They change with a
[Kubernetes version update](#kubernetes-version-updates) or the provider's own patches.

Before you update:

- The cluster must be in `OK` status, and deployments on it wait until the update finishes.
- On K3s, Cilium restarts on each node, so run the update during a maintenance window for production workloads.
  Automatic updates start only inside the automatic Kubernetes upgrade time window.
- On EKS, the first update of a copy that EKS installed replaces it with an EKS-managed add-on. This restarts its pods
  and can overwrite changes made directly to it, such as a custom configuration.

If an update fails, the task shows the error and the cluster returns to `OK`. The update stays available, so you can
run it again.

## Scale the cluster

Set the minimum and maximum node counts of a [managed Kubernetes](managed.md) cluster at
`Clusters > [Cluster] > Kubernetes > Operations`. See [Cluster scalability](scalability.md) for the node count rules of
each provider and how autoscaling works.

## Worker node updates

Wodby has no separate node update. On [managed Kubernetes](managed.md) clusters, worker nodes get a newer image and kernel
in one of two ways:

- **Recycle nodes** replaces nodes without changing the Kubernetes version. It's available on Amazon EKS, Azure AKS and
  DigitalOcean Kubernetes, except for single-node clusters. Use `Recycle nodes` at
  `Clusters > [Cluster] > Kubernetes > Operations`, the
  [`wodby cluster recycle-nodes`](../cli/wodby_cluster_recycle-nodes.html) command, or the [API](../api/index.html).
- **A [Kubernetes version update](#kubernetes-version-updates)** moves nodes to the image that comes with the new version.
  It's available on all managed providers that support version updates, including Google GKE.

Which one delivers a given fix depends on your provider, so check its release notes first.

On [K3s](k3s.md), you own the server, so you update its operating system and kernel yourself. See
[Operating system and kernel updates](k3s.md#operating-system-and-kernel-updates) for the steps.

### Check what changed on your nodes

A successful task doesn't always mean your nodes changed. For example, Amazon EKS leaves a node group alone if it already
runs the latest image, and a Kubernetes version update on K3s keeps your servers.

To check, open the task's log. Recycling and Kubernetes version update tasks list each node's name, creation time, kernel,
and operating system at their start and end. They then compare the two lists:

```text
Compared with the start of this task: 2 replaced or removed, 2 new, 0 not replaced
Kernel at the start: 6.12.96 (2 nodes); at the end: 6.12.113 (2 nodes)
```

Look for these lists in the `Nodes before recycling` and `Nodes after recycling` steps of a recycling task, and in the
`Upgrade plan` and `Outcome` steps of a Kubernetes version update. The task also lists your nodes at the end if it fails,
because a failed task can leave some nodes replaced. If Wodby can't read your nodes, the log says so, and this doesn't
change the task's result.

The log doesn't tell you whether a kernel is fixed, because distributions backport fixes to older version numbers. Compare
the version with the one your provider lists.

When the task ends, the [`Components` list](infrastructure.md#cluster-components) also shows the new kernel and operating
system, with the number of nodes running each.

### Fix CVE-2026-98432 on managed Kubernetes

[CVE-2026-98432](https://nvd.nist.gov/vuln/detail/CVE-2026-98432) is a critical Linux kernel bug in your worker nodes.
Wodby infrastructure upgrades don't change managed nodes. Your cluster can show version `4.1.4`, but that doesn't protect it
from this bug. To fix the bug, move your nodes to a patched image from your provider.

To see whether your nodes have the fix, open `Clusters > [Cluster] > Infrastructure > Security`. The
[vulnerabilities table](security.md) shows CVE-2026-98432 as **Fixed** or **Not fixed**. When the nodes aren't fixed,
the row links to the operation that fixes them, `Recycle nodes` or `Update Kubernetes`. If your provider doesn't offer a fixed
image yet, the row has no link. While the nodes aren't fixed, the cluster shows a red bug icon next to its name in the
`Clusters` list, and a red dot on its `Infrastructure` and `Security` tabs.

Wodby reads this from the node images of EKS and AKS node pools, and from the kernel and GKE versions that DigitalOcean
and GKE nodes report. It checks once a day, and again when a task that replaces nodes, such as `Recycle nodes` or a
Kubernetes version update, finishes. If your provider replaces nodes on its own, for example through automatic
upgrades, the new result can take up to a day to appear. A new cluster shows its first result within about 15
minutes.

The row doesn't appear when Wodby can't tell, for example on OVH Managed Kubernetes, on GKE nodes that run Ubuntu or
GKE 1.37, and on AKS FIPS node images. Follow the steps below for those clusters. The same results are available through
the [API](../api/index.html) as `GET /v1/cluster-security-advisories/{id}` and the [MCP tool](../dev/mcp/tools.md)
`list_cluster_security_advisories`.

1. Check your provider's security bulletin to confirm that it has released a patched node image. For example, see the
   [AWS bulletin](https://aws.amazon.com/security/security-bulletins/2026-160-aws/).
2. Replace your nodes during a maintenance window, using the option for your cluster:

    | Cluster | How to replace nodes |
    | --- | --- |
    | Amazon EKS | Recycle nodes. Each managed node group moves to its latest image, and a group already on it isn't changed. |
    | Azure AKS | Recycle nodes. Every node is replaced, so first confirm the latest image contains the fix. |
    | DigitalOcean Kubernetes | Run a [Kubernetes version update](#kubernetes-version-updates) to a version that the [DigitalOcean changelog](https://docs.digitalocean.com/products/kubernetes/details/changelog/) lists with Linux kernel `6.12.113-1` or newer. DigitalOcean ships kernel updates with its Kubernetes versions. |
    | Google GKE | Run a [Kubernetes version update](#kubernetes-version-updates) to a version that Google lists as fixed. Recycling isn't available. |
    | OVH Managed Kubernetes | Recycling isn't available. Check with OVHcloud whether your nodes have received the fix. |

    See [Worker node updates](#worker-node-updates) for how to recycle nodes.

3. [Check what changed on your nodes](#check-what-changed-on-your-nodes), and confirm that they run the fixed version from
   your provider. A successful task alone doesn't prove that the node image included the fix.

Wodby operates the nodes of Wodby Cloud clusters, so you can't replace them yourself.
