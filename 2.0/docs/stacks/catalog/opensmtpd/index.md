# OpenSMTPD

The Wodby OpenSMTPD catalog stack provides an SMTP relay service on internal port `25`. It can also be included in
application stacks such as Drupal, WordPress, and Matomo. The current service definition is documented in
[`wodby/stack-opensmtpd`](https://github.com/wodby/stack-opensmtpd).

## Production delivery

Do not rely on direct delivery from a Kubernetes node or cloud-cluster IP for production mail. Recipient providers may
reject or classify mail from those addresses as spam.

Create an [SMTP provider integration](../../../providers/smtp.md), then attach it to the OpenSMTPD app service's
`Third-party SMTP server for Relay` integration. Wodby supplies the relay host, port, protocol, username, and password
from the selected provider.

Applications in the same app instance should connect through their stack link. The usual internal connection is the
OpenSMTPD app-service hostname on port `25`; linked PHP services receive that connection automatically through their
mail-transfer-agent link.

## Send a test message

Open a [web terminal](../../../apps/web-terminal.md) on the OpenSMTPD service, then send a small message:

```bash
printf 'Subject: Wodby SMTP test\n\nOpenSMTPD relay test.\n' | \
  sendmail -v -f verified-sender@example.com recipient@example.com
```

Use a sender accepted by the configured provider. The verbose output confirms whether OpenSMTPD accepted the message;
use the app logs and your provider's delivery logs to diagnose later relay or delivery failures.

Add the optional spool volume when queued mail must survive pod replacement.
