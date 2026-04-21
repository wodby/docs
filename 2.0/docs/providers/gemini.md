# Gemini

Gemini is available in Wodby as a `variable` provider. Use it when you want to inject a Gemini API key into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| API Key | Yes | `GEMINI_API_KEY` |

## Usage

After you create a Gemini integration and attach it to an app service or stack, Wodby injects `GEMINI_API_KEY` into the container.
