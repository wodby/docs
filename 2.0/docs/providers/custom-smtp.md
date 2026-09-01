# Custom SMTP

Custom SMTP connects any standards-compatible SMTP relay to Wodby without requiring a provider-specific integration.
Use it with services such as OpenSMTPD when your mail provider is not listed separately in the provider catalog.

## Setup fields

| Field | Required | Description |
| --- | --- | --- |
| Relay host | Yes | Relay hostname without a URL scheme or port, for example `smtp.example.com`. |
| Relay port | No | Relay TCP port. The default is `587`. |
| Relay security | No | `smtp+tls` for mandatory STARTTLS or `smtps` for implicit TLS. The default is `smtp+tls`. |
| Username | No | Relay username. Omit it for relays that authenticate by network identity. |
| Password | No | Relay password, stored as a secret. |

Custom SMTP intentionally supports encrypted relay modes only. Use `smtp+tls` for the usual submission service on port
`587`. Select `smtps` when the provider requires implicit TLS, commonly on port `465`.

## Attach to OpenSMTPD

1. Open the project or organization **Integrations** page and create a **Custom SMTP** integration.
2. Enter the relay host and any credentials required by the provider. Set the port and security mode when the provider
   does not use the defaults.
3. Open the app environment containing OpenSMTPD and select its OpenSMTPD service.
4. Attach the integration to **Third-party SMTP server for Relay**.
5. Redeploy the app environment so OpenSMTPD receives the relay configuration.

Applications continue to send mail to OpenSMTPD on its internal port `25`. OpenSMTPD then forwards the message to the
configured upstream relay.

The relay host is mandatory. Wodby rejects an incomplete Custom SMTP configuration rather than allowing OpenSMTPD to
attempt direct delivery.

See [OpenSMTPD](../stacks/catalog/opensmtpd/index.md) for service usage and a test-message example.
