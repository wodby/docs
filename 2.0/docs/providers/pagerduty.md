# PagerDuty

PagerDuty is available in Wodby as a `variable` provider. Use it to inject an Events API v2 routing key into app
services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Events API v2 Routing Key | Yes | `PAGERDUTY_ROUTING_KEY` |

Wodby stores the routing key as a secret. Use the integration key for the PagerDuty service and Events API v2
integration that should receive events.

## Usage

After you create a PagerDuty integration and attach it to an app service or stack, Wodby injects
`PAGERDUTY_ROUTING_KEY` into the container.
