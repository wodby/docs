# Infrastructure maintenance

You can see your server's infrastructure version on the servers list in the Dashboard. Supported Infrastructure 7 component updates can be applied from the Dashboard when this feature is enabled. For other infrastructure changes, [contact our support team](../support.md) to schedule an upgrade.

!!! success "Current Wodby 1 infrastructure lines"
    Infrastructure 7.0.1 is the default for fresh servers. Infrastructure 6.0.4 is the latest legacy release for existing Infrastructure 6 servers.

!!! warning "No in-place 6 to 7 upgrade"
    Infrastructure 7 requires a fresh Ubuntu 26.04 or Debian 13 server. Migrate or redeploy applications from Infrastructure 6 instead of running Installer 2.x on the existing host.

You will be notified each time a new version of the infrastructure is released.

## Infrastructure 7 maintenance

Infrastructure 7 installs exact versions of Docker, Kubernetes, containerd, cri-dockerd, and networking packages and places the apt packages on hold. Do not upgrade these components independently. Contact [Wodby support](../support.md) before changing a control-plane component or upgrading the host operating system.

Existing Infrastructure 7 servers do not automatically replace an already running Agent merely because the backend release profile changed. Follow a support instruction or use the [documented Agent update command](cli.md#updating-infrastructure-7-agent) when a patch release is required.

### Updating from the Dashboard

!!! info "Availability"
    Dashboard infrastructure updates must be enabled before you can use this workflow. If the controls are unavailable or the Dashboard reports that updates are not enabled, contact [Wodby support](../support.md).

The Dashboard offers approved updates for your server's current Infrastructure 7 version. Each release specifies which components it changes and which versions it supports. Updates follow these supported paths; you cannot select an arbitrary version or skip a required intermediate release. Review and confirm each update separately.

The initial supported update is **7.0.0 → 7.0.1**, which updates Edge to **3.0.9** while preserving its configuration. It does not upgrade the operating system, Installer, Agent, Docker, Kubernetes, networking, or etcd. Those changes require separate maintenance. This workflow applies to supported standalone servers, not clusters, local environments, or Wodby public servers.

!!! warning "Traffic interruption"
    The 7.0.0 → 7.0.1 update briefly interrupts HTTP and HTTPS traffic to applications on the server while Edge restarts. Schedule a suitable maintenance window and review the warnings for every release before confirming.

You need permission to update the server. The server must be available, and active server and application tasks must finish before you start the update. The checks also verify that the installed components and server configuration support the offered release. Contact support if a configuration is not supported.

1. Open the server's settings in the Dashboard and find **Infrastructure update**.
2. Select **Check server for update**. Checking the server does not apply the update.
3. Review the source and target versions, release summary, affected application instances, and warnings. Resolve any reported blockers before proceeding.
4. Select the acknowledgement checkbox, then **Update infrastructure**.
5. Select **View update task and logs** to follow progress. You can leave the page and return later.
6. After the update completes, check that your applications are accessible over HTTP and HTTPS and behave as expected.

A preview expires after 15 minutes and belongs to the user who requested it. Run the checks again if it expires, the server configuration changes, or you need a new preview. Starting an update rechecks the server against the reviewed release.

During the update, the server is reserved for infrastructure maintenance. Other operations that change server resources, including deployments and server deletion, are blocked. Infrastructure update tasks cannot be canceled from the Dashboard. The displayed infrastructure version advances only after the new component rollout and required platform checks succeed.

### If an update does not complete

A failed task or lost connection does not necessarily mean the update was not applied. Reopen the server's settings and follow the recorded operation status before attempting another update.

- If the update stopped before applying a change, maintenance is released and the infrastructure version stays unchanged. Review the task log, resolve the problem, and run new checks before retrying.
- If the outcome is uncertain, the Dashboard shows **Update outcome needs verification** and keeps the server reserved for maintenance. Wait until the displayed recovery time, then select **Check update status** when it becomes available.
- A recovery check verifies the existing server state. It does not repeat the update or roll it back. A healthy target completes the update; an unchanged, healthy source releases maintenance so you can prepare a new attempt.
- If the server cannot be verified in either state, maintenance remains reserved. Contact [Wodby support](../support.md) and include the update task link.

## Infrastructure 6 OS upgrade tips

!!! tip "Create snapshot of your VM first"
    Before performing the upgrade regardless of the method we strongly recommend creating a snapshot of your server if it's a VM.    

!!! warning "Test your upgrades with the dev server first"
    Make sure your prod and dev server are from the same cloud provider and have the same OS distribution/version. After successfully upgrading the dev server and testing all the hosted apps you should continue to upgrading your production server.

These instructions apply only to existing Infrastructure 6 servers. They do not turn an Infrastructure 6 server into Infrastructure 7.

When upgrading an Infrastructure 6 host to a previously supported operating-system version:

1. [Stop Kubernetes and Docker services first](cli.md#restart-docker-and-kubernetes-services)
2. Perform the upgrade
3. Reboot
4. Make sure Docker was not installed from packages (we require a specific version that we manuall install during server connection)
5. Check iptables version via `iptables --version`. If it's `1.8.2` or newer switch it to legacy mode: `update-alternatives --set iptables /usr/sbin/iptables-legacy`
6. Make sure [cgroup v2 is disabled](#infrastructure-6-cgroup2-workaround)

## Infrastructure 6 cgroup2 workaround

Some operating systems such as Debian 11 enable cgroup v2, which is not supported by the Docker version used by Infrastructure 6. To retain Infrastructure 6 compatibility:
- Edit `/etc/default/grub` and add `systemd.unified_cgroup_hierarchy=0` to `GRUB_CMDLINE_LINUX_DEFAULT` (or `GRUB_CMDLINE_LINUX` if it's not present)
- Run `update-grub`
- Reboot the server

## Changelog

### 7.0.1

* Updated Edge to [3.0.9](https://github.com/wodby/edge-alpine/releases/tag/3.0.9), including NGINX **1.31.3 → 1.31.6**.

### 7.0.0

Fresh-server Infrastructure 7 release:

* Added Ubuntu 26.04 and Debian 13 amd64 support
* Kubernetes 1.36.3
* Docker Engine 29.7.2 with containerd 2.3.3 and cri-dockerd 0.4.4
* Canal 3.32.1, combining Calico policy with the Flannel VXLAN data plane
* etcd 3 using the direct v3 API
* Wodby Edge 3.0.0 with support certificates for technical domains
* Wodby Agent 5.5.0

### 6.0.4

Containers' anonymous volumes now clean up by cron

### 6.0.3

- `large_client_header_buffers` set to `4 32k`
- Removed obsolete `http2_max_field_size`

### 6.0.2

Edge's nginx updated to 1.24

### 6.0.1

Bugfix: wodby agent couldn't process certain message

### 6.0.0

Upgraded Docker version

### 5.9.2

Wodby agent now supports connection via http proxy

### 5.9.1

Node domain changed from `wod.by` to `wodby.cloud`

### 5.9.0

- Added support for Debian 11 and other OSs with cgroup2 enabled by default
- Add a custom seccomp profile for Docker as a workaround for faccessat2 [issue](https://github.com/alpinelinux/docker-alpine/issues/182) in Alpine Linux 3.14+
- ⚠️ This upgrade will cause docker daemon restart, all containers on your server will be restarted

### 5.8.6

Client max body size no longer limited on edge

### 5.8.5

Bugfix: `keepalive_requests` wasn't increased to `1000`  

### 5.8.4

- Edge: Nginx 1.19.10
- `keepalive_requests` increased to `1000` https://github.com/wodby/edge-alpine/pull/1 

### 5.8.3

Edge: fixed error_log level to avoid significant error log growth in some cases

### 5.8.2

Kubernetes: fixed issue when servers from some cloud providers like Linode failed to start up containers

### 5.8.1

- Edge: Nginx 1.19.8
- Edge: OpenSSL 1.1.1k (major security update)
- Kubernetes: fixed known issue with a sporadic container logs absence

### 5.8.0

Edge: improved security by generating Let's Encrypt SSL certificate for default virtual host

### 5.7.10

Edge: fixed renewing of SSL certificates for domains with a redirect from www to non-www version (and vice versa) enabled

### 5.7.9

Edge: improved security settings of default Nginx virtual host 

### 5.7.8

Edge: improved and actualized SSL security settings

### 5.7.7

Docker images clean up added to cron (run every night at 2:30) 

### 5.7.6

Edge: fixed renewing Let’s Encrypt SSL certificates via ACME v2

### 5.7.5

Edge: upgraded Let’s Encrypt client 

### 5.7.4

Edge: increased value of `http2_max_field_size` parameter

### 5.7.3

Edge security update for HTTP/2 (CVE-2019-9511, CVE-2019-9513, CVE-2019-9516)

### 5.7.2

Globally disable TLS 1.0, 1.1 for all hosts 

### 5.7.1

Bugfix: edge regenerates dh params after restart 

### 5.7.0

- Nginx updated to 1.16.0
- TLS 1.0, 1.1 disabled. Added TLS 1.3 support 

### 5.6.1

Bugfix: in some cases Diffie-Hellman params failed to generate after the first server connection 

### 5.6.0

- Nginx updated to 1.15.10
- Docker log size limited to 100M
- Docker systemd unit max tasks set to unlimited
- Bugfix: low files upload speed with HTTP2   

### 5.5.8

Added HTTP2 support

### 5.5.7

Edge: DH key length increased to 2048 and now persistent

### 5.5.6

Security fix: server's metrics could be publicly accessible

### 5.5.5

Bugfix (5.5.4): installer did not report changes to IP address

### 5.5.4

Updates to installer, you don't need to update from the previous version

### 5.5.3

[HSTS](hsts.md) can now be configured per domain

### 5.5.2

Security vulnerability fix for dnsmasq [CVE-2017-14491](https://security.googleblog.com/2017/10/behind-masq-yet-more-dns-and-dhcp.html)

### 5.5.1

* Increased kernel param `aio-max-nr` for databases
* Updated paths for systemd unit files
* Uninstall fixes

### 5.5.0

* New Docker 17.06.1
* Improved response codes on Edge

### 5.4.1

* Updated [Let's Encrypt client](../apps/domains.md)

### 5.4.0

* AUFS replaced with Overlay2
* Identified a bug in Debian Kernel 3.16, required upgrade to 4.9
* Fixed a bug with kube-controller service definition that sometime caused deployment failures

### 5.3.0

* New kubernetes version
* Improved agent installer
* Enabled unattended upgrades 
* Significantly improved performance (less load on CPU and disk IO)

### 5.2.0

* Decoupled services for system containers
* Improved agent installer
* Bug fixes

### 5.1.0

* Revamped DNS services
* Improved agent installer
* Bug fixes

### 5.0.0

* New kubernetes
* New installer with frozen docker version
* Revamped wodby agent

### 4.x

First version of cluster infrastructure

### 3.5.0

* Updated Nginx (1.10.1) for a system container Edge  
* New version of Wodby agent supporting containers upgrade
* New version of orchestration system

Release date: `July 1st, 2016`

### 3.4.0

* `includeSubdomains` option removed from [HSTS header](hsts.md)
* Now `X-Robots-Tag` header added always (not only for 20x, 30x response codes)
* New version of Wodby agent. Now with automated infrastructure update (will be announced later)
* Exif extension added to PHP 5.6, 7
* Fixed bug when `X-Wodby-Node` header missed sometimes
* Added default nginx host for port 443 with self-signed certificates 

Release date: `June 16th, 2016`

### 3.3.0

* $base_url orchestration for Drupal
* Auto generation of trusted host patterns for Drupal 8
* Drupal 7.x, 8.x multi-site support
* Drupal 8 and WordPress now come with PHP7 and Redis
* msmtp + opensmtpd replaced with postfix
* Workaround for Drupal `sites/default` auto permissions change. This caused problems when settings.php file was changed

### 3.2.0

* WWW redirect actions for domains
* Basic auth configuration
* Maintenance mode
* Dev, staging instances and all instances accessible by technical `*.wod.by` domains not indexed by search engines (header X-Robots-Tag)  

### 3.1.0

* Enable HTTPS for domains (SSL certificates via Let's Encrypt) 
* Backup mirroring features added.

### 3.0.0

The latest stable version with completely reworked containers structure.

### 2.0.0

In this version we've moved git to the docroot and made major structural changes.

### 1.0.0

Production-ready version with lots of improvements.

### 0.1.0

The first public version of our infrastructure.
