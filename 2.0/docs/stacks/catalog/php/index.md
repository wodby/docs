# PHP

The Wodby PHP catalog stack runs a PHP-FPM service behind Nginx, with MariaDB and Mailpit enabled by default. Apache
HTTP Server, PostgreSQL, Valkey, OpenSMTPD and Gotenberg are available as optional services. The current services and
defaults are documented in [`wodby/stack-php`](https://github.com/wodby/stack-php).

## Build and deployment

Start from the [Composer boilerplate](https://github.com/wodby/php-package-boilerplate) or connect your own repository.
The web server has no repository of its own. Its image is built from the PHP service's source, so both images contain
the code at the same path. A changed static file needs a new build and deployment. See
[Application Builds](../../../apps/builds.md).

The **Nginx docroot** setting defaults to `public`. It must be the directory that holds your front controller.
Nginx passes a path that is not a file to `index.php`, so the application needs no rewrite rules. A path with a static
file extension that matches no file returns 404 instead. Nginx does not read `.htaccess` files. The **HTTPd docroot**
setting of Apache HTTP Server has no default, so Apache serves the repository root until you set it, for example to
`public` or `web`. Apache reads `.htaccess`, and routing every path to `index.php` comes from your own `.htaccess`.

## Database and mail

Do not hardcode connection settings. The PHP service receives these variables from its links, and only while the link
exists and the linked service is enabled:

| Link | Variables |
| --- | --- |
| **DBMS** (MariaDB by default; MySQL or PostgreSQL) | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| **Mail Transfer Agent** (Mailpit by default) | `MSMTP_HOST`, `MSMTP_PORT` |

PHP's `mail()` is delivered through the linked mail service, so no SMTP library or credentials are needed.

Mailpit captures every message and delivers none of them. Use it to inspect mail in non-production environments. Its
web interface is protected with basic auth. Reveal the password in **Endpoints > Auths**. For real delivery, enable
OpenSMTPD, point the PHP service's **Mail Transfer Agent** link at it, and attach an [SMTP
provider](../../../providers/smtp.md). See the [OpenSMTPD guide](../opensmtpd/index.md).

Valkey and Gotenberg are disabled by default, and the PHP service has no link to either one. Wodby sets no variables
for them. Put their addresses in your application's configuration. Valkey listens on port 6379 and always requires its
generated `password` token. Gotenberg listens on port 3000 without authentication. Both are reachable at the name of
their app service inside the environment.

## PHP settings

Set `PHP_*` variables on the PHP service, such as `PHP_MEMORY_LIMIT`, `PHP_MAX_EXECUTION_TIME` or
`PHP_FPM_PM_MAX_CHILDREN`, instead of adding a `php.ini` to the repository. Changes apply with the next deployment.
Uploads are limited by both `NGINX_CLIENT_MAX_BODY_SIZE` on Nginx and the PHP settings.

`WODBY_HOSTS` is a JSON array of the environment's hosts. Use `WODBY_PRIMARY_URL` for links generated outside a request.
`WODBY_ENV_TYPE` tells a development environment from a production-like one. See
[Environment variables](../../../apps/environment-variables.md).

## Data and backups

The PHP service has no volume. Files written inside the container are lost when it is replaced.

MariaDB and PostgreSQL keep data on a 20 GB `data` volume. A backup is a gzipped SQL dump of the environment's database.
A database import replaces the whole data volume. See [Application Backups](../../../apps/backups.md) and
[Application Imports](../../../apps/imports.md).
