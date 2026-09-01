# VPN providers

VPN integrations supply credentials to services that run as persistent private-network nodes inside an app environment.

Machine name: `vpn`

Use this integration type when you want to deploy and manage the network node itself as an app service. This includes
the standalone Tailscale stack and custom stacks containing the Tailscale service.

## VPN nodes versus Application Access

A VPN node and [Application Access](access.md) solve different problems:

| Capability | VPN node | Application Access |
| --- | --- | --- |
| Managed as | An app service in the stack | An app environment Access setting |
| Lifetime | Persists with the service | Reconciled with selected HTTP endpoints |
| Primary use | Join the tailnet as a node | Make app endpoints reachable privately |
| Requires an HTTP endpoint | No | Yes |

Do not add a Tailscale service to a stack only to make its HTTP endpoints private. Use Application Access for that
case. Keep the service model when the Tailscale node itself is the workload you want to deploy.

## Supported providers

| Provider | Notes |
| --- | --- |
| [Tailscale](tailscale.md#tailscale-node) | Provides the built-in Tailscale Node service integration |

## Related pages

- [Integration types](../integrations/types.md)
- [Application Access providers](access.md)
- [Tailscale](tailscale.md)
