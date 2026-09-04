# SendGrid

Twilio SendGrid exposes `smtp` and `variable` integration kinds in Wodby. Both kinds use the same API key, so select
SMTP, Variable, or both without entering the credential twice.

## Setup field

Create a SendGrid API key with only the permissions the application needs. SMTP delivery requires Mail Send access.
Complete sender authentication for the address or domain used by the application.

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `SENDGRID_API_KEY` |

Wodby stores the key as a secret. The Variable kind injects it as `SENDGRID_API_KEY`. For SMTP, Wodby uses the fixed
username `apikey`, the API key as the password, and `smtp.sendgrid.net` on port `587` using STARTTLS.

See [SendGrid SMTP integration](https://www.twilio.com/docs/sendgrid/for-developers/sending-email/integrating-with-the-smtp-api)
and [SendGrid API authentication](https://www.twilio.com/docs/sendgrid/api-reference/how-to-use-the-sendgrid-v3-api/authentication).

## Usage

Attach the SMTP kind to an SMTP-capable service such as OpenSMTPD. Attach the Variable kind to an app service or stack
that consumes `SENDGRID_API_KEY`.

## Related pages

- [SMTP providers](smtp.md)
- [Variable providers](variable.md)
- [Variable integrations](../integrations/variable.md)
