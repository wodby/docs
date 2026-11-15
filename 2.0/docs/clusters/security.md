---
description: See the known vulnerabilities of a cluster in Wodby, from its servers and node images to Kubernetes and infrastructure apps, and how to fix each one.
---

# Cluster security

Wodby lists the known vulnerabilities of each cluster in one table. Open `Clusters > [Cluster] > Infrastructure > Security`.
Cluster vulnerability checks run on every plan.

Wodby Cloud and serverless clusters don't list vulnerabilities, because Wodby or the provider runs every part of them.

## Read the table

Each row is one vulnerability in one part of your cluster. Rows that still need a fix come first, then the most severe.
The same vulnerability can appear several times, once for each server or image it affects.

| Column | What it shows |
| --- | --- |
| `Vulnerability` | Its ID, linked to its public record, or a Wodby check such as `Outdated node image` |
| `Summary` | A short description, or the affected package and its version |
| `Component` | Where the vulnerability is: `Operating system`, `Node image`, `Kubernetes`, or `Infrastructure app` |
| `Affected` | The server, node pool, or image that has it |
| `Severity` | `Critical`, `High`, `Medium`, `Low`, or `Unknown` |
| `Status` | `Not fixed`, `Not mitigated`, `Mitigated`, or `Fixed` |
| `Fixed in` | The version that fixes it, when one is known |
| `Fix` | A link to the operation that fixes it, when there is one |

Use the filters above the table to show one component, one severity, or only the vulnerabilities that are
`Not fixed or mitigated`.

If Wodby couldn't check a component, a warning above the table says so and why. The vulnerabilities found by the last
successful check stay in the table.

## What Wodby checks

| Component | What Wodby checks | Clusters | How often |
| --- | --- | --- | --- |
| `Operating system` | The installed packages and running kernel of each server and worker node, and the [security advisories](#security-advisories) Wodby tracks | K3s | Once a day |
| `Node image` | Whether each node pool runs the provider's newest node image, and the security advisories Wodby tracks | Managed Kubernetes | Once a day |
| `Kubernetes` | The publicly known vulnerabilities of the cluster's Kubernetes version | K3s and managed Kubernetes | Every 12 hours |
| `Infrastructure app` | The container images of the [infrastructure apps](infrastructure.md) and other components Wodby installs | K3s and managed Kubernetes | Once a day |

Wodby doesn't scan your own apps here. See [Vulnerability scanning](../apps/vulnerability-scanning.md) for the images
your app environments run.

## Fix a vulnerability

The `Fix` column links to what fixes the vulnerability:

| Fix | What to do |
| --- | --- |
| `Update server packages` | Install your distribution's updates on the server. See [Server packages on K3s](#server-packages-on-k3s). |
| `Recycle nodes` | Replace the nodes with the provider's newest image. See [Worker node updates](kubernetes.md#worker-node-updates). |
| `Update Kubernetes` | Upgrade to the `Fixed in` version or later. See [Kubernetes version updates](kubernetes.md#kubernetes-version-updates). |
| `Upgrade infrastructure` | Run the infrastructure version upgrade. See [Infrastructure version upgrades](updates.md#infrastructure-version-upgrades). |
| `Upgrade infrastructure apps` | Upgrade the infrastructure app stacks. See [Infrastructure updates](updates.md#infrastructure-updates). |

When a row has no fix, either nothing is needed or no fix has been released yet. The table shows the result of the
latest check, so a fixed vulnerability leaves the table after the next check, usually within a day.

## Server packages on K3s

Once a day, Wodby runs a short job on each server and worker node of a K3s cluster. The job only reads: it lists the
operating system release, the running kernel, whether a restart is pending, and the installed packages. Wodby then
matches the packages against your distribution's own security data, which includes the fixes it backports to older
version numbers. Wodby never installs updates or restarts your servers.

Servers that use `dpkg` (Debian, Ubuntu), `rpm` (for example Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora,
openSUSE), or `apk` (Alpine) are supported. For a server with another package manager, the warning above the table says
that its package manager isn't supported.

Only the running kernel is checked. Older kernels that stay installed after an update aren't listed, because the server
doesn't run them.

To fix the listed packages, connect to the server over SSH and install your distribution's updates:

| Distribution | Command |
| --- | --- |
| Ubuntu, Debian | `sudo apt update && sudo apt upgrade` |
| Fedora, CentOS Stream, Red Hat Enterprise Linux, Rocky Linux, AlmaLinux | `sudo dnf upgrade --refresh` |
| openSUSE, SUSE Linux Enterprise | `sudo zypper refresh && sudo zypper update` |
| Alpine | `sudo apk upgrade --update-cache` |

A server that has installed updates it can't use until it restarts, such as a new kernel, shows a `Restart required`
row. Restart it during a maintenance window. See [Update the kernel](k3s.md#update-the-kernel) for what happens to your
apps while the server restarts.

The table shows the new state after the next daily scan.

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

If the fixed version isn't offered on `Kubernetes > Updates` yet, your provider hasn't released it, or the
[upgrade policy](kubernetes.md#upgrade-policy) offers it in a later step.

Managed Kubernetes providers and K3s can ship fixes in their own builds before the upstream version number changes, so a
listed vulnerability can already be fixed on your cluster. Check your provider's security bulletins to confirm.

## Infrastructure apps

Once a day, Wodby scans the container images of the [infrastructure apps](infrastructure.md) and other components that
Wodby installs on your cluster, such as Envoy Gateway and monitoring. Results cover operating system packages and
application dependencies in the images. An image that several clusters run is scanned once.

When an infrastructure app update is available and the vulnerability has a fix, the row links to
`Upgrade infrastructure apps`. Otherwise, Wodby includes the fix in a later infrastructure app update.

## Security advisories

Some vulnerabilities need more than a version check, such as the Linux kernel bug CVE-2026-98432. Wodby tracks these
separately and lists them in the same table:

- On K3s, the row shows whether Wodby's host protections are in place: `Mitigated` or `Not mitigated`. See
  [Check the host protection](updates.md#check-the-host-protection).
- On managed Kubernetes, the row shows whether your nodes have the fix: `Fixed` or `Not fixed`. See
  [Fix CVE-2026-98432 on managed Kubernetes](kubernetes.md#fix-cve-2026-98432-on-managed-kubernetes).

While a tracked advisory isn't fixed or mitigated, the cluster shows a red bug icon next to its name in the `Clusters`
list, and a red dot on its `Infrastructure` and `Security` tabs.

## API and MCP

The same list is available through the [API](../api/index.html) as `GET /v1/cluster-vulnerabilities/{id}` and the
[MCP tool](../dev/mcp/tools.md) `list_cluster_vulnerabilities`.
