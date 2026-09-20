# Get Started

Wodby deploys and manages web applications on Kubernetes. A stack defines the services your application needs;
app environments let you deploy those services separately for development, staging, and production.

## Deploy your first application

1. Create or choose an [organization](org.md) and a [project](projects.md).
2. [Choose a cluster option](clusters/choose-platform.md): use your cloud account, connect your own server, or let
   Wodby create and manage the cluster.
3. [Create an application](apps/index.md#creating-new-application) from a catalog stack, configure its first
   environment, and deploy it. You can create a Wodby Cloud cluster during app creation.

For a temporary test, enable [Demo](clusters/demo.md) when creating a Wodby Cloud cluster. Demo clusters and their
applications are deleted automatically after 24 hours.

If the catalog does not include what you need, [create a custom stack](stacks/create.md). You can
[create or import services](services/create.md) to add to it.

## Key concepts

To work through an AI client, start with [Use Wodby with an agent](agents/index.md). It covers connection, read-only
verification, permissions, and migration, staging, and troubleshooting workflows.

- [Apps, app environments, and app services](apps/app-vs-environment-vs-service.md)
- [Stacks](stacks/index.md) and [services](services/index.md)
- [Providers and integrations](integrations/providers-vs-integrations.md)
- [Glossary](glossary.md)

## Next steps

- [Set up CI/CD](cicd/index.md)
- [Manage clusters](clusters/index.md)
- [Manage databases](databases/index.md)
- [Organize projects](projects.md) and [teams](teams.md)
