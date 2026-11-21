---
description: Deploy eLabFTW, the open source electronic lab notebook, on Wodby with the eLabFTW catalog stack, which runs it with MySQL and optional email.
---

# eLabFTW stack guide

The Wodby eLabFTW catalog stack runs [eLabFTW](https://www.elabftw.net/), the open source electronic lab notebook for
experiments, protocols, resources, and inventory. It runs the official eLabFTW image with MySQL and an optional
OpenSMTPD service for email. The stack needs no repository. The current composition is documented in
[`wodby/stack-elabftw`](https://github.com/wodby/stack-elabftw).

| Service | What it does |
| --- | --- |
| eLabFTW | Serves the web interface and the API, and sends notifications. Uploaded files and exports are stored on its volume |
| MySQL | Stores experiments, resources, users, teams, and settings |
| OpenSMTPD | Sends eLabFTW's email. Disabled by default |

## Sysadmin account

eLabFTW is installed during the app's first deployment, with a Sysadmin account from the eLabFTW service's settings. Set
them when you create the app:

| Setting | What it sets |
| --- | --- |
| Admin email | The email address the Sysadmin signs in with. Required |
| Admin password | The Sysadmin's password. Required |
| Admin first name | The Sysadmin's first name. Defaults to `Admin` |
| Admin last name | The Sysadmin's last name. Defaults to `Sysadmin` |

The admin password must have at least 24 characters, with an uppercase letter, a lowercase letter, a digit, and a
special character. If it is weaker, the deployment fails before eLabFTW is installed: change the setting and deploy
again.

Open the app's main route and sign in with the admin email and password. The **Sysadmin panel** holds the settings for
the whole installation.

The settings are only used when eLabFTW is installed. Changing them later does not change the account. Change the
password, and invite other people, in eLabFTW. eLabFTW's sign-up page is open by default, and new accounts wait until an
administrator validates them. You can turn off sign-up in the Sysadmin panel.

## Database

eLabFTW needs MySQL 8 or later. It doesn't support MariaDB. The stack includes MySQL. To use a managed MySQL server
instead, link the eLabFTW service to it. See the [Cloud MySQL guide](../cloud-mysql/index.md). eLabFTW connects to
a managed server over TLS when the server has a CA certificate.

If eLabFTW is linked to a MariaDB server or to MySQL older than 8, the deployment fails with a message that names the
server's version.

## Domain

eLabFTW uses the environment's primary URL for links in emails and in API responses. It picks up a new primary domain
when the eLabFTW service is deployed: if links still show the old domain, deploy the service again. See
[Domains](../../../apps/endpoints.md#domains).

TLS ends at Wodby's router, and eLabFTW builds `https://` addresses.

## Mail

eLabFTW sends password resets, notifications, and account requests by email. It keeps its email settings in the
Sysadmin panel, on the **Email** tab.

The OpenSMTPD service is disabled by default. When you enable it, eLabFTW sends through OpenSMTPD from `noreply@` and the
primary domain, unless you already set an SMTP server in the Sysadmin panel. Settings you save there are kept. Attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery, and make sure your
provider accepts that sender. See the [OpenSMTPD guide](../opensmtpd/index.md).

Without OpenSMTPD, set your own SMTP server in the Sysadmin panel.

## Change configuration

Instance settings, such as email, sign-in methods, teams, and file storage, are managed in the Sysadmin panel and kept in
the database. eLabFTW's own environment variables can be added or changed on the eLabFTW service; deploy it to apply
them. See [Environment variables](../../../apps/environment-variables.md).

The `key_bytes` token in **Configuration > Tokens** sets eLabFTW's secret key. It encrypts the SMTP and timestamping
passwords and webhook secrets that eLabFTW stores. If you change it, enter those passwords again and recreate the
webhooks. See [Tokens](../../../apps/tokens.md).

## Resources and replicas

eLabFTW requests 0.05 CPU and 192 MB of memory, with a 2 GB memory limit. Change them in **Runtime > Resources**. See
[Resources tab](../../../apps/services.md#resources-tab).

eLabFTW runs up to 10 PHP processes of up to 512 MB each. Large exports and PDF generation can need more memory: raise
the memory limit, or lower the `PHP_MAX_CHILDREN` and `MAX_PHP_MEMORY` variables on the eLabFTW service.

eLabFTW runs as one replica. Sessions are kept in the eLabFTW container, so a restart or a deployment signs everyone
out.

## Data and backups

MySQL (10 GB by default) holds eLabFTW's data. The eLabFTW volume (20 GB by default) holds uploaded files and exports.
Back up both to keep a complete installation. See [Backups](../../../apps/backups.md) and
[Imports](../../../apps/imports.md).

eLabFTW can also store uploaded files in an S3-compatible bucket, set in the Sysadmin panel.

## Upgrades

eLabFTW updates its database when a newer version starts. Back up the MySQL database and the eLabFTW volume, then choose
the newer version on the [General configuration](../../../apps/services.md#general-configuration) tab or upgrade the
stack. Moving back to an older version is not supported: restore the backup instead.

## Limits

- eLabFTW runs as a single replica.
- Wodby delivers new eLabFTW releases as new versions of the service. The Sysadmin panel can announce a newer eLabFTW
  release before the service offers it.
