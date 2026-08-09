# Connecting server to Wodby

## Instructions

Before connecting a server, make sure it satisfies the [Infrastructure 7 requirements](#infrastructure-7-requirements). In the Wodby dashboard, navigate to `Servers > Add`, select a provider, and follow the generated instructions. Custom-server installation commands must be executed as root.

* [Amazon Web Services](../integrations/aws.md)
* [DigitalOcean](../integrations/digitalocean.md)
* [Azure](../integrations/azure.md)
* [Google Cloud Platform](../integrations/gcp.md)
* [_Custom Cloud Provider_](../integrations/custom.md)

!!! warning "Fresh Infrastructure 7 servers only"
    Infrastructure 7 is not an in-place upgrade for Infrastructure 6. Do not run the generated Infrastructure 7 installation command on an existing Wodby server or another working server.

## Infrastructure 7 requirements

* A fresh amd64 server using systemd; OpenVZ containers are not supported.
* Root SSH or console access.
* [Ubuntu 26.04 or Debian 13](#supported-operating-systems).
* Docker, Kubernetes, containerd, and CNI software must not already be installed or managed independently. The installer installs and pins the required versions.
* Ports 80, 443, 6443, and 10250 must be free during installation.
* Allow public inbound traffic to 80 and 443. Allow 31222-32222/TCP when applications expose SSH or another direct NodePort service. Do not expose Kubernetes or etcd control-plane ports publicly.
* Active UFW must be temporarily disabled during installation and may be re-enabled afterward using the [UFW instructions](ufw.md).
* Swap is disabled by the Infrastructure 7 installer, including active entries in `/etc/fstab`.
* At least 2 vCPU are required. At least 4 GB RAM and 20 GB of disk are recommended, with additional disk capacity for application data, images, backups, and logs.
* Outbound HTTPS and DNS access are required for Wodby, operating-system package repositories, Docker Hub, and the pinned GitHub release artifacts used by the installer.

## Supported operating systems

New Infrastructure 7 installations support these amd64 distributions only:

* Ubuntu 26.04 LTS
* Debian 13

Existing Infrastructure 6 servers retain their current operating-system compatibility. The Infrastructure 7 operating systems above do not make an Infrastructure 6 server upgradeable in place.

Check a host before connecting it:

```shell
uname -m
. /etc/os-release && printf '%s %s\n' "$ID" "$VERSION_ID"
```

The expected architecture is `x86_64`; the operating system must report either `ubuntu 26.04` or `debian 13`.

## Proxy support

Installer 1.x and legacy Agent releases support an explicit HTTP proxy. Set `HTTP_PROXY` while running the installer, then pass the same proxy to Agent as `WODBY_HTTP_PROXY`:

```shell
kubectl -n wodby set env deployment/agent WODBY_HTTP_PROXY="$HTTP_PROXY"
kubectl -n wodby rollout status deployment/agent --timeout=5m
```

For Infrastructure 7, use Agent 5.4.2 or newer. Proxy configuration is not inherited automatically from the host environment.

## Uninstall

To uninstall Wodby infrastructure, execute this command as root:

```shell
wodby uninstall
```

On Infrastructure 7 this removes the kubeadm cluster, installer-owned Kubernetes and Docker packages, CNI state, system units, and the Wodby SSH key. It preserves application and runtime data under `/srv/wodby`, `/var/lib/docker`, and `/var/lib/containerd`.

!!! danger "Applications will stop"
    Uninstalling removes the runtime that serves applications. Preserved data is not a runnable backup and is not deleted automatically. Take provider snapshots and application backups before uninstalling a server that contains important data.
