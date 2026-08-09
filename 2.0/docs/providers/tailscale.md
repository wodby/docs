# Tailscale

Tailscale supports two separate integration types in Wodby:

- `application_access` publishes an app or selected HTTP endpoints through a Wodby-managed connector.
- `vpn` supplies credentials to a persistent Tailscale Node service deployed as part of an app stack.

Both use the same Tailscale provider and OAuth setup, but they have different lifecycles. Application Access is managed
from the app instance's Access settings; a Tailscale Node is an ordinary app service managed through its stack.

## Tailscale-side setup

Before creating the integration in Wodby:

1. Create a tag named `wodby` under `Access Control > Tags` in the Tailscale admin console.
2. Enable both MagicDNS and HTTPS Certificates under `DNS`.
3. Create OAuth credentials under `Settings > Trust credentials`:
   - give the credentials a recognizable description such as `wodby`
   - grant Write access to both `Auth Keys` and `Devices`
   - restrict the credentials to the `wodby` tag

## Setup fields

| Field | Required | Purpose |
| --- | --- | --- |
| Client ID | Yes | OAuth client identity |
| Client Secret | Yes | OAuth client credential |
| Tailnet DNS name | Yes | DNS suffix used for app endpoint hostnames |

The Tailnet DNS name is collected in the final step of integration creation. You can find it on the Tailscale admin
console's DNS page.

## Application Access

Select Protected mode during app creation, or open `Apps > [App] > [Instance] > Settings > Access`. Choose the
Tailscale integration and either Entire app or Selected endpoints scope.

Wodby assigns one endpoint hostname for each distinct enabled external HTTP destination from the app, service, port,
and tailnet names. It creates and retires the tagged Tailscale devices and manages the connector credentials. There is
no DNS-zone, policy, or primary-hostname input in Wodby because access is governed by your tailnet and Tailscale access
controls.

When access is removed or the app instance is deleted, Wodby removes each endpoint connector, tagged device, auth key,
and Wodby-held auth-key secret. Wodby does not remove the `wodby` tag, MagicDNS settings, HTTPS certificate setting, or
your tailnet access rules. Temporary cluster or Tailscale API failures are retained as retryable cleanup obligations on
the integration page; keep the integration credentials available until cleanup finishes.

Protected Tailscale endpoints are not published through Wodby's public gateway. A service port's `private` flag alone
does not create a Tailscale hostname; configure App Access explicitly for the app instance.

## Tailscale Node

Choose the `Tailscale Node` integration type when deploying the standalone Tailscale stack or a custom stack that
contains the Tailscale service. Wodby creates a scoped auth key for that app service, and the resulting persistent
workload joins your tailnet as a node.

This is different from Application Access. The node is visible and configurable as part of the app's services and can
exist without publishing one of the app's HTTP endpoints. Removing Application Access does not remove a standalone
Tailscale Node, and deleting the node service does not change an app instance's Access setting.

OpenClaw uses Application Access and no longer embeds the Tailscale service. The standalone Tailscale stack and custom
node-oriented stacks continue using the `vpn` integration type.

## Related pages

- [App access](../apps/access.md)
- [Application Access providers](access.md)
- [VPN providers](vpn.md)
