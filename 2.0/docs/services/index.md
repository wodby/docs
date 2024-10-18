# Service

## Overview

Service is a basic unit of managed infrastructure. Services are versioned entities and have revisions. For each new update a service revision will be issued.  

Services can be added only by importing a template from a git repository. 

When a service added to a [stack](../stacks/index.md) we call it a _stack service,_ and it can be additionally [customized](../stacks/index.md#configuration) for a specific stack.

## Template


## Inheritance

Services can inherit from other services. Inheritance is a way to extend a service with additional configuration. For example, you can create a new service that inherits from the `php` service and add additional environment variables or links to it.

## Derivatives

Derivatives are services that created from other services. For example, ssh server service added as a derivative to PHP-FPM.

## Options

Options usually used to represent service versions, e.g. Nginx has two options: `1.23` and `1.22`. A service can have multiple options, specify one of them as default and add to some of them End of Life (EOL) date.

## Settings

### Reference

#### Type

Every service has a type. Type defines the behavior of a service and how it managed. There are several types of services:

- `service` stateless (e.g. Nginx) or a stateful (e.g. OpenSMTPD) service. Can be scalable
- `db` database servers, stateful services
- `infrastructure` used in infrastructure applications, currently, can be added only by Wodby.
- `storage` used for distributed storage services, e.g. NFS or Rook
- `datastore` memory storages like Redis and Memcached, stateful services
- `search` stateful services, search engines like Elasticsearch and Solr Cloud.
- `ssh` SSH server, usually used as derivative services

#### Options

#### Endpoints
