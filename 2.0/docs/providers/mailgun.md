# Mailgun

Mailgun exposes `smtp` and `variable` integration kinds in Wodby. Select SMTP to relay outbound mail, Variable to
inject Mailgun API credentials into application containers, or both. Mailgun SMTP credentials and API sending keys are
separate credentials.

## SMTP

SMTP credentials belong to a specific Mailgun sending domain. In Mailgun, open **Sending > Domain Settings**, select
the domain, and copy or create credentials under **SMTP Credentials**.

| Field | Required | Relay variable |
| --- | --- | --- |
| SMTP server | Yes | `RELAY_HOST` |
| SMTP login | Yes | `RELAY_USER` |
| SMTP password | Yes | `RELAY_PASSWORD` |

Choose `smtp.mailgun.org` for a US-region domain or `smtp.eu.mailgun.org` for an EU-region domain. Use the complete
SMTP login shown for the domain, including its domain part. Wodby uses STARTTLS on port `587`.

See [Mailgun SMTP sending](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/send-smtp).

## API Variable

For application API access, create a Domain Sending Key for the verified domain whenever the application only needs to
send messages. It grants less access than a primary account API key.

| Field | Required | Environment variable |
| --- | --- | --- |
| API key | Yes | `MAILGUN_API_KEY` |
| Sending domain | Yes | `MAILGUN_DOMAIN` |

Wodby stores the API key as a secret. The sending domain is the verified Mailgun domain used in API request paths. For
EU-region domains, the application must use Mailgun's EU API base URL; Wodby injects credentials but does not choose an
API endpoint for the application.

See [Mailgun API key management](https://documentation.mailgun.com/docs/mailgun/user-manual/api-key-mgmt/rbac-mgmt)
and [HTTP sending](https://documentation.mailgun.com/docs/mailgun/user-manual/sending-messages/send-http).

## Usage

Attach the SMTP kind to an SMTP-capable service such as OpenSMTPD. Attach the Variable kind to an app service or stack
that consumes `MAILGUN_API_KEY` and `MAILGUN_DOMAIN`. Selecting both kinds keeps the two credential sets separate.

## Related pages

- [SMTP providers](smtp.md)
- [Variable providers](variable.md)
- [Variable integrations](../integrations/variable.md)
