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
