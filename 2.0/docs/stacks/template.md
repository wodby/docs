# Stack Template

Example:

```yaml
name: php
icon: php
title: PHP

services:
  - name: php
    title: PHP
    service: php
    required: true
    links:
      - name: db
        service: mariadb
      - name: sendmail
        service: mailpit

  - name: nginx
    title: Nginx
    service: php-nginx
    required: true
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
    service: mariadb
    volumes:
      - name: data
        size: 20

  - name: httpd
    title: Apache HTTP server
    service: php-httpd
    disabled: true
    containers:
      - name: httpd
        env:
          - name: APACHE_VHOST_PRESET
            value: php
    links:
      - name: backend
        service: php

  - name: postgres
    title: PostgreSQL
    service: postgres
    disabled: true
    volumes:
      - name: data
        size: 20

  - name: valkey
    title: Valkey
    service: valkey
    disabled: true

  - name: mailpit
    title: Mailpit
    service: mailpit

  - name: opensmtpd
    disabled: true
    title: OpenSMTPD
    service: opensmtpd

  - name: gotenberg
    title: Gotenger
    service: gotenberg
    disabled: true  
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
