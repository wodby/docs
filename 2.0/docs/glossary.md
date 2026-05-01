# Glossary

## App

The top-level application object in Wodby. All app instances of the same app share one stack and app identity, but the app itself is not the running deployment.

## App instance

One deployed copy of an app. Each app instance is assigned to an Environment (Env) and has its own services, domains, builds, and configuration.

## App service

One service inside one app instance. An app service is the app-level representation of a stack service for that specific deployed app copy.

## Backup preset

A reusable backup configuration that stores storage destination settings and can optionally schedule automatic backups.

## Demo

The temporary Wodby Cloud option for testing. Demo clusters and their applications are deleted automatically after 24 hours.

## Endpoint

A network entry point exposed by an app service. In practice, endpoints back domains and ports.

## Environment

A named Environment (Env) definition assigned to app instances and other resources. Each Env has a fixed type chosen from `prod`, `staging`, `test`, `dev`, or `feature`, and multiple Envs can share the same type.

## Integration

A configured connection to a third-party service, created from a provider.

## K3S

A lightweight Kubernetes distribution used for self-hosted clusters connected from your own server.

## Main domain

The main domain for the whole app instance. The main domain is always also primary.

## Managed Kubernetes

A Kubernetes cluster created in your own cloud account through a supported provider integration.

## Organization

The top-level workspace boundary for users, teams, projects, billing, and shared settings.

## Primary domain

The default domain for a specific app service endpoint.

## Project

The main resource and access boundary inside an organization.

## Provider

Wodby's definition of how to work with a third-party service, including fields, kinds, and exposed variables.

## Resource owner

The organization or project that owns a resource. The owner determines the default write boundary, while sharing controls which other projects can read/use or modify/delete the resource.

## Service

Wodby's representation of one piece of software, a Helm-based workload, or a workflow. Most services deploy containers; external services represent software that runs outside Wodby.

## Sharing

The project access list for a resource. Sharing can grant `Read/Use` or `Modify/Delete` access without changing the resource owner.

## Stack

The blueprint from which an app is created.

## Stack revision

A versioned snapshot of the stack configuration. App instances can be upgraded between stack revisions.

## Stack service

A service as included in a stack, tied to a specific service revision plus stack-level configuration such as options, settings, links, integrations, and defaults.

## Team

A reusable group of organization members used to assign project access more efficiently.

## Variable integration

An integration whose main purpose is to inject reusable environment variables into apps or stacks.

## Variable provider

A provider that exposes environment variables instead of, or in addition to, infrastructure actions.

## Wodby Cloud

Wodby's managed Kubernetes offering, created from the new app flow instead of the Kubernetes list.

## Related pages

- [Getting started](index.md)
- [Applications overview](apps/index.md)
- [Kubernetes overview](kubernetes/index.md)
- [Integrations overview](integrations/index.md)
