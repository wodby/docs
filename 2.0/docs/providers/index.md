# Providers

Providers are Wodby's definitions for supported third-party services. A provider defines:

- which [integration types](../integrations/types.md) it supports
- which fields or auth methods are required
- which environment variables it exposes, if it is a variable provider
- any provider-specific setup flow such as OAuth or scope selection

When you create a new integration, you first choose the provider and then fill in the fields required by that provider.

If you are choosing by task rather than by vendor, start with [Integration types](../integrations/types.md) and then jump to the matching provider group from there.

## How provider pages are organized

In the documentation navigation, providers are grouped by the integration types they support, such as Kubernetes, databases, storage, Git, CI, registry, SMTP, and VPN.

Each provider group starts with its own `Overview` page that explains what that group is for before listing individual providers.

Variable providers have their own group because they are usually used to inject reusable environment variables rather than to create infrastructure resources.

Some providers support more than one type. Those providers can appear in more than one navigation group.

## Built-in providers

Most providers shown in the dashboard are built in and maintained by Wodby. Their setup details are documented in the `Providers` section of this documentation.

## Custom variable providers

If you only need to inject environment variables and there is no built-in provider for that service, you can create your own variable provider from `Providers > New variable provider` in the dashboard.

Custom variable providers are useful when:

- you need a provider that Wodby does not ship yet
- you want to standardize a set of environment variables across multiple apps
- you want to manage service credentials centrally instead of repeating them in each app

## Related pages

- [Integrations overview](../integrations/index.md)
- [Integration types](../integrations/types.md)
- [Variable integration](../integrations/variable.md)
