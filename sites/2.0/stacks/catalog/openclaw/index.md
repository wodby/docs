Source: https://wodby.com/docs/2.0/stacks/catalog/openclaw/

# OpenClaw stack guide

The Wodby OpenClaw catalog stack runs the OpenClaw gateway and its Control UI. The current composition is documented in
[`wodby/stack-openclaw`](https://github.com/wodby/stack-openclaw).

## Before you create the app

The stack requires Protected access with the Private network type for the entire app. Select a compatible
[Private App Access integration](https://wodby.com/docs/2.0/providers/access/) when you create the app. You cannot change these choices.
Private App Access needs an active paid subscription. See [Private App Access](https://wodby.com/docs/2.0/apps/access/).

Wodby publishes no public route for the gateway. You reach it through the Access provider. Services in the same app
environment reach it directly on port 18789.

## Open the Control UI

Wodby sets up the private address after the first successful deployment.

1. Connect your device to the provider's private network: join the tailnet for [Tailscale](https://wodby.com/docs/2.0/providers/tailscale/),
   or use the Cloudflare One Client for [Cloudflare](https://wodby.com/docs/2.0/providers/cloudflare/#private-network-access).
2. Open the address listed under **Apps > [App] > [Environment] > Endpoints > Domains**.
3. Find the `gateway_token` token on the OpenClaw app service's **Configuration > Tokens** tab, and paste it into
   **Gateway secret**. See [Tokens](https://wodby.com/docs/2.0/apps/tokens/).
4. Approve the browser. A new browser waits for a one-time approval. In a
   [web terminal](https://wodby.com/docs/2.0/apps/web-terminal/), run these commands, and the page connects by itself:

   ```
   openclaw devices list
   openclaw devices approve <requestId>

   ```

Each browser profile needs its own approval. A private window asks again after it closes.

Other clients of the gateway authenticate with the same token.

## Turn on agents and channels

Add these environment variables to the OpenClaw app service, then deploy it. See
[Environment variables](https://wodby.com/docs/2.0/apps/environment-variables/).

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

In a [web terminal](https://wodby.com/docs/2.0/apps/web-terminal/), run `openclaw health --json`. It reports `"ok": true` when the
gateway is up.
