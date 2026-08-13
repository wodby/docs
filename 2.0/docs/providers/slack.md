# Slack

Slack is available in Wodby as a `variable` provider. Its current built-in kind stores the legacy administrator API
token required by Slack Inviter.

!!! warning "Existing legacy token required"

    Slack Inviter uses Slack's undocumented legacy workspace invitation endpoint. It requires a working
    Slackin-compatible legacy administrator API token. Slack no longer issues these tokens, and an ordinary Slack app
    or bot token will not work. Create this integration only when migrating an existing Slackin installation whose
    legacy token remains active.

    Slack's supported [`admin.users.invite`](https://docs.slack.dev/reference/methods/admin.users.invite/) API is
    available only to Enterprise Grid organizations and is not the API used by the current Slack Inviter service.

## Setup fields

| Field            | Required | Environment variable |
| ---------------- | -------- | -------------------- |
| Legacy API token | Yes      | `SLACK_TOKEN`        |

## Usage

After you create a Slack integration and attach it to the Slack Inviter service, Wodby injects `SLACK_TOKEN` into the
container. The Slack workspace subdomain is configured separately through the service's **Slack workspace** setting.
