# Matomo

The Wodby Matomo catalog stack combines Matomo, Nginx, MariaDB, OpenSMTPD, and optional Valkey services. The current
composition is documented in [`wodby/stack-matomo`](https://github.com/wodby/stack-matomo).

## Initial database setup

Wodby provisions an application database and injects its connection values into the Matomo service. During Matomo's
`Database Setup` step, use these runtime variables:

| Matomo field | Runtime variable |
| --- | --- |
| Database server | `MATOMO_DATABASE_HOST` |
| Login | `MATOMO_DATABASE_USERNAME` |
| Password | `MATOMO_DATABASE_PASSWORD` |
| Database name | `MATOMO_DATABASE_DBNAME` |

Open a [web terminal](../../../apps/web-terminal.md) for the Matomo app service and run the following command to display
the values for the current app instance:

```bash
printenv MATOMO_DATABASE_HOST MATOMO_DATABASE_USERNAME MATOMO_DATABASE_PASSWORD MATOMO_DATABASE_DBNAME
```

The hostname is generated from the current database link, so always use the value supplied to the app service.

## Geolocation

The Matomo image includes a GeoLite2 City database. In Matomo, open `Administration > System > Geolocation`, select the
GeoIP 2 PHP provider, and save the setting. Configure Matomo's database updater when you need regular GeoIP database
updates.

## Mail delivery

The Matomo PHP runtime sends mail through the stack's linked OpenSMTPD service. Attach an
[SMTP provider integration](../../../providers/smtp.md) to OpenSMTPD for production delivery. Direct delivery from a
cluster IP is not a reliable production mail strategy.

See the [OpenSMTPD guide](../opensmtpd/index.md) for relay setup and testing.

## Archiving cron

Add an app-level cron schedule to the Matomo service for report archiving. The command can use Wodby's primary URL:

```bash
php console core:archive --url="${WODBY_PRIMARY_URL}"
```

A common schedule is once per hour, for example `5 * * * *`. Wodby cron schedules cannot run more often than hourly.
See [Application Cron Schedules](../../../apps/cron.md).

## Persistent customization

Use Matomo's UI for settings stored in its database. For file-based changes, put the change in the application's build
source or image. Edits made only through a web terminal modify a running container and are lost when that container is
replaced.
