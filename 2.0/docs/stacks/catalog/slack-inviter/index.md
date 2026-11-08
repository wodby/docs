# Slack Inviter

The Wodby Slack Inviter catalog stack runs a public invitation page for a Slack community on the Node.js service. The
source is the [`wodby/slack-inviter`](https://github.com/wodby/slack-inviter) project. The current composition is
documented in [`wodby/stack-slack-inviter`](https://github.com/wodby/stack-slack-inviter).

!!! warning
    This stack needs an existing Slackin-compatible legacy administrator API token. Slack no longer issues these tokens.
    Ordinary Slack app and bot tokens do not work. Use the stack only to migrate a Slackin installation whose token is
    still active.

## Before you create the app

- Use the Slack Inviter repository as the build source, or connect your own compatible repository. See
  [Application Builds](../../../apps/builds.md).
- Set **Slack workspace** to the workspace subdomain only, for example `community` for `community.slack.com`. It is
  required.
- Attach a Slack integration to the **Slack legacy API token** slot. It is required and supplies `SLACK_TOKEN`. See
  [Slack](../../../providers/slack.md).
- Optionally attach a Cloudflare integration with the Turnstile kind to the **Cloudflare Turnstile** slot. It supplies
  `TURNSTILE_SITE_KEY` and `TURNSTILE_SECRET_KEY`. See [Cloudflare](../../../providers/cloudflare.md#turnstile).

The application refuses to start without the workspace and the token. The container log names the variable at fault. Put
the token and keys in integrations, not in the repository or a `.env` file.

## Page content and limits

Set these on the app service's **Configuration > Settings** tab: **Community name**, **Community headline**,
**Community description**, **Community website URL**, **Community logo URL**, **Support URL**, **Privacy URL**, and
**Social image URL**. The logo and social image accept an HTTPS URL or a path starting with `/`.

The rate limits are **Maximum invites per IP** (10 per 3600 seconds by default) and **Maximum invites per email** (3 per
86400 seconds by default). Change the windows with **IP rate-limit window in seconds** and **Email rate-limit window in
seconds**.

The rate limiter keeps its counters in the memory of one process. Replicas do not share them, and a restart resets
them.

## Health check

`/healthz` answers the health check.
