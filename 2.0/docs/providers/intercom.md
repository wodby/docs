# Intercom

Intercom is available in Wodby as a `variable` provider. Use it when you want to inject Intercom credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| App ID | Yes | `INTERCOM_APP_ID` |
| Identity Verification Secret | No | `INTERCOM_IDENTITY_VERIFICATION_SECRET` |

## Usage

After you create an Intercom integration and attach it to an app service or stack, Wodby injects the variables above into the container.
