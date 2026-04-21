# Mailchimp

Mailchimp is available in Wodby as a `variable` provider. Use it when you want to inject Mailchimp API credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `MAILCHIMP_API_KEY` |
| Server Prefix | No | `MAILCHIMP_SERVER_PREFIX` |

## Usage

After you create a Mailchimp integration and attach it to an app service or stack, Wodby injects the variables above into the container.
