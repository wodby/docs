# Variable providers

Variable providers are providers whose integrations expose the `variable` type. Use this group when the main result you want is a reusable set of environment variables rather than a cloud resource created by Wodby.

Machine name: `variable`

Use a variable provider when:

- the same third-party credentials are reused across multiple apps or environments
- you want provider-backed environment variables instead of repeating raw values manually
- you want a provider page to define the expected fields and resulting environment variables

## Where it is used in Wodby

Variable provider integrations are typically attached to:

- app services that need provider-backed environment variables
- stacks that should pass shared variables into every app instance created from that stack
- reusable project-level workflows where the same credentials are needed in multiple places

## Providers in this group

### Multi-type providers with variable support

- [Amazon Web Services](aws.md#variables)

### Variable-focused providers

- [Algolia](algolia.md)
- [Anthropic](anthropic.md)
- [Auth0](auth0.md)
- [Cloudflare](cloudflare.md)
- [Discord](discord.md)
- [Gemini](gemini.md)
- [Intercom](intercom.md)
- [Mailchimp](mailchimp.md)
- [New Relic](newrelic.md)
- [OpenAI](openai.md)
- [Pusher](pusher.md)
- [Sentry](sentry.md)
- [Slack](slack.md)
- [Stripe](stripe.md)
- [Telegram](telegram.md)
- [Twilio](twilio.md)

## Custom variable providers

If a built-in provider is missing, you can create your own variable provider in the dashboard. Use `Quick create` for
a small provider, `From manifest` for a local `provider.yml`, or `Import from Git` to track one or several versioned
providers in a repository.

Custom provider names are scoped to the organization, so their full machine name uses
`<organization>/<provider-name>`. Git-backed providers support manual updates and configurable branch or semantic-tag
auto updates. Every custom provider page also exposes its current manifest, task history, and project sharing settings.

See [Custom variable providers](custom-variable-providers.md) for the manifest format, repository layout, update rules,
and complete dashboard workflow. The standard
[environment-variable naming and reserved-name rules](../apps/environment-variables.md#names-and-reserved-variables)
apply to all custom mappings.

Variables exposed by variable providers are injected into runtime containers only. They are not passed to Docker image
builds. Use build-scoped app-service environment variables or service settings for Dockerfile build arguments.

### Matching service requirements

A service can declare the exact environment variables it consumes under
[`integrations[].variables`](../services/template.md#integrations). This lets the same service work with any built-in or
custom variable provider whose selected kind exposes the required shape.

For a custom provider to match:

- every required variable name must be exposed by the same provider kind
- a secret requirement must map to a secret provider field, and a non-secret requirement must map to a non-secret
  field
- a required service variable cannot map to an optional provider field
- an optional service variable can map to either a required or optional provider field

The provider can expose additional variables. They are not injected through a service integration that declares an
explicit variable contract. The service does not need to name a specific provider, so each organization can create a
provider with its own title and credentials while keeping the same environment-variable interface.

## Related pages

- [Integrations overview](../integrations/index.md)
- [Integration types](../integrations/types.md)
- [Variable integration](../integrations/variable.md)
- [Custom variable providers](custom-variable-providers.md)
- [Environment variables](../apps/environment-variables.md)
- [Providers overview](index.md)
