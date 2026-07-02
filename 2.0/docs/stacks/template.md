# Stack Template

Custom stacks imported from Git are defined by `stack.yml`.

If a repository contains multiple stacks, list their directories in `index.yml`:

```yaml
stacks:
  - php
  - node
```

Each listed directory must contain its own `stack.yml`. Paths used by `services[].configs[].config` are resolved relative to that stack directory.

Only the fields documented on this page are supported. Unknown fields will be rejected during import.

## Example

```yaml
name: php
title: PHP
icon: php

env:
  - name: APP_TYPE
    value: php

tokens:
  - name: app_secret
    generate:
      regex: '[0-9a-z]{32}'

annotations:
  - name: prometheus.io/scrape
    value: "true"

helm:
  - name: imagePullSecrets
    value:
      - registry-creds

services:
  - name: php
    title: PHP
    service: php:8.3
    required: true
    options:
      - version: '8.3'
        default: true
    env:
      - name: PHP_FPM_PM_MAX_CHILDREN
        value: "8"
    tokens:
      - name: xdebug_ide_key
        value: phpstorm
    workloads:
      - name: main
        containers:
          - name: php
            env:
              - name: APP_ENV
                value: prod
            resources:
              request:
                cpu: 100
                memory: 128
              limit:
                cpu: 500
                memory: 512
    cron:
      - name: queue
        title: Queue runner
        command: php /var/www/html/artisan schedule:run
        schedule: "0 * * * *"
    configs:
      - name: php_ini
        config: configs/php.ini
    derivatives:
      - name: php-xhprof
        service: xhprof
        env:
          - name: XHGUI_HOST
            value: http://xhgui

  - name: nginx
    title: Nginx
    service: php-nginx
    serviceRevPinned: true
    required: true
    depends:
      - php
    workloads:
      - name: main
        containers:
          - name: nginx
            env:
              - name: NGINX_VHOST_PRESET
                value: php
    links:
      - name: backend
        service: php

  - name: mariadb
    title: MariaDB
    service: mariadb:11
    disabled: true
    volumes:
      - name: data
        size: 20
```

## Top-Level Fields

### `name`

Type: `string`. Required.

Stack machine name. Use a lowercase slug with letters, numbers, and dashes.

It must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names).

### `title`

Type: `string`. Required.

Human-readable stack title.

### `icon`

Type: `string`.

Icon name shown in the Wodby dashboard.

### `services`

Type: `array`. Required. Must contain at least one item.

List of [stack services](services.md). Each item references an existing [service](../services/index.md) and can apply stack-level overrides to it.

### `env`

Type: `array`.

Stack-wide environment variables. They are applied to app services created from this stack.

Stack environment variables are runtime-only. They are not passed to Docker image builds.

### `tokens`

Type: `array`.

Stack-wide tokens. Tokens can either store a fixed value or generate one from a regular expression. A stack-wide token
overrides a service-defined token with the same name and environment type.

### `annotations`

Type: `array`.

Stack-wide annotations applied to deployed app services where the service template maps annotations into Kubernetes resources. Use app endpoint route settings for HTTP routing behavior.

### `helm`

Type: `array`.

Stack-wide Helm values. Use this to override values required by the service Helm integration.

## Shared Value Objects

### `env[]`

Used by top-level `env`, `services[].env`, and `services[].workloads[].containers[].env`.

- `name`: required environment variable name.
- `value`: required string value. Use quoted strings in YAML.
- `secret`: optional boolean. When `true`, the value is stored as a secret.
- `envType`: optional environment type filter. Allowed values: `prod`, `dev`, `staging`, `test`, `feature`.

Stack env vars do not support build scope. Use a build-scoped service setting, service env var, or app-service env var
when a Dockerfile needs a build argument.

### `tokens[]`

Used by top-level `tokens` and `services[].tokens`.

- `name`: required token name.
- `value`: fixed token value.
- `generate.regex`: regex used to generate the token value.
- `secret`: optional boolean for fixed-value tokens.
- `envType`: optional environment type filter.

Exactly one of `value` or `generate.regex` must be specified. Regex tokens are always secret regardless of the `secret` setting.

Within one token scope, each `name` and `envType` pair must be unique. You can define the same token name more than once
only when each definition has a different `envType`.

### `annotations[]`

Used by top-level `annotations`.

- `name`: required annotation name.
- `value`: required annotation value.
- `envType`: optional environment type filter.

Annotations are Kubernetes resource annotations. They are separate from [app endpoint route settings](../apps/endpoints.md#route-settings).

### `helm[]`

Used by top-level `helm`, `services[].helm`, and `services[].derivatives[].helm`.

- `name`: required Helm values path.
- `value`: required value. Can be a scalar, array, or object.
- `secret`: optional boolean. When `true`, the value is stored as a secret.
- `envType`: optional environment type filter.

## Service Fields

### `services[].name`

Type: `string`. Required.

Stack service machine name. It must be unique within the stack, including derivative stack services.

It must follow the [Kubernetes service name rules](../naming.md#kubernetes-service-names): lowercase letters, numbers, and dashes only; start with a letter; end with a letter or number; 63 characters or shorter.

### `services[].title`

Type: `string`. Required.

Human-readable service title shown in the stack and app UI.

### `services[].service`

Type: `string`. Required.

Reference to an existing service. You can use either a plain service name such as `php` or a versioned reference such as `php:8.3`.

The referenced service must exist and be available to your organization.

Versioned references pin the stack service to the service revision that matches the requested service version. Stack
service revision updates skip pinned services. Use an unversioned reference when the stack service should move to newer
service revisions through manual or automatic stack service revision updates.

### `services[].serviceRevPinned`

Type: `boolean`. Default: `false`.

Pins the stack service to the service revision selected during import. This is useful when the `service` reference is
unversioned but the stack should still keep the current service revision until you update the stack template or unpin
the service in the dashboard.

Derivative stack services inherit the pin state from their parent stack service.

### `services[].required`

Type: `boolean`. Default: `false`.

Marks the service as mandatory when a new app is created from the stack.

### `services[].disabled`

Type: `boolean`. Default: `false`.

Disables the stack service by default.

### `services[].replicas`

Type: `integer`. Default: `1`.

Default number of replicas for the stack service.

### `services[].main`

Type: `boolean`.

Marks the main service in the stack. Only one stack service can be main, and it must reference a service with HTTP
ports. Use it for the primary HTTP service.

If no service is marked as main, Wodby will automatically pick the first HTTP-capable service. The same fallback applies
when a stack without a main service later gains an HTTP-capable service through the dashboard or Git sync. If the stack
has no HTTP-capable services, no main service is required.

### `services[].depends`

Type: `array[string]`.

List of stack service names that this service depends on. Every referenced name must exist in the same stack.

This affects deployment order: a service is deployed after its dependencies and deleted before them.

Wodby also derives deploy-time ordering from the current service links in an app instance. Use `depends` when you need
explicit ordering even when no link exists between the services.

### `services[].options`

Type: `array`.

Limits which options from the referenced service can be used in this stack and sets the default option.

Each item supports:

- `version`: required option version from the referenced service.
- `default`: optional boolean.

If no option is marked as default, the first listed option becomes the default automatically.

### `services[].env`

Type: `array`.

Service-specific environment variables.

### `services[].helm`

Type: `array`.

Service-specific Helm values.

### `services[].workloads`

Type: `array`.

Per-workload overrides for workloads defined by the referenced service.

Each item supports:

- `name`: required workload name from the referenced service manifest. It must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names).
- `containers`: required list of container overrides for that workload.

Each `services[].workloads[].containers[]` item supports:

- `name`: required container name from the referenced service manifest. It must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names).
- `env`: optional container-specific environment variables.
- `resources`: optional resource overrides.

`resources` supports:

- `request.cpu`
- `request.memory`
- `limit.cpu`
- `limit.memory`

CPU values are in millicores and must be multiples of `100`. Memory values are in MiB and must be multiples of `16`.

Use the same workload names and container names declared by the referenced service. You only need to list the workloads
and containers you want to override. Stack import validates these targets against the referenced service manifest.

### `services[].volumes`

Type: `array`.

Overrides sizes for volumes defined by the referenced service.

Each item supports:

- `name`: required service volume name. It must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names).
- `size`: required size in GB, minimum `1`.

### `services[].links`

Type: `array`.

Links a stack service to another stack service to satisfy links defined by the referenced service.

Each item supports:

- `name`: required service-defined link name.
- `service`: required target stack service name.

Required service links must be satisfied in the stack definition.

When both linked services are part of the same app deployment, Wodby deploys the linked target service first. App-level
link overrides can change that order for a specific app instance.

### `services[].cron`

Type: `array`.

Additional cron schedules for the stack service.

Each item supports:

- `name`: required schedule name.
- `title`: required human-readable title.
- `command`: required command to run.
- `schedule`: required cron schedule.

Use standard five-field crontab syntax such as `0 * * * *`. Cron schedules cannot run more often than once per hour.

### `services[].configs`

Type: `array`.

Provides stack-specific file contents for configs defined by the referenced service.

Each item supports:

- `name`: required config name from the referenced service. It must follow the [general Kubernetes name rules](../naming.md#general-kubernetes-names).
- `config`: required file path relative to the stack directory.
- `disabled`: optional boolean.

The stack override only replaces the config content or disables the config. The delivery target (`helm`, `filepath`, or
`filename`) is still defined by the referenced service template.

### `services[].tokens`

Type: `array`.

Service-specific tokens. The object shape is the same as top-level `tokens`. A service-specific token overrides both
service-defined and stack-wide tokens with the same name and environment type.

### `services[].derivatives`

Type: `array`.

Overrides derivative services declared by the referenced service.

Each item supports:

- `name`: required stack service name for the derivative instance.
- `service`: required derivative name from the referenced service.
- `required`: optional boolean.
- `env`: optional environment variables.
- `helm`: optional Helm values.

Only derivatives declared by the referenced service can be used here. Derivative stack service names follow the same
[Kubernetes service name rules](../naming.md#kubernetes-service-names) as `services[].name`.

If the referenced service inherits derivatives from another service, use the rewritten derivative name in `service`. For
example, if `drupal11-php` inherits `php-sshd` from `php`, the stack derivative should reference
`service: drupal11-php-sshd`. The `name` can still be a stack-local alias such as `sshd`.
