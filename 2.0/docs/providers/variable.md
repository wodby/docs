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

If a built-in provider is missing, you can create your own variable provider from `Providers > New variable provider` and define the environment variable names yourself.

## Related pages

- [Integrations overview](../integrations/index.md)
- [Integration types](../integrations/types.md)
- [Variable integration](../integrations/variable.md)
- [Providers overview](index.md)
