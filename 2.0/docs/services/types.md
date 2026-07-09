# Service types

Every service has a `type`. The type controls how the service is deployed and which sections are valid in the service
template.

## `service`

General-purpose application services such as runtimes, web servers, workers, and mail relays. This is the only type
that can define a [`build` section](build.md), and it is also the only type that can be marked as scalable.

### Mail relay services

Wodby does not use a separate `smtp` service type.

Services that send mail through an SMTP relay are modeled as regular services of type `service`. They typically define
[integrations](configuration.md#integrations) so customers can connect third-party SMTP providers such as Brevo or AWS
SES.

## `db`

Database services. These services define a [`database` section](template.md#database) that describes the engine,
default connection settings, and supported database or user management actions.

A service of type `db` creates a [Database](../databases/index.md) for the app.

## `infrastructure`

Infrastructure-level services used in infrastructure apps or to provide shared platform capabilities.

## `storage`

Shared storage services, such as distributed or network-backed filesystems.

Storage services provide shared storage that other services can mount, for example distributed or network-backed
filesystems that support multiple writers.

Use this type when the service's main purpose is to provide storage rather than run application logic.

## `datastore`

In-memory or key-value data stores such as Redis and Memcached.

## `search`

Search and indexing services such as Elasticsearch or Solr.

## `operator`

Services that manage other Kubernetes resources or related workloads.

## `ssh`

SSH access services, usually defined as derivatives of another service.

They are usually defined as [derivatives](derivatives.md) so they inherit the parent service's versions, environment
variables, and related configuration while exposing SSH access separately.

Use this type when you need shell or file-access workflows around an existing application service.

## `vpn`

VPN and private connectivity services.
