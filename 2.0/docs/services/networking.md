# Service networking

Service networking covers how a service exposes ports and how it connects to other services in the same app instance.

Use endpoints for network access exposed by the service. Use links for service-to-service dependencies and connection
rules.

## Endpoints

Services that expose network access can define endpoints. An endpoint groups together one or more ports that belong to
the same exposed workload. Wodby resolves the concrete Kubernetes Service from the Helm chart later. HTTP routes are
attached at the app level.

Supported port protocols are:

1. `http` for web traffic and routes with TLS certificates
2. `tcp` for generic TCP traffic
3. `udp` for UDP traffic

Ports can also be marked as `private` to keep them internal-only.

One port per endpoint can be marked as main. If no port is marked as main, the first port becomes main automatically.

If a service defines a single endpoint, that endpoint becomes main automatically. If it defines multiple endpoints,
mark one of them as main.

When the main service in a stack has a main HTTP endpoint, Wodby attaches the app's main technical route to the main
port of that endpoint.

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
```

`workload` is optional. If omitted, the endpoint targets the primary workload.

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

This ordering follows the current app-service links for that app instance, not only the original stack defaults. In
practice, changing a link at the app level can also change the deployment order for future deployments of that instance.
