# OpenClaw

The Wodby OpenClaw catalog stack runs the OpenClaw gateway and its Control UI. The current composition is documented in
[`wodby/stack-openclaw`](https://github.com/wodby/stack-openclaw).

## Before you create the app

The stack requires Protected access with the Private network type for the entire app. Select a compatible
[Application Access integration](../../../providers/access.md) when you create the app. You cannot change these choices.
Application Access needs an active paid subscription. See [App access](../../../apps/access.md).

The gateway port (18789) is private and gets no public route.

## Gateway token

Clients of the gateway and the Control UI authenticate with the `gateway_token` token. Find it on the OpenClaw app
service's **Configuration > Tokens** tab. See [Tokens](../../../apps/tokens.md).

The Control UI can be opened from the environment's primary host, the service's address inside the cluster, and the
local address.

## Turn on agents and channels

Add these environment variables to the OpenClaw app service, then deploy it. See
[Environment variables](../../../apps/environment-variables.md).

| Variable | Effect |
| --- | --- |
| `OPENAI_API_KEY` | adds the agents `openai` and `openai-code` |
| `ANTHROPIC_API_KEY` | adds the agent `claude` |
| `GEMINI_API_KEY` or `GOOGLE_API_KEY` | adds the agent `gemini` |
| `TELEGRAM_BOT_TOKEN` | enables the Telegram channel |
| `DISCORD_BOT_TOKEN` | enables the Discord channel |

The first provider present, in the order of this table, is the default agent. Without a provider key, the configuration
has no agent list.

Optional variables set agent models and workspaces: `OPENCLAW_OPENAI_MODEL`, `OPENCLAW_OPENAI_CODE_MODEL`,
`OPENCLAW_CLAUDE_MODEL`, `OPENCLAW_GEMINI_MODEL`, `OPENCLAW_AGENTS_WORKSPACE`, and `OPENCLAW_<AGENT>_WORKSPACE`.

## Change configuration

OpenClaw writes its configuration file from the app service's environment variables on every start. Do not edit the
file. To change anything the variables do not cover, edit the **OpenClaw config** template on the app service's
**Configuration > Configs** tab, then deploy.

## Data

The **Data** volume (1 GB by default) holds the OpenClaw state directory. Agent workspaces default to directories that
are not on this volume. Point the workspace variables at a path on the volume to keep them.

## Check the result

In a [web terminal](../../../apps/web-terminal.md), run `openclaw health --json`. It reports `"ok": true` when the
gateway is up.
