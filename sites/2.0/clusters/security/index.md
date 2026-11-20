Source: https://wodby.com/docs/2.0/clusters/security/

# Cluster security

Wodby lists the known vulnerabilities of each cluster in one table. Open `Clusters > [Cluster] > Security`.
Cluster vulnerability checks run on every plan.

Wodby Cloud and serverless clusters don't list vulnerabilities, because Wodby or the provider runs every part of them.

While a cluster has vulnerabilities that raise an alert and aren't fixed, mitigated, or
[ignored](https://wodby.com/docs/2.0/clusters/security/#ignore-a-vulnerability), its `Security` tab shows a red dot. The cluster's status also shows a red bug tag
with their number, in the `Clusters` list, at the top of the cluster page and on its `Overview` tab.

A vulnerability raises an alert when it's known to be exploited, at least 10% likely to be exploited in the next 30
days, or tracked by Wodby, whatever its severity. See [Vulnerabilities that raise an alert](https://wodby.com/docs/2.0/apps/vulnerability-scanning/#vulnerabilities-that-raise-an-alert).
The [security advisories](https://wodby.com/docs/2.0/clusters/security/#security-advisories) Wodby tracks always raise an alert until they're fixed or mitigated.
An outdated node image isn't a single vulnerability, so it doesn't raise an alert.

When nothing raises an alert, the cluster page shows the number of critical and high vulnerabilities that aren't fixed
in a grey bug tag, and the `Clusters` list shows none.

## Read the table

Each row is one vulnerability in one part of your cluster. Rows that still need a fix come first, then those that raise
an alert, then the most severe.
The same vulnerability can appear several times, once for each server or image it affects.

| Column | What it shows |
| --- | --- |
| `Vulnerability` | Its ID, linked to its public record, or a Wodby check such as `Outdated node image` |
| `Summary` | A short description, or the affected package and its version |
| `Component` | Where the vulnerability is: `Operating system`, `Node image`, `Kubernetes`, or `Infrastructure app` |
| `Affected` | The server, node pool, or image that has it. An infrastructure app's image starts with the app's name, for example `Monitoring` |
| `Severity` | `Critical`, `High`, `Medium`, `Low`, or `Unknown` |
| `Exploitable` | `Exploited` or `Likely exploited` when the vulnerability raises an alert, `Tracked by Wodby` for a vulnerability or [security advisory](https://wodby.com/docs/2.0/clusters/security/#security-advisories) that Wodby tracks itself and that isn't fixed or mitigated, `Unlikely` when its EPSS chance is below 10%, or `Unknown` when there's no exploitation data. Empty for a Wodby check such as `Outdated node image` |
| `Status` | `Not fixed`, `Not mitigated`, `Fixed after restart`, `Mitigated`, `Fixed`, or `Ignored` |
| `Fixed in` | The version that fixes it, when one is known |
| `Fix` | A link to the operation that fixes it, when there is one |

Use the filters above the table to show one component, one severity, or only the vulnerabilities that are
`Not fixed or mitigated`.

If Wodby couldn't check a component, a warning above the table says so and why. The vulnerabilities found by the last
successful check stay in the table.

## What Wodby checks

| Component | What Wodby checks | Clusters | How often |
| --- | --- | --- | --- |
| `Operating system` | The installed packages and running kernel of each server and worker node, and the [security advisories](https://wodby.com/docs/2.0/clusters/security/#security-advisories) Wodby tracks | K3s | Once a day |
| `Node image` | Whether each node pool runs the provider's newest node image, and the security advisories Wodby tracks | Managed Kubernetes | Once a day |
| `Kubernetes` | The publicly known vulnerabilities of the cluster's Kubernetes version | K3s and managed Kubernetes | Every 12 hours |
| `Infrastructure app` | The container images of the [infrastructure apps](https://wodby.com/docs/2.0/clusters/infrastructure/) and other components Wodby installs | K3s and managed Kubernetes | Once a day |

Wodby doesn't scan your own apps here. See [Vulnerability scanning](https://wodby.com/docs/2.0/apps/vulnerability-scanning/) for the images
your app environments run.

## Fix a vulnerability

The `Fix` column links to what fixes the vulnerability:

| Fix | What to do |
| --- | --- |
| `Update server packages` | Install your distribution's updates on the server. Clicking the fix opens [Update server packages](https://wodby.com/docs/2.0/clusters/k3s/#update-server-packages). |
| `Restart server` | Restart the server so it runs the updates already installed on it, such as a new kernel. Clicking the fix opens [Restart servers](https://wodby.com/docs/2.0/clusters/k3s/#restart-servers). |
| `Recycle nodes` | Replace the nodes with the provider's newest image. See [Worker node updates](https://wodby.com/docs/2.0/clusters/kubernetes/#worker-node-updates). |
| `Update Kubernetes` | Upgrade to the `Fixed in` version or later. See [Kubernetes version updates](https://wodby.com/docs/2.0/clusters/kubernetes/#kubernetes-version-updates). |
| `Upgrade infrastructure` | Run the infrastructure version upgrade. See [Infrastructure version upgrades](https://wodby.com/docs/2.0/clusters/updates/#infrastructure-version-upgrades). |
| `Upgrade infrastructure apps` | Upgrade the infrastructure app stacks. See [Infrastructure updates](https://wodby.com/docs/2.0/clusters/updates/#infrastructure-updates). |

When a row has no fix, either nothing is needed or no fix has been released yet. The table shows the result of the
latest check, so a fixed vulnerability leaves the table after the next check, usually within a day.

## Ignore a vulnerability

Ignore a vulnerability that you have reviewed and accepted, for example one that doesn't apply to how you use the
cluster or has no fix yet.

1. Open `Clusters > [Cluster] > Security`.
2. Click `Ignore` in the vulnerability's row.
3. Enter a reason if you want to keep one, then click `Ignore`.

Wodby ignores that vulnerability in every component of the cluster, including in later checks. Other clusters aren't
affected. An ignored vulnerability:

- Shows `Ignored` as its status. Hover over the status to see the real status and the reason.
- Moves to the end of the table.
- Doesn't count toward the red dot on the `Security` tab or the red bug tag in the cluster's status.
- Isn't shown by the `Not fixed or mitigated` filter.

To count it again, click `Stop ignoring` in its row.

You may ignore a vulnerability while it doesn't raise an alert, and it may start raising one later: it's added to CISA's
catalog, its EPSS chance reaches 10%, or Wodby starts tracking it. Your ignore then stops applying. The vulnerability
counts again and raises the alert, and its status shows an orange `Ignored before alert` tag. Hover over the tag to see
your earlier reason. To keep ignoring it, click `Ignore again`. The ignore then applies while the vulnerability raises
the alert, and your earlier reason stays unless you enter a new one.

Ignoring a vulnerability and taking that back require permission to modify the cluster. The
[security advisories](https://wodby.com/docs/2.0/clusters/security/#security-advisories) Wodby tracks and the `Outdated node image` and `Restart required` rows
can't be ignored.

## Server packages on K3s

Once a day, Wodby runs a short job on each server and worker node of a K3s cluster. The job only reads: it lists the
operating system release, the running kernel, whether a restart is pending, and the installed packages. Wodby then
matches the packages against your distribution's own security data, which includes the fixes it backports to older
version numbers. The check never changes the server. To install the updates or restart servers, see
[Operating system and kernel updates](https://wodby.com/docs/2.0/clusters/k3s/#operating-system-and-kernel-updates).

Servers that use `dpkg` (Debian, Ubuntu), `rpm` (for example Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora,
openSUSE), or `apk` (Alpine) are supported. For a server with another package manager, the warning above the table says
that its package manager isn't supported.

Only the running kernel's packages are listed. Older kernels that stay installed after an update aren't listed, because
the server doesn't run them.

If a newer kernel is installed but the server still runs an older one, Wodby checks the newer kernel too.
Vulnerabilities of the running kernel that the newer kernel doesn't have show as `Fixed after restart`, with
`Restart server` as the fix. The fix is already on the server, but the server stays exposed until it restarts into the
new kernel, so these rows still count as not fixed. Vulnerabilities that the newer kernel has too stay `Not fixed`.

To fix the listed packages, start [Update server packages](https://wodby.com/docs/2.0/clusters/k3s/#update-server-packages), or connect to the server over
SSH and install your distribution's updates:

| Distribution | Command |
| --- | --- |
| Ubuntu, Debian | `sudo apt update && sudo apt upgrade` |
| Fedora, CentOS Stream, Red Hat Enterprise Linux, Rocky Linux, AlmaLinux | `sudo dnf upgrade --refresh` |
| openSUSE, SUSE Linux Enterprise | `sudo zypper refresh && sudo zypper update` |
| Alpine | `sudo apk upgrade --update-cache` |

A server that has installed updates it can't use until it restarts shows a `Restart required` row. The row names the new
kernel and, on Debian and Ubuntu, the other updates waiting for the restart, such as `libc6`. Restart the server during
a maintenance window with [Restart servers](https://wodby.com/docs/2.0/clusters/k3s/#restart-servers), which also says what happens to your apps while
the server restarts.

After you update or restart servers from Wodby, the table shows the new state within about 15 minutes. After changes
you make over SSH, it shows it after the next daily scan.

## Node images on managed Kubernetes

On Amazon EKS and Azure AKS, Wodby compares the image of each node pool with the provider's newest image once a day. A
node pool on an older image shows an `Outdated node image` row with the newest image in `Fixed in`. Recycle the nodes to
move them to it. A newer image carries the provider's latest security fixes, so the row's severity is `Unknown`.

Google GKE and DigitalOcean Kubernetes ship node images with Kubernetes versions. Update Kubernetes to get their newer
node images.

## Kubernetes version

Wodby looks up the vulnerabilities of your cluster's Kubernetes version in the [OSV](https://osv.dev) vulnerability
database, for the upstream Kubernetes version. For example, a cluster that reports `v1.33.5+k3s1` or
`v1.33.5-eks-113cf36` is checked as Kubernetes `1.33.5`. `Fixed in` shows the closest Kubernetes version that fixes the
vulnerability, a patch of your current minor version when there is one.

Wodby also checks each of these vulnerabilities against CISA's catalog and EPSS whenever it refreshes the list, so one
that is known or likely to be exploited [raises an alert](https://wodby.com/docs/2.0/apps/vulnerability-scanning/#vulnerabilities-that-raise-an-alert)
like any other. A vulnerability without a CVE ID has no exploitation data and shows as `Unknown`.

If the fixed version isn't offered on `Kubernetes > Updates` yet, your provider hasn't released it, or the
[upgrade policy](https://wodby.com/docs/2.0/clusters/kubernetes/#upgrade-policy) offers it in a later step.

Managed Kubernetes providers and K3s can ship fixes in their own builds before the upstream version number changes, so a
listed vulnerability can already be fixed on your cluster. Check your provider's security bulletins to confirm.

## Infrastructure apps

Once a day, Wodby scans the container images of the [infrastructure apps](https://wodby.com/docs/2.0/clusters/infrastructure/) and other components that
Wodby installs on your cluster, such as Envoy Gateway and monitoring. Results cover operating system packages and
application dependencies in the images. An image that several clusters run is scanned once.

When an infrastructure app update is available and the vulnerability has a fix, the row links to
`Upgrade infrastructure apps`. Otherwise, Wodby includes the fix in a later infrastructure app update.

## Security advisories

Some vulnerabilities need more than a version check, such as the Linux kernel bug CVE-2026-98432. Wodby tracks these
separately and lists them in the same table:

- On K3s, the row shows whether Wodby's host protections are in place: `Mitigated` or `Not mitigated`. See
  [Check the host protection](https://wodby.com/docs/2.0/clusters/updates/#check-the-host-protection).
- On managed Kubernetes, the row shows whether your nodes have the fix: `Fixed` or `Not fixed`. See
  [Fix CVE-2026-98432 on managed Kubernetes](https://wodby.com/docs/2.0/clusters/kubernetes/#fix-cve-2026-98432-on-managed-kubernetes).

## API and MCP

The same list is available through the [API](https://wodby.com/docs/2.0/api/) as `GET /v1/cluster-vulnerabilities/{id}` and the
[MCP tool](https://wodby.com/docs/2.0/dev/mcp/tools/) `list_cluster_vulnerabilities`.
