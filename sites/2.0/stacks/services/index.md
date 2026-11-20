Source: https://wodby.com/docs/2.0/stacks/services/

# Stack services

A stack service is a [service](https://wodby.com/docs/2.0/services/) as included in a stack. It always points to a specific service revision.

It combines the underlying service with stack-level configuration such as:

- enabled or disabled state
- selected options and defaults
- settings, environment variables, and Helm values
- resources and volumes
- integrations and links to other stack services
- configs, tokens, annotations, and cron schedules

Links are defined between stack services, so the stack describes how services work together.

When you create an app environment, each stack service becomes an [app service](https://wodby.com/docs/2.0/apps/services/) for that deployed copy of the app.

When a later stack revision adds a stack service, upgrading an app environment creates the corresponding app service for
that environment. When a later stack revision removes a stack service, upgrading an app environment marks the obsolete app
service for deletion and uninstalls its Kubernetes resources after the upgrade.

Stack service machine names must follow the [Kubernetes service name rules](https://wodby.com/docs/2.0/naming/#kubernetes-service-names) and be unique within the stack, including derivative stack services.

See [Stack configuration](https://wodby.com/docs/2.0/stacks/configuration/#stack-services) for the stack-level controls available for stack services.
