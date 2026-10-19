# Provider vs Integration

A **provider** defines how Wodby connects to a third-party service. An **integration** stores your connection settings
and credentials for that provider.

| Provider | Example integration | Use |
| --- | --- | --- |
| AWS | Your production AWS account | Create clusters, store backups, or use other enabled AWS capabilities |
| GitHub | Your team's GitHub connection | Access repositories |
| Sentry | Your staging Sentry DSN | Supply environment variables to app services |

## Create and use an integration

1. Choose a provider and enter its required connection settings.
2. Choose whether the integration belongs to the organization or a project.
3. [Share it with additional projects](../sharing.md) if needed.
4. Select the integration when configuring an app service, stack, cluster, database, or backup.

See [Integration types](types.md) for the operations each type supports and [Providers](../providers/index.md) for
provider-specific setup instructions.

## Variable providers and variable integrations

A variable provider defines fields that Wodby can pass to containers as environment variables. For example, a Sentry
integration holds a DSN that app services can use for error reporting.

Use a [variable integration](variable.md) to reuse credentials across apps or environments. For a value used by only
one service, you can set an [app-service environment variable](../apps/environment-variables.md) directly.

If your service has no built-in provider, [create a custom variable provider](../providers/custom-variable-providers.md)
to define the fields and environment variables it needs.
