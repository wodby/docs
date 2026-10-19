# PostHog

PostHog is available in Wodby as a `variable` provider. Use it to inject a project token and optional PostHog instance
address into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Project token | Yes | `POSTHOG_API_KEY` |
| Instance address | No | `POSTHOG_HOST` |

Set **Instance address** when the application should use a specific PostHog Cloud region or a self-hosted PostHog
instance.

## Usage

After you create a PostHog integration and attach it to an app service or stack, Wodby injects `POSTHOG_API_KEY` and
the configured optional `POSTHOG_HOST` into the container.
