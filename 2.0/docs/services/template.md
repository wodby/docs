# Service template

## Example

```
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
  args: ['drush', 'cc', 'all']
  type: button
  title: Clear all cache
# - name: drush9_alias
#   args: ['make', 'drush9-alias']
#   type: output
#   title: Generate drush 9 alias
- name: user_login
  args: ['make', 'user-login']
  type: output
  title: Generate one-time login link
  privileged: true
```

## Reference

## `name`

Machine name of a service, must be unique, cannot be changed. Only alphanumeric and dash symbols allowed.

Mandatory.

## `type`

Service type, can be one of the following:

- `service` stateless (e.g. Nginx) or a stateful (e.g. OpenSMTPD) service. Can be scalable
- `db` database servers, stateful services
- `infrastructure` used in infrastructure applications, currently, can be added only by Wodby.
- `storage` used for distributed storage services, e.g. NFS or Rook
- `datastore` memory storages like Redis and Memcached, stateful services
- `search` stateful services, search engines like Elasticsearch and Solr Cloud.
- `ssh` SSH server, usually used as derivative services

Can be used in selectors.

Mandatory.

## `icon`

Icon name in Wodby dashboard.

## `from`

Inherit specified service.

## `title`

Human-readable title of a service, can be changed.

Mandatory.

## `hostname`

Hostname that will be used as the name of a kubernetes service. Mandatory for non-external services.

## `scalable`

Whether this service support scalability. Should be always `true` for stateless services. For stateful services depends on the implementation. 

## `labels`

List of text labels for a service, to be used in selectors.

## `options`

Option represent version and variants of service. Mandatory to specify at least on option.

## `containers`

Definition of containers of a service. Not allowed for external services. Mandatory for non-external services.

## `build`

Configuration for buildable services.

## `derivatives`

Configuration of derivative services. 

Example:

```yml
derivatives:
- name: php-sshd
  icon: ssh
  title: SSHD
  args: ['sudo', '/usr/sbin/sshd', '-De']
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

## `links`

Configuration of [service links](links.md).

## `volumes`

Configuration of [service volumes](volumes.md)

## `integrations`

Configuration of [service integrations](integrations.md)

## `settings`

Configuration of [service settings](settings.md)

## `backups`

Configuration of [service backups](backups.md)

## `imports`

Configuration of [service imports](imports.md)

## `tokens`

Configuration of [service tokens](tokens.md)

## `actions`

Configuration of [service actions](actions.md)

## `helm`

Configuration of [service helm integration](helm.md). Mandatory for non-external services.

## `certs`

Configuration of [service certificates](certs.md).

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

## `configs`

Configuration of [service configs](configs.md).


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

Machine name of a specific database type. Mandatory for database.

#### `database.kind`

Can be one of the following kinds:

- `mysql`
- `mariadb`
- `postgres`

Mandatory for database.

#### `database.port`

Database connection port number.

Mandatory for database.

#### `database.ssl`


#### `database.root`

Database super admin (root) user details. Mandatory for database.

##### `database.root.username`

Database super admin (root) username. Mandatory for database.

##### `database.root.password`

Database super admin (root) password. Mandatory for database.

#### `database.charsets`

List of charsets supported by database.

#### `database.charsets.[].name`

Machine name of a charset.

#### `database.charsets.[].title`

Human-readable title of a charset.

#### `database.charsets.[].collaction`

Charset collation.

#### `database.db`

Database DB configuration settings.

##### `database.db.name`

Name of DB to create, tokens usage allowed.

##### `database.db.charset`

Default charset for a DB.

##### `database.db.collation`

Default collation for a DB.

##### `database.db.actions`

Defines actions for container-based database to run a kubernetes job to create and to drop DBs.

#### `database.user`

Database user configuration settings.

##### `database.user.name`

Database user's name, tokens usage allowed.

##### `database.user.password`

Database user's password, tokens usage allowed.

##### `database.user.actions`

Defines actions for container-based database to run kubernetes job to create/drop database users and to grant/revoke permissions to a DB.

