# Variable integration

Variable integrations let you manage third-party credentials and configuration as reusable provider-backed environment variables.

They have the same end result as adding environment variables directly to an app service, but they are easier to reuse and maintain because the values are stored once in an integration and then attached where needed.

Machine name: `variable`

Typical use cases include:

- API keys for third-party services
- DSNs and license keys
- shared credentials reused across multiple apps
- stack-level defaults applied to all app instances created from that stack

Variable integrations are a good fit when:

- the same third-party credentials are reused in more than one app or environment
- you want to centralize sensitive values instead of repeating them in raw env vars
- you want a provider page to define the expected fields and resulting environment variables

Use plain app-service environment variables instead when a value is one-off and not worth centralizing.

## Where it is used in Wodby

Variable integrations are typically attached to:

- app services that need provider-backed environment variables
- stacks that should pass shared variables into every app instance created from that stack
- reusable project-level workflows where the same credentials are needed in multiple places

## Supported providers

### Multi-type providers

- [Amazon Web Services variables](../providers/aws.md#variables)
- [Cloudflare Turnstile](../providers/cloudflare.md#turnstile)

### Variable-only built-in providers

- [Algolia](../providers/algolia.md)
- [Anthropic](../providers/anthropic.md)
- [Auth0](../providers/auth0.md)
- [Discord](../providers/discord.md)
- [Gemini](../providers/gemini.md)
- [Intercom](../providers/intercom.md)
- [Mailchimp](../providers/mailchimp.md)
- [New Relic](../providers/newrelic.md)
- [OpenAI](../providers/openai.md)
- [Pusher](../providers/pusher.md)
- [Sentry](../providers/sentry.md)
- [Slack](../providers/slack.md)
- [Stripe](../providers/stripe.md)
- [Telegram](../providers/telegram.md)
- [Twilio](../providers/twilio.md)

## How it works

1. Create or choose a provider.
2. Create an integration from that provider and fill in its fields.
3. Attach the integration to an app service or stack.
4. Wodby injects the provider's environment variables into the container, using the service-defined output mapping
   when the service declares one.

Variable integration env vars are runtime-only. They are not passed to Docker image builds or exported as CI build
arguments. Use a build-scoped app-service environment variable or service setting when a Dockerfile needs a value
during build.

## Service-owned environment mappings

By default, a variable integration exports matched provider variables under the names defined by the provider. A
service author can instead declare the provider variables the service needs and map them to application-facing runtime
names. The mapping can also add literal values owned by the service, such as a driver or mode name.

With a service-owned mapping:

- the integration still matches a provider by the declared variable contract rather than a hard-coded provider name
- only mapped outputs are injected, so extra provider variables are not exposed to the container
- secret inputs must remain secret outputs
- an exact mapping for a missing optional input is omitted
- services without a mapping retain the default direct-export behavior

See [`integrations` in the service template reference](../services/template.md#integrations) for the manifest syntax,
validation rules, and a complete example.

## Built-in vs custom variable providers

Wodby ships a growing set of built-in variable providers such as Sentry, OpenAI, Stripe, Algolia, and others.

If a provider is missing, you can [create a custom variable provider](../providers/custom-variable-providers.md)
interactively, from a local manifest, or from a Git repository containing one or several provider manifests. The
standard
[environment-variable naming and reserved-name rules](../apps/environment-variables.md#names-and-reserved-variables)
apply to custom mappings.

Services can declare an exact variable contract instead of naming a particular provider. Wodby then accepts only
integrations whose selected provider kind supplies the required names, secret classifications, and optionality. This is
useful for reusable services that need credentials such as `BILLING_API_TOKEN` but should not depend on one globally
defined provider. See the [`integrations[].variables` service template reference](../services/template.md#integrations)
and [matching custom provider requirements](../providers/variable.md#matching-service-requirements).

## Related pages

- [Integration types](types.md)
- [Providers overview](../providers/index.md)
- [Provider vs integration](providers-vs-integrations.md)
- [Environment variables](../apps/environment-variables.md)
