# Ghost

The Wodby Ghost catalog stack combines Ghost, MySQL, and OpenSMTPD services. The current composition is documented in
[`wodby/stack-ghost`](https://github.com/wodby/stack-ghost).

## Before you create the app

Set **Email sender** on the Ghost app service. It is required. Use the form `Ghost <ghost@example.com>`, with an address
that your mail relay accepts.

Ghost needs MySQL 8.4. MariaDB is not supported.

## First sign-in

Wodby does not create an administrator account. Open `/ghost/` on the app's main route and create the owner account in
the browser.

## Mail delivery

Ghost sends mail through the stack's OpenSMTPD service. Password resets, staff invitations, and member email need
working mail delivery. Recipient mail servers often reject mail sent directly from a cluster, so attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production. See the
[OpenSMTPD guide](../opensmtpd/index.md) for relay setup and testing.

Ghost also has the **Verify new devices by email** setting on the app service's **Configuration > Settings** tab. It
is `false` by default. When it is `true`, staff who sign in from a new device must enter a code sent by email. Turn it
on only after you have confirmed that mail is delivered. Otherwise staff cannot sign in.

## Change configuration

Add or change environment variables on the Ghost app service, then deploy it. Use Ghost's `section__key` form, for
example `mail__from`. Database and mail connection values come from the stack links. Do not set them elsewhere. See
[Environment variables](../../../apps/environment-variables.md).

Ghost builds its links from the environment's primary URL, so they change when the primary host changes.

## Data and backups

- The **Content** volume (20 GB by default) holds images, themes, and other content files.
- Posts, users, and settings are in the MySQL database.

The Ghost content backup and content import cover only the volume. They accept `tar`, `tar.gz`, `tgz`, and `zip`
archives for imports. They do not include the database, so also back up MySQL. See [Backups](../../../apps/backups.md)
and [Imports](../../../apps/imports.md).

## Limits

- Ghost runs as one replica. Use an external CDN or cache for more delivery capacity instead of adding replicas.
- The route accepts request bodies up to 50 MiB.
- Ghost 7 uses a different content path and needs an explicit storage migration. Do not treat it as a routine update.
