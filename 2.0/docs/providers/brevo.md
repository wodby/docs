# Brevo

Brevo is available in Wodby as an `smtp` provider. Use it when you want an SMTP-capable service, such as OpenSMTPD, to relay outbound email through Brevo.

## Setup fields

| Field | Required | Environment variable |
| --- | --- | --- |
| Login | Yes | `RELAY_USER` |
| SMTP key | Yes | `RELAY_PASSWORD` |

## Usage

After you create a Brevo integration, attach it to the mail service that should use Brevo as its outbound relay.
