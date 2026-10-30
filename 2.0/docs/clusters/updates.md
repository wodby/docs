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

Before starting either type of infrastructure upgrade, Wodby checks for application work that could change cluster
resources. An upgrade cannot start while the cluster has active app creation or deletion, deployments,
post-deployment scripts, app stack upgrades, service uninstall tasks, or infrastructure app builds. Wait for those
operations to finish and then retry the upgrade. Automatic upgrade attempts skip a busy cluster and try again during a
later scheduled check.

Regular app builds can continue and do not prevent an upgrade from starting. If a build makes its deployment ready
while the cluster is upgrading, the deployment remains `awaiting` and Wodby starts it automatically after the cluster
returns to `ok`. After a failed infrastructure upgrade, deployment waits until the cluster returns to `ok`. The
[K3S host CA security update](#k3s-host-ca-security-update-412) restores that status after a failed attempt unless a
separate health problem prevents it.

While an upgrade is running, new app environment creation or deletion, direct deployments, post-deployment script retries,
and app stack upgrades cannot start on that cluster. Operations that are part of the infrastructure upgrade itself
continue normally.

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

In the dashboard, auto-update settings are in the same two cards as the manual actions:

- `Infrastructure > Operations > Wodby infrastructure > Auto updates`
- `Infrastructure > Operations > Infrastructure app stacks > Auto updates`

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

## Worker node updates

For [managed Kubernetes](managed.md) clusters, the simplest way to refresh worker nodes is usually to recycle them.

## Kubernetes version updates

Kubernetes version updates are separate from Wodby infrastructure version and infrastructure app updates. Wodby reads
the current cluster state and asks the provider for direct upgrade targets each time you open the upgrade operation.
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

- If a newer patch is available in the current Kubernetes minor, only the newest available patch is offered first.
- After the current minor is patched, you can move to the immediately following minor version.
- Skipping a minor or changing the Kubernetes major version is not offered as a direct upgrade.
- Preview Kubernetes versions are excluded.

The plan shows provider warnings and blockers before an upgrade starts. An upgrade is blocked when the cluster is not
in `OK` status, when the provider integration is unavailable, or when the version reported by the provider does not
match the version observed through the Kubernetes API. Resolve the reported condition and load the plan again.

### Run an upgrade

Open `Clusters`, select the cluster, and go to `Infrastructure > Operations`. Review the Kubernetes version operation,
select one of the available direct targets, and start the upgrade. Run production upgrades during a maintenance window:
the provider can rotate control-plane components and worker nodes, and the Kubernetes API can be temporarily
unavailable.

The upgrade runs as a task and puts the cluster into `Upgrading` status. Wodby:

1. Records the source and target versions in the task.
2. Starts or resumes the provider upgrade.
3. Waits for the provider operation to complete.
4. Verifies that the Kubernetes API reports the target and that every node is `Ready`.
5. Records the observed version and returns the cluster to normal operation.

Open the task to follow progress and review provider details. If an upgrade fails after the provider has applied it to
the control plane or some node pools, repeat the failed task. The retry detects the partially applied target and resumes
the remaining stages instead of trying to start an unrelated transition.

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
