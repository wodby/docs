# Endpoints

Endpoints are the public or private entry points to your app services. They consist of HTTP domains, redirects, and
published ports.

From `Apps > [App] > [Environment] > Endpoints` you can manage:

- `Domains`
- `Ports`
- `Settings` for HTTP routes and published ports
- `Auths`
- `Redirects`

Domains and redirects are stored as routes behind the scenes, so API, CLI, task, and infrastructure documentation may
still use the term _route_. The dashboard separates them by what users configure.

To temporarily replace enabled public HTTP and HTTPS routes with a fixed `503 Service Unavailable` response, use
[app environment maintenance mode](maintenance.md).

## Domains

Domains receive HTTP and HTTPS traffic for an app service. A domain matches a hostname and path, then serves the
request from an app service endpoint.

Each domain has:

- app service
- endpoint
- port
- hostname
- path
- path match type: `prefix` or `exact`
- TLS mode: `Let's Encrypt`, `Custom`, or `None`
- whether the domain should be `Main`
- whether the domain should be `Primary`

The dashboard automatically selects and hides the endpoint or port field when the selected app service has only one
eligible choice. Only public HTTP ports can serve domains.

## Redirects

Redirects receive requests on a source hostname and path, then send the client to another URL. They are supported on
clusters that use Envoy Gateway.

Each redirect has:

- source hostname and path
- destination scheme, hostname, and optional replacement path
- status code: `301 Permanent` or `302 Temporary`
- TLS for the source hostname
- an associated app service, endpoint, and public HTTP port

Leave the destination hostname empty to keep the source hostname. Leave the destination path empty to preserve the
requested path. The destination hostname, when provided, must be a hostname rather than a full URL.

When adding a redirect, the source hostname field suggests existing custom hostnames but also accepts a new hostname.
If you select an existing hostname, the redirect inherits that hostname's current TLS certificate. If you enter a new
hostname, choose its TLS mode: `Let's Encrypt`, `Custom`, or `None`. A certificate is needed for the source only when
clients will reach the redirect over HTTPS; the redirect destination manages its own TLS separately.

A redirect does not send traffic to its associated app service, but the association remains part of its lifecycle.
Disabling the app service disables its redirects; re-enabling the service re-enables redirects that were disabled with
the service. During a routing deployment, redirects can remain available even when the associated service has no
successful runtime because a redirect does not need a service backend.

## Technical domains

By default, Wodby generates technical routes for app services that expose public HTTP endpoints. Ports marked
`private` do not receive Wodby technical routes.

The default hostname pattern is:

- `<service-name>.<environment-name>.<app-name>.<org-name>.wodby.app`

The main app service also owns the shorter root technical hostname:

- `<environment-name>.<app-name>.<org-name>.wodby.app`

Changing the main app service retargets this existing root technical route to the new service's primary public HTTP
endpoint. The hostname, certificate, and route settings stay with the route. This does not change which route is the
app environment's `Main` route.

Wodby automatically issues and renews Let's Encrypt certificates for these technical routes. Certificate validation for
technical routes uses Wodby-managed DNS records, so the certificate can be issued before the app service itself is
serving traffic.

Technical routes are managed by Wodby. You can disable one to stop serving it, but you cannot retarget it, change its
generated hostname or path, or delete it. Wodby removes generated routes when the underlying endpoint structure no
longer requires them.

<a id="custom-routes"></a>

## Custom domains and redirects

The dashboard presents custom serving routes as domains and redirect routes as redirects:

- open `Endpoints > Domains` and select `New domain` to connect a hostname and path to an app service
- open `Endpoints > Redirects` and select `Add redirect` to redirect a source hostname and path

Creating or editing custom domains and redirects requires an active paid subscription. Wodby-managed technical routes
and their SSL certificates remain available on all active plans.

Use a custom route when you want to:

- attach your own hostname
- serve an app service under a specific path, such as `example.com/blog`
- choose whether the route should become the main app environment route or the primary route for a service endpoint

Use a redirect when you want to move traffic to another hostname, path, or scheme without serving an app backend.

Only services with HTTP endpoints are available in this flow.

Domains and redirects have separate editors. A domain and redirect cannot use the same hostname, path, and path match
type at the same time. To replace a domain with a redirect, or a redirect with a domain, delete the existing item and
create the other type.

You can retarget an existing custom domain or redirect association to a public HTTP port on another enabled app
service. Retargeting preserves the hostname, path, TLS certificate, route settings, and route authentication.
Wodby-generated technical routes cannot be retargeted from this form.

On clusters with Wodby infrastructure version `4.0.0` or newer, route changes are applied through an app environment
[routing deployment](deploys.md#routing-deployments). They do not require the source or target app service to be
redeployed. Older infrastructure versions continue to apply the change through an app-service deployment.

When you create a custom domain or redirect with Let's Encrypt, certificate issuance runs separately from application
deployment. An unattached or incorrectly routed hostname does not fail the deployment or change the app environment to an
errored state. You can also delete a custom domain or redirect while its app environment is errored, so a bad hostname
never blocks cleanup.

Deleting a custom domain or redirect also removes its route-specific HTTP settings and authentication scope. Reusable
organization-level custom certificates remain available until you delete them separately.

## Main and primary

Wodby distinguishes between two default-route flags:

- `Main` is the canonical route for the whole app environment
- `Primary` is the default route for a specific endpoint

The main route can be either a Wodby-generated technical route or a custom route. Main routes are always primary. In
practice:

- an app environment with enabled public routes has one main route
- each endpoint can have its own primary route

The main route and the main app service are separate choices. The main route determines the canonical hostname used by
the app, while the main app service determines where the root Wodby technical hostname sends traffic.

An enabled main route remains main until it becomes unavailable or you explicitly replace it. A custom main route can
also be deleted; a Wodby-generated technical route cannot. Wodby also preserves a valid primary route for an endpoint
instead of replacing it during routine reconciliation.

When the selected main or primary route becomes unavailable, Wodby chooses a replacement. Enabled custom routes are
preferred over generated technical routes only when such a replacement is necessary.

## TLS certificates

Wodby can issue TLS certificates for endpoint routes. For public docs, treat [Let's Encrypt](https://letsencrypt.org/) as the supported issuer for managed certificate flows today. Wodby automatically renews Let's Encrypt certificates before they expire.

For generated technical routes, Wodby validates certificates through managed DNS. Custom route certificates are
validated through the public HTTP route. Before contacting Let's Encrypt, Wodby publishes a temporary challenge and
checks that the hostname returns its exact challenge response. DNS resolution by itself, or an unrelated successful
HTTP response from another server, is not enough.

A custom hostname can be proxied through Cloudflare or another reverse proxy. It is considered attached when requests
to `/.well-known/acme-challenge/*` are forwarded to the Wodby route and return Wodby's challenge response. The public
DNS record may therefore resolve to proxy addresses instead of directly to the cluster. If the proxy sends challenge
requests to another origin, replaces the response, or redirects them somewhere that does not reach Wodby, certificate
issuance remains pending. Adjust the proxy's origin or routing rules, or temporarily disable proxying while the initial
certificate is issued.

New managed certificates have a `Pending` status until Wodby verifies the route and Let's Encrypt issues the
certificate. A requested issuer of `Let's Encrypt` does not by itself mean that a certificate has already been issued.
If public DNS does not resolve, the route reports `Awaiting DNS`. If DNS resolves but the exact challenge does not reach
Wodby, it reports `Not connected`. The separate certificate task fails, while the certificate remains `Pending` and
Wodby retries pending routes hourly. This does not fail an application deployment or change the app environment status.
Infrastructure errors are reported separately as `Error`.

After fixing DNS or proxy routing, open the route and select `Reconcile certificate` to check attachment immediately
instead of waiting for the next automatic retry. This starts a certificate task, not an application deployment. If a
certificate check for the route is already running, Wodby reuses that task rather than starting a duplicate.

Certificate renewals are scheduled automatically and spread over time. If Let's Encrypt is temporarily busy or rate
limits a renewal request, Wodby schedules another renewal attempt and includes the retry time in the failed renewal
notification.

`Organization > Certificates` shows issued and uploaded certificates by issuer, hostname, status, issue date, renewal
date, expiry date, and where each certificate is used. Use the issuer filter to show all certificates, Let's Encrypt
certificates, or certificates from a detected custom certificate authority. The list is paginated and can include
certificates used by application routes and supported database resources. Select a certificate row to see its key
details, all DNS names, SHA-256 fingerprint, validity dates, and individual route usages.

#### Upload a custom certificate

Uploading and applying custom TLS certificates requires an active paid subscription. Custom certificates are reusable
organization-level assets. To add one, open `Organization > Certificates`, select `Add custom certificate`, and
provide:

- the server certificate and intermediate certificates in PEM format
- the matching unencrypted private key in PEM format

The certificate input can contain the leaf certificate and its intermediate chain in one text value. The order does not
matter: Wodby identifies the leaf by matching it to the private key and stores the chain in the correct order. You may
include a self-signed root certificate, but Wodby removes it because TLS servers normally send the leaf and
intermediates, not the trusted root.

Accepted private keys are:

- PKCS#8 PEM with a `BEGIN PRIVATE KEY` header
- PKCS#1 RSA PEM with a `BEGIN RSA PRIVATE KEY` header, using at least 2048 bits
- SEC1 EC PEM with a `BEGIN EC PRIVATE KEY` header, using P-256, P-384, or P-521

Encrypted or password-protected private keys are not supported. Wodby also does not currently accept PFX/P12 files or
ZIP archives. If your certificate authority supplies an archive, extract the PEM certificate, intermediate chain, and
private key first. Certificate authorities commonly supply certificates and intermediates but do not supply the private
key when you created the certificate signing request yourself; use the private key generated with that request.

Before saving, Wodby verifies that:

- the private key matches the server certificate
- the certificate is currently valid and supports TLS server authentication
- the leaf is not a CA certificate
- the certificate contains at least one DNS Subject Alternative Name (SAN)
- every included non-root certificate belongs to the selected chain

The private key and certificate material are stored as secrets. Certificate listings expose metadata such as DNS names,
validity, key type, and a SHA-256 fingerprint, but never return the private key.

#### Apply a custom certificate to a domain or redirect

When creating or editing a custom domain or redirect, select `Custom` as the TLS mode and choose an uploaded
certificate. Wodby shows only active custom certificates whose DNS SANs cover the source hostname. Standard X.509
hostname rules apply: for example, `*.example.com` covers `www.example.com`, but not `example.com` or
`shop.eu.example.com`.

Wodby repeats the same checks when saving the route, so a certificate cannot be attached across organizations, after
expiry, or to a hostname it does not cover. Changing the TLS mode to `Let's Encrypt` starts or reuses the managed
certificate flow. Changing it to `None` removes TLS from the hostname.

TLS is selected per hostname. If an app environment has multiple route paths for the same host, changing the certificate
on one of them changes it for every path using that host. Uploaded certificates remain available for reuse after they
are detached. You can delete an uploaded certificate only after it is no longer used by any route or other supported
resource. To remove one, select its hostname in `Organization > Certificates`, then select `Delete certificate`. The
delete action remains unavailable until every usage shown on the certificate page has been detached. Wodby does not
renew uploaded certificates automatically; upload and select a replacement before the current certificate expires.
Organization admins receive staged expiration warnings 30, 14, 7, and 1 day before expiry, plus an expired
notification. Each user can control these emails with the `Custom certificate expiration` notification setting.

Before scheduling a downgrade to the free Developer plan, delete every uploaded custom certificate. Detaching a
certificate from its routes is not sufficient because the reusable organization-level certificate remains a paid
feature until it is deleted.

## Domain and redirect status

The Domains and Redirects lists each have a `Status` column. It shows `OK` only when routing and any requested
certificate are both ready; otherwise it identifies which state still needs attention. The `Certificate` column shows
certificate status, while the issuer icon before the source hostname distinguishes managed and custom certificates.
Domain and redirect details show the issuer, certificate status, and latest attachment-check state separately. An
issuer of `Let's Encrypt` does not by itself mean that a certificate has been issued. Attachment status is independent
from deployment status: a route can exist and the app can be healthy while its custom hostname is still waiting for
DNS or points to another origin.

When [App Access](access.md) is configured, the provider owns the selected endpoints' connection path. Wodby suppresses
ordinary public routes in the selected scope and uses the Access primary hostname as the app environment's canonical
address. The Domains and Redirects lists show the effective Access hostname; Cloudflare Protected and Tailscale use
provider-facing hostnames, while Cloudflare Private network reuses the suppressed Wodby technical hostname. Routes that
target the same app port share one Access hostname. With Selected endpoints scope, routes for unselected endpoints
remain public.

The `private` flag on a port does not create a Cloudflare or Tailscale endpoint by itself. Private ports without an
explicit App Access configuration remain reachable only through internal Kubernetes networking.

<a id="route-settings"></a>

## HTTP settings

The dashboard's `HTTP settings` screen controls route settings for clusters that use Envoy Gateway. They are predefined
settings rather than arbitrary Kubernetes annotations.

An effective domain setting can come from three layers, in this order:

- app environment defaults, inherited by serve routes in the app environment
- defaults declared by the selected service endpoint port
- domain-specific settings, which override both default layers for one domain

Redirects use app environment defaults and redirect-specific overrides, but do not use service port defaults. The
effective route-settings API reports which layer supplies each value. A service default does not prevent you from
overriding the setting for an app environment or individual domain.

Supported route settings are:

| Setting | Value |
| --- | --- |
| `https_redirect` | `true` or `false` |
| `no_index` | `true` or `false` |
| `request_body_size` | size with `Ki`, `Mi`, or `Gi`, such as `64Mi` |
| `session_affinity` | `cookie` or `header` |
| `path_rewrite` | path starting with `/` |
| `hsts` | `disabled`, `enabled`, or `include_subdomains` |
| `request_timeout` | Gateway API duration such as `30s`, `5m`, or `1h`; `0s` disables the timeout |
| `backend_request_timeout` | Gateway API duration such as `30s`, `5m`, or `1h`; `0s` disables the timeout |
| `rate_limit_per_ip` | positive request count per period, such as `300/minute`; each client IP has a separate limit |
| `rate_limit_total` | positive request count per period, such as `1000/second`; all clients share the route limit |

Domains support every setting in this table. Redirects support `https_redirect`, `no_index`, and `hsts`; settings that
depend on an application backend are not available for redirects. Domain and redirect options are grouped separately
when you select an override target.

### Request rate limits

`rate_limit_per_ip` limits requests from one client IP, while `rate_limit_total` limits requests from all clients to the
route. When both settings are present, a request must satisfy both limits. Requests over either limit receive
`429 Too Many Requests` at the gateway instead of reaching the app service.

Values use the form `<requests>/<period>`. The request count must be a positive integer. Supported periods are
`second`, `minute`, `hour`, `day`, `month`, and `year`, written in lowercase and singular form.

Non-cluster app environments default to `300/minute` per IP and `1000/second` total on every serve route. You can change
the app environment defaults or add a domain-specific value when an endpoint needs a different limit. A service port
can also declare a default for its routes.

These are local Envoy Gateway limits. Each route and each Envoy data-plane replica maintains its own counters, so
`rate_limit_total` is not one combined quota for the whole app environment or cluster. With multiple gateway replicas,
the effective traffic capacity can be higher than the configured value. The per-IP limit uses the client address after
the configured proxy chain is processed; clients sharing a NAT address also share one limit.

### Request timeouts

`request_timeout` limits the complete client request, including the response sent back to the client.
`backend_request_timeout` limits one request from the gateway to the selected app service. A finite backend request
timeout cannot be longer than a finite request timeout.

Use `0s` when a long-lived HTTP or WebSocket endpoint must not have that timeout. If a timeout is absent from every
effective settings layer, Wodby leaves it unset and the gateway implementation's default behavior applies.

### HSTS

HTTP Strict Transport Security (HSTS) tells browsers to use HTTPS for future requests to a hostname. Wodby applies the
setting only after the route has an active TLS certificate:

- `disabled` does not add an HSTS response header. Use it as a route-specific override when an inherited HSTS setting
  must be disabled.
- `enabled` sends `Strict-Transport-Security: max-age=63072000`.
- `include_subdomains` sends the same two-year policy with `includeSubDomains`.

Use `include_subdomains` only when every subdomain of the route hostname supports HTTPS. Browsers remember HSTS policy,
so disabling the setting later does not immediately remove policy already cached by visitors. Wodby does not add the
`preload` directive automatically.

Wodby enables the `enabled` policy on public Wodby-managed technical routes. Private App Access routes are excluded.
On Envoy Gateway clusters, the New domain form also enables HSTS by default; clear the checkbox when a domain must
remain accessible without an HSTS policy. Existing custom domains are not changed automatically.

For Envoy Gateway app environments, Wodby creates default route settings for routing compatibility and baseline request
protection:

- HTTPS redirect is enabled by default
- session affinity uses cookies by default
- request rate limits default to `300/minute` per IP and `1000/second` total for each serve route
- generated technical routes get `no_index` enabled by default
- public generated technical routes get HSTS enabled by default

On infrastructure version `4.0.0` or newer, changing route settings starts a routing deployment and does not mark app
services as needing redeploy. Older infrastructure versions continue to mark the affected service or app environment as
needing redeploy.

!!! note "Legacy ingress settings"
    Older clusters that still use Ingress Nginx may expose legacy ingress annotation settings. Envoy Gateway clusters use the route settings above. Kubernetes annotations are still available separately where service or stack templates support Kubernetes resource annotations.

## Auths

The `Auths` screen manages HTTP basic authentication.

Each auth entry has:

- username
- password
- optional realm
- optional app service scope
- optional domain or redirect scope

This gives you three practical scopes:

- app-level, when both service and route are left empty
- service-level, when a service is selected and route is left empty
- domain- or redirect-level, when a specific item is selected

Auth precedence is most-specific first:

- domain or redirect auth overrides service auth
- service auth overrides app-level auth

The edit screen can also reveal the current password for an existing auth entry. You need
[runtime secret reveal permission](../access-control.md#secret-reveal-permissions) and recent
[secret reveal confirmation](../user/security.md#secret-reveal-confirmation).

On infrastructure version `4.0.0` or newer, changing auth settings starts a routing deployment and does not mark app
services as needing redeploy. Older infrastructure versions continue to mark the affected app services and app
environment as needing redeploy.

## Ports

The `Ports` screen lists endpoint ports defined by your app services.

Each port has:

- app service
- endpoint name
- protocol
- internal port number
- whether the service template marks it as private
- optional public port

### Publishing ports

Manual port publishing is intended for non-HTTP ports such as SSH or other TCP or UDP services.

- HTTP exposure is handled through routes, not through manual public-port publishing
- only non-private, non-HTTP ports can be published or unpublished from this screen
- publishing or unpublishing a port may redeploy the cluster gateway app before the public port becomes available

On clusters with Wodby infrastructure version `4.0.0` or newer, TCP publishing requires the cluster's `TCPRoute`
capability and UDP publishing requires its `UDPRoute` capability. Some provider-managed Gateway API installations use
the Standard channel, which can support Wodby's HTTP/HTTPS routing without these optional route types. When a protocol
is unavailable, the port page explains the limitation and prevents the port from being published. You can review the
detected capabilities under `Clusters > [Cluster] > Infrastructure > Operations`; see
[Gateway API compatibility](../clusters/infrastructure.md#gateway-api-compatibility) for details.

Wodby assigns the public port automatically from the cluster-wide range `31222`-`32222`. The first available port in that range is used.

On regular managed Kubernetes clusters, published ports are exposed through the cluster load balancer. In single-node managed clusters that use direct node traffic instead of a load balancer, Wodby manages the node firewall rules for this published-port range.

When a port is published, the dashboard shows the assigned public port. For SSHD services, it also shows ready-to-use `ssh`, `sftp`, and `scp` command examples based on the app environment main route.

If you plan to use published SSH ports, see [SSH keys](../user/ssh-keys.md).

### Port Settings

Port settings are supported for published TCP ports on Envoy Gateway clusters. They are not applied to unpublished ports or UDP ports.

Supported port settings are:

| Setting | Value |
| --- | --- |
| `idle_timeout` | duration such as `30s`, `5m`, or `1h` |
| `connection_limit` | positive integer |
| `tcp_keepalive` | `true` or `false` |

Changing port settings marks the app environment as needing redeploy and redeploys the cluster gateway app.
