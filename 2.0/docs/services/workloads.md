# Service workloads

## Overview

Workloads describe the Kubernetes resources that Wodby manages for a service.

Use workloads to define:

- which Kubernetes controller Wodby should target
- which containers exist inside that controller
- which workload is considered primary
- where Wodby should inject workload- and container-level Helm values

For non-external services, workloads are normally required unless they are inherited from `from`.

External services do not define workloads.

## Why workloads exist

A service is no longer treated as a single Deployment with a single container.

Charts can expose multiple resources, for example:

- a web workload and a daemon workload
- a Deployment plus a StatefulSet
- one workload with more than one container

Wodby uses workload definitions to resolve the correct target for:

- logs and shell
- endpoints
- cron jobs
- backups
- imports
- actions
- database actions
- container-scoped env vars and resources

## Template

Workloads are defined under the [`workloads` section](template.md#workloads) in a service template.

### Single-workload example

```yaml
workloads:
- name: main
  selector:
    matchLabels:
      app.kubernetes.io/instance: "{{helm.release}}"
  kind: deployment
  primary: true
  helm:
    labels: commonLabels
    annotations: commonAnnotations
    volumes: extraVolumes
    sidecars: extraSidecars
  containers:
  - name: php
    image: wodby/php
    build: true
    helm:
      resources: resources
      env: extraEnvVars
      mounts: extraVolumeMounts
      image:
        repository: image.repository
        tag: image.tag
        registry: image.registry
        pullPolicy: image.pullPolicy
```

### Multi-workload example

```yaml
workloads:
- name: webserver
  selector:
    matchLabels:
      app.kubernetes.io/instance: "{{helm.release}}"
      component: dagster-webserver
  kind: deployment
  primary: true
  containers:
  - name: dagster
    image: dagster/dagster-celery-k8s

- name: daemon
  selector:
    matchLabels:
      app.kubernetes.io/instance: "{{helm.release}}"
      component: dagster-daemon
  kind: deployment
  containers:
  - name: dagster
    image: dagster/dagster-celery-k8s
```

## Workload fields

Each `workloads[]` item supports:

- `name`: required stable workload name used by stack, app, and GraphQL overrides.
- `selector`: required Kubernetes selector used by Wodby to find the rendered workload resource.
- `kind`: required workload kind. Allowed values: `deployment`, `statefulset`, `daemonset`.
- `primary`: optional boolean. Marks the default workload for runtime operations.
- `helm`: optional workload-level Helm mappings.
- `containers`: required list of containers for this workload.

### Workload names

`workloads[].name` is a Wodby identifier, not a Kubernetes resource name.

Use it consistently in:

- `endpoints[].workload`
- `cron[].workload`
- `backups[].workload`
- `imports[].workload`
- `actions[].workload`
- `database.actions[].workload`
- stack overrides
- app-level mutations that target a specific workload/container

Keep workload names stable once a service is published. Renaming or removing workloads can break existing stack and app data.

### Selectors

`selector.matchLabels` must point to exactly one rendered workload of the declared `kind`.

Example:

```yaml
selector:
  matchLabels:
    app.kubernetes.io/instance: "{{helm.release}}"
    app.kubernetes.io/name: php
```

Selectors are preferred over resource names because they survive chart naming differences and helper logic.

For Wodby charts, use stable workload labels whenever possible. For third-party charts, use the labels that uniquely
identify each workload in the rendered chart.

## Primary workload

One workload should be treated as primary.

If a service has only one workload, Wodby uses it as primary automatically.

If a service has multiple workloads, mark one with `primary: true`.

When no explicit workload is selected, Wodby falls back to the primary workload for:

- shell
- logs
- endpoints
- cron jobs
- backups
- imports
- actions
- database actions

## Containers

Every workload must define at least one container.

Each `workloads[].containers[]` item supports:

- `name`: required pod container name
- `image`: optional runtime image reference
- `build`: optional boolean for build target containers
- `hostname`: optional container hostname
- `env`: optional container-scoped env vars
- `resources`: optional container-scoped resources
- `helm`: optional container-level Helm mappings

Container names must match the real container names created by the chart.

### Build targets

Buildable services mark target containers with `build: true`.

- At least one container must be marked when the service defines `build`.
- Containers must not use `build: true` when the service has no `build` section.
- Multiple containers can be marked only when they are intended to receive the same built image.

See also: [Service build](build.md).

## Helm mappings

### Workload-level Helm mappings

`workloads[].helm` supports:

- `labels`
- `annotations`
- `volumes`
- `sidecars`

These are Helm value paths used when Wodby injects workload-scoped data.

### Container-level Helm mappings

`workloads[].containers[].helm` supports:

- `resources`
- `env`
- `envKV`
- `mounts`
- `image`

These are Helm value paths used when Wodby injects container-scoped data.

### Container image Helm mappings

`workloads[].containers[].helm.image` supports:

- `repository`
- `tag`
- `registry`
- `pullPolicy`

Defaults:

- `repository`: `image.repository`
- `tag`: `image.tag`
- `registry`: `image.registry`
- `pullPolicy`: `image.pullPolicy`

By default, Wodby splits an image like `registry.example.com/team/app:1.2.3` into:

- `registry`: `registry.example.com`
- `repository`: `team/app`
- `tag`: `1.2.3`

Set `registry: ""` when the chart expects the full image path to stay in `repository` instead of splitting registry and repository into separate values.

Example:

```yaml
image:
  repository: dagsterWebserver.image.repository
  tag: dagsterWebserver.image.tag
  registry: ""
```

With this configuration, Wodby writes the full repository path such as `registry.example.com/team/app` into
`dagsterWebserver.image.repository` and does not inject a separate registry value.

See also: [Helm](helm.md).

## Validation rules

Service import validates workloads strictly.

- Workload names must be unique.
- One workload can be primary.
- Every workload must contain at least one container.
- Container names must be unique within a workload.
- Selectors must be structurally valid.
- When the chart can be rendered during validation, each selector must resolve to exactly one rendered workload of the declared kind.
- Workload references used by endpoints, cron jobs, backups, imports, actions, and database actions must point to existing workloads.
- In inherited services, overridden workloads and containers must already exist in the base service.
