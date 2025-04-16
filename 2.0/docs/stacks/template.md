# Stack Template

Example:

```
name: drupal9
icon: drupal9
title: Drupal 9

services:
- name: php
  title: PHP
  service: php-drupal9
  required: true
  options:
  - version: '8.1'
    default: true
  - version: '8.0'
  - version: '7.4'
  containers:
  - name: php
    env:
    - name: PHP_MEMORY_LIMIT
      value: 512M
    resources:
      request:
        cpu: 100
        memory: 16
  volumes:
  - name: files
    size: 50
  links:
  - name: db
    service: mariadb

- name: nginx
  title: Nginx
  service: nginx-drupal9
  required: true
  links:
  - name: backend
    service: php

- name: mariadb
  title: MariaDB
  service: mariadb
  volumes:
  - name: data
    size: 20

- name: mariadb-cloud
  title: Cloud MariaDB
  service: mariadb-cloud
  disabled: true
  options:
  - version: '10.3'

- name: mysql-cloud
  title: Cloud MySQL
  service: mysql-cloud
  disabled: true
  options:
  - version: '5.7'
  - version: '8'

tokens:
- name: random_token
  generate:
    regex: '[0-9a-z]{5,10}'
- name: db_backup_ignore_tables
  value: 'cache_%;cache;ctools_object_cache;ctools_views_cache;flood;history;queue;search_index;semaphore;sequences;sessions;watchdog'
```

## Reference

### name

Stack machine name, cannot be changed.

### title

Stack human-readable title, can be changed.

### icon

Icon name of a stack in Wodby dashboard.

### env

Stack-wide environment variables.

### tokens

Stack-wide tokens. Tokens can either have a plain value or a regular expression that will be used to generate a random secret value when an app services created/updated. You can use tokens in environment variables' values.

### services

Under `services` you can define list of [services](../services/index.md) your stack consist of.

#### service.name 

Machine name of a [stack service](services.md), must be unique, cannot be changed.

#### service.title

Human-readable title of a service in your stack, can be changed.

#### service.service 

Machine name of an existing public [service](../services/index.md).

#### service.options 

Limitations of service options that can be used in a stack, also defines the default option. 

#### service.derivatives 

Configuration of specific service derivatives.  

#### service.env 

Service-specific environment variables. 

#### service.disabled 

When set the service will be disabled by default 

#### service.required

When set service is mandatory to include when a new app created. All services linked in a mandatory service will also be mandatory.

#### service.volumes

Overrides a default size of a service volume

#### service.links

Set up links with existing stack services for service-defined links.

```
links:
- name: name-of-existing-service-defined-link
  service: stack-service-to-link-that-satisfies-link-selectors
```

#### service.containers

Configuration of container-specific resources and environment variables.

#### service.container.env

Container-specific environment variables.  

#### service.container.resources

Container-specific resources.  
