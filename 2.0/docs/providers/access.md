# Application Access providers

Application Access providers publish HTTP endpoints without exposing the matching routes through Wodby's ordinary
public gateway.

Machine name: `application_access`

Use an Application Access provider when:

- an internal app should be available only to approved users or devices
- an admin or operational endpoint should be protected while the main site remains public
- the access provider should own the external hostname and connection path

Application Access is configured for an app instance, not attached to an individual service. The selected scope can
cover the entire app or only selected HTTP endpoints.

## Supported providers

| Provider | Access model |
| --- | --- |
| [Cloudflare](cloudflare.md) | Cloudflare Access identity policies or private-network routing through Cloudflare One |
| [Tailscale](tailscale.md) | Private-network access through a Tailscale tailnet |

The providers use one common Wodby workflow but keep their provider-specific access types and settings. Cloudflare
Protected access requires a DNS zone, customer hostname, and reusable Access policy. Cloudflare Private network and
Tailscale assign or reuse provider-routed hostnames and do not require DNS-zone or policy selection in Wodby.

See [App access](../apps/access.md) for modes, scopes, endpoints, route suppression, and primary-hostname behavior.
