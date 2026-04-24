# Service endpoints

## Overview

Services that expose network access can define endpoints. An endpoint groups together one or more ports that belong to
the same exposed workload. Wodby resolves the concrete Kubernetes Service from the Helm chart later. Domains are
attached at the app level.

Supported port protocols are:

1. `http` for web traffic and domains with TLS certificates
2. `tcp` for generic TCP traffic
3. `udp` for UDP traffic

Ports can also be marked as `private` to keep them internal-only.

One port per endpoint can be marked as main. If no port is marked as main, the first port becomes main automatically.

If a service defines a single endpoint, that endpoint becomes main automatically. If it defines multiple endpoints,
mark one of them as main.

When the main service in a stack has a main HTTP endpoint, Wodby attaches the app's main technical domain to the main
port of that endpoint.

## Template

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

Workload targeting and selectors are described in [service workloads](workloads.md).
