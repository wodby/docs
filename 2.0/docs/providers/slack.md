# Slack

Slack is available in Wodby as a `variable` provider. Use it when you want to inject a Slack token into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Token | Yes | `SLACK_TOKEN` |

## Usage

After you create a Slack integration and attach it to an app service or stack, Wodby injects `SLACK_TOKEN` into the container.
