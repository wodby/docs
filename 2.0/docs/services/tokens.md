# Service tokens

Service tokens are named text values defined by a service.

They can either:

- have a fixed value
- use a regular expression to generate a random secret value when the app is created or updated

Service tokens can be referenced from environment variables and other generated configuration.

Built-in runtime tokens are documented in [app tokens](../apps/tokens.md), because they resolve in app-service
context and can be used from service, stack, and app configuration.

Service tokens are defined under the [`tokens` section](template.md#tokens) in a service template.
