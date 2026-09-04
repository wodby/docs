# Intercom

Intercom is available in Wodby as a `variable` provider. Use it when you want to inject Intercom credentials into app services or stacks through an integration.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| App ID | Yes | `INTERCOM_APP_ID` |
| Identity Verification Secret | No | `INTERCOM_IDENTITY_VERIFICATION_SECRET` |
| Access Token | No | `INTERCOM_ACCESS_TOKEN` |

Use the identity verification secret when the application signs Messenger user identities. Add the access token only
when a private application needs to call the Intercom API for its own workspace; Wodby stores both optional values as
secrets.

See [Intercom authentication](https://developers.intercom.com/docs/build-an-integration/learn-more/authentication) and
[Messenger identity verification](https://developers.intercom.com/installing-intercom/web/identity-verification).

## Usage

After you create an Intercom integration and attach it to an app service or stack, Wodby injects the variables above into the container.
