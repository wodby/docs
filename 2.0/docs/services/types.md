# Service type

Every service has a type, depending on the type there will be 

## `service`

These types of services are usually stateless (e.g. Nginx) or a stateful (if none other match) service. Can be scalable.

## `db`

Used for [Database services](database.md), stateful services.

## `storage` 

Used for distributed storage services, e.g. NFS or Rook.

## `datastore` 

Memory storages like Redis and Memcached, stateful services

## `search` 

Stateful services, search engines like Elasticsearch and Solr Cloud.

## `ssh` 

SSH server, usually used as derivative services.

## `infrastructure` 

Used in infrastructure applications, currently, can be added only by Wodby.
