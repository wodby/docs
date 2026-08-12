# FRP Server

The Wodby FRP Server catalog stack runs an [`frps`](https://gofrp.org/en/)
server for workloads that are outside the cluster. An external `frpc` client
connects to the server's published control port and registers one or more HTTP
hostnames. Wodby terminates public TLS for those hostnames and forwards HTTP to
FRPS, which sends the requests through the tunnel to the external workload.

This application stack is separate from the FRPC infrastructure component
installed on Kubernetes machines. It does not configure cluster connectivity
or require Kubernetes permissions.

## Deploy and expose FRPS

1. Create an app from the **FRP Server** catalog stack and deploy it.
2. Open **Apps > [App] > [Instance] > Endpoints > Ports**, select the `proxy`
   endpoint, and publish its `control` TCP port. Wodby assigns a public port in
   the cluster's published port range.
3. Record the public hostname and assigned port. Open the FRPS app service's
   **Configuration > Tokens** tab and reveal its generated `auth_token` value.
   Every FRPC client must use the same token.
4. Add a custom route for every hostname listed in an FRPC proxy's
   `customDomains`. Target the FRPS service's `proxy` endpoint and
   `proxy-http` port.

The `dashboard` port on the `proxy` endpoint has separate generated
`dashboard_user` and `dashboard_password` token values. Its port-specific
technical Wodby route is suitable for administration; do not reuse the
dashboard password as the FRPC token.

## Configure an FRPC client

The following client configuration exposes a dashboard and API running on an
external server. Replace the example hostname, published port, and token with
the values from the Wodby app:

```toml
serverAddr = "tunnel.example.com"
serverPort = 31500

auth.method = "token"
auth.token = "replace-with-the-generated-auth-token"
transport.tls.enable = true

[[proxies]]
name = "dashboard"
type = "http"
localIP = "127.0.0.1"
localPort = 3000
customDomains = ["tunnel.example.com"]

[[proxies]]
name = "api"
type = "http"
localIP = "127.0.0.1"
localPort = 8080
customDomains = ["api.tunnel.example.com"]
```

Create routes for both `tunnel.example.com` and
`api.tunnel.example.com`. Point their DNS records at the Wodby cluster before
enabling Let's Encrypt. Do not publish the `proxy-http` port manually; HTTP
traffic enters through Wodby routes.

## Migrate the Wodby backend Compose clients

The backend Compose setup already runs one FRPC container for the dashboard
and one for the API. For an FRPS app whose published control hostname is also
the route's root hostname, update these environment variables:

```dotenv
FRPC_HOST=tunnel.example.com
FRPC_PORT=31500
FRPC_AUTH_TOKEN=replace-with-the-generated-auth-token
```

The Compose clients register `tunnel.example.com` for the dashboard and
`api.tunnel.example.com` for the API. Restart both FRPC containers after the
change, confirm the proxies are online in the FRPS dashboard, and test both
Wodby routes before removing the previous FRPS server.

When a client workload itself moves into Wodby, route directly to that app
service instead of tunneling it back through FRPS.
