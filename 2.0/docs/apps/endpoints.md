# Endpoints

Endpoints are the public or private entry points to your app services. They consist of HTTP routes and/or published ports.

From `Apps > [Instance] > Endpoints` you can manage:

- `Routes`
- `Ports`
- route settings
- port settings
- `Auths`

## Routes

Routes are used for HTTP and HTTPS traffic. A route matches a hostname and path, then either sends traffic to an app service endpoint or redirects the request.

Each backend route has:

- app service
- endpoint
- port
- hostname
- path
- path match type: `prefix` or `exact`
- TLS mode: `Let's Encrypt` or `None`
- whether the route should be `Main`
- whether the route should be `Primary`

Redirect routes are supported on clusters that use Envoy Gateway. A redirect route can set the target scheme, host, path, and status code. Supported redirect status codes are `301` and `302`.

### Technical routes

By default, Wodby generates technical routes for app services that expose HTTP endpoints.

The default hostname pattern is:

- `<service-name>.<instance-name>.<app-name>.<org-name>.wodby.app`

The main service with HTTP endpoints also gets a shorter technical hostname:

- `<instance-name>.<app-name>.<org-name>.wodby.app`

Wodby automatically issues and renews Let's Encrypt certificates for these technical routes.

### Custom routes

From the dashboard you can add a custom route to an HTTP app service endpoint.

Use a custom route when you want to:

- attach your own hostname
- serve an app service under a specific path, such as `example.com/blog`
- create an HTTP redirect
- choose whether the route should become the main app instance route or the primary route for a service endpoint

Only services with HTTP endpoints are available in this flow.

### Main and primary

Wodby distinguishes between two default-route flags:

- `Main` is the main route for the whole app instance
- `Primary` is the default route for a specific app service endpoint

Main routes are always primary. In practice:

- an app instance has one main route
- each app service can have its own primary route

### TLS certificates

Wodby can issue TLS certificates for endpoint routes. For public docs, treat [Let's Encrypt](https://letsencrypt.org/) as the supported issuer for managed certificate flows today. Wodby automatically renews Let's Encrypt certificates before they expire.

`Organization > Certificates` shows issued certificates, issuer, key type, status, issue date, renewal date, expiry date, and where each certificate is used. The list can include certificates used by application routes and supported database resources.

Custom certificate upload is coming soon. The planned model is organization-level certificate management with endpoint-level selection.

### Route status and private routes

The route list shows status, certificate issuer, and whether a route is main or primary.

You may also see private routes generated for internal use. Those are not managed the same way as regular public custom routes.

## Route Settings

Route settings control HTTP routing behavior for clusters that use Envoy Gateway. They are predefined settings rather than arbitrary Kubernetes annotations.

Route settings can be configured at two scopes:

- app instance defaults, inherited by backend routes in the app instance
- route-specific settings, which override app instance defaults for one route

Supported route settings are:

| Setting | Value |
| --- | --- |
| `https_redirect` | `true` or `false` |
| `no_index` | `true` or `false` |
| `request_body_size` | size with `Ki`, `Mi`, or `Gi`, such as `64Mi` |
| `session_affinity` | `cookie` or `header` |
| `path_rewrite` | path starting with `/` |

For new Envoy Gateway app instances, Wodby creates default route settings to match the previous ingress behavior:

- HTTPS redirect is enabled by default
- session affinity uses cookies by default
- generated technical routes get `no_index` enabled by default

Changing route settings marks the affected app service or app instance as needing redeploy.

!!! note "Legacy ingress settings"
    Older clusters that still use Ingress Nginx may expose legacy ingress annotation settings. Envoy Gateway clusters use the route settings above. Kubernetes annotations are still available separately where service or stack templates support Kubernetes resource annotations.

## Auths

The `Auths` screen manages HTTP basic authentication.

Each auth entry has:

- username
- password
- optional realm
- optional app service scope
- optional route scope

This gives you three practical scopes:

- app-level, when both service and route are left empty
- service-level, when a service is selected and route is left empty
- route-level, when a specific route is selected

Auth precedence is most-specific first:

- route auth overrides service auth
- service auth overrides app-level auth

The edit screen can also reveal the current password for an existing auth entry.

Changing auth settings marks the affected app services and app instance as needing redeploy.

## Ports

The `Ports` screen lists endpoint ports defined by your app services.

Each port has:

- app service
- endpoint name
- protocol
- internal port number
- optional public port

### Publishing ports

Manual port publishing is intended for non-HTTP ports such as SSH or other TCP or UDP services.

- HTTP exposure is handled through routes, not through manual public-port publishing
- only non-private, non-HTTP ports can be published or unpublished from this screen
- publishing or unpublishing a port may redeploy the cluster gateway app before the public port becomes available

Wodby assigns the public port automatically from the cluster-wide range `31222`-`32222`. The first available port in that range is used.

When a port is published, the dashboard shows the assigned public port. For SSHD services, it also shows ready-to-use `ssh`, `sftp`, and `scp` command examples based on the app instance main route.

If you plan to use published SSH ports, see [SSH keys](../user/ssh-keys.md).

### Port Settings

Port settings are supported for published TCP ports on Envoy Gateway clusters. They are not applied to unpublished ports or UDP ports.

Supported port settings are:

| Setting | Value |
| --- | --- |
| `idle_timeout` | duration such as `30s`, `5m`, or `1h` |
| `connection_limit` | positive integer |
| `tcp_keepalive` | `true` or `false` |

Changing port settings marks the app instance as needing redeploy and redeploys the cluster gateway app.
