Source: https://wodby.com/docs/2.0/providers/newrelic/

# New Relic provider

New Relic is available in Wodby as a `variable` provider. Use it when you want to inject your New Relic license key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| License | Yes | `NEWRELIC_LICENSE` |

## Usage

After you create a New Relic integration and attach it to an app service or stack, Wodby injects `NEWRELIC_LICENSE` into the container.
