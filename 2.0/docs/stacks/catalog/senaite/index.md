---
description: Deploy SENAITE LIMS, the open source laboratory information management system, on Wodby with its database server and optional email.
---

# SENAITE LIMS stack guide

The Wodby SENAITE LIMS catalog stack runs [SENAITE](https://www.senaite.com/), the open source laboratory information
management system for samples, analyses, instruments, and result reports. The stack needs no repository: SENAITE comes
ready to run. The current composition is documented in
[`wodby/stack-senaite`](https://github.com/wodby/stack-senaite).

| Service | What it does |
| --- | --- |
| SENAITE LIMS | Serves the web interface. Can run more than one replica |
| SENAITE database (ZEO) | Stores SENAITE's database and uploaded files on its volume. Runs as one replica |
| OpenSMTPD | Sends SENAITE's email. Disabled by default |

## Administrator account

The first deployment creates the SENAITE site and its administrator from the SENAITE LIMS service's settings. Set them
when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The administrator's password, at least 12 characters |
| Admin username | `admin` | The administrator's username |
| Admin email | empty | The administrator's email address |
| Language | `en` | The site's language, such as `de` or `pt-br` |
| Time zone | `UTC` | The site's time zone, such as `Europe/Berlin` |

The first deployment takes a few minutes. If the admin password is missing or shorter than 12 characters, the
deployment fails before the site is created: change the setting and deploy again.

These settings are only used when the site is created. Changing them later doesn't change the site or the account.
Change the password and manage users in SENAITE, and change the time zone in SENAITE's date and time settings.

## Sign in

Open the app's main route. SENAITE redirects to its sign-in page; sign in with the admin username and password. SENAITE
is served at the root of the app's domains over HTTPS, and signing in works only over HTTPS.

## Mail

SENAITE sends password resets, notifications, and published results by email. It keeps its mail settings in
**Site setup > Mail**.

The OpenSMTPD service is disabled by default. When you enable it, SENAITE sends through OpenSMTPD from `noreply@` and
the app's primary domain, unless you already set a mail server in **Site setup > Mail**. A mail server you set there is
kept on later deployments. Attach an [SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for
production delivery, and make sure your provider accepts that sender. See the [OpenSMTPD guide](../opensmtpd/index.md).

Without OpenSMTPD, set your own mail server in **Site setup > Mail**.

## Replicas

The SENAITE LIMS service can run more than one replica, and every replica uses the same database server. Change the
number of replicas on the [General configuration](../../../apps/services.md#general-configuration) tab. See
[Replicas](../../../apps/services.md#replicas).

The SENAITE database service is fixed at one replica. Keep one database server per environment: every SENAITE replica
must use it.

## Data and backups

The SENAITE database service's volume (20 GB by default) holds both the database and the uploaded files. The SENAITE
LIMS service stores nothing of its own.

The database grows with every change. The **Pack the database** cron job runs every Sunday and removes old revisions
and files nothing uses any more. It keeps a week of history, so SENAITE's undo works only for changes from the last
seven days.

Back up the SENAITE database service with the **SENAITE database and files** backup. It makes a consistent copy of the
database and the uploaded files while SENAITE keeps running, as one `.tar.gz` archive. A backup needs free space about
the size of the database, both on the volume and on the node that runs the database server. See
[Backups](../../../apps/backups.md).

Wodby can't import this archive into the database service. Restoring one needs access to the volume in your cluster:

1. Download the backup.
2. Stop the SENAITE LIMS and database services, for example by
   [pausing the environment](../../../apps/environments.md#pausing-and-resuming-an-environment).
3. Empty the database service's volume and unpack the archive into it, so the volume holds the `filestorage` and
   `blobstorage` folders.
4. Start the services again, for example by resuming the environment.

Don't unpack an archive into the volume while the database server runs.

## Upgrades

A newer SENAITE version applies its upgrade steps after the deployment, while SENAITE keeps serving. Back up the SENAITE
database service first, then upgrade the stack, or choose the same newer version for both the SENAITE LIMS and the
SENAITE database services on their [General configuration](../../../apps/services.md#general-configuration) tabs.
Moving back to an older version is not supported: restore the backup instead.

## Limits

- SENAITE 2.x runs on Python 2.7 and Plone 5.2, which no longer get fixes from their upstream projects. The service
  includes SENAITE's official security hotfix `SenaiteHotfix20260602`. Vulnerability scans still report findings in
  Python 2 packages.
- Zope's management interface isn't reachable through the app's domains.
- The database server runs as a single replica.
- Wodby can't import a backup archive; restoring one needs access to the volume in your cluster. See
  [Data and backups](#data-and-backups).
