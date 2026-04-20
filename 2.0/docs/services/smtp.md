# Mail services

Wodby does not use a separate `smtp` service type.

Services that send mail through an SMTP relay are modeled as regular services of type `service`. They typically define
[integrations](integrations.md) so customers can connect third-party SMTP providers such as Brevo or AWS SES.

If you are documenting a mail relay service template, use the regular service features described in
[service types](types.md), [integrations](integrations.md), and the [service template reference](template.md).
