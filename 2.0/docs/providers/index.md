# Providers

Providers are Wodby's definitions for supported third-party services. A provider defines:

- which [integration types](../integrations/types.md) it supports
- which fields or auth methods are required
- which environment variables it exposes, if it is a variable provider
- any provider-specific setup flow such as OAuth or scope selection

When you create a new integration, you first choose the provider and then fill in the fields required by that provider.

Provider changes are published as new revisions. New integrations use the current revision. Existing integrations can
be advanced by a compatible managed rollout or remain pinned until they are
[updated explicitly](../integrations/updates.md).

If you are choosing by task rather than by vendor, start with [Integration types](../integrations/types.md) and then jump to the matching provider group from there.

## Custom variable providers

If you only need to inject environment variables and there is no built-in provider for that service, you can create
your own variable provider from the dashboard. Providers can be created interactively, from a local manifest, or from
a Git repository containing one or several provider manifests.

The new variable provider form has an `Owner` selector. Choose `Organization <organization>` for an organization-owned provider or `Project <project>` for a project-owned provider.

Custom variable providers are useful when:

- you need a provider that Wodby does not ship yet
- you want to standardize a set of environment variables across multiple apps
- you want to manage service credentials centrally instead of repeating them in each app

Custom provider machine names are namespaced by organization. Git-backed providers can be updated manually or from
matching branch and semantic-version tag events. See [Custom variable providers](custom-variable-providers.md) for the
manifest, Git layout, update, task, and sharing workflows.

## Related pages

- [Integrations overview](../integrations/index.md)
- [Integration types](../integrations/types.md)
- [Variable integration](../integrations/variable.md)
- [Integration provider updates](../integrations/updates.md)
- [Custom variable providers](custom-variable-providers.md)
