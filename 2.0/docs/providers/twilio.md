# Twilio

Twilio is available in Wodby as a `variable` provider. Use it when you want to inject Twilio credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Account SID | Yes | `TWILIO_ACCOUNT_SID` |
| Auth Token | Yes | `TWILIO_AUTH_TOKEN` |

## Usage

After you create a Twilio integration and attach it to an app service or stack, Wodby injects the variables above into the container.
