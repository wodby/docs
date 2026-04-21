# Telegram

Telegram is available in Wodby as a `variable` provider. Use it when you want to inject a Telegram bot token into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Telegram Bot Token | Yes | `TELEGRAM_BOT_TOKEN` |

## Usage

After you create a Telegram integration and attach it to an app service or stack, Wodby injects `TELEGRAM_BOT_TOKEN` into the container.
