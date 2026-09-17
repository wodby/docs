# Glossary

## App

An application that groups one or more instances. Each instance is a deployed environment of that app. See [App model](apps/app-vs-instance-vs-service.md).

## API key

A credential used to authenticate API requests and automation, including CI pipelines. New keys are scoped to one organization and use their creator's permissions. See [API keys](user/api-keys.md).

## Backup

An archive of an instance's database, persistent files, or both, supported by its stack. Restoring a backup restores the selected data; it does not roll back application code or the stack version. See [Backups](apps/backups.md).

## Build

A recorded CI build with service images that can be deployed to an instance. Build history remains after image cleanup, but redeployment requires the images to remain available. See [Builds](apps/builds.md).

## Container

A running instance of a container image that provides software for a stack service. See [Containers](infrastructure/containers.md).

## Container image

A packaged version of software and its dependencies used to run a container. CI workflows build and release service images before deploying them.

## Container registry

Storage for container images. CI builds can use Wodby's registry or an external registry. See [Container registry](cicd/docker-registry.md).

## Direct Git deployment

A workflow that pulls application code from a connected Git repository and can run post-deployment scripts. It is available for Drupal and WordPress stacks and their forks. See [Direct Git](cicd/git.md).

## Domain

A hostname used to reach an instance over HTTP or HTTPS. Instances can use generated technical domains and attached custom domains. See [Domains](apps/domains.md).

## Edge

The reverse proxy on a connected server that sends public traffic to application services, handles configured redirects, and terminates TLS. See [Single-server infrastructure](infrastructure/index.md).

## Infrastructure

The container platform installed on a connected server to run applications. Infrastructure and application stacks are versioned and maintained separately.

## Instance

One isolated environment of an app, with its own destination, stack configuration, domains, and deployment settings. See [Instances](apps/instances.md).

## Instance type

A classification such as dev, staging, or production that influences stack configuration. Its effects depend on the stack, including differences in error reporting and health checks.

## Integration

A configured connection to an external provider, such as a Git service, cloud provider, or container registry.

## Organization

The workspace that owns applications, servers, repositories, integrations, stacks, billing, and memberships. Roles determine members' access to these resources. See [Organization](org.md).

## Post-deployment script

A script run after code deployment, such as database updates or cache cleanup. See [Post-deployment scripts](cicd/post-deployment-scripts.md).

## Server

A host connected to Wodby on which application instances run. Instances of the same app can run on different servers. See [Connecting a server](infrastructure/connecting-server.md).

## Service

One component of a stack, such as an HTTP server, application runtime, or database. Services have container implementations and can be configured per instance. Some services are optional.

## SSH key

A public key added to your account for access to SSH containers in instances you can access. The matching private key stays on your device. See [SSH keys](user/ssh-keys.md).

## Stack

A preconfigured package of services and their configuration used to deploy an application. See [Stacks](stacks/index.md).

## Stack version

A release of a stack's configuration and service implementations. Updating an organization's stack and upgrading an instance are separate operations. See [Stacks maintenance](stacks/maintenance.md).

## Technical domain

A generated domain in the form `[instance].[app name].[organization name].wodby.cloud`. Find it under **Instance > Domains**.

## Third-party CI

An external continuous integration system that uses the Wodby CLI to initialize, build, release, and deploy service images. See [Third-party CI](cicd/third-party.md).

## Related pages

- [Get Started](index.md)
- [App model](apps/app-vs-instance-vs-service.md)
- [CI/CD](cicd/index.md)
