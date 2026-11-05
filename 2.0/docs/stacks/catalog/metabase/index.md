# Metabase

The Wodby Metabase catalog stack runs [Metabase](https://www.metabase.com/), the open source business intelligence
tool, with PostgreSQL and an optional OpenSMTPD service for mail. Metabase uses the official open source edition image.
The current composition is documented in
[`wodby/stack-metabase`](https://github.com/wodby/stack-metabase).

## Administrator account

Set the first administrator in the Metabase service's settings when you create the app. Both settings are required:

| Setting | What it sets |
| --- | --- |
| Admin email | The email address the administrator signs in with |
| Admin password | The administrator's password |

The first deployment creates this administrator before Metabase accepts any requests, so Metabase's setup page is never
shown and nobody else can claim a new installation. The site name is set to the app's title, and Metabase's anonymous
usage tracking is turned off. You can change both in Metabase's admin settings.

The password must meet Metabase's
[password rules](https://www.metabase.com/docs/latest/configuring-metabase/environment-variables#mb_password_complexity):
by default, at least 6 characters with at least one digit. If Metabase refuses the password, Metabase does not start,
and the Metabase service log shows Metabase's reason. Fix the setting and deploy again.

The settings are only used when the application database has no users. Changing them later does not change the
account. Change the password, and add other people, in Metabase.

## Site URL

Metabase's site URL is the Metabase service's primary domain. Metabase uses it in emails, sharing links, and embeds.
Because Wodby sets it, it can't be changed in Metabase's admin settings. After you add a domain or change the primary
domain, deploy the Metabase service. See [Domains](../../../apps/endpoints.md#domains).

## Connect your data

The stack's PostgreSQL service is Metabase's application database. It holds Metabase's own data: users, questions,
dashboards, saved connections, and settings. Do not use it for the data you want to analyze.

Add the databases you want to analyze in Metabase, under **Admin settings > Databases > Add a database**. Metabase
connects to them over the network, so they must be reachable from the cluster. They are not Wodby links.

Metabase encrypts the saved connection details with a key Wodby generates for the Metabase service, the
`encryption_key` token in **Configuration > Tokens**. Keep it. If the key changes, Metabase can no longer read the saved
connections. See [Tokens](../../../apps/tokens.md).

## Mail

Metabase sends invitations, password resets, and dashboard subscriptions by email. The OpenSMTPD service is
disabled by default. Either enable it, or enter your own SMTP server in Metabase's email settings.

While Metabase is linked to OpenSMTPD, it gets the SMTP server's host and port from the link, and these can't be changed
in Metabase. Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery.
Metabase sends from `notifications@metabase.com` by default, so set a sender address your provider accepts in Metabase's
email settings. See the [OpenSMTPD guide](../opensmtpd/index.md).

## Resources

The Metabase container requests 0.5 CPU and 1.5 GB of memory and is limited to 2 CPUs and 3 GB. Metabase's Java heap
uses up to 75% of the memory limit, so keep a memory limit when you change resources in **Runtime > Resources**. See
[Resources tab](../../../apps/services.md#resources-tab).

You can run several Metabase replicas. They share the application database, and each one gets these resources. See
[Replicas](../../../apps/services.md#replicas).

## Data and backups

PostgreSQL (10 GB by default) holds all of Metabase's data. The Metabase service has no volume. The databases you
analyze are not part of the app and are not backed up with it.

The Metabase service has no backup or import operation in Wodby. The PostgreSQL service does. See
[Backups](../../../apps/backups.md) and [Imports](../../../apps/imports.md). A database restored into another
environment needs the same `encryption_key` token, or Metabase can't read the saved connections.

## Upgrades

Metabase migrates its application database when a newer version starts, and an older version can't use the migrated
database. Back up the PostgreSQL database before you choose a newer version on the
[General configuration](../../../apps/services.md#general-configuration) tab or upgrade the stack.

You can't move back to an older version: Metabase refuses to start on a database that a newer version migrated. Restore
the backup instead.

## Limits

- Every deployment stops all Metabase replicas before the new ones start, so Metabase is unavailable while its
  service is deployed.
- The stack runs Metabase's open source edition. Features of Metabase's paid plans are not available.
