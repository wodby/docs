---
description: Deploy Mautic marketing automation on Wodby with the Mautic catalog stack, which runs it with MariaDB, shared NFS storage, OpenSMTPD and two workers.
---

# Mautic

The Wodby Mautic catalog stack runs [Mautic](https://www.mautic.org/), the open source marketing automation platform,
with MariaDB, shared NFS storage for Mautic's files, and OpenSMTPD for mail. Two workers run Mautic's cron jobs and
its queue. The current composition is documented in [`wodby/stack-mautic`](https://github.com/wodby/stack-mautic).

The stack runs Wodby's prebuilt Mautic image, so there's nothing to build and no repository to connect.

## Administrator account

Mautic is installed during the app's first deployment, so you never use Mautic's web installer. Set the administrator
account in the Mautic service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The administrator's password, at least 6 characters |
| Admin email | none, required | The administrator's email address |
| Admin username | `admin` | The administrator's username |

- Mautic sends email from the admin email, with the app's title as the sender name. Change both in Mautic under
  **Settings > Configuration > Email Settings**.
- These settings are only used when Mautic is installed. To change the administrator later, use Mautic.

If the first deployment can't install Mautic, for example because the admin password or email is missing, the
deployment's post-deploy step fails with the reason. Fix it and deploy again. Later deployments update Mautic's database
instead.

## Site address

Mautic uses the app environment's main domain as its address, in links in emails and in cron jobs. The address saved
in Mautic's settings is ignored. When you change the main domain, deploy the Mautic service again so Mautic picks up the
new address. To use another address, set the `MAUTIC_SITE_URL`
[environment variable](../../../apps/environment-variables.md) on the Mautic service.

## Cron jobs and queue

- The `cron` worker runs Mautic's cron jobs, such as segment and campaign updates, sending scheduled emails and
  broadcasts, imports, webhooks and scheduled reports, one after another every five minutes. You don't need to add a
  [cron schedule](../../../apps/cron.md).
- The `worker` worker sends queued email and records queued page hits.

Both start working once Mautic is installed, and let the current job finish when they stop. Their logs show each run.

## Mail

Mautic sends mail through the stack's OpenSMTPD service. For production delivery, attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD, and set a sender address your provider accepts in
Mautic's email settings. See the [OpenSMTPD guide](../opensmtpd/index.md). You can also enter another mail server in
Mautic's email settings.

## Plugins and updates

Mautic's code is part of the image, so you can't add plugins or themes. Mautic's built-in plugins, such as its CRM and
social integrations, are available.

New Mautic releases arrive as updates of the Mautic service; see [stack upgrades](../../../apps/stack.md#upgrade). The
deployment after an update migrates Mautic's database. Back up the app before you upgrade.

## Data and backups

- The `files` volume holds Mautic's settings file, uploaded files and images, language packs, imports, logs and
  sessions. The Mautic service and both workers share it through the NFS storage service.
- The MariaDB database holds everything else.

The settings file holds Mautic's secret key and every setting saved in Mautic. Without it, Mautic can't use its
database, and the next deployment refuses to install Mautic over the existing data. Back up both the database and the
`files` volume, and restore them together; see [Application Backups](../../../apps/backups.md).

## Limits

- Mautic supports only MariaDB and MySQL, and can't connect to a database server over TLS. A database that requires
  TLS connections can't be used.
- Uploads are limited to 64 MB. Mautic's own limit for assets is 6 MB until you change it in Mautic's settings.
- Development workspaces are not available for Mautic.
