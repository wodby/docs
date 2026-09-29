# OpenCode Zen

OpenCode Zen is available in Wodby as a `variable` provider. Use it when you want to inject an
[OpenCode Zen](https://opencode.ai/docs/zen/) API key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `OPENCODE_API_KEY` |

Create the key in OpenCode Zen after adding billing details to your Zen workspace.

## Usage

After you create an OpenCode Zen integration and attach it to an app service or stack, Wodby injects
`OPENCODE_API_KEY` into the container. OpenCode reads this variable for Zen models, so `opencode` running in that
container can use the key without further setup.
