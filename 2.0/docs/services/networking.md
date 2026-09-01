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
explicit app environment [App Access](../apps/access.md) setting rather than an automatic effect of the `private` flag.

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
