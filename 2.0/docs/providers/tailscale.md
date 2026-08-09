# Tailscale

Tailscale is an `application_access` provider. Use it to make an app or selected HTTP endpoints reachable through your
tailnet instead of Wodby's public gateway.

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

## Configure an app

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

## Related pages

- [App access](../apps/access.md)
- [Application Access providers](access.md)
