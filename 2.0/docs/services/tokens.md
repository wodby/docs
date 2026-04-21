# Service tokens

Service tokens are named text values defined by a service.

They can either:

- have a fixed value
- use a regular expression to generate a random secret value when the app is created or updated

Service tokens can be referenced from environment variables and other generated configuration.

See [app tokens](../apps/tokens.md) for the app-level token model and the list of built-in tokens.

Service tokens are defined under the [`tokens` section](template.md#tokens) in a service template.
