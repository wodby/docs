# Service types

Every service has a `type`. The type controls how the service is deployed and which sections are valid in the service
template.

## `service`

General-purpose application services such as runtimes, web servers, workers, and mail relays. This is the only type
that can define a [`build` section](build.md), and it is also the only type that can be marked as scalable.

Mail relay services use the regular `service` type. See [Mail services](smtp.md).

## [`db`](database.md)

Database services. These services define a [`database` section](template.md#database) that describes the engine,
default connection settings, and supported database or user management actions.

## `infrastructure`

Infrastructure-level services used in infrastructure apps or to provide shared platform capabilities.

## [`storage`](storage.md)

Shared storage services, such as distributed or network-backed filesystems.

## `datastore`

In-memory or key-value data stores such as Redis and Memcached.

## `search`

Search and indexing services such as Elasticsearch or Solr.

## `operator`

Services that manage other Kubernetes resources or related workloads.

## [`ssh`](ssh.md)

SSH access services, usually defined as derivatives of another service.

## `vpn`

VPN and private connectivity services.
