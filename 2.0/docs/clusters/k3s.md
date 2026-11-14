---
description: Connect your own server to Wodby as a K3S cluster. Requirements, installation command, disk capacity, pods per node, upgrades, OS updates and troubleshooting.
---

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
- Outbound HTTPS access to Wodby and the public package/chart registries used during installation
- Outbound TCP access to `frps.wodby.com:31225`, either directly or through an HTTP CONNECT proxy

For more details, see the official [K3S installation requirements](https://docs.k3s.io/installation/requirements).

The FRPS ports `7500` and `8080` are server-side dashboard and HTTP virtual-host ports. A K3S server does not need
outbound access to those ports; its FRPC connection uses `frps.wodby.com:31225`.

## Connect server flow

1. Open `Clusters > Connect server` in the dashboard.
2. Select the cluster `Owner`. Choose `Organization <organization>` for an organization-owned cluster or `Project <project>` for a project-owned cluster.
3. Enter the cluster name and title.
4. Select the `Provider` your server runs on, such as Hetzner or OVHcloud, or leave `Custom`. The cluster shows the
   provider's icon, and the Nodes tab links to the provider's private network instructions. You can change it later
   from `Clusters > [Cluster] > Edit`.
5. Decide whether to leave `Enable monitoring` turned on. It is enabled by default.
6. Decide whether to leave automatic infrastructure upgrades enabled. They are enabled by default and can be changed later
   from `Clusters > [Cluster] > Infrastructure > Updates`.
7. Decide whether to leave `Auto upgrade Kubernetes and components` selected. It is selected by default and can be
   changed later from `Clusters > [Cluster] > Kubernetes > Updates`. See
   [automatic Kubernetes upgrades](updates.md#automatic-kubernetes-upgrades).
8. Create the cluster.

New K3S clusters are created in the `Awaiting` state. This means Wodby is waiting for you to run the generated installation command on your server.

## Installation command

After creation, Wodby redirects you to the cluster page and shows a one-time installation command.

- Run the command on the target server as `root` or with `sudo`
- The download token inside that command expires after 15 minutes
- If it expires, reload the cluster page to generate a fresh command

The generated script performs the current bootstrap flow for you. It:

- installs the rollback command at `/usr/local/bin/wodby-k3s-uninstall`
- disables swap
- installs required NFS client packages
- installs firewall rules that restrict public access to the K3S API endpoint
- [reduces exposure to CVE-2026-98432](updates.md#k3s-host-protection-for-cve-2026-98432-414) by dropping incoming IPv4 TCP
  packets with IP options and turning off MPTCP on the server
- installs K3S, with each node running up to [250 pods](#pods-per-node)
- installs Helm 4
- installs Cilium for pod networking and NetworkPolicy enforcement
- prepares local kubeconfig on the server
- installs Wodby's proxy client so the cluster can securely connect back to Wodby
- sends the final initialization request to Wodby

### Install behind an outbound proxy

The installation command supports a server whose only internet access is through an HTTP forward proxy. The proxy must
support the CONNECT method because the installer uses it for HTTPS downloads and for Wodby's FRPC control connection.

#### Recommended proxy rules

Configure the proxy to:

- allow HTTP and HTTPS access to the Wodby API, including its monitoring metrics endpoint, and the package,
  installation, chart, and container registries used by K3S, Helm, Cilium, and FRPC
- allow `CONNECT frps.wodby.com:31225` from the K3S server
- resolve `frps.wodby.com` and permit the proxy host to connect to its TCP port `31225`
- bypass TLS interception for `frps.wodby.com:31225` because the CONNECT tunnel carries the FRP protocol, not HTTP
- apply the same source, authentication, and destination restrictions your organization normally requires
- place the specific FRPS allow rule before a general CONNECT or destination deny rule

Port `443` remains necessary for normal HTTPS destinations. The FRPC control connection uses port `31225`; the K3S
server does not need access to the FRPS dashboard and HTTP virtual-host ports `7500` and `8080`.

Strict destination allowlists must also include all download and registry endpoints used by the selected Linux
distribution and the installed component versions. These can include OS package mirrors, `get.k3s.io`, GitHub release
downloads, `raw.githubusercontent.com`, `helm.cilium.io`, and the OCI registry endpoints used by K3S and Wodby charts.

#### Squid example

The following Squid example permits a specific K3S server to establish the FRPC tunnel:

```squidconf
acl CONNECT method CONNECT
acl SSL_ports port 443
acl SSL_ports port 31225
acl wodby_k3s_client src 192.0.2.10/32
acl wodby_frps dstdomain frps.wodby.com
acl wodby_frps_port port 31225
http_access allow wodby_k3s_client wodby_frps wodby_frps_port CONNECT
```

Replace the example client address with the K3S server's address as seen by Squid. Reuse the existing `CONNECT` and
`SSL_ports` ACLs if they are already defined, and keep the organization's authentication conditions in the allow rule.
When SSL bumping is enabled, add `frps.wodby.com:31225` to the applicable splice or bypass policy.

#### Configure the server

Open a root shell on the target server, export the proxy variables in that same shell, and then paste the one-time
installation command shown by Wodby:

```sh
sudo -i
export HTTP_PROXY='http://proxy-user:proxy-password@proxy.example.internal:3128'
export HTTPS_PROXY="$HTTP_PROXY"
export NO_PROXY='127.0.0.1,localhost,.example.internal'

# Paste and run the installation command from the cluster page here.
```

An HTTP forward proxy commonly uses an `http://` URL even when the destination is HTTPS; HTTPS traffic travels through a
CONNECT tunnel. Follow the proxy product's URL requirements. If the username or password contains characters such as
`@`, `:`, `/`, `#`, or `%`, percent-encode those characters in the URL. Avoid placing proxy credentials in shared
scripts or logs.

The bootstrap verifies Wodby API access through the proxy and verifies that the proxy can open a CONNECT tunnel to the
FRPS endpoint before changing the server. It then:

- passes both uppercase and lowercase proxy variables to installation tools and K3S
- adds localhost, Kubernetes pod/service networks, and cluster DNS names to `NO_PROXY`
- persists the proxy for K3S and container image pulls
- stores the proxy configuration in a cluster-local Secret used by FRPC, its upgrade jobs, and Wodby's monitoring
  infrastructure app

These settings apply to K3S system operations, Wodby's FRPC component, and Wodby's monitoring remote writes. They are
not automatically injected into customer app containers deployed on the cluster.

Existing proxy-enabled clusters start using the proxy for monitoring after the monitoring infrastructure app is
upgraded or redeployed. If automatic infrastructure app updates are disabled, apply the available monitoring update
from the cluster's infrastructure operations.

## Uninstall after a failed installation

If the installation script fails partway through, run the rollback command on the same server before retrying:

```sh
sudo /usr/local/bin/wodby-k3s-uninstall
```

The rollback command is installed at the beginning of the bootstrap script. It is safe to run after a partial installation and continues cleanup even when some components were never installed.

The command removes:

- Wodby k3s API firewall rules and systemd unit, including the filter for IPv4 TCP packets with IP options (MPTCP stays
  off until the next reboot)
- the Wodby proxy client Helm release, when Kubernetes is reachable
- the Cilium Helm release, when Kubernetes is reachable
- Cilium host networking artifacts and stale kube-router network policy rules
- K3S, using the official `/usr/local/bin/k3s-uninstall.sh` script when available
- root kubeconfig generated by the bootstrap script
- Helm, only when Helm was installed by the Wodby K3S bootstrap script

The command does not remove NFS client packages and does not re-enable swap. After it completes, reload the cluster page to generate a fresh installation command and run it again.

On a [worker node](#worker-nodes), the same command removes only the worker's own setup: the host firewall, Cilium host
networking artifacts and the K3S agent. It never removes Cilium or the proxy client from the cluster.

## What happens next

After the script completes successfully, Wodby initializes the cluster and deploys the required infrastructure components.

- Envoy Gateway is deployed for public HTTP, HTTPS, TCP, and UDP entrypoints
- Cilium enforces app environment network policies
- Monitoring components are deployed if you left monitoring enabled
- The cluster moves out of `Awaiting` and eventually becomes ready for app deployments

Once the cluster is ready, create new apps and choose that cluster from `My clusters`.

## Disk capacity and persistent volumes

The default K3S local-path storage class stores persistent-volume data on the server's host disk. The 20 GB installation
requirement is only a minimum for K3S and Wodby infrastructure; size production disks for application data, container
images, logs, backups, imports, and operating-system growth.

For new apps on an existing K3S cluster, Wodby checks storage before saving and again before deployment. The deployment
check also applies when a configuration change, such as adding an omitted optional volume, can create a new claim:

1. Before saving the app, it totals the requested sizes of enabled, physical local-path volumes and compares that
   allocation with the host filesystem's available bytes after keeping a 10% safety reserve. It also compares the
   total size claimed by existing and requested local-path volumes with the usable host capacity.
2. Before a deployment creates persistent volume claims, it repeats the check inside the cluster's serialized
   storage-operation queue. This catches capacity consumed after the form was submitted or before a later volume was
   added. A retry does not count claims that already exist as new allocations.

The first check returns an error without creating app records when the requested allocation does not fit in the known
available bytes after the safety reserve, or when the node reports `DiskPressure`. The second appears as
`Check storage capacity` in the deployment task and stops before the deployment starts under the same conditions.

The claimed-volume comparison is advisory. If existing and requested local-path volume sizes exceed usable host
capacity but measured free space is still sufficient, Wodby shows a warning and continues. A local-path volume request
is a maximum claim and does not mean that the same amount of disk is already in use.

App-service backups and imports also check the backing node's `DiskPressure` condition and, when available, kubelet
volume statistics before storage work begins.

When authoritative capacity is unavailable, creation continues and the deployment or operation task shows a warning.
Storage classes backed by a provisioner other than K3S local-path, such as a class installed by a future Rook
infrastructure app, also remain non-blocking until Wodby has a capacity resolver for that provisioner.

These checks run at operation time and do not provide proactive low-disk alerts. Monitor the server filesystem
separately and leave enough headroom for transactional imports, which temporarily keep the current data volume while
creating a replacement volume and a 10 GiB scratch volume.

If a preflight blocks an operation, free space or increase the backing disk capacity, confirm that Kubernetes no longer
reports `DiskPressure`, and retry. See [Application persistent storage](../apps/storage.md) for storage-class behavior.

## Infrastructure upgrades

New K3S clusters use the current Wodby cluster infrastructure version. Existing K3S clusters can be marked as outdated
when Wodby releases a K3S-specific infrastructure upgrade.

K3S-specific infrastructure upgrades can change networking or host security. Review the
[infrastructure changelog](infrastructure.md#changelog) before upgrading. The upcoming
[host CA security update](updates.md#k3s-host-ca-security-update-412) requires a K3S restart even if the operating
system has already applied the CA fix.

Some upgrades restart K3S or change pod networking, which can briefly interrupt cluster access or application traffic.
Run infrastructure upgrades during a maintenance window for production workloads.

Automatic infrastructure upgrades are available for K3S clusters and are enabled by default for new clusters. Disable
them when automatic maintenance is not acceptable for that cluster. See
[Kubernetes cluster updates](updates.md#automatic-infrastructure-upgrades) for the automatic upgrade settings.

## Operating system and kernel updates

Wodby updates K3S and the cluster infrastructure, but not the server's operating system. You install operating system
and kernel updates yourself. Wodby never updates or reboots your server.

A new kernel takes effect only after a reboot. Your distribution's automatic updates may already have installed one, so
the server can keep running an older kernel until you reboot it. To see the kernel the server runs, open
`Clusters > [Cluster] > Kubernetes > Updates` and find the `kernel` row in the component table.

### Update the kernel

1. Connect to the server over SSH and install the updates:

    | Distribution | Command |
    | --- | --- |
    | Ubuntu, Debian | `sudo apt update && sudo apt upgrade` |
    | Fedora, CentOS Stream, Red Hat Enterprise Linux | `sudo dnf upgrade --refresh 'kernel*'` |
    | openSUSE, SUSE Linux Enterprise | `sudo zypper refresh && sudo zypper update kernel-default` |

    `apt upgrade` also updates your other packages. K3S isn't installed from your distribution's packages, so these
    commands don't change your K3S version.

2. Compare the kernel the server runs, shown by `uname -r`, with the kernels now installed:

    | Distribution | Command |
    | --- | --- |
    | Ubuntu, Debian | `dpkg-query -W 'linux-image-*'` |
    | Fedora, CentOS Stream, Red Hat Enterprise Linux | `rpm -q kernel` |
    | openSUSE, SUSE Linux Enterprise | `rpm -q kernel-default` |

    If no newer kernel is installed, you don't need to reboot.

3. During a maintenance window, reboot the server with `sudo reboot`. All your apps on this cluster are unavailable until
   the server and K3S have started again, usually for a few minutes. K3S and Wodby's host protections start
   automatically.
4. Run `uname -r` to confirm that the server runs the new kernel, then check that your apps are available. The
   component table shows the new kernel the next time it refreshes, within about six hours.

When you install a kernel for a specific security fix, check your distribution's security tracker for the fixed version
and compare it with the version you installed. Distributions backport fixes to older version numbers, so compare with
your distribution's version, not the upstream kernel version. The newest kernel your distribution offers may not include
the fix yet.

### Unsupported operating system releases

When your operating system release reaches the end of its support, it stops getting kernel fixes. Use its extended
security support if it has one, or connect a new K3S server with a supported release and move your apps to it with
[app environment cluster migration](../apps/migration.md).

## Worker nodes

A K3S cluster has one server, which runs Kubernetes itself and receives public traffic, and can have worker nodes that
run your apps. Add worker nodes when your apps need more CPU, memory or disk than one server has.

Worker nodes don't make the cluster highly available. When the K3S server is down, Kubernetes and public traffic stop
for the whole cluster.

`Clusters > [Cluster] > Nodes` lists the server and the worker nodes with their status, K3S version, CPU, memory, disk,
GPUs when a node has them, and private and public IP.

### Worker node requirements

- The cluster status is `OK` and its infrastructure is on [version `4.1.6`](infrastructure.md#416) or newer. If an
  infrastructure upgrade is available, apply it from `Clusters > [Cluster] > Infrastructure > Updates` first.
- The worker meets the same [requirements](#requirements) as the K3S server, including outbound access to Wodby and
  `frps.wodby.com:31225`.
- The worker and the K3S server share a private network, such as a cloud VPC, a Hetzner vSwitch or Cloud Network (see
  [Connect Hetzner servers](#connect-hetzner-servers)), an OVHcloud vRack (see
  [Connect OVHcloud servers](#connect-ovhcloud-servers)), or a WireGuard or Tailscale network. Their addresses on it are
  in `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` or `100.64.0.0/10`.
- The K3S server uses its private address for cluster traffic. K3S picks its address at installation: connect the
  private network before you install K3S on the server, or
  [switch an installed server to its private address](#switch-an-installed-server-to-its-private-address). The join
  command refuses to run while the server uses a public address.
- The private network allows TCP `6443`, `4240` and `10250`, and UDP `8473`, between the servers. Wodby's host firewall
  allows these ports from private addresses only.
- Each server has a different hostname. The hostname becomes the node name.
- Behind an outbound proxy, export the same proxy variables as for the K3S server before you run the join command. See
  [Install behind an outbound proxy](#install-behind-an-outbound-proxy).

### Connect Hetzner servers

Connect the servers through one of Hetzner's private networks. Traffic on these networks is free. Keep the servers in
one location: traffic between nodes in different locations slows down requests between apps on different nodes.

| Your servers | Private network |
| --- | --- |
| Hetzner Cloud servers | A Cloud Network |
| Dedicated servers | A vSwitch |
| Both | A vSwitch coupled to a Cloud Network |

#### Cloud servers

1. In the Hetzner Cloud Console, open `Networks`, click `Create network` and choose an IP range, for example
   `10.0.0.0/16`.
2. Open the network, click `Attach Resource` and attach the K3S server and every worker. Hetzner gives each server a
   private address and configures it automatically on its standard images.
3. On each server, check that `ip -brief address` lists the private address, and that the servers answer `ping` on
   each other's private addresses.

#### Dedicated servers

1. In Hetzner Robot, open `Server > vSwitches`, create a vSwitch with a VLAN ID from `4000` to `4091`, and add the K3S
   server and every worker.
2. On each server, add an interface on the vSwitch with MTU `1400` and a private address of its own. Find the name of
   the main network interface with `ip -brief link`. On Ubuntu, create `/etc/netplan/60-vswitch.yaml` with your
   interface name, VLAN ID and the server's address:

    ```yaml
    network:
      version: 2
      vlans:
        enp0s31f6.4000:
          id: 4000
          link: enp0s31f6
          mtu: 1400
          addresses:
            - 10.0.1.2/24
    ```

    Run `sudo chmod 600 /etc/netplan/60-vswitch.yaml`, then `sudo netplan try`. It applies the change and rolls it back
    unless you confirm it within two minutes, so a mistake doesn't cut off your SSH access.

3. If you use the firewall for dedicated servers in Robot, allow traffic from your private range. It also filters
   vSwitch traffic.
4. On each server, check that `ip -brief address` lists the private address, and that full-size packets reach the
   other servers: `ping -M do -s 1372 10.0.1.3` sends packets of exactly `1400` bytes.

#### Cloud and dedicated servers together

1. Create the vSwitch and add the dedicated servers as in step 1 above, but don't configure their interfaces yet.
2. In the Hetzner Cloud Console, open your Cloud Network, then `Subnets` and `Add subnet`. Enable the dedicated server
   vSwitch connection, select the vSwitch and choose a range for the dedicated servers, for example `10.0.1.0/24`.
3. Configure the interface on each dedicated server as in step 2 above, with an address from that range and a route
   to the Cloud Network through the range's first address:

    ```yaml
          addresses:
            - 10.0.1.2/24
          routes:
            - to: 10.0.0.0/16
              via: 10.0.1.1
    ```

Hetzner couples a vSwitch to a Cloud Network only in Falkenstein, Nuremberg and Helsinki, and a Cloud Network takes
one vSwitch.

### Connect OVHcloud servers

Connect the servers through a vRack, OVHcloud's private network. A vRack is free and its traffic isn't metered. A vRack
can span OVHcloud regions, but keep the servers in one region: traffic between nodes in different regions slows down
requests between apps on different nodes.

| Your servers | Private network |
| --- | --- |
| Dedicated servers | A vRack |
| Public Cloud instances | A private network of your Public Cloud project |
| Both | One vRack with the dedicated servers and the Public Cloud project |

Rise, Advance, Scale and High Grade dedicated servers support the vRack. Kimsufi servers don't, and on other Eco servers
it may be missing or limited: check the server's private bandwidth before you order it.

#### Dedicated servers

1. In the OVHcloud Control Panel, order a vRack from `Add a service`, then open it in the network section and add the
   K3S server and every worker to it.
2. On each server, find the private network interface. The server's `Network interfaces` tab in the Control Panel shows
   the MAC address of its private interface, and `ip -brief link` on the server lists each interface's name with its
   MAC address.
3. Give the interface a private address of its own. On Ubuntu, create `/etc/netplan/60-vrack.yaml` with your interface
   name and the server's address:

    ```yaml
    network:
      version: 2
      ethernets:
        eno2:
          dhcp4: false
          addresses:
            - 192.168.0.2/16
    ```

    Run `sudo chmod 600 /etc/netplan/60-vrack.yaml`, then `sudo netplan try`. It applies the change and rolls it back
    unless you confirm it within two minutes, so a mistake doesn't cut off your SSH access.

    If the server's network interfaces are bonded with OVHcloud Link Aggregation, put the address on the private bond
    instead of the interface.

4. On each server, check that `ip -brief address` lists the private address, and that the servers answer `ping` on
   each other's private addresses.

#### Public Cloud instances

1. In your Public Cloud project, open `Network > Private Network` and create a private network in the instances'
   region. New projects come with a vRack; add an older project to a vRack first.
2. Attach the K3S server and every worker to the network: choose it when you create an instance, or attach it from the
   `Private network` card of an existing instance.
3. On each instance, check that `ip -brief address` lists the private address, and that the instances answer `ping` on
   each other's private addresses.

#### Dedicated servers and Public Cloud instances together

1. Add the dedicated servers and the Public Cloud project to the same vRack.
2. Create the Public Cloud private network with `Set VLAN ID` turned on and VLAN ID `0`, the VLAN that dedicated
   servers use, and without a gateway.
3. Configure the interface on each dedicated server as in step 3 for dedicated servers, with an address from the
   private network's range that its DHCP pool doesn't hand out.

### Install K3S or switch the server

Install K3S on the K3S server once its private address works. The installation picks the private address for cluster
traffic and keeps the public one for public traffic. If K3S is already installed on the server,
[switch it to its private address](#switch-an-installed-server-to-its-private-address). In
`Clusters > [Cluster] > Nodes`, the K3S server's internal IP is then its private address, and workers can join.

### Switch an installed server to its private address

A K3S server installed before it had a private network uses its public address for cluster traffic, and workers can't
join it. Once you have connected the server to a private network, switch it to its private address:

1. Open `Clusters > [Cluster] > Nodes` and click `Switch to private address` in the warning above the node list.
2. Choose the address on the private network your workers share. Wodby lists the private addresses it finds on the
   server and shows whether the server's network configuration keeps each one after a reboot. An address that isn't
   kept needs your confirmation, because K3S doesn't start when its address is gone.
3. Click `Switch address` and wait until the switch finishes.

K3S restarts once. Wodby's connection to the cluster pauses for about a minute while your apps keep running, and new
deployments wait until the switch ends. The server keeps its public IP for public traffic, so your domains and DNS
records stay the same. If K3S doesn't come back on the private address, the server restores its previous settings and
keeps working on its public address.

The switch needs the cluster status `OK` and infrastructure version [`4.1.6`](infrastructure.md#416) or newer. Wodby
refuses it while app operations, such as deployments, are running; start it again once they finish.

### Add a worker node

1. Open `Clusters > [Cluster] > Nodes` and click `Add node`.
2. Run the command on the new server as `root` or with `sudo` within 15 minutes.
3. Wait until the node shows as `Ready` in the node list.

The join command checks the worker's network access, then sets up the worker the same way as the K3S server: the
rollback command, host CA certificates, NFS client packages, the host firewall and
[protections against CVE-2026-98432](updates.md#k3s-host-protection-for-cve-2026-98432-414), and the daily host check.
It installs the same K3S version as the server.

### How apps use worker nodes

- New pods run on any `Ready` node.
- Public traffic keeps entering through the K3S server's public IP. A worker doesn't need a public IP and doesn't
  accept public traffic for your apps.
- A persistent volume on the default local-path storage is kept on the node where its app first started, and the app
  always runs on that node. If that node is lost, the volume's data is lost. Back up data you need.
- When you create an app, Wodby checks that its new volumes fit on the nodes. If they fit on some nodes but not all, you
  see a warning and the app is created; it's refused only when they fit on none. See
  [Disk capacity and persistent volumes](#disk-capacity-and-persistent-volumes).
- Kubernetes upgrades update the K3S server first and then each worker, one at a time. Before a worker is upgraded,
  its pods move to other nodes.

### Remove a worker node

1. Open `Clusters > [Cluster] > Nodes` and click `Remove` on the worker.
2. Wodby moves the worker's pods to other nodes, stops K3S on it and removes it from the cluster.
3. Run `sudo /usr/local/bin/wodby-k3s-uninstall` on that server to remove K3S and Wodby's setup from it.

Wodby refuses to remove a worker that stores persistent volumes, because their data would be lost. Delete or
[migrate](../apps/migration.md) the app environments that use them first. If the worker is already lost, remove it with
`Force`, which accepts the loss of those volumes' data.

You can't remove the K3S server.

## Pods per node

Each node runs a limited number of pods. A node that reaches its limit takes no new pods, even with CPU and memory to
spare, and new pods wait in `Pending` until another node has room. Kubernetes uses a limit of 110 pods unless it's
changed. Wodby sets K3S nodes to 250, the most that a node's pod network allows.

New K3S clusters and new worker nodes start at 250. Existing clusters move to 250 with infrastructure version
[`4.1.7`](infrastructure.md#417). Until then, their nodes run up to 110 pods.

To change the limit:

1. Open `Clusters > [Cluster] > Settings`.
2. Under `Pods per node`, enter a number from 50 to 250 and click `Update pods per node`.
3. Confirm the K3S restart and wait until the task finishes.

The limit applies to every node of the cluster. K3S restarts on each node whose limit changes, one node at a time. Your
apps keep running. Wodby's connection to the cluster pauses for about a minute while the K3S server restarts, and new
deployments wait until the change finishes.

Wodby refuses the change when:

- the cluster status isn't `OK`, or app operations such as deployments are running. Retry once they finish.
- a node already runs more pods than the new limit. Choose a higher number or move apps off that node.
- a node runs as many pods as its current limit allows. Wodby runs a short job on each node to apply the change, and it
  needs one free pod slot. Delete or scale down a pod on that node, then retry.
- your own K3S configuration on a node sets `max-pods`, for example in `/etc/rancher/k3s/config.yaml`. Remove it and
  retry; Wodby keeps its own setting in `/etc/rancher/k3s/config.yaml.d/60-wodby-max-pods.yaml`.

## Public traffic

If Wodby cannot detect the correct public ingress IP for a K3S cluster, update it from
`Clusters > [Cluster] > Settings`. The update is available only while the cluster status is `OK`.

Envoy Gateway still uses a Kubernetes `LoadBalancer` service on K3S. K3S handles that service through its built-in
ServiceLB controller on the K3S server, so Wodby does not create a cloud provider load balancer for K3S.

## Troubleshooting

- If the command has expired, reload the cluster page and use the new command.
- If the cluster stays in `Awaiting`, the bootstrap script likely never completed the final initialization step.
- If the script fails, fix the server issue, run `sudo /usr/local/bin/wodby-k3s-uninstall`, and then rerun a fresh command from the cluster page.
- If the join command can't connect to the K3S server on port `6443`, check that both servers are on the same private
  network and that its firewall allows the [worker node ports](#worker-node-requirements).
- If new pods stay `Pending` while the node has free CPU and memory, the node may have reached its
  [pods per node](#pods-per-node) limit. Raise the limit or add a [worker node](#worker-nodes).
- If the join command says the K3S server uses its public address, connect the server to a private network and
  [switch it to its private address](#switch-an-installed-server-to-its-private-address).
- Without a proxy, make sure the server can reach the public internet, Wodby API endpoints, and
  `frps.wodby.com:31225` directly during installation.
- Behind a proxy, `HTTP 403` during the FRPS check usually means the CONNECT destination or port is denied by proxy
  policy. Allow `frps.wodby.com:31225` and ensure the allow rule takes precedence over the relevant deny rule.
- `HTTP 407` means the proxy rejected or did not receive the proxy credentials. Check the proxy URL, percent-encoding,
  and authentication policy.
- A connection error without an HTTP status usually means the server cannot resolve or reach the proxy, or the proxy
  cannot resolve or reach the requested destination.
- If cluster metrics remain unavailable after a proxy installation, upgrade or redeploy the monitoring infrastructure
  app and confirm that the proxy permits HTTPS access to the Wodby API monitoring endpoint.
- Do not open FRPS ports `7500` or `8080` on the K3S server; they do not carry the outbound FRPC control connection.
