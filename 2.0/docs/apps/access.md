# App access

App access controls whether an app environment is published through ordinary Wodby routes or through a supported access
provider. It applies to HTTP endpoints and is configured independently for each app environment.

## Availability

Application Access requires an active paid subscription. Organizations on the free Developer plan can create apps in
`Public` mode, but `Protected` mode is unavailable until the organization upgrades.

Before scheduling a downgrade to Developer, remove Application Access from every app environment. If paid access becomes
unavailable while an existing configuration remains, its protection stays active and readable, but it cannot be
changed. You can still remove it, and Wodby can still finish provider cleanup.

## Modes

The app creation form offers two modes:

- `Public` is the default. Wodby publishes enabled HTTP routes normally.
- `Protected` uses an [Application Access integration](../providers/access.md). The provider supplies either protected
  publishing or private-network routing for the selected endpoints, and Wodby suppresses the corresponding public
  routes.

Some stacks require Protected mode. The stack can also require an access type and scope, and can optionally restrict
the provider. In that case the required choices cannot be changed and you must select a compatible Application Access
integration before creating the app.

Protected mode requires an active Application Access integration, an enabled HTTP endpoint, and a cluster that uses
managed app routing.

A standalone Tailscale Node is not an Access mode. It remains an app service for cases where the node itself is the
deployed workload; see [VPN providers](../providers/vpn.md).

## Configure access during app creation

In Step 4, `App settings`, select `Protected` under `Access` and then configure:

1. `Access provider`: the integration that will provide the app's protected or private connection path.
2. `Access type`: Protected publishing or Private network when the selected provider offers both. Providers with one
   type select it automatically.
3. `Scope`: whether access covers the entire app or selected endpoints. With Selected endpoints, choose one or more
   enabled HTTP destinations and mark one as primary.
4. Provider-specific settings, such as a Cloudflare DNS zone and Access policy for Protected publishing.
5. A primary hostname when the provider uses your own domain.

For Entire app scope, Wodby automatically includes every enabled HTTP destination that normally has an external route.
Routes and paths that target the same app port share one provider address. For Selected endpoints, the form lists the
eligible HTTP destinations from the enabled stack services and starts with the main destination selected. You can
change the selection before creation or later from `Apps > [App] > [Environment] > Settings > Access`.

Wodby waits until the first successful workload deployment before creating the provider resources. Public routes in
the selected scope are suppressed from the beginning, so the app is not temporarily published while provider access
is being prepared.

## Scope

### Entire app

The access provider becomes the publication path for the app environment. Wodby creates a provider address for every
distinct enabled external HTTP destination and suppresses all ordinary public HTTP routes for the environment. Enabling
or disabling an app service automatically reconciles this address inventory after deployment.

For example, a Drupal stack can receive one Access address for Drupal and another for Mailpit when both expose external
HTTP routes. Routes with different paths or aliases that target the same app port share one Access address.
A database or other service that only exposes a private or non-HTTP port does not receive an App Access address.

An app with published public TCP or UDP ports cannot switch to Entire app access until those ports are unpublished.
Application Access protects HTTP endpoints; it does not place arbitrary TCP or UDP ports behind an identity proxy.

### Selected endpoints

Only routes targeting the selected HTTP endpoints are suppressed. Other HTTP routes and published ports keep their
existing behavior. Use this for an admin interface, dashboard, or other internal endpoint while the public site remains
available normally.

## Access types

### Protected publishing

Protected publishing creates provider-facing hostnames that remain reachable from the Internet but require the
provider's identity policy before traffic reaches the app. Cloudflare implements this with a managed Tunnel,
customer-zone DNS records, and a reusable Cloudflare Access policy.

### Private network

Private network access makes endpoints reachable only from devices connected to the provider's private network. It
does not display a public identity login page. Tailscale uses tailnet hostnames; Cloudflare uses the existing Wodby
technical hostnames as private hostname routes for Cloudflare One Client devices.

Cloudflare Private network requires the customer's Gateway TCP and UDP proxy, device enrollment, Split Tunnels, and
DNS routing to be configured before users can connect. Wodby manages the app tunnel and private hostname routes, not
the customer's device or Gateway policies. See [Cloudflare](../providers/cloudflare.md#private-network-access).

Private network access controls how traffic reaches the app; it does not make the hostname itself secret. A Cloudflare
private endpoint's Wodby technical hostname may still resolve outside WARP, but Wodby's public gateway does not serve
the suppressed route.

## Primary hostname

The primary hostname is the canonical protected address of the app environment. Wodby uses it as:

- the primary domain shown for the app environment
- the provider's primary application domain
- `WODBY_PRIMARY_HOST` and `WODBY_PRIMARY_URL` inside app services
- part of `WODBY_HOSTS`, which applications can use for allowed-host configuration
- the base address for links generated outside an incoming request, such as email links and cron callbacks

For Cloudflare Protected access, select the DNS zone and then choose the `Flattened` or `Hierarchical` hostname
structure. The form previews the pattern and an example hostname that Wodby will use for additional services:

- `Flattened` keeps every name directly below the selected zone. A root-domain prefix of `dev.cms` and zone
  `example.com` produce `dev-cms.example.com`; an additional Mailpit endpoint becomes
  `mailpit-dev-cms.example.com`. This is the default and works with Cloudflare Universal SSL.
- `Hierarchical` preserves the prefix as `dev.cms.example.com`; Mailpit becomes
  `mailpit.dev.cms.example.com`. The form warns that you must create an active
  [Cloudflare Advanced Certificate](https://developers.cloudflare.com/ssl/edge-certificates/advanced-certificate-manager/)
  covering both `dev.cms.example.com` and `*.dev.cms.example.com`. Wodby does not create, manage, or inspect this
  certificate; certificate coverage is your responsibility. Cloudflare
  [Total TLS](https://developers.cloudflare.com/ssl/edge-certificates/additional-options/total-tls/) does not issue
  certificates for Cloudflare Tunnel hostnames, so it cannot provide this coverage.

You can replace the suggested primary hostname with another hostname in the selected zone. Wodby derives the other
endpoint hostnames from it.

Enter a hostname only: do not include `https://`, a path, or a port. Using a subdomain is safer than selecting the zone
apex because the apex may already serve another site.

Cloudflare Private network reuses the Wodby technical hostname for each selected endpoint. Tailscale assigns the
hostname from the app and tailnet names. Neither private-network type shows a hostname field.

Wodby does not offer `*.trycloudflare.com` addresses for App Access. Cloudflare Quick Tunnels assign a random,
temporary hostname and are intended for testing and development without an uptime guarantee. Wodby uses a managed,
persistent Tunnel instead. Protected publishing uses stable hostnames in a customer-owned Cloudflare zone; Private
network access reuses stable Wodby technical hostnames. See
[Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/).

## Routes, technical domains, and private ports

Protected endpoints are not served through Wodby's public gateway. Their matching public routes, including generated
technical routes, are disabled while access is active. The Domains and Redirects lists display the effective Cloudflare
or Tailscale address for each protected destination. For Cloudflare Private network this is the same technical hostname,
now routed privately through Cloudflare One instead of published by Wodby's public gateway. Routes that target one app
port share that address. For Selected endpoints scope, routes for unselected endpoints remain public.

The `private` flag in a service definition is different. It prevents a port from being published through public Wodby
routing, but it does not create a Cloudflare or Tailscale address. Application Access is the explicit app environment
setting that asks a provider to publish an eligible HTTP endpoint.

### Published TCP and UDP ports

Published ports use the cluster's public gateway and are outside the Application Access connector. They do not receive
a Cloudflare or Tailscale hostname or inherit an identity or private-network policy.

- With Entire app scope, Wodby requires existing published ports to be unpublished and prevents publishing new ones
  while Access is active.
- With Selected endpoints scope, TCP and UDP ports can remain published, but they remain public and are not protected
  by the Access provider.
- An unpublished non-HTTP port remains reachable only through internal Kubernetes networking.

Use [Publishing ports](endpoints.md#publishing-ports) for public TCP or UDP exposure. App Access endpoint selection
contains HTTP destinations only.

## Providers

| Provider | Access type | Hostname |
| --- | --- | --- |
| [Cloudflare](../providers/cloudflare.md) | Protected: Cloudflare Tunnel plus a reusable Access policy | A hostname in a selected Cloudflare DNS zone |
| [Cloudflare](../providers/cloudflare.md#private-network-access) | Private network: Cloudflare hostname route for enrolled Cloudflare One Client devices | The endpoint's Wodby technical hostname |
| [Tailscale](../providers/tailscale.md) | Private network: a tailnet endpoint reachable by authorized Tailscale users and devices | Assigned from the app and tailnet names |

Wodby creates and reconciles provider resources when access is enabled or changed, and removes them when access is
removed or the app environment is deleted. Removing access restores the matching ordinary public routes unless the stack
requires Protected mode.

The access type is fixed while Access is enabled. To move an existing app environment between Protected publishing and
Private network access, remove Access and enable it again with the other type. Wodby finishes the old provider cleanup
before creating the replacement resources.

## Resource cleanup

Wodby records the provider resources it creates so cleanup can continue even after App Access or the app environment has
been removed. Cleanup also runs after an initial access setup fails, before that configuration can be retried.

Removing App Access restores the matching Wodby public routes first. Deleting an app environment removes its workloads
first so an access connector cannot continue reaching the app while provider policy is being removed. Wodby then
removes its connector resources, provider endpoints, credentials, and other managed resources.

A temporary provider or cluster API failure does not prevent app deletion or leave App Access enabled in Wodby. The
task finishes with a warning, Wodby retains a cleanup obligation, and a separate cleanup task is attempted. You can
review the warning and select `Retry cleanup` from either:

- `Apps > [App] > [Environment] > Settings > Access`, while the app environment still exists
- the access integration page, including after the app environment has been deleted

The integration cannot be deleted while cleanup is outstanding because Wodby still needs its credentials. Correct an
expired credential or missing provider permission on the integration, then retry cleanup.

Cleanup only mutates resources Wodby still recognizes as its own. For example, if a Cloudflare DNS record or private
hostname route was changed after Wodby created it, Wodby leaves the resource untouched and records a warning instead
of deleting it or restoring an older value. Customer-managed Cloudflare policies and certificates, and
customer-managed Tailscale tags and access rules, are never deleted.

## Related pages

- [Endpoints](endpoints.md)
- [App environments](environments.md)
- [Application Access providers](../providers/access.md)
- [Integration types](../integrations/types.md)
