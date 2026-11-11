---
description: Run Mailpit on Wodby with the Mailpit catalog stack, a mail catcher for development and testing that accepts SMTP mail and shows it in a web interface.
---

# Mailpit

The Wodby Mailpit catalog stack runs Mailpit, a mail catcher for development and testing. It accepts mail over SMTP and
shows it in a web interface. It does not deliver mail to recipients. The current composition and defaults are in
[`wodby/stack-mailpit`](https://github.com/wodby/stack-mailpit).

## Send mail to Mailpit

Use these values from a service in the same app environment:

- SMTP host: the Mailpit app service name
- SMTP port: `1025`

Mailpit uses no TLS, no username, and no password, and Wodby generates no token. An application that requires SMTP
authentication or TLS fails against it. Configure the application's mail transport without them.

Mailpit satisfies the mail link of application services. A linked PHP service receives `MSMTP_HOST` and `MSMTP_PORT`,
and PHP's `mail()` then sends to Mailpit. Other runtimes receive variables named by their own service, such as
`SMTP_HOST` and `SMTP_PORT`. Read those variables instead of hardcoding the host.

## Open the web interface

Port `8025` serves the web interface and Mailpit's REST API under `/api/v1/`. Use it to read, search, and delete
messages.

Captured mail can include password reset links and other secrets, so Wodby protects the public domains with basic auth
by default. Each Mailpit app service gets its own generated password. Reveal it under **Endpoints > Auths** for the app
environment. See [Auths](../../../apps/endpoints.md#auths). Services inside the environment reach port `8025`
directly, without the password. A request to the REST API from outside the environment sends the same username and
password.

## What to expect

- Mailpit captures every message sent to it, whatever the recipient. Nothing leaves the environment, so mail never
  reaches real mailboxes.
- For real delivery, the environment needs a relay such as [OpenSMTPD](../opensmtpd/index.md).
- Mailpit keeps a limited number of messages and deletes the oldest first.
- Set Mailpit options as [environment variables](../../../apps/environment-variables.md) on the app service in
  Mailpit's `MP_*` form. Wodby sets none by default.

## Keep messages across restarts

The optional **Data** volume is mounted at `/data`. Mailpit stores messages in a temporary file that is removed when it
exits. Captured mail survives a restart only when the volume exists and `MP_DATABASE` is set to a path under `/data`.
Wodby defines no backups or imports for this service.

## Check that it works

Send a test message from the application, then open the web interface. From a service in the environment, you can also
request `GET http://<app service name>:8025/api/v1/messages`.
