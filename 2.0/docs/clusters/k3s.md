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
4. Decide whether to leave `Enable monitoring` turned on. It is enabled by default.
5. Decide whether to leave automatic infrastructure upgrades enabled. They are enabled by default and can be changed later
   from `Clusters > [Cluster] > Infrastructure > Operations`.
6. Create the cluster.

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
- installs K3S
- installs Helm
- installs Cilium for pod networking and NetworkPolicy enforcement
- prepares local kubeconfig on the server
- installs Wodby's proxy client so the cluster can securely connect back to Wodby
- sends the final initialization request to Wodby

### Install behind an outbound proxy

The installation command supports a server whose only internet access is through an HTTP forward proxy. The proxy must
support the CONNECT method because the installer uses it for HTTPS downloads and for Wodby's FRPC control connection.

#### Recommended proxy rules

Configure the proxy to:

- allow HTTP and HTTPS access to the Wodby API and the package, installation, chart, and container registries used by
  K3S, Helm, Cilium, and FRPC
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
- stores the proxy configuration in a cluster-local Secret used by FRPC and its upgrade jobs

These settings apply to K3S system operations and Wodby's FRPC component. They are not automatically injected into app
containers deployed on the cluster.

## Uninstall after a failed installation

If the installation script fails partway through, run the rollback command on the same server before retrying:

```sh
sudo /usr/local/bin/wodby-k3s-uninstall
```

The rollback command is installed at the beginning of the bootstrap script. It is safe to run after a partial installation and continues cleanup even when some components were never installed.

The command removes:

- Wodby k3s API firewall rules and systemd unit
- the Wodby proxy client Helm release, when Kubernetes is reachable
- the Cilium Helm release, when Kubernetes is reachable
- Cilium host networking artifacts and stale kube-router network policy rules
- K3S, using the official `/usr/local/bin/k3s-uninstall.sh` script when available
- root kubeconfig generated by the bootstrap script
- Helm, only when Helm was installed by the Wodby K3S bootstrap script

The command does not remove NFS client packages and does not re-enable swap. After it completes, reload the cluster page to generate a fresh installation command and run it again.

## What happens next

After the script completes successfully, Wodby initializes the cluster and deploys the required infrastructure components.

- Envoy Gateway is deployed for public HTTP, HTTPS, TCP, and UDP entrypoints
- Cilium enforces app instance network policies
- Monitoring components are deployed if you left monitoring enabled
- The cluster moves out of `Awaiting` and eventually becomes ready for app deployments

Once the cluster is ready, create new apps and choose that cluster from `My clusters`.

## Infrastructure upgrades

New K3S clusters use the current Wodby cluster infrastructure version. Existing K3S clusters can be marked as outdated
when Wodby releases a K3S-specific infrastructure upgrade.

The current K3S-specific upgrade path is described in
[Kubernetes cluster infrastructure](infrastructure.md#infrastructure-versions). It replaces the default K3S
flannel/kube-router networking setup with Cilium.

The upgrade can briefly interrupt pod networking while K3S restarts and Cilium takes over. Run it during a maintenance
window for production workloads.

Automatic infrastructure upgrades are available for K3S clusters and are enabled by default for new clusters. Disable
them when automatic maintenance is not acceptable for that cluster. See
[Kubernetes cluster updates](updates.md#automatic-infrastructure-upgrades) for the automatic upgrade settings.

## Single server model

K3S clusters connected to Wodby are single-server clusters.

Wodby does not support joining additional K3S nodes to the cluster. Multi-node self-hosted Kubernetes requires extra decisions around networking, storage, and node operations that are outside the supported K3S flow.

In the dashboard, K3S clusters are shown as one-node clusters. They do not have scalable Kubernetes controls and cannot
be scaled from Wodby.

If Wodby cannot detect the correct public ingress IP for a K3S cluster, update it from
`Clusters > [Cluster] > Infrastructure > Settings`. The update is available only while the cluster status is `OK`.

Envoy Gateway still uses a Kubernetes `LoadBalancer` service on K3S. K3S handles that service through its built-in ServiceLB controller, so Wodby does not create a cloud provider load balancer for K3S.

## Troubleshooting

- If the command has expired, reload the cluster page and use the new command.
- If the cluster stays in `Awaiting`, the bootstrap script likely never completed the final initialization step.
- If the script fails, fix the server issue, run `sudo /usr/local/bin/wodby-k3s-uninstall`, and then rerun a fresh command from the cluster page.
- Without a proxy, make sure the server can reach the public internet, Wodby API endpoints, and
  `frps.wodby.com:31225` directly during installation.
- Behind a proxy, `HTTP 403` during the FRPS check usually means the CONNECT destination or port is denied by proxy
  policy. Allow `frps.wodby.com:31225` and ensure the allow rule takes precedence over the relevant deny rule.
- `HTTP 407` means the proxy rejected or did not receive the proxy credentials. Check the proxy URL, percent-encoding,
  and authentication policy.
- A connection error without an HTTP status usually means the server cannot resolve or reach the proxy, or the proxy
  cannot resolve or reach the requested destination.
- Do not open FRPS ports `7500` or `8080` on the K3S server; they do not carry the outbound FRPC control connection.
