# Datadog

Datadog is available in Wodby as a `variable` provider. Use it to inject a Datadog API key and optional site into app
services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `DD_API_KEY` |
| Site | No | `DD_SITE` |

To change the site of an existing integration, enter the API key again. Your application sends the key to that site, so
a new site can't reuse it without you entering it.

Wodby stores the API key as a secret. Set **Site** when the application needs a Datadog site such as `datadoghq.com`
or `datadoghq.eu`.

## Usage

After you create a Datadog integration and attach it to an app service or stack, Wodby injects `DD_API_KEY` and the
configured optional `DD_SITE` into the container.
