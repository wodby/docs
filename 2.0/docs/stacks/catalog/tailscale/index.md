# Tailscale

The Wodby Tailscale catalog stack runs a persistent Tailscale node as an app service. The node joins your tailnet. The
current composition and defaults are in [`wodby/stack-tailscale`](https://github.com/wodby/stack-tailscale).

## Before you create the app

The stack requires one Tailscale integration of the `Tailscale Node` type. Set up Tailscale and create the integration
first. See [Tailscale-side setup](../../../providers/tailscale.md#tailscale-side-setup) and
[Tailscale Node](../../../providers/tailscale.md#tailscale-node).

Wodby creates a scoped auth key for the app service, and the node uses it to join your tailnet.

## Node state

The stack creates a **State** volume of 1 GB for the node. The volume is required.

## Serve another service

The optional **Service to serve** link points the node at another service in the app environment. The stack contains
only the node, so use this link in a custom stack that also contains the service to serve.

## Limits

- Do not add a Tailscale node to a stack only to make its HTTP endpoints private. Use
  [Application Access](../../../apps/access.md) for that. Keep this stack when the node itself is the workload you want
  to deploy.
- Deploying a node does not expose other app services and does not change the app environment's Access setting.
- Removing Application Access does not remove the node, and deleting the node service does not change Access.

See [VPN providers](../../../providers/vpn.md) for how nodes and Application Access differ.
