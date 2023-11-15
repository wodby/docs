# Service

## Overview

Service (stack service) is a basic unit of managed infrastructure. Services have versions and manifests. Services can be added only by importing from a git repository. Most services have a template (Wodby template) and kubernetes manifests, however some types of services (like `config`) may not have kubernetes manifests. 

## Type

Every service has a type. Type defines the behavior of a service and how it managed. There are several types of services:

### `service`

Stateless service, e.g. Nginx. Can be scaled up and down. Usually, services of this type have a template and kubernetes manifests

### `db`

Database servers, stateful services. Usually, services of this type have a template and kubernetes manifests

### `infrastructure`

Used in infrastructure applications, currently, can be added only by Wodby.

### `storage`

Used for distributed storage services, e.g. NFS, Rook or Longhorn. Usually, services of this type have a template and kubernetes manifests

### `datastore`

Memory storages like Redis and Memcached, stateful services. Usually, services of this type have a template and kubernetes manifests

### `search`

Stateful services, search engines like Elasticsearch and Solr Cloud.

### `ssh`

SSH server, usually used as derivative services

### `proxy`

Reverse proxy servers like Varnish and HAProxy

## Inheritance

Services can inherit from other services. Inheritance is a way to extend a service with additional configuration. For example, you can create a new service that inherits from the `php` service and add additional environment variables or links to it.

## Derivatives

Derivatives are services that created from other services. For example, ssh server service added as a derivative to PHP-FPM. 

## Options

Options usually used to represent service versions, e.g. Nginx has two options: `1.23` and `1.22`. A service can have multiple options, specify one of them as default and add to some of them End of Life (EOL) date. 

## Settings

