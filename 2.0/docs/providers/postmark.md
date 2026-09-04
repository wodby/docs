# Postmark

Postmark exposes `smtp` and `variable` integration kinds in Wodby. Both kinds use the same Server API token, so select
SMTP, Variable, or both without entering the credential twice.

## Setup field

Open the Postmark server, select **API Tokens**, and copy a Server API token. Do not use an Account API token. The
sender signature or domain used by the application must be verified in Postmark, and SMTP access must be enabled for
the server when using the SMTP kind.

| Field | Required | Environment variable |
| --- | --- | --- |
| Server API token | Yes | `POSTMARK_SERVER_TOKEN` |

Wodby stores the token as a secret. The Variable kind injects it as `POSTMARK_SERVER_TOKEN`. For SMTP, Wodby uses the
same token as both username and password with `smtp.postmarkapp.com` on port `587` using STARTTLS. This preset targets
transactional email and Postmark's default transactional message stream.

See [Postmark SMTP sending](https://postmarkapp.com/developer/user-guide/send-email-with-smtp) and the
[Postmark API overview](https://postmarkapp.com/developer/api/overview).

## Usage

Attach the SMTP kind to an SMTP-capable service such as OpenSMTPD. Attach the Variable kind to an app service or stack
that consumes `POSTMARK_SERVER_TOKEN`.

## Related pages

- [SMTP providers](smtp.md)
- [Variable providers](variable.md)
- [Variable integrations](../integrations/variable.md)
