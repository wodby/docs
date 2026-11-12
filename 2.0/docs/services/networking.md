---
description: Define how a Wodby service exposes ports through endpoints and connects to other services in the same app environment through links.
---

# Service networking

Service networking covers how a service exposes ports and how it connects to other services in the same app environment.

Use endpoints for network access exposed by the service. Use links for service-to-service dependencies and connection
rules.

## Endpoints

Services that expose network access can define endpoints. An endpoint groups together one or more ports that belong to
the same exposed workload. Wodby resolves the concrete Kubernetes Service from the Helm chart later. HTTP routes are
attached at the app level.

Each endpoint must resolve to a distinct Kubernetes Service. When one rendered Service exposes several ports, define
all of those ports under one endpoint even when they use different protocols or serve different purposes. Use multiple
endpoints only when the chart renders separate Kubernetes Services for them.

Supported port protocols are:

1. `http` for web traffic and routes with TLS certificates
2. `tcp` for generic TCP traffic
3. `udp` for UDP traffic

Ports can also be marked as `private` to keep them internal-only. A private port remains available to Kubernetes
services inside the cluster, but Wodby does not generate a technical route for it and it cannot be used by a public
custom route or published as a public TCP or UDP port.

`private` is a service-template policy, not the current publication state of a port. A non-private port that has no
route is still public-capable and can be exposed later; a private port cannot. Provider-backed publication is an
explicit app environment [Private App Access](../apps/access.md) setting rather than an automatic effect of the
`private` flag.

One port per endpoint can be marked as main. If no port is marked as main, the first port becomes main automatically.

If a service defines a single endpoint, that endpoint becomes main automatically. If it defines multiple endpoints,
mark one of them as main.

When an app service is main, Wodby attaches the app environment's root technical route to a public HTTP port on the
service's main endpoint. This technical route is independent of the app environment's canonical `Main` route, which may be
a custom domain.

Service endpoints are defined under the [`endpoints` section](template.md#endpoints) in a service template.

```yaml
endpoints:
- name: http
  workload: main
  ports:
  - name: http
    number: 80
    protocol: http
    main: true
    routeDefaults:
      request_timeout: 5m
      backend_request_timeout: 2m
```

`workload` is optional. If omitted, the endpoint targets the primary workload.

HTTP ports can define `routeDefaults` when the service normally needs specific
[HTTP route settings](../apps/endpoints.md#route-settings). These are defaults, not restrictions. Wodby resolves the
effective value from app environment defaults, then the active service revision's port defaults, then an explicit domain
override. A service revision upgrade or rollback therefore selects the matching revision's defaults without copying
them into every app route.

`routeDefaults` is not supported on TCP or UDP ports. Service import validates setting names and values, including the
relationship between request and backend request timeouts. Inherited services merge route defaults by endpoint name,
port name, and setting name; a child value replaces the matching base value. Derivative endpoints use the same port
format and behavior.

### HTTP/2 and gRPC

Wodby domains answer clients over HTTP/1.1, which most web applications need. Clients that require HTTP/2, such as gRPC
clients, can't connect that way. Mark the port with `http2: true`, and domains that serve it accept HTTP/2 as well:

```yaml
endpoints:
- name: api
  ports:
  - name: grpc
    number: 8080
    protocol: http
    main: true
    http2: true
    routeDefaults:
      request_timeout: 0s
      backend_request_timeout: 0s
```

The backend must also accept cleartext HTTP/2 (h2c) from the gateway. Declare this on the port of the Kubernetes Service
that your chart renders, with `appProtocol: kubernetes.io/h2c`. The generic `stateful` chart supports it from version
`0.3.0` in `service.ports[].appProtocol`.

The gateway then sends every request to that port over HTTP/2, including WebSocket upgrades, which most servers don't
accept that way. If the service also serves WebSockets, expose them on a separate endpoint without `appProtocol`. Long
gRPC streams usually also need the route timeouts turned off, as in the example.

A browser that has an HTTP/2 connection open to such a domain can reuse it for another domain of the same environment
and get `404 Not Found` there. Set `http2` only on ports whose clients need it.

### Dynamic public backend ports

Most published TCP and UDP ports keep a fixed port inside Kubernetes and use a separately assigned public port. Some
charts instead use one value as both the advertised public port and the port rendered on their Kubernetes Service.
Those charts can opt in to public-port-driven routing:

```yaml
endpoints:
- name: ssh
  workload: shell
  ports:
  - name: ssh
    number: 22
    protocol: tcp
    routeToPublicPort: true

helm:
  values:
  - name: shell.port
    value: "{{service.endpoints.ssh.ports.ssh.effectivePort}}"
```

Set `routeToPublicPort: true` only when the chart renders its Kubernetes Service port from the public assignment.
Wodby then targets the assigned number when it creates the TCP or UDP route. When the port is published or unpublished,
Wodby starts a partial deployment of the owning app service right away if that service is deployed, enabled, and in `OK`
status, so the chart and the route cannot keep different port numbers. Otherwise, the next deployment applies the change.
Unless the chart renders the assigned number during import, its Service port must use the manifest port's name. The option is supported only for non-private TCP and UDP ports. When `routeToPublicPort` is
omitted, Wodby routes to the manifest's fixed `number`.

When a service's Helm values, environment variables, or processed configs read a port's `publicPort` or
`effectivePort` token, publishing or unpublishing the port marks the app environment as
[`needs redeploy`](../apps/deploys.md#needs-redeploy), as a domain change does. The next deployment applies the new
value. The mark also stays if the immediate deployment of a `routeToPublicPort` port fails, so you can deploy again.

The stable endpoint and port names provide access to the internal, public, and effective values through
[service endpoint-port tokens](../apps/tokens.md#service).

Endpoint names must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names). Port names must follow the [port name rules](../naming.md#port-names).

Workload targeting and selectors are described in [service workloads](workloads.md).

## Links

A service link describes how one service connects to another service.

One common example is an Nginx link to its upstream backend such as PHP-FPM.

Some links are mandatory and some are optional. If a link is mandatory, the stack must specify which other service satisfies it.

For example, in a Drupal stack the PHP service may require a `Database` link. That link can point either to a container-based `MariaDB` service or to an external cloud database service.

Service links are defined under the [`links` section](template.md#links) in a service template.

Links also affect deployment ordering. When two linked app services are included in the same deployment, Wodby deploys
the linked target service first and then deploys the service that depends on it.

This ordering follows the current app-service links for that app environment, not only the original stack defaults. In
practice, changing a link at the app level can also change the deployment order for future deployments of that environment.

Required links remain configured when their source service is disabled. An enabled source cannot use a disabled target
for a required link; enabling the source also enables its configured required-link targets and their required
dependencies. Both services may be disabled together. Wodby never chooses a missing target automatically. The combined
dependency graph formed by service links and explicit stack dependencies must not contain cycles, including cycles
involving disabled services.

### Link targets

A link points at one of:

- **A service in the same app environment.** The usual case, set by the stack or on the app service.
- **A service of another app or app environment**, when the link allows it (`crossApp`) and the target service accepts
  links from other apps. See [Links to other apps](#links-to-other-apps).
- **A custom target**, when the link allows it (`custom`): you enter the values the link needs, such as the address and
  key of a hosted service. Secret values are stored as secrets.

A link has one target at a time. Setting a different kind replaces the previous target.

### Links to other apps

You can link to a service of another app when you are allowed to see that app environment's secrets, and the other
app belongs to the same organization: to the same project, to the organization, or shared to your project.

- **On the same cluster**, the service connects over the cluster's private network. Wodby opens the other app
  environment to the linked environments only, on the ports the target shares. On clusters where Wodby cannot enforce
  network isolation, such as k3s without Cilium, the link works but traffic between environments is not isolated.
- **On another cluster**, the service connects to the target's public domain, so the target's port needs one.

The linked service reads only what the target [exports](template.md#exports), such as its address and token. Links to
other apps don't change deployment order and never deploy the other app. When the target is deleted, moves to another
cluster, or changes its token or domains, the linked app services are marked as needing a deployment.

### Link groups

A service can require at least one of several links, for example a collector that must send data somewhere but may
use any of several destination links. While such a service is enabled, the required number of links in the group must
be set. See [`linkGroups`](template.md#linkgroups).

