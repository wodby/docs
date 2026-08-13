# Slack

Slack is available in Wodby as a `variable` provider. It stores a Slack API token and exposes it only to services that
request the Slack integration. Choose the [token type](https://docs.slack.dev/authentication/tokens/) and OAuth scopes
required by the consuming application.

## Setup fields

| Field     | Required | Environment variable |
| --------- | -------- | -------------------- |
| API token | Yes      | `SLACK_TOKEN`        |

## Usage

After you create a Slack integration and attach it to a compatible service, Wodby injects the secret as `SLACK_TOKEN`
into that service's containers. Refer to the consuming application's documentation for its required token type and
scopes.
