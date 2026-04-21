# Algolia

Algolia is available in Wodby as a `variable` provider. Use it when you want to manage Algolia credentials once and expose them to app services or stacks through integrations.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Application ID | Yes | `ALGOLIA_APP_ID` |
| API Key | Yes | `ALGOLIA_API_KEY` |

## Usage

After you create an Algolia integration and attach it to an app service or stack, Wodby injects the variables above into the container.
