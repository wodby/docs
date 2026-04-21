# Sentry

Sentry is available in Wodby as a `variable` provider. Use it when you want to inject your Sentry DSN into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| DSN | Yes | `SENTRY_DSN` |

## Usage

After you create a Sentry integration and attach it to an app service or stack, Wodby injects `SENTRY_DSN` into the container.
