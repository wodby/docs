# Cluster updates

Cluster updates are managed from the dashboard at `Clusters > [Cluster] > Infrastructure`.

Wodby tracks two update states for each cluster:

- Wodby infrastructure version updates
- infrastructure app stack updates

The cluster can show that updates are available when either state is outdated. If both are outdated, update the Wodby
infrastructure version first. Wodby's automatic upgrade flow uses the same order.

## Infrastructure updates

[Infrastructure apps](infrastructure.md) are managed with the same stack-and-version model as regular apps.

When Wodby releases an update to one of the infrastructure services, a new infrastructure stack revision becomes
available and the cluster is marked as having outdated infrastructure apps. You can then upgrade the infrastructure app
stacks manually, or let Wodby upgrade them automatically when automatic infrastructure upgrades
are enabled.

Infrastructure app updates can include changes to platform services such as Envoy Gateway, monitoring, the FRPC proxy
tunnel, or provider-specific controller apps.

In the dashboard, open `Clusters`, select the cluster, and go to `Infrastructure > Operations`. The
`Infrastructure app stacks` card shows whether stack updates are available. When Wodby can identify the affected
infrastructure apps, the card lists each app and the current and target stack revision numbers.

### Review an infrastructure app changelog

Select `Show changelog` in the `Infrastructure app stacks` card to load the changes for the currently available upgrade.
Wodby recalculates the current upgrade targets when you open the changelog. The result is grouped by infrastructure app
and shows its current and target stack versions and revision numbers.

For each app, the changelog identifies stack services that will be added, removed, or moved to another service
revision. For a newer semantic service version, published notes include stable release tags after the current version
through the target version. For same-version revision changes or other version formats, Wodby can show the target tag's
notes when the service is tag-backed. Release notes come from the Git provider, so some service updates show that no
published release notes were found.

The changelog summarizes stack service membership and service revision changes. A newer stack revision can contain no
service revision changes and still change configuration such as environment variables, Helm values, links, or
resources. The changelog calls out this case, but it is not a complete configuration diff.

The `Infrastructure Apps` tab lists the infrastructure apps installed on the cluster. Use it when you need to inspect
the app list or open an individual infrastructure app page.

## Infrastructure version upgrades

Some changes affect the cluster-level infrastructure version rather than only an infrastructure app stack revision.
These upgrades can change cluster networking, routing, platform controllers, or host security.

An infrastructure version upgrade can include an upgrade of a required infrastructure app. This prerequisite is part
of the infrastructure version workflow even though the dashboard tracks general infrastructure app stack updates
separately; you do not need to run the separate infrastructure app stack upgrade first.

See [Kubernetes cluster infrastructure](infrastructure.md#infrastructure-versions) for infrastructure version details,
the changelog, current versions, and cluster-type-specific upgrade behavior.

Run K3S infrastructure version upgrades during a maintenance window for production workloads. Some updates restart K3S
or change networking and can briefly interrupt cluster access or application traffic. Review the changelog for the
offered update before starting it.

Infrastructure version `4.0.0` also performs a one-time routing ownership migration. Wodby first upgrades the Envoy
Gateway infrastructure app when required, reconciles the cluster entrypoint, and verifies Gateway API compatibility.
It then removes legacy routing resources from eligible app-service releases and creates independent app routing
releases without rebuilding or redeploying application workloads. HTTP and HTTPS traffic can be briefly interrupted
while an app environment is handed over from its service releases to its routing release. Run this upgrade during a
maintenance window for production applications.

The upgrade verifies the provider's Gateway API resources before beginning the ownership migration. HTTP/HTTPS
ListenerSet support is required. TCPRoute and UDPRoute support is optional, but the upgrade is blocked when an existing
published port uses an unavailable protocol so no port is silently disconnected. When a protocol is unavailable, the
cluster `Infrastructure > Overview` page and port page show the limitation and new ports of that protocol cannot be
published. See
[Gateway API compatibility](infrastructure.md#gateway-api-compatibility) for provider-specific ownership and upgrade
behavior.

Paused app environments are skipped during the cluster-wide 4.0 migration. They migrate automatically during their next
full deployment after being resumed; you do not need to unpause every environment before upgrading the cluster.

If both an infrastructure version upgrade and infrastructure app stack upgrade are pending, Wodby handles the
infrastructure version upgrade first. Infrastructure app upgrades are checked again after the cluster is no longer
outdated at the infrastructure version level.

In the dashboard, open `Clusters`, select the cluster, and go to `Infrastructure > Operations`. The
`Wodby infrastructure` card shows the current infrastructure version, the target version when an upgrade is available,
and a manual upgrade button. The manual button is disabled when no infrastructure version upgrade is available.

If the latest infrastructure version upgrade or infrastructure app stack upgrade failed and can be retried, the
dashboard shows `Retry available` and replaces the normal upgrade button with a re-run button for the failed task. Open
the failed task from the dialog when you need to review logs before re-running it.

### K3S host protection for CVE-2026-98432 (4.1.4)

!!! info "Self-hosted K3S only"
    Infrastructure version `4.1.4` applies to self-hosted K3S clusters. For managed Kubernetes clusters, see
    [Fix CVE-2026-98432 on managed Kubernetes](#fix-cve-2026-98432-on-managed-kubernetes).

[CVE-2026-98432](https://nvd.nist.gov/vuln/detail/CVE-2026-98432) is a critical Linux kernel bug. Someone on the network
can reach it by sending specially crafted TCP connection requests, without logging in. It can lead to running code as
root on the server.

This update reduces your exposure but doesn't fix the bug. To fix it, you also need to
[install a patched kernel](#install-a-patched-kernel).

#### Apply the update

Use an account with permission to upgrade the cluster.

1. Open `Clusters > [Cluster] > Infrastructure > Operations` and check the current version in the
   `Wodby infrastructure` card. If it already shows `4.1.4` or newer, this update is complete.
2. Choose a maintenance window and start the offered infrastructure version upgrade. If earlier versions are offered
   first, apply them in order until the cluster reaches `4.1.4`.
3. Follow the upgrade task and confirm that it succeeds and the card shows `4.1.4`.

Automatic infrastructure upgrades apply this update when enabled and permitted by the cluster's version policy and time
window.

#### What changes on the server

Wodby makes these changes and applies them again each time the server boots:

- It drops incoming IPv4 TCP packets that carry IP options, which is how the bug is triggered. Normal traffic doesn't use
  IP options.
- It turns off Multipath TCP (MPTCP) on the server, because the published exploit needs a service that accepts MPTCP.

Wodby then restarts K3S and Cilium so they stop accepting MPTCP. Cluster access can be briefly interrupted during the
restart.

Check these before you upgrade:

- Services you run directly on the server can't use MPTCP. Containers aren't affected, because each pod keeps its own
  setting.
- The server can't use IP options on TCP connections, including CIPSO security labels.

#### What it doesn't cover

An application running in a pod can still send these packets to other pods on the same server. If an attacker has already
compromised a pod, only a patched kernel protects your other pods.

#### Install a patched kernel

1. Check your operating system's status for this bug: [Ubuntu](https://ubuntu.com/security/CVE-2026-98432),
   [Debian](https://security-tracker.debian.org/tracker/CVE-2026-98432),
   [Red Hat Enterprise Linux](https://access.redhat.com/security/cve/CVE-2026-98432), or
   [SUSE](https://www.suse.com/security/cve/CVE-2026-98432.html). Other distributions publish their own status. Note
   the fixed kernel version for your release.
2. Follow [Update the kernel](k3s.md#update-the-kernel) to install the kernel and reboot the server.
3. Compare the version `uname -r` shows with the fixed version from step 1. Distributions backport fixes, so compare
   against your distribution's version rather than the upstream kernel version.

If your distribution hasn't released a fix yet, keep version `4.1.4` in place and check again later. If your operating
system release no longer gets fixes, see [Unsupported operating system releases](k3s.md#unsupported-operating-system-releases).

The protections stay on after you install the patched kernel. You don't need to remove them, and normal traffic isn't
affected by them. Wodby applies them again each time the server boots, whichever kernel it runs.

#### If the update fails

The task reports the error and leaves the infrastructure version unchanged. Wodby returns the cluster to `OK` if no
separate health problem prevents that.

The server needs `iptables` with the `u32` match or `nftables` to drop these packets. If it has neither, install
`nftables` and retry the update. New K3S servers without either tool finish installing with a warning in the output, and
they don't have this protection until you install one and run `/usr/local/bin/wodby-k3s-firewall`.

### K3S host CA security update (4.1.2)

!!! info "Self-hosted K3S only"
    Infrastructure version `4.1.2` applies to self-hosted K3S clusters. Managed Kubernetes clusters do not use this host
    update.

This update addresses host trust in certificate chains affected by the eMudhra intermediate CA compromise. See
[Mozilla's security advisory](https://www.openwall.com/lists/oss-security/2026/10/20/1) and, for Ubuntu servers,
[Ubuntu security notice USN-8944-1](https://ubuntu.com/security/notices/USN-8944-1).

#### Apply the update

Use an account with permission to upgrade the cluster.

1. Open `Clusters > [Cluster] > Infrastructure > Operations` and check the current version in the
   `Wodby infrastructure` card. If it already shows `4.1.2` or newer, this infrastructure update is complete.
2. Choose a maintenance window and start the offered infrastructure version upgrade. If earlier versions are offered
   first, review their changelog and apply them in order until the cluster reaches `4.1.2` or newer.
3. Follow the upgrade task and confirm that it succeeds and the card shows `4.1.2` or newer.

Automatic infrastructure upgrades can apply this patch when enabled and permitted by the cluster's version policy and
time window. Check the current version and task history if a security email refers to an update that has already run.

#### What changes on the server

Wodby checks the host CA trust stores, updates the operating system's CA packages when needed, and verifies that the
affected CA keys are no longer trusted. The update uses the distribution's package manager and requires a CA package
that removes the affected trust. Package mirrors must be reachable when a package update is needed.

If the host trust stores already pass verification, Wodby skips package downloads. It still restarts K3S so the running
service reloads trust instead of retaining cached certificates. Cluster access can be temporarily interrupted during
the restart. Wodby verifies the connection and host trust again before recording the new infrastructure version.

#### If the update fails

The task reports the error and leaves the infrastructure version unchanged. Failure of this security update alone
does not put the cluster into a failed state: Wodby returns it to `OK` if no separate health problem prevents that.
App deployments waiting for the upgrade can resume when the cluster is `OK`. An actual connectivity or health problem
can still affect cluster status.

Review the task logs, resolve the reported condition, and retry. For example, the distribution may not yet provide a
CA package that removes all affected trust, a package mirror may be unavailable, or custom host trust settings may need
manual review. Installing the latest available package is not sufficient if verification still finds affected CAs.

#### Update application trust separately

This upgrade checks the server's host trust stores. Application containers, language runtimes, and custom CA bundles
can keep their own trust stores. Update affected images or runtime bundles and rebuild or redeploy applications as
needed. Other host services that cache CA trust may also need a reload or restart.

Removing trust can make HTTPS connections to legitimate endpoints under the removed roots fail. If an application
depends on such an endpoint, arrange a replacement certificate chain with its operator.

## App activity during infrastructure upgrades

These rules apply to infrastructure upgrades, [Kubernetes version updates](#kubernetes-version-updates),
[component updates](#component-updates), and node recycling.

Before starting an upgrade, Wodby checks for application work that could change cluster resources or be cut off by
the upgrade. An upgrade cannot start while the cluster has active app creation or deletion, deployments,
post-deployment scripts, app stack upgrades, service uninstall tasks, infrastructure app builds, backups, cron jobs,
app service actions, or database and database user tasks. Wait for those operations to finish and then retry the
upgrade. Automatic upgrade attempts skip a busy cluster and try again during a later scheduled check.

Regular app builds can continue and do not prevent an upgrade from starting. If a build makes its deployment ready
while the cluster is upgrading, the deployment remains `awaiting` and Wodby starts it automatically after the cluster
returns to `ok`. After a failed infrastructure upgrade, deployment waits until the cluster returns to `ok`. The
[K3S host protection](#k3s-host-protection-for-cve-2026-98432-414) and
[K3S host CA](#k3s-host-ca-security-update-412) security updates restore that status after a failed attempt unless a
separate health problem prevents it.

While an upgrade is running, new app environment creation or deletion, direct deployments, post-deployment script retries,
and app stack upgrades cannot start on that cluster. Operations that are part of the infrastructure upgrade itself
continue normally.

Backups, cron jobs, app service actions, and database tasks on the cluster that start while an upgrade is running wait
for it. Their tasks show `Waiting for cluster maintenance to finish` and run when the upgrade ends, so a scheduled
backup or cron job that comes due during the upgrade runs a little late instead of failing. A task still stops at its
usual time limit if the upgrade takes longer: one hour for cron jobs and app service actions, about six hours for
backups.

Manual infrastructure version upgrades and manual infrastructure app stack upgrades are not available for Wodby Cloud
clusters. Wodby Cloud infrastructure is operated by Wodby and can still be upgraded automatically by Wodby.

## Automatic infrastructure upgrades

Automatic infrastructure upgrades are configured per cluster with separate controls for two upgrade types:

| Control | Applies to |
| --- | --- |
| Infrastructure | Cluster-level infrastructure version upgrades |
| Infrastructure apps | Infrastructure app stack revision upgrades |

Each upgrade type has its own semver-only policy. The policy controls whether automatic patch, minor, and major semver
updates are allowed. By default, patch and minor updates are allowed, and major updates are not.

Infrastructure app stacks can also follow a newer stack revision that keeps the same stable semantic version. This is
useful when an infrastructure service is republished without changing its version. Same-version revision upgrades are
enabled by default and apply only to infrastructure app stacks. Cluster-level infrastructure versions must still move
to a newer semantic version, and prerelease or non-semver targets are not selected automatically.

Each upgrade type has its own `Auto upgrade` switch. Disabling both switches disables automatic infrastructure upgrades
for the cluster.

Each upgrade type can also use its own [automation time window](../automation-time-windows.md), so cluster
infrastructure version upgrades and infrastructure app stack upgrades can start during different selected hours.

Version policy settings affect automatic upgrades only. You can still run a manual infrastructure or infrastructure app
upgrade when the dashboard offers one.

In the dashboard, open `Infrastructure > Operations`. Each upgrade type has its own card:

- `Wodby infrastructure auto upgrade settings`
- `Infrastructure apps auto upgrade settings`

Each section has an `Auto upgrade` switch and `Patch versions`, `Minor versions`, and `Major versions` policy
checkboxes. The infrastructure app stacks section also has a `Same version (newer revisions)` checkbox. Same-version,
patch, and minor updates are enabled by default. `Major versions` is visible but is not enabled by default.

### Defaults by cluster type

| Cluster type | Default |
| --- | --- |
| Wodby Cloud | Enabled and locked on. Major automatic upgrades are not allowed. |
| Managed Kubernetes in your cloud account | Enabled in the dashboard creation form. You can disable it during creation or later from `Infrastructure > Operations`. |
| K3S | Enabled in the dashboard creation form. You can disable it during creation or later from `Infrastructure > Operations`. |

Wodby Cloud clusters always keep automatic infrastructure upgrades enabled because Wodby operates the cluster
infrastructure. The dashboard shows these settings as managed by Wodby. Major automatic upgrades remain disabled for
Wodby Cloud.

### Notifications and tasks

Automatic infrastructure upgrades create tasks, the same as manual upgrades. Task history shows whether Wodby upgraded
the cluster infrastructure version or infrastructure app stacks.

Wodby sends email notifications when automatic infrastructure upgrades succeed or fail. You can manage these from
`User settings > Notifications`.

## Component updates

Some cluster components can be updated on their own, without a Kubernetes or infrastructure upgrade. When an update is
available, the `Component updates` card appears above the component list at
`Clusters > [Cluster] > Infrastructure > Components`. Choose `Update` and confirm to run it as a task.

| Cluster | Components |
| --- | --- |
| K3S | Cilium, once the cluster's Wodby infrastructure version is up to date. |
| Amazon EKS | The VPC CNI, kube-proxy, CoreDNS, and EBS CSI driver add-ons. The update moves them to the AWS default for the cluster's Kubernetes version. |

Other cluster types don't offer component updates, because the provider manages these components. They change with a
[Kubernetes version update](#kubernetes-version-updates) or the provider's own patches.

Before you update:

- The cluster must be in `OK` status, and deployments on it wait until the update finishes.
- On K3S, Cilium restarts on each node, so run the update during a maintenance window for production workloads.
- On EKS, the first update of a copy that EKS installed replaces it with an EKS-managed add-on. This restarts its pods
  and can overwrite changes made directly to it, such as a custom configuration.

If an update fails, the task shows the error and the cluster returns to `OK`. The update stays available, so you can
run it again.

## Worker node updates

Wodby has no separate node update. On [managed Kubernetes](managed.md) clusters, worker nodes get a newer image and kernel
in one of two ways:

- **Recycle nodes** replaces nodes without changing the Kubernetes version. It's available on Amazon EKS, Azure AKS and
  DigitalOcean Kubernetes, except for single-node clusters. Use `Recycle nodes` at
  `Clusters > [Cluster] > Infrastructure > Kubernetes`, the
  [`wodby cluster recycle-nodes`](../cli/wodby_cluster_recycle-nodes.html) command, or the [API](../api/index.html).
- **A [Kubernetes version update](#kubernetes-version-updates)** moves nodes to the image that comes with the new version.
  It's available on all managed providers that support version updates, including Google GKE.

Which one delivers a given fix depends on your provider, so check its release notes first.

On [K3S](k3s.md), you own the server, so you update its operating system and kernel yourself. See
[Operating system and kernel updates](k3s.md#operating-system-and-kernel-updates) for the steps.

### Check what changed on your nodes

A successful task doesn't always mean your nodes changed. For example, Amazon EKS leaves a node group alone if it already
runs the latest image, and a Kubernetes version update on K3S keeps your servers.

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

## Kubernetes version updates

Kubernetes version updates are separate from Wodby infrastructure version and infrastructure app updates. Wodby reads
the current cluster state and asks the provider for direct upgrade targets each time you open the `Kubernetes` tab.
The plan is cluster-specific rather than a generic list of Kubernetes releases.

Wodby supports this workflow for:

- Amazon EKS
- Azure AKS
- Google GKE Standard clusters
- DigitalOcean Kubernetes
- OVH Managed Kubernetes
- self-hosted K3S clusters

GKE Autopilot and other serverless clusters do not use this workflow. Kubernetes versions for Wodby Cloud clusters are
managed by Wodby and cannot be changed manually.

### Upgrade policy

Wodby filters the provider's direct targets to keep upgrades incremental and recoverable:

- If a newer patch is available in the current Kubernetes minor, only the newest available patch is offered first. On
  DigitalOcean Kubernetes and Google GKE, this includes a newer provider build of the same Kubernetes version, such as
  `1.36.5-do.1` to `1.36.5-do.2`, because providers can ship security fixes that way.
- After the current minor is patched, you can move to the immediately following minor version. On K3S, it is offered only
  after your current minor version reaches end of life. On managed clusters you can choose it earlier, but it shows as
  an update only after end of life.
  The dashboard labels this step `Major`, because a new Kubernetes minor version can remove APIs your workloads use.
- Skipping a minor or changing the Kubernetes major version is not offered as a direct upgrade.
- Preview Kubernetes versions are excluded.

The plan shows provider warnings and blockers before an upgrade starts. An upgrade is blocked when the cluster is not
in `OK` status, when the provider integration is unavailable, or when the version reported by the provider does not
match the version observed through the Kubernetes API. Resolve the reported condition and load the plan again.

### Run an upgrade

Open `Clusters`, select the cluster, and go to `Infrastructure > Kubernetes`. In the `Kubernetes version` card, select
one of the available direct targets, and start the upgrade. Run production upgrades during a maintenance window:
the provider can rotate control-plane components and worker nodes, and the Kubernetes API can be temporarily
unavailable.

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

- **Managed Kubernetes:** providers usually update worker nodes by replacing them. Kubernetes moves your pods from each
  old node to its replacement, so every pod restarts once. An app that keeps a volume can take longer, because the
  volume has to detach from the old node and attach to the new one.
- **DigitalOcean Kubernetes:** before the upgrade, Wodby turns on surge upgrades for the cluster. DigitalOcean then
  starts a replacement node before it removes an old one, so your pods have somewhere to move. The extra node is billed
  while it runs, and your DigitalOcean account needs room for one more Droplet.
- **K3S:** Wodby updates K3S in place. The server node isn't drained, so apps on it keep running, and the Kubernetes API
  is unavailable for a short time while K3S restarts. In clusters with agent nodes, Wodby drains each agent node in
  turn, so pods on agent nodes restart once.

On a single-node cluster, an app with one replica is unavailable while its pod restarts. To keep an app available during
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

Wodby can upgrade a cluster's Kubernetes version for you during a time window you choose. An automatic upgrade is the
same upgrade you can start from the `Kubernetes version` card, and it follows the same
[upgrade policy](#upgrade-policy).

Automatic Kubernetes upgrades are on by default for every cluster, for patch versions only. Wodby Cloud clusters and
serverless clusters such as GKE Autopilot don't have them.

To change them:

1. Open `Clusters > [Cluster] > Infrastructure > Kubernetes`.
2. In the `Kubernetes auto upgrade settings` card, turn `Auto upgrade` on or off.
3. Under `Version changes`, choose which upgrades Wodby can start. Select at least one:
    - `Patch versions`: a newer patch of the current minor version, such as `1.36.4` to `1.36.5`. This includes a newer
      provider build of the same version, such as `1.36.5-do.1` to `1.36.5-do.2`.
    - `Minor versions`: the next minor version, such as `1.36` to `1.37`. With
      `Only after the current minor reaches end of life` selected, Wodby waits until your current minor version reaches
      end of life. While its end-of-life date is unknown, Wodby doesn't start the upgrade.
4. Set the [time window](../automation-time-windows.md) and save.

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
other upgrade or [blocking app activity](#app-activity-during-infrastructure-upgrades) is running, and the policy allows
the next version.

An automatic upgrade affects your apps the same way as a manual one. See
[How upgrades affect your apps](#how-upgrades-affect-your-apps).

Wodby runs one automatic upgrade on a cluster at a time. If an infrastructure version upgrade is pending and
[automatic infrastructure upgrades](#automatic-infrastructure-upgrades) will apply it, Wodby runs it first, during its
own time window. The Kubernetes upgrade starts after it. Pending infrastructure app upgrades wait for the Kubernetes
upgrade.

Some providers keep clusters up to date on their own, so automatic patch upgrades often have nothing left to do:

- OVH Managed Kubernetes clusters created by Wodby update themselves.
- Google upgrades GKE clusters enrolled in a release channel.
- Amazon EKS applies control plane patches itself.

#### Tasks and failures

An automatic upgrade runs as a task, the same as a manual one. Task history shows it as started by Wodby.

If an automatic upgrade fails before the provider starts changing the cluster, the cluster returns to `OK`. Wodby
doesn't try the same version again automatically for 24 hours. If it fails after the provider has started, the cluster
stays in an error state and Wodby stops automatic upgrades for it. Open the failed task, resolve the reported problem,
and repeat the task. See [Run an upgrade](#run-an-upgrade).

Wodby sends email notifications when an automatic Kubernetes upgrade succeeds or fails. You can manage these from
`User settings > Notifications`. Automatic Kubernetes upgrades also appear in the weekly organization report.
