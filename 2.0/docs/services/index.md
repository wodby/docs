# Service

## Overview

Service is a basic build block of your application's [stack](../stacks/index.md). Services represent a single running service in your application that runs in a container (except external services), e.g. Node.js or Nginx. Services are versioned entities and have revisions that normally correspond to a git tag or commit from a source repository. Services defined with a [template](#template) that imported from a git repository. For each new update a service revision will be issued.

Wodby provides a wide range of services, some of them a generic, some of them are designed to be used a specific stack. You can define your own services and import from a git repository.

A service representation in a stack called a _stack
service_, stack service always references a specific revision of a service and provides additional [configuration](../stacks/configuration.md).

## Type

Every service has a type. Type defines the behavior of a service and how it managed. There are several types of services:

- `service` stateless (e.g. Nginx) or a stateful (e.g. OpenSMTPD) service. Can be scalable
- [`db`](database.md) database servers, stateful services
- `infrastructure` used in infrastructure applications, currently, can be added only by Wodby.
- [`storage`](storage.md) used for distributed storage services, e.g. NFS or Rook
- `datastore` memory storages like Redis and Memcached, stateful services
- `search` stateful services, search engines like Elasticsearch and Solr Cloud.
- [`smtp`](smtp.md) services for mail delivery, integrate with external SMTP providers
- [`ssh`](ssh.md) SSH server, usually used as derivative services

## [Template](template.md)

Service can be created from a template that imported from a git repository. See [template reference](template.md).

## External

External services are the services that do not deploy a container but instead integrate with a third-party service. For example a Cloud MySQL service is an external
_db_ type service that requires a database integration (e.g. AWS RDS) to be connected to work.

## [Derivatives](derivatives.md)

Derivatives are services that created from other services. For example, ssh server service added as a derivative to PHP-FPM.

## [Endpoints](endpoints.md)

Endpoints used to define available ports for a service.

## [Options](options.md)

Options usually used to represent service versions, e.g. Nginx has two options: `1.23` and
`1.22`. A service can have multiple options, specify one of them as default and add to some of them End of Life (EOL) date.

## [Build](build.md)

Build section used for buildable service that build something from a git repository in [CI/CD](../cicd/index.md) process.

Build can provide templates that are boilerplates for demo purposes with defined pipeline for Wodby CI.

## [Links](links.md)

Links define service connectivity and integration with other services, e.g. PHP-FPM service can be linked to a database service. Links are used to define pass information between services (e.g. database connections details), announce requirements to a user (e.g. requires a database to work) and limit with which services it can be connected (e.g. supports MySQL but not PostgreSQL).

## [Settings](settings.md)

Settings are simple configuration options that a service represents and wants a user to configure from UI. When a user changes a setting value it usually means that an environment variable (know to a service's docker image) with this value will be added to the container deployment.

## [Configs](configs.md)

Configs are more complicated templates that represent configuration files within a service. Think of Nginx's virtual host config file. Configs usually always have default values and can be overridden by a user in a stack or in an app instance.

## [Helm](helm.md)

All services (except external) must specify their helm chart information. Helm chart is where the service stores Kubernetes resources that will be deployed.

## [Tokens](tokens.md)

Tokens used to generate random values or reuse a value.

## [Backups](backups.md)

Services can define backup function that implemented in its container image, results in an archive file that will be uploaded to a cloud storage.

## [Imports](imports.md)

Services can define import function that implemented in its container image, works with a URL (specified by user, backup URL or uploaded via Wodby dashboard).

## [Database](database.md)

Database services provide additional configuration on how to work [database](../databases/index.md).

## [Cron](cron.md)

Services can define cron schedules to run automated tasks.

## [Actions](actions.md)

Services can define actions to execute commands during certain events: after deployment (one time or every time), after stack upgrade or when a user clicks a button in UI.

## [Annotations](annotations.md)

Services can define annotations for additional configuration of its Helm chart.

## [Certificates](certs.md)

Services may require generation of self-signed TLS certificates that will be mounted to a running container.

## [Integrations](integrations.md)

Services can define which integrations (except `variable` that allowed for all) they allow or require to be connected. 

## [Volumes](volumes.md)

Services can define volumes for data persistence. 
