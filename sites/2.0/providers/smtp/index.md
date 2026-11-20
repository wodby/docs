Source: https://wodby.com/docs/2.0/providers/smtp/

# SMTP providers

SMTP providers are third-party services whose integrations expose the `smtp` type. Use this group when you want an outbound email provider connected to Wodby services that need to send mail.

Machine name: `smtp`

Use an SMTP provider when:

- an app or mail service needs a relay for outbound email
- you want SMTP credentials to be reusable instead of configured manually per service
- you want provider-managed mail delivery outside the application itself

## Where it is used in Wodby

SMTP provider integrations are used for:

- SMTP-capable app services such as OpenSMTPD
- stacks or services that need a provider-backed mail relay
- reusable outbound mail configuration shared across apps

## Supported providers

| Provider | Mail product |
| --- | --- |
| [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#ses) | SES |
| [Brevo](https://wodby.com/docs/2.0/providers/brevo/) | Brevo SMTP |
| [Cloudflare](https://wodby.com/docs/2.0/providers/cloudflare/#smtp) | Email Service (beta) |
| [Mailgun](https://wodby.com/docs/2.0/providers/mailgun/) | Mailgun SMTP |
| [Postmark](https://wodby.com/docs/2.0/providers/postmark/) | Postmark transactional SMTP |
| [Resend](https://wodby.com/docs/2.0/providers/resend/) | Resend SMTP |
| [SendGrid](https://wodby.com/docs/2.0/providers/sendgrid/) | Twilio SendGrid SMTP |
| [Custom SMTP](https://wodby.com/docs/2.0/providers/custom-smtp/) | Any standards-compatible SMTP relay |

For AWS SES, enter a raw IAM access key pair. Wodby derives the region-specific SMTP password at runtime. Existing AWS
integrations that store legacy SES SMTP credentials remain supported; see [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#ses).

Use [Custom SMTP](https://wodby.com/docs/2.0/providers/custom-smtp/) when the relay is not represented by a provider-specific integration. It supports
mandatory STARTTLS and implicit TLS and can be attached directly to OpenSMTPD.

Brevo and Mailgun use SMTP credentials that are separate from their API credentials. Postmark, Resend, SendGrid, and
Cloudflare reuse an API token or key for SMTP authentication. Cloudflare is the exception to the normal relay defaults:
it uses implicit TLS on port `465`; the other built-in presets use STARTTLS on port `587` unless their provider page
states otherwise.

## Related pages

- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Mail relay services](https://wodby.com/docs/2.0/services/types/#mail-relay-services)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
