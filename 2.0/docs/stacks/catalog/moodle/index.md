# Moodle

The Wodby Moodle catalog stack runs [Moodle LMS](https://moodle.org/) 5.3 with Nginx, MariaDB, shared NFS storage for
Moodle's files, OpenSMTPD for mail, and an optional Valkey service for sessions. A separate worker runs Moodle's cron.
The current composition is documented in [`wodby/stack-moodle`](https://github.com/wodby/stack-moodle).

The stack runs Wodby's prebuilt Moodle image, so there's nothing to build and no repository to connect.

## Administrator account

Moodle is installed during the app's first deployment, so you never use Moodle's web installer. Set the administrator
account in the Moodle service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The administrator's password |
| Admin username | `admin` | The administrator's username |
| Admin email | empty | The administrator's email address |

- A password that doesn't meet Moodle's password policy works for the first sign-in, and Moodle then asks for a new one.
- Without an email, Moodle asks for it at the first sign-in.
- The site's full name and short name start as the app's title and name. Change them in Moodle under
  **Site administration > Site home > Site home settings**.

These settings are only used when Moodle is installed. To change the administrator later, use Moodle.

If the first deployment can't install Moodle, for example because the admin password is missing, the deployment's
post-deploy step fails with the reason. Fix it and deploy again.

## Site address

Moodle uses the app environment's main domain as its address and redirects other domains of the app to it. When you
change the main domain, deploy the Moodle service again so Moodle picks up the new address. To use another address, set
the `MOODLE_WWWROOT` [environment variable](../../../apps/environment-variables.md) on the Moodle service.

## Configuration and plugins

Moodle's `config.php` reads the database, address, data directory and session settings from the app environment.

Moodle's code is part of the image, so you can't add plugins or themes. Installing them from Moodle's web interface is
turned off, because the next deployment would remove them.

## Updates and upgrades

New Moodle releases arrive as updates of the Moodle service; see [stack upgrades](../../../apps/stack.md#upgrade). The
deployment after an update runs Moodle's upgrade, and Moodle switches to maintenance mode while it upgrades. Back up the
app before you upgrade.

## Cron

The `cron` service keeps Moodle's cron running all the time, as Moodle requires. You don't need to add a
[cron schedule](../../../apps/cron.md). When the cron service stops, it lets the running task finish first.

## Mail and sessions

Moodle sends mail through the stack's OpenSMTPD service. For production delivery, attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD; see the [OpenSMTPD guide](../opensmtpd/index.md).

Sessions are stored as files in Moodle's data directory. Enable the Valkey service to keep them in Valkey instead.

## Data and backups

- The `moodledata` volume holds uploaded files and Moodle's file caches. The Moodle service and its cron worker share it
  through the NFS storage service.
- The MariaDB database holds everything else.

Back up both the database and the `moodledata` volume; see [Application Backups](../../../apps/backups.md).

## Limits

- Moodle 5.3 runs on PHP 8.3 or 8.4 and needs MariaDB 11.4 or later.
- Uploads are limited to 256 MB.
