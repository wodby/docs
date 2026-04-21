# Anthropic

Anthropic is available in Wodby as a `variable` provider. Use it when you want to inject an Anthropic API key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API Key | Yes | `ANTHROPIC_API_KEY` |

## Usage

After you create an Anthropic integration and attach it to an app service or stack, Wodby injects `ANTHROPIC_API_KEY` into the container.
