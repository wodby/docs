# Integrations

Integrations are reusable connections between Wodby and third-party services. You create an integration from a [provider](../providers/index.md), choose an owner, and then use sharing when the integration should be available to additional projects.

An integration can represent a cloud account, a Git provider connection, an SMTP relay, a registry account, a VPN integration, or a set of provider-managed environment variables.

## When to use integrations

Use integrations when:

- Wodby needs to connect to an external account or service on your behalf
- you want to reuse the same credentials or connection across multiple apps or projects
- you want provider-backed environment variables instead of repeating raw values manually

In the dashboard, the integration creation form has an `Owner` selector. Choose `Organization <organization>` for an organization-owned integration or `Project <project>` for a project-owned integration. Use the integration's `Sharing` page later when other projects need `Read/Use` or `Modify/Delete` access.

If you are unsure about the difference between providers and integrations, start with [Provider vs integration](providers-vs-integrations.md).

## Providers vs integrations

- A **provider** is the definition of how Wodby works with a third-party service, including its kinds, fields, auth methods, and any variables it exposes.
- An **integration** is your actual connection created from that provider, such as a specific AWS account, GitHub installation, or Sentry DSN.

Wodby ships built-in providers, and you can also create your own variable-only providers when you need custom environment variables that are not covered by the built-in catalog.

## Kinds

Each integration exposes one or more [types](types.md). The type-specific overviews live in the [Providers](../providers/index.md) section because providers are grouped that way in the documentation navigation.

- [Kubernetes providers](../providers/kubernetes.md) for provider-managed cluster provisioning
- [Database providers](../providers/databases.md) for managed database provisioning
- [Storage providers](../providers/storage.md) for backup destinations
- [Git providers](../providers/git.md) for remote repositories used as build sources
- [CI providers](../providers/ci.md) for build and deployment pipelines
- [Registry providers](../providers/registry.md) for container image registries
- [SMTP providers](../providers/smtp.md) for outbound mail relays
- [VPN providers](../providers/vpn.md) for private-network connectivity
- [Variable integrations](variable.md) for reusable provider-backed environment variables

The selected type determines where the integration can be used in the dashboard.

## Where integrations are used

Depending on the provider and type, integrations can be used for:

- Kubernetes cluster creation
- Managed database creation
- App service and stack integrations
- SMTP relay configuration
- External container registries
- Backup storage destinations
- CI/CD workflows

## Related pages

- [Provider vs integration](providers-vs-integrations.md)
- [Providers overview](../providers/index.md)
- [Integration types](types.md)
- [Variable integration](variable.md)
