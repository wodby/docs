Source: https://wodby.com/docs/2.0/providers/variable/

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
- stacks that should pass shared variables into every app environment created from that stack
- reusable project-level workflows where the same credentials are needed in multiple places

## Providers in this group

### Multi-type providers with variable support

- [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#variables)
- [Brevo](https://wodby.com/docs/2.0/providers/brevo/#api-variable)
- [Cloudflare](https://wodby.com/docs/2.0/providers/cloudflare/#api)
- [Mailgun](https://wodby.com/docs/2.0/providers/mailgun/#api-variable)
- [Postmark](https://wodby.com/docs/2.0/providers/postmark/#setup-field)
- [Resend](https://wodby.com/docs/2.0/providers/resend/#setup-field)
- [SendGrid](https://wodby.com/docs/2.0/providers/sendgrid/#setup-field)

### Variable-focused providers

- [Algolia](https://wodby.com/docs/2.0/providers/algolia/)
- [Anthropic](https://wodby.com/docs/2.0/providers/anthropic/)
- [Auth0](https://wodby.com/docs/2.0/providers/auth0/)
- [Datadog](https://wodby.com/docs/2.0/providers/datadog/)
- [Discord](https://wodby.com/docs/2.0/providers/discord/)
- [Gemini](https://wodby.com/docs/2.0/providers/gemini/)
- [Google Analytics](https://wodby.com/docs/2.0/providers/google-analytics/)
- [Google Tag Manager](https://wodby.com/docs/2.0/providers/google-tag-manager/)
- [Intercom](https://wodby.com/docs/2.0/providers/intercom/)
- [LaunchDarkly](https://wodby.com/docs/2.0/providers/launchdarkly/)
- [Mailchimp](https://wodby.com/docs/2.0/providers/mailchimp/)
- [New Relic](https://wodby.com/docs/2.0/providers/newrelic/)
- [OpenAI](https://wodby.com/docs/2.0/providers/openai/)
- [OpenCode Zen](https://wodby.com/docs/2.0/providers/opencode/)
- [PagerDuty](https://wodby.com/docs/2.0/providers/pagerduty/)
- [PostHog](https://wodby.com/docs/2.0/providers/posthog/)
- [Pusher](https://wodby.com/docs/2.0/providers/pusher/)
- [Sentry](https://wodby.com/docs/2.0/providers/sentry/)
- [Slack](https://wodby.com/docs/2.0/providers/slack/)
- [Stripe](https://wodby.com/docs/2.0/providers/stripe/)
- [Telegram](https://wodby.com/docs/2.0/providers/telegram/)
- [Twilio](https://wodby.com/docs/2.0/providers/twilio/)

## Custom variable providers

If a built-in provider is missing, you can create your own variable provider in the dashboard. Use
`New variable provider` for a small provider, `New from manifest` for a local `provider.yml`, or `Import from git` to
track one or several provider manifests in a repository.

Custom provider names are scoped to the organization, so their full machine name uses
`<organization>/<provider-name>`. Git-backed providers support manual updates and configurable branch or semantic-tag
auto updates. Every custom provider page also exposes its current manifest, task history, and project sharing settings.

See [Custom variable providers](https://wodby.com/docs/2.0/providers/custom-variable-providers/) for the manifest format, repository layout, update rules,
and complete dashboard workflow. The standard
[environment-variable naming and reserved-name rules](https://wodby.com/docs/2.0/apps/environment-variables/#names-and-reserved-variables)
apply to all service-defined integration environment variables.

Variables exposed by variable providers are injected into runtime containers only. By default they retain the names
defined by the provider; [service-defined integration environment variables](https://wodby.com/docs/2.0/services/template/#integrations)
can expose only selected variables under application-facing names. They are not passed to Docker image builds. Use build-scoped
app-service environment variables or service settings for Dockerfile build arguments.

### Matching service requirements

A service can declare the exact environment variables it consumes under
[`integrations[].variables`](https://wodby.com/docs/2.0/services/template/#integrations). This lets the same service work with any built-in or
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

- [Integrations overview](https://wodby.com/docs/2.0/integrations/)
- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Variable integration](https://wodby.com/docs/2.0/integrations/variable/)
- [Custom variable providers](https://wodby.com/docs/2.0/providers/custom-variable-providers/)
- [Environment variables](https://wodby.com/docs/2.0/apps/environment-variables/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
