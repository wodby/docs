# Tailscale

Tailscale supports two separate integration types in Wodby:

- `application_access` publishes an app or selected HTTP endpoints through a Wodby-managed connector.
- `vpn` supplies credentials to a persistent Tailscale Node service deployed as part of an app stack.

Both use the same Tailscale provider and OAuth setup, but they have different lifecycles. Application Access is managed
from the app environment's Access settings; a Tailscale Node is an ordinary app service managed through its stack.

## Tailscale-side setup

Before creating the integration in Wodby:

1. Create a tag named `wodby` under `Access Control > Tags` in the Tailscale admin console.
2. Enable both MagicDNS and HTTPS Certificates under `DNS`.
3. Create OAuth credentials under `Settings > Trust credentials`:
   - give the credentials a recognizable description such as `wodby`
   - grant Write access to both `Auth Keys` and `Devices`
   - restrict the credentials to the `wodby` tag

## Setup fields

| Field | Required | Provider variable | Purpose |
| --- | --- | --- | --- |
| Client ID | Yes | `TAILSCALE_CLIENT_ID` | OAuth client identity |
| Client Secret | Yes | `TAILSCALE_CLIENT_SECRET` | OAuth client credential |
| Tailnet DNS name | Yes | `TAILSCALE_TAILNET` | DNS suffix used for app endpoint hostnames |

The Tailnet DNS name is collected in the final step of integration creation. You can find it on the Tailscale admin
console's DNS page.

## Application Access

Select Protected mode during app creation, or open `Apps > [App] > [Environment] > Settings > Access`. Choose the
Tailscale integration and either Entire app or Selected endpoints scope.
Tailscale provides the Private network access type automatically; there is no separate protected-publishing type.

Wodby assigns one endpoint hostname for each distinct enabled external HTTP destination from the app, service, port,
and tailnet names. It creates and retires the tagged Tailscale devices and manages the connector credentials. There is
no DNS-zone, policy, or primary-hostname input in Wodby because access is governed by your tailnet and Tailscale access
controls.

When access is removed or the app environment is deleted, Wodby removes each endpoint connector, tagged device, auth key,
and Wodby-held auth-key secret. Wodby does not remove the `wodby` tag, MagicDNS settings, HTTPS certificate setting, or
your tailnet access rules. Temporary cluster or Tailscale API failures are retained as retryable cleanup obligations on
the integration page; keep the integration credentials available until cleanup finishes.

Tailscale Application Access endpoints are not published through Wodby's public gateway. A service port's `private`
flag alone does not create a Tailscale hostname; configure App Access explicitly for the app environment.

### HTTP endpoints and application ports

Tailscale Application Access currently carries HTTP endpoints only. It does not advertise arbitrary app TCP or UDP
ports, such as SSH, database, Redis, or custom-protocol ports, into the tailnet.

Entire app scope prevents public TCP or UDP port publishing while Access is active. Selected endpoints scope can
coexist with separately published TCP or UDP ports, but those ports remain public through Wodby's gateway and are not
protected by Tailscale. Unpublished ports remain cluster-internal.

The Tailscale Node integration below is a separate service-credential workflow. Deploying a node does not
automatically expose other app services or change the App Access endpoint set.

## Tailscale Node

Choose the `Tailscale Node` integration type when deploying the standalone Tailscale stack or a custom stack that
contains the Tailscale service. Wodby creates a scoped auth key for that app service, and the resulting persistent
workload joins your tailnet as a node.

This is different from Application Access. The node is visible and configurable as part of the app's services and can
exist without publishing one of the app's HTTP endpoints. Removing Application Access does not remove a standalone
Tailscale Node, and deleting the node service does not change an app environment's Access setting.

OpenClaw uses Application Access and no longer embeds the Tailscale service. The standalone Tailscale stack and custom
node-oriented stacks continue using the `vpn` integration type.

## Related pages

- [App access](../apps/access.md)
- [Application Access providers](access.md)
- [VPN providers](vpn.md)
