# Service template

Services can be created only via templates. You can connect your git integration and import a custom service from a
template.

## Example

```yml
name: drupal11-php
type: service
from: php
title: PHP (Drupal 11)
labels:
  - drupal
  - drupal11

options:
  - version: '8.3'
    default: true
    eol: '2026-11-23T00:00:00+00:00'

update: auto

containers:
  - name: php
    image: wodby/drupal-php

links:
  - name: files
    title: Files storage
    required: true
    selectors:
      - type: storage
  - name: solr
    title: Solr
    env:
      - name: SOLR_CLOUD_SERVER
        value: '{{link.host}}'
      - name: SOLR_CLOUD_PASSWORD
        value: '{{link.tokens.password}}'
        secret: true
    selectors:
      - type: search
        labels:
          - solr
  - name: redis
    title: Redis
    env:
      - name: REDIS_PORT
        value: '{{link.port}}'
      - name: REDIS_HOST
        value: '{{link.host}}'
      - name: REDIS_PASSWORD
        value: '{{link.tokens.password}}'
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
    title: drush cron
    command: drush -r ${HTTP_ROOT} -l ${WODBY_PRIMARY_URL} cron
    schedule: 0 0 * * *

env:
  - name: DRUPAL_FILES_SYNC_SALT
    value: '{{sync_salt}}'
    secret: true
  - name: DRUPAL_HASH_SALT
    value: '{{hash_salt}}'
    secret: true
  - name: DRUPAL_VERSION
    value: '11'
  - name: HTTP_ROOT
    value: "${APP_ROOT}/${DOCROOT_SUBDIR}"

build:
  dockerfile: Dockerfile
  connect: true
  templates:
    - name: vanilla
      title: Vanilla Drupal
      repo: https://github.com/wodby/drupal-vanilla
      branch: 11.x

settings:
  - name: docroot
    title: Drupal root subdirectory
    description: Composer-based projects have Drupal under 'web' directory by default
    placeholder: path/relative/to/git/root
    default: web
    var: DOCROOT_SUBDIR
  - name: sitedir
    title: Drupal site dir
    required: true
    default: default
    var: DRUPAL_SITE

tokens:
  - name: sync_salt
    generate:
      regex: '[0-9a-z]{32}'
  - name: hash_salt
    generate:
      regex: '[0-9a-z]{32}'

actions:
  - name: clear_cache
    args: [ 'drush', 'cc', 'all' ]
    type: button
    title: Clear all cache
  - name: user_login
    args: [ 'make', 'user-login' ]
    type: output
    title: Generate one-time login link
    privileged: true
```

## Reference

### `name`

Type: `string`.

Machine name of a service, must be unique, cannot be changed. Only alphanumeric and dash symbols allowed.

Required.

### `type`

Type: `enum`. Required.

[Service type](types.md).

Following values allowed:

- `service`
- `db`
- `infrastructure`
- `storage`
- `datastore`
- `search`
- `ssh`
- `smtp`

Can be used in selectors.

### `icon`

Type: `string`.

Icon name in Wodby dashboard.

### `from`

Type: `string`.

Inherit specified service. Must specify existing service from Wodby catalog.

### `title`

Type: `string`.

Human-readable title of a service.

Required.

### `hostname`

Type: `string`.

Hostname that will be used as the name of a kubernetes service. Mandatory for non-external services.

### `scalable`

Type: `boolean`. Default: `false`

Whether this service support scalability. Should be always `true` for stateless services. For stateful services depends
on the implementation.

### `labels`

Type: `string list`.

List of text labels for a service, to be used in selectors.

### `options`

Option represent version and variants of service. Mandatory to specify at least on option.

#### `options.[].version`

Type: `string`. Required.

Human-readable version

#### `options.[].tag`

Type: `string`.

Image docker for the selected version. If not set, `version` will be used instead.

#### `options.[].default`

Type: `boolean`.

Whether selected version should be selected by default. If none specified, first option will be chosen as default.

#### `options.[].eol`

Type: `string`.

Optional date of end of life (EOL) of the version. Specify in format `YYYY-MM-DDT00:00:00+00:00`

### `containers`

Definition of containers of a service. Not allowed for external services. Mandatory for non-external services.

#### `containers.[].name`

Type: `string`. Required.

Machine name of the container.

#### `containers.[].image`

Type: `string`. Required.

Docker image of the container.

### `build`

Configuration for [buildable services](build.md).

#### `build.dockerfile`

Type: `string`.

Dockerfile file name from service repository.

#### `build.connect`

Type: `boolean`.

Whether this service requires a git repository to be connected.
Otherwise, assumed the service will be built as a part of a build of different service.

#### `build.templates`

List of build templates (boilerplate) user can choose from for Demo purposes or clone to own repository.

##### `build.templates.[].name`

Type: `string`. Required.

Machine name of template. Must be unique, cannot be changed.

##### `build.templates.[].title`

Type: `string`. Required.

Human-readable title.

##### `build.templates.[].repo`

Type: `string`. Required.

Address to a git repository from GitHub (must be specified in `https://` format)

##### `build.templates.[].branch`

Type: `string`.

Branch name of a git repository, if not specified default branch will be used.

### `endpoints`

Collection of [service endpoints](endpoints.md).

#### `endpoints.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Endpoint's machine name.

#### `endpoints.[].ports`

Collection of a service endpoint's ports.

##### `endpoints.[].ports.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Endpoint's port machine name.

##### `endpoints.[].ports.[].number`

Type: `integer`. Required.

Endpoint's port number.

##### `endpoints.[].ports.[].type`

Type: `enum`. Allowed values are `tcp`, `udp` and `http`

Endpoint port's type.

##### `endpoints.[].ports.[].main`

Type: `boolean`.

Set to true to mark the port as main. Only one per endpoint. If none marked the first one set as main.

### `links`

Collection of [service links](links.md).

#### `links.[].name`

Type: `string`. Required.

Machine name of a link. Must be unique, cannot be changed.

#### `links.[].title`

Type: `string`.

Human-readable title of a link.

#### `links.[].required`

Type: `boolean`.

When set to true, the link is required to set in a stack.

#### `links.[].selectors`

Collection of selectors that a linked service must match. Must match at least one of the selectors.

##### `links.[].selectors.[].type`

Type: `enum`.

[Type](types.md) of service that can be linked.

Following values allowed:

- `service`
- `db`
- `storage`
- `datastore`
- `search`
- `ssh`

##### `links.[].selectors.[].labels`

Type: `string list`.

List of labels that a linked service must have.

#### `links.[].env`

Collection of environment variables that will be added when the link set.

##### `links.[].env.[].name`

Type: `string`. Required.

Name of the environment variable.

##### `links.[].env.[].value`

Type: `string`.

Value of the environment variable. Can contain [`{{tokens}}`](tokens.md).

##### `links.[].env.[].env`

Type: `enum`.

If set, the environment variable will be added only to application instances that have the provided [environment type](../apps/env.md#type).

##### `links.[].env.[].secret`

Type: `boolean`.

True if the environment variable should be secret. Secret environment variable's value stored in Kubernetes secret resource and not shown in Wodby dashboard.

### `volumes`

Collection of [service volumes](volumes.md)

#### `volumes.[].name`

Type: `string`. Required.

Volume's machine name. Must be unique, cannot be changed.

#### `volumes.[].title`

Type: `string`.

Volume's human-readable title.

#### `volumes.[].size`

Type: `int`.

Default size of the volume, in GB.

#### `volumes.[].optional`

Type: `boolean`.

True if volume is optional. When a volume optional and size not specified during new app creation, the persistent volume
won't be created.

#### `volumes.[].helm`

Additional Helm configuration for the volume.

##### `volumes.[].helm.values`

Collection of helm values.

###### `volumes.[].helm.values.[].name`

Type: `string`

Name of the helm value.

###### `volumes.[].helm.values.[].value`

Type: `string`, `string list`, `object`

Value of the helm value. Can contain [`{{tokens}}`](tokens.md).

### `integrations`

Collection of [service integrations](integrations.md)

#### `integrations.[].name`

Type: `string`. Required.

Integration's machine name. Must be unique, cannot be changed.

#### `integrations.[].title`

Type: `string`.

Integration's human-readable title.

#### `integrations.[].type`

Type: `enum`.

[Type of integration](../integrations/types.md) that can be connected.

#### `integrations.[].required`

Type: `boolean`.

Set to true when it's mandatory to connect at least one integration.

#### `integrations.[].multiple`

Type: `boolean`.

Set to true when multiple integrations can be connected.

#### `integrations.[].providers`

Collection of extra configurations for specific providers.

##### `integrations.[].providers.[].name`

Machine name of the [provider](../integrations/providers.md) for which this configuration should apply.

##### `integrations.[].providers.[].env`

Collection of extra environment variables that will be added when integration of the specific provider added.

###### `integrations.[].providers.[].env.[].name`

Type: `string`. Required.

Name of the environment variable.

###### `integrations.[].providers.[].env.[].value`

Type: `string`.

Value of the environment variable. Can contain [`{{tokens}}`](tokens.md).

###### `integrations.[].providers.[].env.[].env`

Type: `enum`.

If set, the environment variable will be added only to application instances that have the provided [environment type](../apps/env.md#type).

###### `integrations.[].providers.[].env.[].secret`

Type: `boolean`.

True if the environment variable should be secret. Secret environment variable's value stored in Kubernetes secret resource and not shown in Wodby dashboard.

### `settings`

Collection of [service settings](settings.md)

#### `settings.[].name`

Type: `string`. Required.

Setting's machine name. Must be unique, cannot be changed.

#### `settings.[].title`

Type: `string`.

Setting's human-readable title.

#### `settings.[].var`

Type: `string`. Required.

Name of the setting's environment variable that will be added with the value of the setting.

#### `settings.[].description`

Type: `string`.

Setting's description. Will be shown in Wodby's dashboard.

#### `settings.[].placeholder`

Type: `string`.

Setting's placeholder for the setting's input. Will be shown in Wodby's dashboard.

#### `settings.[].default`

Type: `string`.

Setting's default value.

### `backups`

Collection of [service backups](backups.md).

Example #1 [simple files backup](backups.md#1-simple-files-backup):

```yml
backups:
  - name: files
title: Files backup
upload:
  dir: /export
  gzip: false
```

Example #2 backup [through action](backups.md#2-through-action):

```yml
backups:
  - name: database
    title: Default database backup
    create:
      args:
        - make
        - backup
        - 'host="{{database.host}}"'
        - 'db="{{database.db.name}}"'
        - 'ignore="{{db_backup_ignore_tables}}"'
        - 'filepath=/var/lib/mysql/backup.sql.gz'
    upload:
      filepath: /var/lib/mysql/backup.sql.gz
      extension: sql.gz
```

#### `backups.[].name`

Type: `string`. Required.

Backup's machine name. Must be unique, cannot be changed.

#### `backups.[].title`

Type: `string`.

Backup's human-readable title.

#### `backups.[].create`

Container's configuration for the backup creation action. App service's pod container will be used to run a Kubernetes
job with the provided configuration to create a backup. The job should result in an archive file.

Mandatory unless it's a [simple files backup](backups.md#1-simple-files-backup).

##### `backups.[].create.args`

Type: `string list`.

List of container's args to override for the action. Can contain [`{{tokens}}`](tokens.md).

##### `backups.[].create.command`

Type: `string list`.

Container's command to override for the action.

#### `backups.[].upload`

Configuration for how to upload the backup archive to the cloud storage of the attached integration.

##### `backups.[].upload.filepath`

Type: `string`. Mandatory unless it's a [simple files backup](backups.md#1-simple-files-backup).

Filepath of the backup archive.

##### `backups.[].upload.extension`

Type: `string`. Mandatory unless it's a [simple files backup](backups.md#1-simple-files-backup).

Extension of the archive file for the cloud storage.

##### `backups.[].upload.dir`

Type: `string`. Mandatory for [simple files backups](backups.md#1-simple-files-backup).

Directory with files that should be backed up.

##### `backups.[].upload.gzip`

Type: `boolean`. Only for [simple files backups](backups.md#1-simple-files-backup).

If set to true, the files tarball will be additionally gzipped.

### `imports`

Collection of [service imports](imports.md).

Example #1 [simple files import](imports.md#1-simple-files-import):

```yml
imports:
  - name: files
    volume: data
    title: Files import
    destination: '/export/pvc-{{import_pvc_uid}}'
    extensions:
      - tar
      - tar.gz
      - tgz
      - zip
```

Example #2 import [through init volume](imports.md#2-through-init-volume):

```yml
imports:
  - name: database
    title: Database import
    volume: data
    init:
      mount: /docker-entrypoint-initdb.d
      env:
        - name: MYSQL_DATABASE
          value: '{{database.db.name}}'
    extensions:
      - gz
      - tar.gz
      - tgz
      - zip
```

#### `imports.[].name`

Type: `string`. Required.

Import's machine name. Must be unique, cannot be changed.

#### `imports.[].title`

Type: `string`.

Import's human-readable title.

#### `imports.[].volume`

Type: `string`.

Machine name of the [volume](volumes.md) where import should be imported to.

###### `imports.[].extensions`

Type: `string list`.

List of support import archive extensions.

#### `imports.[].destination`

Type: `string`. Can contain [`{{tokens}}`](tokens.md). Supports extra token `{{import_pvc_uid}}` that has UID of the
volume PVC.

Destination path in a container where to unpack a tarball with files. Only
for [simple files import](imports.md#1-simple-files-import)

#### `imports.[].init`

Configuration for [import through init volume](imports.md#2-through-init-volume).

##### `imports.[].init.mount`

Type: `string`. Required.

Mount path in a container of the init volume that implements import.

##### `imports.[].init.env`

Collection of additional environment variables to be added during import.

###### `imports.[].init.env.[].name`

Type: `string`. Required.

Name of the environment variable.

###### `imports.[].init.env.[].value`

Type: `string`.

Value of the environment variable. Can contain [`{{tokens}}`](tokens.md).

###### `imports.[].init.env.[].env`

Type: `enum`.

If set, the environment variable will be added only to application instances that have the provided [environment type](../apps/env.md#type).

###### `imports.[].init.env.[].secret`

Type: `boolean`.

True if the environment variable should be secret. Secret environment variable's value stored in Kubernetes secret resource and not shown in Wodby dashboard.

### `tokens`

Collection of [service tokens](tokens.md). A token must specify either a plain text value or a regular expression to
generate a random value.

#### `tokens.[].name`

Type: `string`. Required.

Token's name. Must be unique, cannot be changed.

#### `tokens.[].value`

Type: `string`.

Token's plain text value.

#### `tokens.[].generate`

Configuration for how to randomly generate token's value.

##### `tokens.[].generate.regex`

Type: `string`.

Regular expression to use for generating a random token's value.

##### `tokens.[].secret`

Type: `boolean`.

True if the token should be secret. Secret token's value stored in Kubernetes secret resource and not shown in Wodby dashboard.

##### `tokens.[].env`

Type: `enum`.

If set, the token will be added only to application instances that have the provided [environment type](../apps/env.md#type).

### `actions`

Collection of [service actions](actions.md)

#### `actions.[].name`

Type: `string`. Required.

Action's name. Must be unique, cannot be changed.

#### `actions.[].title`

Type: `string`.

Action's human-readable title.

#### `actions.[].args`

Type: `string list`.

List of container args to override of the main container for the kubernetes job when action executed.

#### `actions.[].command`

Type: `string list`.

Container's command to override of the main container for the kubernetes job when action executed.

#### `actions.[].type`

Type: `enum`. Allowed values: `button`, `post_upgrade`, `post_deploy`, `post_deploy_once`

[Action's type](actions.md#types). Defines how and when action will be executed.

#### `actions.[].template`

Type: `string`.

Used only for `post_deploy` and `post_deploy_once`. Limits action to be run only if specified build source template
selected.

#### `actions.[].privileged`

Type: `boolean`.

When set true, privileged permissions will be set for the action's kubernetes job.

#### `actions.[].depends`

Type: `string list`.

A list of existing actions that this action depends on. The action will run only after all specified actions
successfully executed.

### `helm`

Configuration for [service Helm integration](helm.md). Mandatory for non-external services.

Example:

```yml
helm:
  name: wodby
  source: oci://registry-1.docker.io/wodby/nfs-provisioner
  chart: oci://registry-1.docker.io/wodby/nfs-provisioner
  version: 0.1.2
  configurations:
    - name: nfs
      annotations: podAnnotations
      labels: podLabels
      env: envVars
      resources: resources
```

#### `helm.name`

Type: `string`. Required.

Helm repository's name.

#### `helm.source`

Type: `string`. Required.

Helm repository's source. Supports `oci://` and `https://` sources.

#### `helm.chart`

Type: `string`. Required.

Helm chart's name.

#### `helm.version`

Type: `string`. Required.

Helm chart's version.

#### `helm.configurations`

Collection of Helm configurations. Required.

##### `helm.configurations.[].name`

Type: `string`. Required.

Helm configuration's name. Must be the same as main container's name.

##### `helm.configurations.[].annotations`

Type: `string`.

Helm value's key for adding extra annotations.

##### `helm.configurations.[].resources`

Type: `string`.

Helm value's key for setting kubernetes resources.

##### `helm.configurations.[].env`

Type: `string`.

Helm value's key for adding environment variables.

##### `helm.configurations.[].labels`

Type: `string`.

Helm value's key for adding labels.

##### `helm.configurations.[].volumes`

Type: `string`.

Helm value's key for adding volumes.

##### `helm.configurations.[].mounts`

Type: `string`.

Helm value's key for adding volume mounts.

##### `helm.configurations.[].sidecars`

Type: `string`.

Helm value's key for adding sidecar containers.

#### `helm.values`

Extra helm values to add.

###### `helm.values.[].name`

Type: `string`

Name of the helm value.

###### `helm.values.[].value`

Type: `string`, `string list`, `object`

Value of the helm value. Can contain [`{{tokens}}`](tokens.md).

### `certs`

Collection of service's [self-signed certificates](certs.md) to generate.

Example:

```yml
certs:
  - name: webhook
    days: 36500
    key:
      type: rsa
      length: 4096
    dns:
      - aws-load-balancer-webhook-service.{{service.name}}.svc
      - aws-load-balancer-webhook-service.{{service.name}}.svc.cluster.local
    helm:
      cert: webhookTLS.cert
      key: webhookTLS.key
      ca: webhookTLS.caCert
```

#### `certs.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Certificate's name.

#### `certs.[].days`

Type: `int`. Required.

Certificate's days to expiration.

#### `certs.[].key`

Certificate key configuration. Required.

##### `certs.[].key.type`

Type: `enum`. Required. Allowed values: `rsa`

Certificate key's type.

##### `certs.[].key.length`

Type: `int`. Required.

Certificate key's length.

#### `certs.[].dns`

Type: `string list`.

Domains names of certificate subject. Can contain [`{{tokens}}`](tokens.md).

#### `certs.[].helm`

Helm integration configuration to add generated certificates to the Helm chart.

##### `certs.[].helm.cert`

Helm value's key to add a base64 encoded certificate in PEM format.

##### `certs.[].helm.key`

Helm value's key to add a base64 encoded private key in PEM format.

##### `certs.[].helm.ca`

Helm value's key to add a base64 encoded CA certificate in PEM format.

### `configs`

Collection of [service configs](configs.md).

Example:

```yml
configs:
  - name: main
    title: Main
    filepath: /etc/gotpl/config/nginx.conf.tmpl
    config: nginx.conf.tmpl
  - name: vhost
    title: Virtual host
    filepath: /etc/gotpl/vhost.conf.tmpl
    config: vhost.conf.tmpl
```

#### `configs.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Config's machine name.

#### `configs.[].title`

Type: `string`.

Config's human-readable title.

#### `configs.[].filepath`

Type: `string`.

Filepath where to mount the config file in a container.

#### `configs.[].config`

Type: `string`.

Filepath to the default config file in a service's repository.

### `cron`

Collection of [cron schedules](cron.md).

#### `cron.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Cron schedule's machine name.

#### `cron.[].title`

Type: `string`.

Cron schedule's human-readable title.

#### `cron.[].command`

Type: `string`.

Cron schedule's command for kubernetes job.

#### `cron.[].schedule`

Type: `string`.

Cron schedule's schedule in crontab format.

### `annotations`

Collection of [service annotations](annotations.md).

### `annotations.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Annotation's machine name.

### `annotations.[].value`

Type: `string`.

Annotation's value.

### `annotations.[].env`

Type: `enum`.

If set, the annotation will be added only to application instances that have the provided [environment type](../apps/env.md#type).

### `database`

Configuration of [service database](database.md)

Only allowed for `database` type services. Provides configuration for database.

Example:

```yml

database:
  type: mariadb
  kind: mariadb
  port: 3306
  ssl: true
  root:
    username: root
    password: '{{root_password}}'
  db:
    name: '{{app.name}}_{{instance.name}}'
    charset: 'utf8mb4'
    collation: 'utf8mb4_unicode_520_ci'
    actions:
      create:
        args:
          - make
          - create-db
          - 'name="{{database.db.name}}"'
          - 'charset="{{database.db.charset}}"'
          - 'collation="{{database.db.collation}}"'
          - 'host="{{database.host}}"'
      drop:
        args:
          - make
          - drop-db
          - 'name="{{database.db.name}}"'
          - 'host="{{database.host}}"'
  user:
    name: '{{app.name}}_{{instance.name}}'
    password: '{{password}}'
    actions:
      create:
        args:
          - make
          - create-user
          - 'username="{{database.user.name}}"'
          - 'password="{{database.user.password}}"'
          - 'host="{{database.host}}"'
      drop:
        args:
          - make
          - drop-user
          - 'username="{{database.user.name}}"'
          - 'host="{{database.host}}"'
      grant:
        args:
          - make
          - grant-user-db
          - 'username="{{database.user.name}}"'
          - 'db="{{database.db.name}}"'
          - 'host="{{database.host}}"'
      revoke:
        args:
          - make
          - revoke-user-db
          - 'username="{{database.user.name}}"'
          - 'db="{{database.db.name}}"'
          - 'host="{{database.host}}"'
  charsets:
    - name: utf16
      title: UTF-16 Unicode
      collation: utf16_general_ci
    - name: utf16le
      title: UTF-16LE Unicode
      collation: utf16le_general_ci
    - name: utf32
      title: UTF-32 Unicode
      collation: utf32_general_ci
    - name: utf8
      title: UTF-8 Unicode
      collation: utf8_general_ci
    - name: utf8mb4
      title: 4-Byte UTF-8 Unicode
      collation: utf8mb4_unicode_520_ci
      default: true
```

#### `database.type`

Type: `string`. Required.

Machine name of a specific database type.

#### `database.kind`

Type: `enum`. Required.

Can be one of the following kinds:

- `mysql`
- `mariadb`
- `postgres`

#### `database.port`

Type: `int`. Required.

Database connection port number.

#### `database.ssl`

Type: `boolean`.

Whether to use SSL connection for connecting to the database server.

#### `database.root`

Database super admin (root) user details. Required.

##### `database.root.username`

Type: `string`. Required.

Database super admin (root) username.

##### `database.root.password`

Type: `string`. Required.

Database super admin (root) password.

#### `database.db`

Database DB configuration settings.

##### `database.db.name`

Type: `string`. Required.

Name of DB to create. Can contain [`{{tokens}}`](tokens.md).

##### `database.db.charset`

Type: `string`. Required.

Default charset for a DB.

##### `database.db.collation`

Type: `string`. Required.

Default collation for a DB.

##### `database.db.actions`

Defines actions for container-based database to run a kubernetes job to create and to drop DBs.

##### `database.db.actions.create`

Action to create a database DB.

###### `database.db.actions.create.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.db.actions.create.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

##### `database.db.actions.drop`

Action to drop a database DB.

###### `database.db.actions.drop.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.db.actions.drop.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

#### `database.user`

Database user configuration settings. Required.

##### `database.user.name`

Type: `string`. Required.

Database user's name. Can contain [`{{tokens}}`](tokens.md).

##### `database.user.password`

Type: `string`. Required.

Database user's password. Can contain [`{{tokens}}`](tokens.md).

##### `database.user.actions`

Defines actions for container-based database to run kubernetes job to create/drop database users and to grant/revoke permissions to a DB.

##### `database.user.actions.create`

Action to create a database user.

###### `database.user.actions.create.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.user.actions.create.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

##### `database.user.actions.drop`

Action to drop a database user.

###### `database.user.actions.drop.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.user.actions.drop.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

##### `database.user.actions.grant`

Action to drop a database user.

###### `database.user.actions.grant.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.user.actions.grant.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

##### `database.user.actions.revoke`

Action to drop a database user.

###### `database.user.actions.revoke.args`

Type: `string list`.

Container's args for action's kubernetes job to override.

###### `database.user.actions.revoke.command`

Type: `string list`.

Container's command for action's kubernetes job to override.

#### `database.charsets`

List of charsets supported by database.

##### `database.charsets.[].name`

Type: `string`. Required.

Machine name of a charset.

##### `database.charsets.[].title`

Type: `string`.

Human-readable title of a charset.

##### `database.charsets.[].collation`

Type: `string`.

Charset collation.

### `derivatives`

Configuration of [derivative services](derivatives.md).

Example:

```yml
derivatives:
  - name: php-sshd
    icon: ssh
    title: SSHD
    args: [ 'sudo', '/usr/sbin/sshd', '-De' ]
    type: ssh
    default: true
    required: false
    endpoints:
      - name: sshd
        ports:
          - name: sshd
            main: true
            number: 22
            type: tcp
    env:
      - name: SSHD_GATEWAY_PORTS
        value: clientspecified
    helm:
      values:
        - name: livenessProbe
          value: ""
        - name: readinessProbe
          value: ""
        - name: containerPort.name
          value: sshd
        - name: containerPort.number
          value: 22
```

#### `derivatives.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Derivative's machine name.

#### `derivatives.[].title`

Type: `string`. Required.

Derivative's human-readable title.

#### `derivatives.[].icon`

Type: `string`.

Icon name of the derivative, shown in Wodby dashboard.

#### `derivatives.[].type`

Type: `enum`.

Override type of the derivative service.

#### `derivatives.[].args`

Type: `string list`.

List of container args to override.

#### `derivatives.[].command`

Type: `string list`.

Container command to override.

#### `derivatives.[].default`

Type: `boolean`.

True to make derivative be enabled by default when the parent service selected.

#### `derivatives.[].required`

Type: `boolean`.

True to make derivative required mandatory when the parent service selected.

#### `derivatives.[].env`

Extra environment variables for the derivative.

##### `derivatives.[].env.[].name`

Type: `string`. Required.

Environment variable's name.

##### `derivatives.[].env.[].value`

Type: `string`.

Environment variable's value. Can contain [`{{tokens}}`](tokens.md).

##### `derivatives.[].env.[].env`

Type: `enum`.

If set, the environment variable will be added only to application instances that have the provided [environment type](../apps/env.md#type).

##### `derivatives.[].env.[].secret`

Type: `boolean`.

True if the environment variable should be secret. Secret environment variable's value stored in Kubernetes secret resource and not shown in Wodby dashboard.

#### `derivatives.[].endpoints`

Collection of [endpoints](endpoints.md) for the derivative. This will override parent service endpoints.

##### `derivatives.[].endpoints.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Machine name of the endpoint.

##### `derivatives.[].endpoints.[].ports`

Collection of endpoint's ports.

###### `derivatives.[].endpoints.[].ports.[].name`

Type: `string`. Alphanumeric and dash symbols allowed. Required.

Endpoint port's machine name.

###### `derivatives.[].endpoints.[].ports.[].main`

Type: `boolean`.

True to make the derivative's endpoint's port as main. If none marked as main, the first port will be chosen as main.

###### `derivatives.[].endpoints.[].ports.[].number`

Type: `integer`.

Port's number.

###### `derivatives.[].endpoints.[].ports.[].type`

Type: `enum`. Allowed values are `tcp`, `udp` and `http`

Port's type.

#### `derivatives.[].helm`

Extra helm configuration for the derivative.

##### `derivatives.[].helm.values`

Collection of helm values.

###### `derivatives.[].helm.values.[].name`

Type: `string`

Name of the helm value.

###### `derivatives.[].helm.values.[].value`

Type: `string`, `string list`, `object`

Value of the helm value. Can contain [`{{tokens}}`](tokens.md).
