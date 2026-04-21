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

### Variable-only built-in providers

- [Algolia](../providers/algolia.md)
- [Anthropic](../providers/anthropic.md)
- [Auth0](../providers/auth0.md)
- [Cloudflare](../providers/cloudflare.md)
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
4. Wodby injects the provider's environment variables into the container.

## Built-in vs custom variable providers

Wodby ships a growing set of built-in variable providers such as Sentry, OpenAI, Stripe, Algolia, and others.

If a provider is missing, you can create your own variable provider from `Providers > New variable provider` and define the environment variable names yourself.

## Related pages

- [Integration types](types.md)
- [Providers overview](../providers/index.md)
- [Provider vs integration](providers-vs-integrations.md)
