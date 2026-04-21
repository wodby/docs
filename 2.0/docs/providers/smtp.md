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
| [Amazon Web Services](aws.md#ses) | SES |
| [Brevo](brevo.md) | Brevo SMTP |

## Related pages

- [Integration types](../integrations/types.md)
- [Mail services](../services/smtp.md)
- [Providers overview](index.md)
