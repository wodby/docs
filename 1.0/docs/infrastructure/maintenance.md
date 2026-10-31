# Infrastructure maintenance

Check your server's infrastructure version on the servers list in the Dashboard. The current releases are **7.0.7** for Infrastructure 7 and **6.1.1** for existing Infrastructure 6 servers. Infrastructure and [stacks](../stacks/maintenance.md) are updated separately.

Infrastructure 6 cannot be upgraded in place to Infrastructure 7. To move to Infrastructure 7, [connect a fresh supported server](connecting-server.md) and migrate or redeploy your applications.

## Infrastructure components

Open the server's settings to see its **Infrastructure components**: the installed and latest version of each component, its status, and who updates it. The server's version in the servers list is highlighted orange when a component needs an update and red when one is critical.

| Status | What to do |
| --- | --- |
| **Critical** | A known security issue affects the installed version, or the version is past its end of support. Update the component as soon as possible. |
| **Update recommended** | Update the component in your next maintenance window. Edge has a newer release, Infrastructure 6 Agent has a newer release, or the installed version is older than Wodby supports, close to its end of support, or affected by a known issue. |
| **Update available** | No action needed. A newer version exists. |
| **Up to date** | No action needed. |
| **No updates** | Infrastructure 6 components that cannot be updated in place. |

The list shows only components whose installed version is known.

When a known issue affects a component, its advisory ID appears next to the status and links to the details.

New servers always receive the latest versions. On existing servers, Kubernetes, Docker and the other host components are updated only when security or support requires it: they do not serve public traffic, and some of their updates restart application containers or briefly interrupt networking. Edge serves your applications' public traffic, so keep Agent and Edge up to date.

**Updated by** shows how each component is updated:

* **Update** button: update this component yourself, as described in [Updating individual components](#updating-individual-components).
* **Infrastructure update**: update this component yourself when an update is available, as described in [Updating from the Dashboard](#updating-from-the-dashboard).
* **Wodby support**: Wodby support updates these components with you, at a time that suits your applications: the installer, Kubernetes, Docker Engine, containerd, cri-dockerd and Canal, plus etcd on servers below Infrastructure 7.0.7. When an update is due, select **Request update** to start a support conversation, or contact [Wodby support](../support.md).
* **Wodby installer**: the server updates this itself. See [Kubernetes certificates](#kubernetes-certificates).

## Kubernetes certificates

Infrastructure 7 servers use internal Kubernetes certificates that last one year. The server renews them automatically, so you don't need to do anything.

When fewer than 90 days are left, the server renews its certificates between 02:00 and 05:00 server time. Server management, including deployments, pauses for about a minute. Applications keep running. If a deployment fails during this time, run it again.

If a renewal doesn't complete, the server goes back to its existing certificates and tries again the next night. Management can be unavailable for up to about 10 minutes when this happens.

To check the certificates, open the server's settings and find **Kubernetes certificates** under **Infrastructure components**. Servers that haven't reported their certificates don't show this row.

| Status | What to do |
| --- | --- |
| **Valid** | No action needed. |
| **Needs attention** | A renewal failed, a certificate expires within 30 days, or the certificate authority expires within a year. After a failed renewal, the server tries again the next night. If the status stays, select **Request update** or contact [Wodby support](../support.md). |
| **Critical** | A certificate expires within 7 days or has already expired. Select **Request update** or contact [Wodby support](../support.md) as soon as possible. Once a certificate expires, deployments and other server management stop working, although running applications keep working. |
| **Not reported** | The server hasn't reported its certificates recently. Check that the server is online. If the status stays, contact [Wodby support](../support.md). |

Certificate authorities last ten years and aren't renewed automatically.

## Updating individual components

On Infrastructure 7.0.7 and later, you can update Agent, etcd and Edge without changing the server's infrastructure version. Servers on earlier versions first [update to 7.0.7](#updating-from-the-dashboard).

These updates stay within the component's current release line. A larger version change arrives with a new infrastructure version.

| Component | During the update |
| --- | --- |
| **Agent** | Server management briefly disconnects. Applications and Edge keep running. |
| **etcd** | Server management pauses for up to about 20 seconds. Applications and Edge keep running. |
| **Edge** | HTTP and HTTPS traffic is briefly interrupted while Edge restarts. |

To update:

1. Open the server's settings and find **Infrastructure components**.
2. Select **Update** next to a component, or **Update all** to update every component that has an update. This checks the server without applying changes.
3. Under **Infrastructure update**, review the summary, affected application instances, and warnings. Resolve any reported blockers.
4. Select the acknowledgement checkbox, then the update button, such as **Update etcd**.
5. Open **View update task and logs** to follow progress. You can leave the page and return later.
6. After completion, check that your applications are accessible over HTTP and HTTPS and behave as expected.

Selected components update one at a time, in this order: Agent, etcd, Edge. If one can't be verified, the components after it aren't updated.

An update can require a minimum version of another component. If the check reports this, select **Update all** or update that component first.

If the check reports that Wodby cannot read etcd on the server, contact [Wodby support](../support.md). This is a one-time change on servers connected before etcd updates were available, and nothing restarts. Then select **Check server again**.

The requirements and restrictions in [Updating from the Dashboard](#updating-from-the-dashboard) also apply, including check expiry and blocked changes during the update.

If an update doesn't complete, see [If an update does not complete](#if-an-update-does-not-complete). If etcd doesn't return, applications keep running, but deployments and other server management stay unavailable until Wodby support repairs it.

## Updating from the Dashboard

Infrastructure 7.0.0–7.0.6 servers can update directly to 7.0.7 with one check and confirmation. The update applies the required component changes in order.

The Dashboard offers the next supported update for your server. The server must be available, and you need permission to update it. Wait for active server and application tasks to finish. Server checks identify unsupported versions or configurations.

Review the interruption warnings and choose a suitable maintenance window. Component images are downloaded before the running components are replaced. Edge updates still briefly interrupt HTTP and HTTPS traffic while Edge restarts. Agent updates briefly disconnect server management while application containers and Edge continue running.

1. Open the server's settings and find **Infrastructure update**.
2. Select **Check server for update**. This checks the server without applying changes.
3. Review the versions, release summary, affected application instances, and warnings. Resolve any reported blockers.
4. Select the acknowledgement checkbox, then **Update infrastructure**.
5. Open **View update task and logs** to follow progress. You can leave the page and return later.
6. After completion, check that your applications are accessible over HTTP and HTTPS and behave as expected.

Checks expire after 15 minutes. Run them again if they expire or the server configuration changes. Each user must run their own checks.

During an update, deployments and other server changes are blocked. You cannot cancel the update or delete the server. Do not apply manual infrastructure changes while the update is in progress.

Dashboard component updates do not upgrade the operating system, Docker or Kubernetes. Contact [Wodby support](../support.md) before changing the host operating system or infrastructure components manually.

### If an update does not complete

Reopen the server's settings and check the update task before retrying. A failed task can leave some components updated, so the server may remain in maintenance until its state is verified.

If the Dashboard shows **Update outcome needs verification**, wait until the displayed recovery time, then select **Check update status**. This checks the installed state without repeating the update.

If the update was not applied and maintenance has ended, resolve the problem shown in the task log and run new checks. If the server remains in maintenance or disconnected, contact [Wodby support](../support.md) with the task link before attempting a manual update or rollback.

## Host CA security update

Updates from Infrastructure 6.0.0–6.0.4 or 6.1.0 to 6.1.1, and from 7.0.0–7.0.6 to 7.0.7, attempt a host CA certificate update for the [eMudhra security incident](https://ubuntu.com/blog/emudhra-ca-compromise-fixes-available) after their component updates are verified. Failure of this step does not fail the infrastructure upgrade.

During updates to Infrastructure 6.1.1 or 7.0.7, Debian and Ubuntu hosts can disable the affected **emSign ECC Root CA - G3** and **Comodo AAA Services root** certificates through the system CA configuration and rebuild the trust store. This works even when the configured repositories do not offer a fixed package. Other operating systems require vendor security packages. Older systems may need extended security support. Affected custom CA copies require manual remediation.

Each supported upgrade to the current infrastructure release checks host CA trust, including when an earlier CA update was attempted. A clean host needs no changes. Servers already on 6.1.1 or 7.0.7 can have host CA trust checked and repaired separately through [Wodby support](../support.md), without changing infrastructure versions or component images. Check the CA result in the server task history. Successful verification is logged as **Host CA trust files were verified against the eMudhra incident.** If the host CA update was not verified or no result is recorded, apply your operating-system vendor's CA security fix and verify the host trust store, or contact [Wodby support](../support.md). The infrastructure version alone does not confirm successful CA remediation.

The CA update does not restart host services. Long-running services may need a separately scheduled reload or restart to use the updated trust store. Application images and language-runtime CA bundles require separate updates. Certificates chaining to removed roots may no longer be trusted.

## Changelog

### 7.0.7

* Updated Edge to [3.0.28](https://github.com/wodby/edge-alpine/tree/3.0.28), including the Brotli security fix for [CVE-2026-111497](https://github.com/google/brotli/releases/tag/v1.2.1).
* Included [host CA remediation](#host-ca-security-update) from every supported earlier Infrastructure 7 version. Review the server task for verification or manual-remediation warnings.

### 7.0.6

* Updated Agent to 5.7.1.

### 7.0.5

* Updated Agent to 5.7.0.
* Added a best-effort [host CA security update](#host-ca-security-update). Review the update task for verification or manual-remediation warnings.

### 7.0.4

* Updated Edge to [3.0.27](https://github.com/wodby/edge-alpine/tree/3.0.27).

### 7.0.3

* Updated Agent to 5.6.2.

### 7.0.2

* Updated Agent to 5.6.0.

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

### 6.1.1

* Updated Agent to 5.7.1.
* Included [host CA remediation](#host-ca-security-update) when updating from 6.1.0 or earlier supported Infrastructure 6 versions. Review the update task for verification or manual-remediation warnings.

### 6.1.0

Available for existing Infrastructure 6.0.0–6.0.4 servers.

* Updated Agent to 5.7.0.
* Updated Edge to [2.7.2](https://github.com/wodby/edge-alpine/releases/tag/2.7.2).
* Added a best-effort host CA security update. Check the update task for any required manual remediation.

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
