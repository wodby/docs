# Tailscale

Tailscale is available in Wodby as a `vpn` provider. Use it when you want Wodby-managed app services to join your Tailscale network.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Client ID | Yes | `TAILSCALE_CLIENT_ID` |
| Client Secret | Yes | `TAILSCALE_CLIENT_SECRET` |
| Tailnet DNS name | Yes | `TAILSCALE_TAILNET` |

`TAILSCALE_TAILNET` is collected as a finalization step during integration setup.

## Tailscale-side setup

Before creating the integration in Wodby:

1. Create a tag named `wodby` in the Tailscale admin console.
2. Enable both MagicDNS and HTTPS Certificates for the tailnet.
3. Create OAuth credentials with write access to Auth Keys and the `wodby` tag.

## Usage

Wodby uses these permissions to create auth keys for app services served through Tailscale. Those auth keys are deleted when the corresponding app service is removed.

The current Tailscale integration creates a private provider route only when all of the following are true:

- an enabled Tailscale VPN app service links to the target app service
- the target service's main endpoint has a main HTTP port marked `private`
- the VPN app service uses a configured Tailscale integration

The resulting hostname belongs to the tailnet and is not published through Wodby's public HTTP gateway. It can be the
target endpoint's `Primary` route, but it cannot be the app instance's public `Main` route.

A non-main private port does not receive a Tailscale hostname merely because it is marked `private`. For example, an
internal metrics port remains available through Kubernetes service networking without appearing as a public or
Tailscale route.
