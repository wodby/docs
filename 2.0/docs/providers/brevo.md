# Brevo

Brevo exposes `smtp` and `variable` integration kinds in Wodby. Select SMTP to relay outbound mail, API Variable to
inject a Brevo API key into application containers, or both. Brevo SMTP keys and API keys are separate credentials.

## SMTP

Open **SMTP & API** in Brevo, select the SMTP tab, and copy the SMTP login and an SMTP key. Do not enter a Brevo API
key as the SMTP key.

| Field | Required | Relay variable |
| --- | --- | --- |
| Login | Yes | `RELAY_USER` |
| SMTP key | Yes | `RELAY_PASSWORD` |

Wodby supplies `smtp-relay.brevo.com` as the relay host. Attach the SMTP kind to an SMTP-capable service such as
OpenSMTPD.

See [Brevo SMTP relay integration](https://developers.brevo.com/docs/smtp-integration).

## API Variable

Create a key under the API keys tab in **SMTP & API**. Brevo shows the key only once, so copy it before closing the
dialog.

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `BREVO_API_KEY` |

Attach the Variable kind to an app service or stack that consumes `BREVO_API_KEY`. Wodby stores the value as a secret
and injects it only at runtime.

See [Brevo API key authentication](https://developers.brevo.com/docs/api-key-authentication).
