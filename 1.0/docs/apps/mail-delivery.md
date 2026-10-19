# Mail delivery

Many managed stacks include OpenSMTPD as their mail transfer agent. By default,
messages are sent from the server hosting the application. You can change the
active mail service from `Instance > Stack > Settings` when the stack provides
another supported option.

## Production delivery

Direct delivery from a public-cloud IP is often unreliable because the address
can have no mail reputation, can be present on a blocklist, or can be blocked
from outbound SMTP by the hosting provider. For production mail, configure
OpenSMTPD in relay mode with a transactional email provider such as
[AWS SES](../integrations/aws.md), [SendGrid](../integrations/sendgrid.md), or
another SMTP relay supported by your stack.

Use provider credentials limited to sending mail and store passwords as
protected service variables. Configure and validate the provider's SPF, DKIM,
return-path, and DMARC records for every sending domain. Wodby does not create
those external DNS records automatically.

Before relying on a new configuration, test delivery to several mailbox
providers and inspect both the application log and SMTP-provider activity.

## Development mail with Mailhog

When the stack provides Mailhog, select it for development or staging instances
to catch outbound messages instead of delivering them to real recipients. Open
the generated Mailhog domain to inspect messages. A captured message can be
released manually through an SMTP server when that function is configured.

Do not use a mail catcher as the production delivery path: it intentionally
retains messages and can expose message contents to anyone who can access its
interface. Protect its domain when it contains sensitive test data.

## Troubleshooting

If mail is not delivered:

1. Confirm which mail service is active for the instance.
2. Check the application and OpenSMTPD task/container logs.
3. Verify the relay hostname, port, username, and protected password.
4. Check whether the hosting provider blocks the selected outbound SMTP port.
5. Review the relay provider's rejection, suppression, and rate-limit reports.
6. Validate the sending domain's SPF, DKIM, and DMARC records.

See the [OpenSMTPD stack documentation](../stacks/opensmtpd/index.md) for its
service variables.
