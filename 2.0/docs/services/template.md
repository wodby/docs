# Service template

## Service types

| Type             | Description                                                        |
|------------------|--------------------------------------------------------------------|
| `service`        | Stateless service, e.g. PHP-FPM                                    |
| `db`             | Database services, usually stateful sets                           |
| `config`         |                                                                    |
| `infrastructure` | Used for infrastructure apps, e.g. ingress, certmanager            |
| `nfs`            | Programmatically created NFS service, used only for shared storage |
| `ssh`            | Stateless service that can work with SSH keys                      |
| `cache`          | Cache storage, e.g. memcached                                      |
| `proxy`          | Proxy servers, reverse proxy servers, e.g. varnish                 |
 

##  Example

```
name: drupal9-php
type: service
icon: php
title: PHP (Drupal 9)
hostname: php
scalable: true
labels:
- php
- php-fpm
- drupal
- drupal9
options:
- version: '8.1'
  default: true
  eol: '2024-11-25T00:00:00+00:00'
- version: '8.0'
  eol: '2023-11-26T00:00:00+00:00'
- version: '7.4'
  eol: '2022-11-28T00:00:00+00:00'
- version: '7.3'
  eol: '2021-12-06T00:00:00+00:00'
containers:
- name: php
  image: wodby/drupal-php
  # if main not specified the first port becomes main.
  main: true
  resources:
    request:
      memory: 16
  env:
  - name: DRUPAL_FILES_SYNC_SALT
    value: '{{sync_salt}}'
    secret: true
  - name: DRUPAL_HASH_SALT
    value: '{{hash_salt}}'
    secret: true
  - name: DRUPAL_VERSION
    value: '9'
  - name: PHP_FPM_ENV_VARS
    value: '["WODBY_APP_NAME","WODBY_APP_INSTANCE_NAME","WODBY_ENVIRONMENT_NAME","WODBY_ENVIRONMENT_TYPE","WODBY_BUILD_NUMBER"]'
  - name: PHP_ERROR_REPORTING
    value: 'E_ALL & ~E_DEPRECATED & ~E_STRICT'
    envType: prod
  - name: PHP_DISPLAY_ERRORS
    value: 'Off'
    envType: prod
  - name: PHP_DISPLAY_STARTUP_ERRORS
    value: 'Off'
    envType: prod
  - name: PHP_TRACK_ERRORS
    value: 'Off'
    envType: prod
  - name: ENV_TEST
    value: 'test{{app.name}}123'
  ports:
  - name: fpm
    number: 9000
    # if missing, the first port of the main container considered as main.
    main: true
    type: tcp

build:
  dockerfile: Dockerfile
  connect: true
  templates:
  - name: vanilla
    title: Vanilla Drupal
    repo: https://github.com/wodby/drupal-vanilla
    branch: 9.x

derivatives:
- name: drupal9-php-sshd
  icon: ssh
  title: SSHD
  args: ['sudo', '/usr/sbin/sshd', '-De']
  type: ssh
  default: true
  required: false
  ports:
  - name: sshd
    main: true
    number: 80
    type: tcp
  # for remote xdebug.
  - name: fpm
    number: 9000
    type: tcp
  resources:
    request:
      memory: 16
    limit:
      memory: 512
  env:
  - name: SSHD_GATEWAY_PORTS
    value: clientspecified
  - name: DEBUG
    value: '1'

links:
- name: db
  title: DBMS
  required: true
  env:
  - name: DB_HOST
    value: '{{link.database.host}}'
  - name: DB_PORT
    value: '{{link.database.port}}'
  - name: DB_USER
    value: '{{link.database.user.name}}'
  - name: DB_NAME
    value: '{{link.database.db.name}}'
  - name: DB_PASSWORD
    value: '{{link.database.user.password}}'
    secret: true
  - name: DB_DRIVER
    value: '{{link.database.driver}}'
  selectors:
  - type: db
    labels:
    - mariadb
  - type: db
    labels:
    - mysql
  - type: db
    labels:
    - postgres
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
  - type: db
    labels:
    - redis
- name: varnish
  title: Varnish
  selectors:
  - type: proxy
    labels:
    - varnish
- name: blackfire
  title: Blackfire
  selectors:
  - type: monitoring
    labels:
    - blackfire
  env:
  - name: PHP_BLACKFIRE
    value: '1'
  - name: PHP_BLACKFIRE_AGENT_HOST
    value: '{{link.host}}'
  - name: PHP_BLACKFIRE_AGENT_PORT
    value: '8707'

volumes:
- name: files
  title: Files
  shared: true
  path: /mnt/files
  size: 10

integrations:
- name: variable
  title: Variable
  type: variable
  required: false
  multiple: true
  providers:
  - name: newrelic
    env:
    - name: PHP_NEWRELIC_LICENSE
      value: '{{integration.variables.NEWRELIC_LICENSE}}'
      secret: true
    - name: PHP_NEWRELIC_APPNAME
      value: '{{wodby_app_name}}'

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

imports:
- name: files
  title: Drupal files import
  args:
  - make
  - files-import
  - 'source="{{wodby_import_url}}"'
  extensions:
  - tar
  - tar.gz
  - tgz
  - zip

env:
- name: WODBY_APP_NAME
  value: '{{app.name}}'

tokens:
- name: sync_salt
  generate:
    regex: '[0-9a-z]{32}'
- name: hash_salt
  generate:
    regex: '[0-9a-z]{32}'

backups:
- name: files
  title: Files backup
  upload:
    dir: /mnt/files
    gzip: false
  integrations:
  - backup-destination

actions:
- name: clear_cache
  args: ['drush', 'cc', 'all']
  type: button
  title: Clear all cache
- name: drush9_alias
  args: ['make', 'drush8-alias']
  type: output
  title: Generate drush 9 alias
- name: user_login
  args: ['make', 'user-login']
  type: output
  title: Generate one-time login link
  privileged: true
```