# Service template

Custom services imported from Git are defined by `service.yml`.

If a repository contains multiple services, list their directories in `index.yml`:

```yaml
services:
  - php
  - nginx
```

Each listed directory must contain its own `service.yml`. Paths used by fields such as `configs[].config`, `build.dockerfile`, `build.dockerignore`, and `build.templates[].pipeline` are resolved relative to that service directory.

Only the fields documented on this page are supported. Unknown fields will be rejected during import.

## Example

```yaml
name: drupal11-php
type: service
from: php
title: PHP (Drupal 11)
labels:
  - drupal
  - drupal11

options:
  - version: "8.3"
    default: true
    eol: "2026-11-23T00:00:00+00:00"

update: auto

links:
  - name: files
    title: Files storage
    required: true
    selectors:
      - type: storage
  - name: redis
    title: Redis
    env:
      - name: REDIS_PORT
        value: "{{link.port}}"
      - name: REDIS_HOST
        value: "{{link.host}}"
      - name: REDIS_PASSWORD
        value: "{{link.tokens.password}}"
        secret: true
    selectors:
      - type: datastore
        labels:
          - redis
      - type: datastore
        labels:
          - valkey

volumes:
  - name: files
    title: Files
    shared: true
    size: 10
    link: files
    path: /mnt/files
    import:
      owner: 82
      group: 82

cron:
  - name: drush
    title: Drupal cron
    command: drush -r ${HTTP_ROOT} -l ${WODBY_PRIMARY_URL} cron
    schedule: "0 0 * * *"

env:
  - name: DRUPAL_FILES_SYNC_SALT
    value: "{{sync_salt}}"
    secret: true
  - name: DRUPAL_HASH_SALT
    value: "{{hash_salt}}"
    secret: true
  - name: DRUPAL_VERSION
    value: "11"

workloads:
  - name: main
    selector:
      matchLabels:
        app.kubernetes.io/instance: "{{helm.release}}"
    kind: deployment
    primary: true
    containers:
      - name: php
        image: wodby/drupal-php
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
    helm:
      labels: commonLabels
      annotations: commonAnnotations
      volumes: extraVolumes
      sidecars: extraSidecars

build:
  dockerfile: Dockerfile
  connect: true
  templates:
    - name: vanilla
      title: Vanilla Drupal
      repo: https://github.com/wodby/drupal-vanilla
      branch: 11.x

helm:
  name: wodby
  source: oci://registry-1.docker.io/wodby/php
  chart: oci://registry-1.docker.io/wodby/php
  version: 0.1.0
  imagePullSecrets: image.pullSecrets

settings:
  - name: docroot
    title: Drupal root subdirectory
    description: Composer-based projects usually keep Drupal under the web directory
    placeholder: path/relative/to/git/root
    default: web
    var: DOCROOT_SUBDIR

tokens:
  - name: sync_salt
    generate:
      regex: "[0-9a-z]{32}"
  - name: hash_salt
    generate:
      regex: "[0-9a-z]{32}"

actions:
  - name: clear_cache
    args: ["drush", "cc", "all"]
    type: button
    title: Clear all cache
  - name: user_login
    args: ["make", "user-login"]
    type: output
    title: Generate one-time login link
    privileged: true
```

## General rules

- `service.yml` defines one service.
- `from` lets you inherit from an existing service and override only the parts you need.
- Non-external services normally define `workloads` and `helm`. If the service inherits them from `from`, you do not
  need to repeat them.
- If you override inherited workloads or containers, use workload names and container names that already exist in the
  base service.
- Only services of type `service` can use the `build` section.
- Only services of type `db` can use the `database` section.
- `external: true` is for services managed outside Wodby. External services cannot define `workloads`, `build`,
  `links`, `volumes`, `settings`, `env`, `configs`, `actions`, `certs`, `cron`, or `derivatives`.
- Infrastructure services cannot be external and do not use `options`, `tokens`, or `imports`.

## Shared values

### Environment variable object

Used by `env`, `workloads[].containers[].env`, `links[].env`, `integrations[].providers[].env`, `imports[].init.env`, and
`derivatives[].env`.

- `name`: required environment variable name.
- `value`: required string value.
- `secret`: optional boolean. When `true`, the value is stored as a secret.
- `envType`: optional environment type filter. Allowed values: `prod`, `dev`, `staging`, `test`, `feature`.

### Helm value object

Used by `links[].helm`, `volumes[].helm.values`, `helm.values`, and `derivatives[].helm.values`.

- `name`: required Helm value path.
- `value`: required value. Can be a scalar, array, or object.

### Resources object

Used by `workloads[].containers[].resources` and `derivatives[].resources`.

- `request.cpu`
- `request.memory`
- `limit.cpu`
- `limit.memory`

CPU values are in millicores and must be multiples of `100`. Memory values are in MiB and must be multiples of `16`.

### Selector object

Used by `links[].selectors` and `kubernetes.infrastructure[].selectors`.

- `type`: service type to match.
- `option`: optional service option version to match.
- `labels`: optional labels that the matching service must have.

## Reference

### `name`

Type: `string`. Required.

Service machine name. Use lowercase letters, numbers, and dashes.

### `type`

Type: `enum`. Required.

Allowed values:

- `service`
- `db`
- `infrastructure`
- `ssh`
- `datastore`
- `operator`
- `search`
- `vpn`
- `storage`

This value is also used in selectors.

### `icon`

Type: `string`.

Icon name shown in the Wodby dashboard.

### `from`

Type: `string`.

Inherit configuration from an existing service available to your organization.

When overriding inherited workloads or containers, use only workload names and container names declared by the base
service.

### `update`

Type: `enum`.

Controls how service updates are pulled from Git. Allowed values:

- `auto`
- `manual`

### `title`

Type: `string`. Required.

Human-readable service title.

### `external`

Type: `boolean`. Default: `false`.

Marks the service as externally managed.

### `scalable`

Type: `boolean`. Default: `false`.

Whether this service supports running multiple replicas. This can only be enabled for services of type `service`.

### `labels`

Type: `array[string]`.

Labels used by selectors and service discovery rules.

### `env`

Type: `array`.

Service-wide environment variables. Uses the environment variable object described above.

Environment variable values can use [built-in runtime tokens](../apps/tokens.md) and service-defined tokens.

### `options`

Type: `array`.

Service versions or deployment variants. Services that do not inherit from another service usually define at least one option, unless they are infrastructure services.

Each item supports:

- `version`: required option version.
- `tag`: optional image tag for that version.
- `default`: optional boolean.
- `eol`: optional end-of-life date in ISO datetime format.

Only one option can be default. If none is marked as default, the first option becomes the default automatically.

### `workloads`

Type: `array`.

Workload definitions for the service. Non-external services normally define workloads unless they inherit them from `from`.

Each workload declares:

- a stable workload `name`
- a rendered Kubernetes target selected by `selector.matchLabels`
- a `kind`
- one or more `containers`
- optional workload- and container-level Helm value mappings

If the service has multiple workloads, mark one as `primary`. The primary workload is the default target used by
runtime features when no explicit workload is selected.

Full field reference and examples: [Service workloads](workloads.md).

### `build`

Type: `object`.

Build configuration for services of type `service`.

Each object supports:

- `dockerfile`: Dockerfile path.
- `dockerignore`: `.dockerignore` path.
- `connect`: whether the service requires a connected git repository.
- `templates`: starter repositories users can clone as a starting point.

Set build targets with `workloads[].containers[].build: true`. Buildable services must mark at least one container.

Each `build.templates[]` item supports:

- `name`: required template name.
- `title`: required template title.
- `repo`: required GitHub repository URL in `https://github.com/...` format.
- `branch`: git branch to use.
- `tag`: git tag or tag pattern to use.
- `pipeline`: optional pipeline file path.

Specify either `branch` or `tag` for each build template.

### `endpoints`

Type: `array`.

Service endpoints exposed by the service.

Each `endpoints[]` item supports:

- `name`: required endpoint name.
- `workload`: optional workload name. If omitted, Wodby targets the primary workload.
- `main`: marks the main endpoint.
- `ports`: required list of ports.

Each `endpoints[].ports[]` item supports:

- `name`: required port name.
- `number`: required port number.
- `protocol`: required protocol. Allowed values: `http`, `tcp`, `udp`.
- `private`: optional boolean.
- `main`: marks the main port within that endpoint.

Only one endpoint can be main. If the service has a single endpoint, it becomes main automatically. If you define
multiple endpoints, mark one of them as main.

Only one port per endpoint can be main. If no port is marked as main, the first port becomes main automatically.

The endpoint backend service is resolved from the Helm chart based on the target workload and the endpoint ports. For
multi-workload services, set `workload` explicitly when the endpoint should target a non-primary workload.

### `links`

Type: `array`.

Service links define which other services can be connected to this service in a stack.

Each item supports:

- `name`: required link name.
- `title`: required link title.
- `required`: optional boolean.
- `selectors`: required selectors. A linked service must match at least one selector.
- `env`: optional environment variables added when the link is set.
- `helm`: optional Helm values added when the link is set.

Each `links[].selectors[]` item uses the selector object described above.

### `volumes`

Type: `array`.

Service volumes.

Each item supports:

- `name`: required volume name.
- `title`: required volume title.
- `shared`: optional boolean.
- `readOnly`: optional boolean.
- `link`: optional link name associated with this volume.
- `optional`: optional boolean.
- `path`: optional absolute mount path.
- `from`: optional link name to reuse a volume from a linked service.
- `size`: optional default size in GB. Minimum `1`.
- `import`: optional ownership settings for imported files.
- `helm`: optional Helm integration for the volume.

`volumes[].import` supports:

- `owner`: required numeric owner ID.
- `group`: required numeric group ID.

`volumes[].helm` supports:

- `labels`: optional Helm value path for labels.
- `values`: optional Helm values.

### `integrations`

Type: `array`.

Integrations that can be connected to the service.

Each item supports:

- `name`: required integration name.
- `title`: required integration title.
- `type`: required integration type.
- `required`: optional boolean.
- `multiple`: optional boolean.
- `labels`: optional labels used to filter compatible integrations.
- `providers`: optional provider-specific overrides.

Each `integrations[].providers[]` item supports:

- `name`: required provider name.
- `env`: optional provider-specific environment variables.

### `settings`

Type: `array`.

Service settings shown when creating or configuring an app.

Each item supports:

- `name`: required setting name.
- `title`: required setting title.
- `description`: optional description.
- `placeholder`: optional placeholder text.
- `default`: optional default value.
- `from`: optional link name to reuse the same setting from a linked service.
- `required`: optional boolean.
- `var`: required environment variable name created from this setting.

### `imports`

Type: `array`.

Service import definitions.

Each item supports:

- `name`: required import name.
- `title`: required import title.
- `volume`: required target volume name.
- `extensions`: required supported file extensions.
- `destination`: destination path for unpacking files.
- `init`: init-volume import settings.
- `args`: optional arguments.
- `command`: optional command override.

`imports[].destination` can use `{{import_pvc_uid}}`.

`imports[].init` supports:

- `mount`: required mount path.
- `env`: optional environment variables for the import.

### `tokens`

Type: `array`.

Service tokens. Each token must define either a fixed value or a generated value.

Each item supports:

- `name`: required token name.
- `value`: fixed token value.
- `generate.regex`: regex used to generate the value.
- `secret`: optional boolean for fixed-value tokens.
- `envType`: optional environment type filter.

Generated tokens are always treated as secrets. Exactly one of `value` or `generate.regex` must be set.

### `actions`

Type: `array`.

Service actions.

Each item supports:

- `name`: required action name.
- `title`: required action title.
- `args`: required argument list.
- `command`: optional command override.
- `type`: required action type.
- `template`: optional build template name filter.
- `privileged`: optional boolean.
- `depends`: optional list of actions that must run first.

Allowed `type` values:

- `button`
- `output`
- `post_upgrade`
- `post_deploy`
- `post_deploy_once`

### `backups`

Type: `array`.

Service backup definitions.

Each item supports:

- `name`: required backup name.
- `title`: required backup title.
- `upload`: required upload settings.
- `create`: optional action-based backup creation settings.

`backups[].create` supports:

- `args`: required argument list when `create` is used.

`backups[].upload` supports:

- `filepath`: file to upload for action-based backups.
- `extension`: uploaded file extension for action-based backups.
- `dir`: directory to archive for simple file backups.
- `gzip`: optional gzip compression for simple file backups.

### `helm`

Type: `object`.

Helm integration for the service. Non-external services normally define `helm` unless they inherit it from `from`.

The object supports:

- `name`: required chart source name.
- `source`: optional Helm repository or OCI source URL.
- `chart`: required chart name.
- `version`: required chart version.
- `imagePullSecrets`: optional Helm value path for image pull secrets. Defaults to `image.pullSecrets`.
- `crds`: optional CRD file list.
- `values`: optional extra Helm values. `helm.values[].value` can use [built-in runtime tokens](../apps/tokens.md)
  and service-defined tokens.

Workload- and container-specific Helm mappings are defined under `workloads[].helm` and
`workloads[].containers[].helm`.

When a service is imported, Wodby validates configured Helm value paths against the chart's merged values and schema
when they are available.

### `certs`

Type: `array`.

Self-signed certificates generated for the service.

Each item supports:

- `name`: required certificate name.
- `days`: required lifetime in days. Allowed range: `365` to `36500`.
- `dns`: optional subject names.
- `key`: required key configuration.
- `helm`: required Helm mapping for the generated certificate.

`certs[].key` supports:

- `type`: required key type. Allowed value: `rsa`.
- `length`: required key length. Allowed values: `2048`, `4096`.

`certs[].helm` supports:

- `cert`: Helm value path for the certificate.
- `key`: Helm value path for the private key.
- `ca`: Helm value path for the CA certificate.

### `configs`

Type: `array`.

Service config files.

Each item supports:

- `name`: required config name.
- `title`: optional config title.
- `config`: required default config content or a relative file path to load it from the repository.
- `helm`: optional Helm value path that receives the resolved config content. Use this when the chart manages the
  ConfigMap or Secret for the config itself.
- `filepath`: optional mount path in the container. Wodby creates a ConfigMap and mounts it at this path.
- `filename`: optional filename to create in a ConfigMap without mounting it. Use this when the chart expects an
  existing ConfigMap name and mounts it on its own.
- `processTokens`: optional boolean. When `true`, Wodby resolves template tokens inside the effective config content
  before passing it to Helm or creating the ConfigMap. This is useful for generated configs such as Alloy or
  Prometheus agent configs. See [app tokens](../apps/tokens.md) for the public built-in token list. Leave it disabled
  for literal templates that use their own `{{ ... }}` syntax.
- `version`: optional service version this config applies to.

For a new config, specify exactly one target with either `helm`, `filepath`, or `filename`. When overriding a config
inherited from `from`, you can reuse the existing target and only replace what you need.

Config delivery modes:

- `helm`: Wodby passes the resolved config content into a Helm value. Use this when the chart itself creates and mounts
  the ConfigMap or Secret.
- `filepath`: Wodby creates a ConfigMap and mounts the file into the container at the given path.
- `filename`: Wodby creates a ConfigMap entry but does not mount it. Use this when the chart expects the name of an
  existing ConfigMap and mounts it on its own.

### `cron`

Type: `array`.

Service cron schedules.

Each item supports:

- `name`: required schedule name.
- `title`: required schedule title.
- `command`: required command.
- `schedule`: required schedule string.

Use standard five-field crontab syntax such as `0 * * * *`. Cron schedules cannot run more often than once per hour.

### `annotations`

Type: `array`.

Service annotations.

Each item supports:

- `name`: required annotation name.
- `value`: required annotation value.
- `envType`: optional environment type filter.

### `database`

Type: `object`.

Database configuration for services of type `db`.

The object supports:

- `type`: required database type name.
- `kind`: required database family.
- `port`: database port. Required for non-external database services.
- `ssl`: optional boolean.
- `root`: optional admin credentials.
- `db`: required database definition.
- `user`: required user definition.
- `charsets`: charset list. Required for non-external database services.

Allowed `kind` values:

- `mysql`
- `mariadb`
- `postgres`
- `sqlserver`
- `oracle`

`database.root` supports:

- `username`
- `password`

`database.db` supports:

- `name`: required database name.
- `charset`: required default charset.
- `collation`: required default collation.
- `actions`: optional database management actions.

`database.user` supports:

- `name`: required user name.
- `password`: required user password.
- `actions`: optional user management actions.

`database.db.actions` supports:

- `create.args`
- `drop.args`

`database.user.actions` supports:

- `create.args`
- `drop.args`
- `grant.args`
- `revoke.args`

`database.charsets[]` supports:

- `name`: required charset name.
- `title`: required charset title.
- `collation`: required collation.
- `default`: optional boolean.

### `derivatives`

Type: `array`.

Derivative services created from the main service.

Each item supports:

- `name`: required derivative service name.
- `title`: required derivative title.
- `icon`: optional icon.
- `type`: required derivative service type.
- `args`: required container args.
- `default`: optional boolean.
- `required`: optional boolean.
- `env`: optional environment variables.
- `endpoints`: optional endpoint overrides.
- `resources`: optional resource overrides.
- `helm`: optional Helm values.

Derivative names must start with the parent service name followed by a dash. For example, derivatives of `php` should
use names like `php-sshd`.

Each `derivatives[].endpoints[]` item uses the same structure as `endpoints[]`.

`derivatives[].helm` supports:

- `values`: optional Helm values.

### `kubernetes`

Type: `object`.

Additional Kubernetes-specific metadata.

Supported today:

- `infrastructure`: infrastructure service selectors.

Each `kubernetes.infrastructure[]` item supports:

- `name`: required item name.
- `title`: optional title.
- `selectors`: required selectors that identify matching infrastructure services.
