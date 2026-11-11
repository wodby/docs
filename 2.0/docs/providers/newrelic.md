---
description: Use the New Relic provider in Wodby to store your New Relic license key and inject it into app services and stacks as NEWRELIC_LICENSE.
---

# New Relic

New Relic is available in Wodby as a `variable` provider. Use it when you want to inject your New Relic license key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| License | Yes | `NEWRELIC_LICENSE` |

## Usage

After you create a New Relic integration and attach it to an app service or stack, Wodby injects `NEWRELIC_LICENSE` into the container.
