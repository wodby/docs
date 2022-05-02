# Stack template

## Example

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