# Matomo

The Wodby Matomo catalog stack runs [Matomo](https://matomo.org/) web analytics with MariaDB, shared NFS storage for
Matomo's files, and OpenSMTPD for mail. The current composition is documented in
[`wodby/stack-matomo`](https://github.com/wodby/stack-matomo).

The stack runs Wodby's prebuilt Matomo image, so there's nothing to build and no repository to connect.

## Superuser and first website

Matomo is installed during the app's first deployment, so you never use Matomo's web installer. Set the superuser and
the first website in the Matomo service's settings when you create the app:

| Setting | Default | What it sets |
| --- | --- | --- |
| Admin password | none, required | The superuser's password |
| Admin email | none, required | The superuser's email address |
| Admin username | `admin` | The superuser's login |
| Website URL | empty | The address of the first website to track, such as `https://www.example.com` |

- The first website is named after the app's title. Without a website URL, Matomo asks for a website at the first
  sign-in.
- These settings are only used when Matomo is installed. To change the superuser later, use Matomo.

If the first deployment can't install Matomo, for example because the admin password or email is missing, the
deployment's post-deploy step fails with the reason. Fix it and deploy again. Later deployments update Matomo's database
instead.

## Domains

Matomo uses the app environment's main domain as its address and accepts requests for every domain of the app. After
you add a domain or change the main domain, deploy the Matomo service again.

## Archiving

Matomo processes reports in the background, not when someone views them. The Matomo service defines an hourly
**Archive reports** cron schedule, at five minutes past the hour, which also sends scheduled email reports. Change the
schedule or run it manually from the app environment's [Cron](../../../apps/cron.md) page.

Cron schedules require an active paid subscription. Without them, Matomo's reports are not updated.

## Plugins and updates

Install plugins from Matomo's Marketplace. They are kept on the shared files volume, so every replica loads them and
they stay after updates. After you activate a plugin that changes Matomo's tracking code, restart the Matomo service so
every replica serves the new code.

New Matomo releases arrive as updates of the Matomo service; see [stack upgrades](../../../apps/stack.md#upgrade). The
deployment after an update runs Matomo's database update. Matomo's own updater is turned off.

## Geolocation

The Matomo image includes a GeoLite2 City database. In Matomo, open **Administration > System > Geolocation**, select
the GeoIP 2 PHP provider, and save the setting.

## Mail

Matomo sends mail through the stack's OpenSMTPD service. Attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery. Direct delivery from a
cluster IP is not a reliable production mail strategy. See the [OpenSMTPD guide](../opensmtpd/index.md).

## Data and backups

- The `files` volume holds Matomo's settings file, custom logos and Marketplace plugins. Every Matomo replica and the
  archiving job share it through the NFS storage service.
- The MariaDB database holds reports, visits, users and sessions.

Back up both the database and the `files` volume, and restore them together; see
[Application Backups](../../../apps/backups.md). Use Matomo's UI for settings: changes made to files in a
[web terminal](../../../apps/web-terminal.md) outside the files volume are lost when the container is replaced.

Matomo mixes a salt that Wodby generates for the Matomo service, the `matomo_salt` token in **Configuration > Tokens**,
into every password, API token and session. Keep it. If it changes, existing passwords, API tokens and sessions stop
working. A database restored into another app environment needs the same token. See
[Tokens](../../../apps/tokens.md).

## Apps created before the prebuilt image

Earlier versions of the Matomo stack built Matomo from a repository and served it with a separate Nginx service. Apps
created from them keep that setup, because a new major version of a service is never applied automatically. Archive
their reports with an app-level [cron schedule](../../../apps/cron.md) on the Matomo service that runs
`php console core:archive --url="${WODBY_PRIMARY_URL}"` once an hour. To move to the prebuilt image, create a new app
from the Matomo stack.

## Limits

- Matomo supports only MariaDB and MySQL.
- Development workspaces are not available for Matomo.
