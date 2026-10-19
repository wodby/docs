# Google Tag Manager

Google Tag Manager is available in Wodby as a `variable` provider. Use it to inject a web container ID into app
services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Container ID | Yes | `GOOGLE_TAG_MANAGER_CONTAINER_ID` |

The container ID must start with `GTM-` and contain uppercase letters or numbers after the prefix.

## Usage

After you create a Google Tag Manager integration and attach it to an app service or stack, Wodby injects
`GOOGLE_TAG_MANAGER_CONTAINER_ID` into the container.
