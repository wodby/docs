# Discord

Discord is available in Wodby as a `variable` provider. Use it when you want to inject a Discord bot token into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Discord Bot Token | Yes | `DISCORD_BOT_TOKEN` |

## Usage

After you create a Discord integration and attach it to an app service or stack, Wodby injects `DISCORD_BOT_TOKEN` into the container.
