# Stack services

A stack service is a [service](../services/index.md) as included in a stack. It always points to a specific service revision.

It combines the underlying service with stack-level configuration such as:

- enabled or disabled state
- selected options and defaults
- settings, environment variables, and Helm values
- resources and volumes
- integrations and links to other stack services
- configs, tokens, annotations, and cron schedules

Links are defined between stack services, so the stack describes how services work together.

When you create an app instance, each stack service becomes an [app service](../apps/services.md) for that deployed copy of the app.

See [Stack configuration](configuration.md#stack-services) for the stack-level controls available for stack services.
