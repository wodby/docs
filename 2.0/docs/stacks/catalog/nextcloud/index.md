# Nextcloud

The Wodby Nextcloud catalog stack runs [Nextcloud](https://nextcloud.com/) file storage and sharing with PostgreSQL,
Redis, and an optional OpenSMTPD mail relay. Nextcloud uses the official Nextcloud Apache image. The current composition
is documented in [`wodby/stack-nextcloud`](https://github.com/wodby/stack-nextcloud).

## Before you create the app

- Nextcloud, PostgreSQL, and Redis are required. OpenSMTPD is optional and selected by default. You can leave it out
  when you create the app.
- Enter **Admin username** and **Admin password** on the Nextcloud service. Nextcloud creates this administrator account
  during the first deployment. Both values are stored as secrets and Wodby does not show them again, so keep a copy.
- Choose volume sizes now. The Nextcloud volume is 50 GB and the PostgreSQL volume is 20 GB by default. A volume cannot
  be resized from the app service settings after it is created. See
  [Application persistent storage](../../../apps/storage.md).
- If file contents should be stored in a bucket instead of the Nextcloud volume, set that up before the first
  deployment. See [Object storage for files](#object-storage-for-files).

## First sign-in

Nextcloud installs itself when it first starts. After the first deployment, open the app's main domain and sign in with
the administrator username and password you entered.

Changing **Admin username** or **Admin password** later does not change the account. Change the password in Nextcloud,
or reset it with an [occ command](#run-occ-commands).

## Domains

Nextcloud accepts requests only for its trusted domains. Wodby sets them from the app environment's domains, including
[Private App Access](../../../apps/access.md) hostnames, each time Nextcloud starts. This list replaces trusted domains
set in Nextcloud's own configuration, so manage domains in Wodby.

After you add or remove a domain, or change the main domain, deploy the Nextcloud service. Until then, Nextcloud rejects
requests for a new hostname with an untrusted domain error. Links that Nextcloud creates in background jobs, such as
email notifications, use the primary domain. See [Domains](../../../apps/endpoints.md#domains).

The optional **Trusted proxies** setting lists proxy IP addresses or CIDR ranges, separated by spaces, whose forwarded
client address headers Nextcloud trusts. Do not enter a range wider than your cluster's proxy network.

## Background jobs

A cron container in the Nextcloud pod runs Nextcloud's background jobs every five minutes. On the first run, Nextcloud
switches its background jobs setting to **Cron**. You do not need a Wodby [cron schedule](../../../apps/cron.md). Keep
**Cron** selected under **Administration settings > Basic settings > Background jobs**.

## Mail delivery

While the Nextcloud service is linked to OpenSMTPD, Nextcloud sends mail through it and takes its email server settings
from Wodby. The sender address is built from two Nextcloud service settings: **Mail sender**, `nextcloud` by default,
and **Mail domain**, the app's primary hostname by default.

Recipient mail servers often reject mail sent directly from a cluster. For production, attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD and set **Mail sender** and **Mail domain** to an
address your provider accepts. Then deploy the Nextcloud service. See the [OpenSMTPD guide](../opensmtpd/index.md) for
relay setup and testing.

Without the OpenSMTPD link, set up an email server in Nextcloud under **Administration settings > Basic settings**.

## Uploads and timeouts

The Nextcloud domain passes uploads through to Nextcloud as they arrive, and its request and backend timeouts are one
hour. The **PHP upload limit** setting is `3G`, and the **Apache request body limit** setting is `0`, which means no
Apache limit. Nextcloud clients normally upload large files in smaller parts, so these limits apply to each part.

To accept larger single requests, raise the **PHP upload limit**, then deploy the Nextcloud service. Do not set the
`request_body_size` [HTTP setting](../../../apps/endpoints.md#http-settings) on the Nextcloud domain: it makes the
route hold each upload in memory until it is complete. **PHP memory limit** is `512M` by default.

## Caching

Nextcloud keeps a local cache in its own container and uses Redis for the shared cache, file locking, and browser
sessions. In this stack, Redis has no volume and keeps nothing on disk. It can use up to 512 MB of memory and never
removes keys to free memory, so file locks and sessions are not lost while Redis runs. When Redis restarts or is
deployed, its data is cleared, and people signed in through the browser may need to sign in again. See the [Redis
guide](../redis/index.md).

## Object storage for files

Nextcloud can store file contents in Amazon S3, Cloudflare R2, or Backblaze B2 instead of the Nextcloud volume. Set it
up before the first deployment:

1. Create an empty bucket used only by this app environment's Nextcloud. For Amazon S3, create it in the region selected
   in the AWS integration.
2. Create an [AWS](../../../providers/aws.md#s3), [Cloudflare R2](../../../providers/cloudflare.md#r2), or
   [Backblaze B2](../../../providers/backblaze.md#b2-cloud-storage) integration whose credentials can read, write, and
   delete objects in that bucket.
3. On the Nextcloud service, attach the integration to **S3 primary storage** on the
   [Integrations tab](../../../apps/services.md#integrations-tab) and enter the bucket name in the **S3 bucket**
   setting. Nextcloud uses the bucket only when both are set.

!!! warning "Data loss"
    Do not enable object storage on an installation that already has files: files stored on the volume become
    inaccessible. For the same reason, do not detach the integration or clear **S3 bucket** later, or the files in the
    bucket become inaccessible.

The bucket holds file contents under internal names. Folder structure and file names are stored in PostgreSQL, so you
cannot browse users' folders in the bucket. Do not store anything else in it, including Wodby backups.

## Data and backups

- The Nextcloud volume holds the Nextcloud installation, its configuration, installed apps, themes, and, without object
  storage, all user files.
- PostgreSQL holds accounts, shares, file records, and app data.
- Redis holds only temporary data.

The Nextcloud service has no backup or import operation in Wodby. The PostgreSQL service does: a backup is a compressed
SQL dump of the database, and an import replaces the whole database. See [Backups](../../../apps/backups.md) and
[Imports](../../../apps/imports.md).

A PostgreSQL backup on its own does not restore Nextcloud: the database records which files exist, so a restored
database does not match the files on the volume or in the bucket. Wodby cannot back up the Nextcloud volume, so copy it,
and the bucket if you use one, with your own tools together with a PostgreSQL backup, and restore them together. To keep
the copies consistent, turn on maintenance mode while you make them.

## Run occ commands

Open a [web terminal](../../../apps/web-terminal.md) on the Nextcloud service, choose the `nextcloud` container, and run
`occ` as the `www-data` user:

```bash
su -s /bin/sh www-data -c 'php /var/www/html/occ status'
```

For example, use `maintenance:mode --on` and `maintenance:mode --off` around a backup, or `user:resetpassword <user>` to
set a new password for an account.

## Upgrades

Nextcloud upgrades itself when it starts with a newer version, for example after you change the version on the
[General configuration](../../../apps/services.md#general-configuration) tab or after a stack update. Nextcloud's
built-in web updater is turned off. The upgrade runs before Nextcloud serves requests, and Wodby gives it about 15
minutes before the container is restarted.

- Back up before you upgrade.
- Upgrade one major version at a time, for example from 33 to 34. If you skip a major version, Nextcloud does not start.
- You cannot return to an older version. Nextcloud does not start when its data is newer than the selected version.
  Restore a backup instead.
- Apps that are not compatible with the new version are disabled during the upgrade. The Nextcloud service log lists
  them.

## Limits

- Nextcloud runs as one replica, and the old pod stops before the new one starts. Nextcloud is unavailable while its
  service is deployed.
- The stack does not include an online office server, such as Collabora Online.
