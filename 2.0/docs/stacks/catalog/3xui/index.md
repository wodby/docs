# 3X UI

The Wodby 3X UI catalog stack runs the 3X UI panel. The current composition and defaults are in
[`wodby/stack-3xui`](https://github.com/wodby/stack-3xui).

## Open the panel

The panel listens on port `2053`, the only endpoint of the service. Wodby protects the service's public domains with
basic auth by default. Each app service gets its own generated password. Reveal it under **Endpoints > Auths** for the
app environment. See [Auths](../../../apps/endpoints.md#auths). You can turn the protection off when you create the
app, or later by deleting the auth entry.

On the first start with an empty database, the panel creates its default administrator account. Wodby generates no
credentials. Change the account in the panel.

## Panel settings

The panel keeps its settings, including the panel port and path, in its database. Change them in the panel, not
through environment variables. Keep the panel port at `2053`, because the endpoint and the health checks use it.

Wodby does not expose the ports of inbounds that you create in the panel.

Add other variables as [environment variables](../../../apps/environment-variables.md) on the app service and deploy.

## Data

The stack creates two volumes, each 1 GB:

| Volume | Path | Contents |
| --- | --- | --- |
| **Data** | `/etc/x-ui` | The panel database with users, panel settings, and inbounds |
| **Certs** | `/root/cert` | Files kept in the `/root/cert` directory |

Wodby defines no links, backups, or imports for this service.
