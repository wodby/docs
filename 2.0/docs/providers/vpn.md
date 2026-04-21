# VPN providers

VPN providers are third-party services whose integrations expose the `vpn` type. Use this group when you want supported Wodby services connected to a private network.

Machine name: `vpn`

Use a VPN provider when:

- you want app services to join a private network instead of being reachable only through public ingress
- you need private service-to-service access through a supported VPN provider
- you want Wodby to manage provider-specific connection details on behalf of a service

## Where it is used in Wodby

VPN provider integrations are used for:

- app services that should join a Tailscale tailnet
- private-network access patterns where the service should not rely only on public endpoints

## Supported providers

| Provider | Notes |
| --- | --- |
| [Tailscale](tailscale.md) | Currently the only built-in VPN provider |

## Related pages

- [Integration types](../integrations/types.md)
- [Tailscale](tailscale.md)
- [Providers overview](index.md)
