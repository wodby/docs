# Service

## Overview

A service is Wodby's reusable definition of one part of an application platform. Depending on the service, it can
represent actual software running in Kubernetes, an abstraction over a Helm chart, or an operational workflow packaged
as a service.

Most services deploy one or more containers in the cluster. External services are the exception: they do not run their
own containers in Wodby and instead model a connection to software managed elsewhere.

Services are versioned. Each change creates a new service revision, and stacks reference specific revisions. Custom
services imported from git are defined by a [template](template.md).

Inside a stack, a service revision becomes a [stack service](../stacks/services.md). Stack services let you enable,
disable, connect, and customize a service for that stack.

## Type

Every service has a type that defines how Wodby treats it and which template sections are available.

- `service`: general-purpose application services, including runtimes, web servers, workers, and mail relays
- [`db`](database.md): database services
- `infrastructure`: infrastructure-level services used in infrastructure apps
- [`storage`](storage.md): shared storage services
- `datastore`: in-memory and key-value stores such as Redis or Memcached
- `search`: search and indexing services
- `operator`: services that manage other Kubernetes resources or workloads
- [`ssh`](ssh.md): SSH access services, usually used as derivatives
- `vpn`: VPN and private connectivity services

See [service types](types.md) for details.

## [Template](template.md)

Custom services imported from git are defined by a template. See the [template reference](template.md).

## External

External services do not deploy their own containers in Wodby. Instead, they connect your app to services managed
outside Wodby, such as a cloud database or another third-party system.

## [Derivatives](derivatives.md)

Derivatives are additional services created from another service. A common example is an SSH service added as a
derivative of an application runtime.

## [Endpoints](endpoints.md)

Endpoints define the ports a service exposes.

## [Options](options.md)

Options usually represent supported versions or variants of a service.

## [Build](build.md)

Only services of type `service` can define build instructions for [CI/CD](../cicd/index.md). A build can also provide
starter templates for new projects.

## [Links](links.md)

Links define how services connect to each other, what dependencies they require, and which services are compatible.

## [Settings](settings.md)

Settings are simple configuration values exposed in the UI. They usually map to environment variables used by the
service.

## [Configs](configs.md)

Configs represent configuration files that can be mounted into a service and overridden at stack or app level.

## [Helm](helm.md)

Non-external services define Helm information and can provide default Helm values that tell Wodby how to deploy their
Kubernetes resources.

## [Kubernetes](kubernetes.md)

Some services define additional Kubernetes-specific metadata, such as infrastructure selectors.

## [Tokens](tokens.md)

Tokens provide reusable fixed or generated values that services can reference.

## [Backups](backups.md)

Services can define backup functionality that creates archives for upload to connected storage.

## [Imports](imports.md)

Services can define import workflows for restoring files or data into a running service.

## [Database](database.md)

Database services define extra information for working with [databases](../databases/index.md).

## [Cron](cron.md)

Services can define cron schedules for recurring tasks.

## [Actions](actions.md)

Services can define actions that run commands automatically during lifecycle events or on demand from the UI.

## [Annotations](annotations.md)

Services can define annotations for additional Helm or Kubernetes configuration.

## [Certificates](certs.md)

Services may require self-signed TLS certificates that are then mounted into deployed resources.

## [Integrations](integrations.md)

Services can define which integrations they support or require. A common example is a [mail service](smtp.md) that
connects to a third-party SMTP provider.

## [Volumes](volumes.md)

Services can define volumes for persistent or shared data.
