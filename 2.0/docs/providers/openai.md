# OpenAI

OpenAI is available in Wodby as a `variable` provider. Use it when you want to inject an OpenAI API key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API Key | Yes | `OPENAI_API_KEY` |

## Usage

After you create an OpenAI integration and attach it to an app service or stack, Wodby injects `OPENAI_API_KEY` into the container.
