# Service

## Overview

A service is Wodby's reusable definition of one part of an application platform. Depending on the service, it can
represent actual software running in Kubernetes, an abstraction over a Helm chart, or an operational workflow packaged
as a service.

Most services deploy one or more containers in the cluster. External services are the exception: they do not run their
own containers in Wodby and instead model a connection to software managed elsewhere.

Services are versioned. Each change creates a new service revision, and stacks reference specific revisions. Custom
services are defined by a [template](template.md).

Public Wodby services are listed in [`wodby/services`](https://github.com/wodby/services), with links to their source
repositories. To create a new service in Git, start from the [`wodby/service`](https://github.com/wodby/service)
boilerplate.

Inside a stack, a service revision becomes a [stack service](../stacks/services.md). Stack services let you enable,
disable, connect, and customize a service for that stack.

## Service model

Every service has a type that defines how Wodby treats it and which template sections are available.

- `service`: general-purpose application services, including runtimes, web servers, workers, and mail relays
- `db`: database services
- `infrastructure`: infrastructure-level services used in infrastructure apps
- `storage`: shared storage services
- `datastore`: in-memory and key-value stores such as Redis or Memcached
- `search`: search and indexing services
- `operator`: services that manage other Kubernetes resources or workloads
- `ssh`: SSH access services, usually used as derivatives
- `vpn`: VPN and private connectivity services

See [service types](types.md) for details.

## Authoring

Use these pages when creating or maintaining custom services:

- [Create](create.md): create services from Git, local manifests, or Helm chart scaffolds.
- [Updates](updates.md): update Git-backed services manually or automatically.
- [Template reference](template.md): full `service.yml` schema.

## Runtime model

Use these pages to understand how a service deploys and connects inside an app:

- [Workloads](workloads.md): Kubernetes workload mapping, selectors, containers, primary workloads, and build targets.
- [Helm](helm.md): chart references, Helm values, and image mappings.
- [Build](build.md): CI/CD build configuration for buildable services.
- [Networking](networking.md): endpoints and service-to-service links.
- [Derivatives](derivatives.md): additional services derived from a parent service, such as SSH access services.

## Configuration and operations

Use these pages for stack and app-service customization surfaces:

- [Configuration](configuration.md): options, settings, configs, volumes, tokens, annotations, certificates, and integrations.
- [Operations](operations.md): actions, backups, imports, and cron schedules.

External services do not deploy their own containers in Wodby. Instead, they connect your app to services managed
outside Wodby, such as a cloud database or another third-party system.
