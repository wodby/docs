# Resend

Resend exposes `smtp` and `variable` integration kinds in Wodby. Both kinds use the same API key, so select SMTP,
Variable, or both without entering the credential twice.

## Setup field

Create a Resend API key and verify the domain used by the application's sender address.

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `RESEND_API_KEY` |

Wodby stores the key as a secret. The Variable kind injects it as `RESEND_API_KEY`. For SMTP, Wodby uses the fixed
username `resend`, the API key as the password, and `smtp.resend.com` on port `587` using STARTTLS.

See [Resend SMTP sending](https://resend.com/docs/send-with-smtp) and the
[Resend API introduction](https://resend.com/docs/api-reference/introduction).

## Usage

Attach the SMTP kind to an SMTP-capable service such as OpenSMTPD. Attach the Variable kind to an app service or stack
that consumes `RESEND_API_KEY`.

## Related pages

- [SMTP providers](smtp.md)
- [Variable providers](variable.md)
- [Variable integrations](../integrations/variable.md)
