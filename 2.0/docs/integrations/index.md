# Integrations

Integrations are reusable connections between Wodby and third-party services. You create an integration from a [provider](../providers/index.md), choose an owner, and then use sharing when the integration should be available to additional projects.

An integration can represent a cloud account, a Git provider connection, an SMTP relay, a registry account, an
Application Access connection, a private-network node, or a set of provider-managed environment variables.

## When to use integrations

Use integrations when:

- Wodby needs to connect to an external account or service on your behalf
- you want to reuse the same credentials or connection across multiple apps or projects
- you want provider-backed environment variables instead of repeating raw values manually

In the dashboard, the integration creation form has an `Owner` selector. Choose `Organization <organization>` for an organization-owned integration or `Project <project>` for a project-owned integration. Use the integration's `Sharing` page later when other projects need `Read/Use` or `Modify/Delete` access. Eligible canonical OAuth integrations can also be [shared with another Wodby organization](organization-sharing.md) through an owner-approved invitation.

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
- [Application Access providers](../providers/access.md) for identity-protected or private-network HTTP access
- [VPN providers](../providers/vpn.md) for persistent service-managed private-network nodes
- [Variable integrations](variable.md) for reusable provider-backed environment variables

The selected type determines where the integration can be used in the dashboard.

## Environment availability

An integration can have a primary [environment type](../apps/environment-types.md) and an availability policy:

- `Any environment type` allows the integration to be used by app environments and resources of every type.
- `Restricted` allows only the selected environment types.

The primary type is descriptive and must be included when a restricted policy is used. The same fixed type list is
used for clusters, managed databases, backup presets, and app environments, so policies do not depend on custom
organization-level environment records.

### Add kinds to an existing integration

When a provider supports more than one kind, you can open the integration's **Edit** page and select additional kinds.
Existing kinds stay selected and cannot be removed. Create another integration when you need a narrower set of kinds,
different credentials, or a different permission scope.

The dashboard submits the integration details, selected kinds, and changed credential fields as one update. If any part
is invalid, none of the changes are saved.

Most new kinds become available immediately. AWS, GCP, and Azure integrations also start a read-only permission test.
GCP and Azure OAuth integrations may first start a provider setup task; only the new kinds remain in **Activating**
state while that task runs. Existing kinds remain available. A failed activation is shown only on the affected new kind.

Permission findings do not undo the update or disable the integration. Review the task warnings before using a newly
added kind. Some resource-creation permissions cannot be proven without changing provider resources and are therefore
reported as unverifiable rather than treated as an update failure. For AWS, GCP, and Azure, you can rerun the permission
test from the integration's **Edit** page.

## Provider revisions and updates

Provider changes create new revisions. When an integration remains on the provider revision it was configured against,
it is marked **Outdated** if a newer revision is available. Compatible integrations can be updated explicitly from
their detail page; incompatible integrations remain pinned and show why a migration is required.

See [Integration provider updates](updates.md) for the update workflow and compatibility rules.

## Where integrations are used

Depending on the provider and type, integrations can be used for:

- Kubernetes cluster creation
- Managed database creation
- App service and stack integrations
- SMTP relay configuration
- External container registries
- Backup storage destinations
- CI/CD workflows
- Protected app access through Cloudflare or Tailscale
- Tailscale Node services that join a tailnet as persistent workloads

## Related pages

- [Provider vs integration](providers-vs-integrations.md)
- [Providers overview](../providers/index.md)
- [Integration types](types.md)
- [Integration provider updates](updates.md)
- [Share an OAuth integration with another organization](organization-sharing.md)
- [Variable integration](variable.md)
