# Matomo stack documentation

## Setup

Use the following credentials during the initial setup on the Database Setup step:

* Database Server: `matomo`
* Login: `matomo`
* Password: Copy the value of `MYSQL_PASSWORD` from `[Instance] > Stack > Database` page
* Database Name: `matomo`

## Geolocation

Since version [0.6.0](#060) Matomo comes with GeoIP 2 databases. On Matomo settings page go to `Geolocation` under `System`, choose option `GeoIP 2 (Php)` and click save.

## Customization

You can customize matomo settings by editing `config/config.ini.php` file from the SSH container. After the initial release you may not have permissions to do so, to fix that, you just need to redeploy your stack from `[Instance] > Stack > Operations` page.

## Redis integration

You can use redis to store Matomo cache (by default stored in the local filesystem):

* Enable redis service in your application stack from `[Instance] > Stack` page
* Copy your instance UUID from `[Instance] > Settings` page
* Access the server hosting your matomo instance as root and append `/srv/wodby/instances/[INSTANCE UUID]/app/config/config.ini.php` file with the following values:

```
[Cache]
backend = chained

[ChainedCache]
backends[] = array
backends[] = redis

[RedisCache]
host = "redis"
port = 6379
timeout = 0.0
password = "Copy the value of `REDIS_PASSWORD` from `[Instance] > Stack > Redis page`"
database = 14
```

## Mail delivery

Go to `Settings > System > General settings > Email server settings` in your Matomo instance. Specify `opensmtpd` as server address and `25` as port. For more details how to configure guaranteed email delivery see [OpenSMTPD stack documentation](../opensmtpd/index.md)

## Cron

By default we run the following cron command from [crond container](#crond) every hour:

```
/usr/local/bin/php /var/www/html/console core:archive --url=${WODBY_URL_PRIMARY}
```

## Containers

### PHP

{!containers/php.md!}

### Crond

{!containers/php-crond.md!}

`$WODBY_HOST_PRIMARY` is a domain marked as primary. 

### SSHd

{!containers/php-sshd.md!}

### [OpenSMTPD](../opensmtpd/index.md)

### [MariaDB](../mariadb/index.md)

### [Redis](../redis/index.md)

## Changelog

This changelog is for Matomo stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/matomo/releases).

### 1.0.6

🔁 Matomo rebuilt against the latest PHP image

### 1.0.5

⬆️ Matomo 4.15.1

### 1.0.3

⬆️ Matomo 4.14.2

### 1.0.2

⬆️ Matomo 4.14.1

### 1.0.1

🏔 Alpine updated to 3.17.2

### 1.0.0

- ⚠️ This version of stack requires server infrastructure 6.0.0+
- ⬆️ Matomo 4.13.3

### 0.16.1

⬆️ Matomo 4.13.0

### 0.16.0

⬆️ Matomo 4.12.3

### 0.15.4

⬆️ Matomo 4.11.0

### 0.15.3

- 🔃 Matomo rebuilt against updated PHP image
- ⭐️ Added Nginx 1.23, 1.22

### 0.15.2

⬆️ Matomo 4.10.1

### 0.15.1

⬆️ Matomo 4.10.0

### 0.15.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- ⬆️ Matomo 4.9.0
- 🏔 Alpine Linux updated to 3.15

### 0.14.3

🏔 Security updates for base OS Alpine Linux

### 0.14.2

⬆️ Matomo 4.8.0

### 0.14.1

- Bugfix: access to html files under plugins directory forbidden
- Bugfix: unexpected text files
- Bugfix: matomo.js is not writable by the web server

### 0.14.0

- ⬆️ Matomo 4.7.1
- ⬆️ Matomo 4 rebased to PHP 8.1
- ⭐️ Added new Nginx service with Matomo preset that provides a better security, we recommend switching to this service 
- 🪦 Matomo 3 has reached EOL

### 0.13.0

⬆️&nbsp; Matomo 4.6.2

### 0.12.2

⬆️&nbsp; Matomo 4.3.1

### 0.12.1

⬆️&nbsp; Matomo 4.2.1

### 0.12.0

Added Matomo v4

### 0.11.2

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 0.11.1

Matomo 3.14.1

### 0.11.0

Matomo 3.14

### 0.10.3

Matomo updated to 3.13.6

### 0.10.2

Matomo updated to 3.13.5

### 0.10.1

Matomo updated to 3.13.4

### 0.10.0

Matomo updated to 3.13.0

### 0.9.1

Matomo updated to 3.12.0

### 0.9.0

- Matomo updated to 3.11.0
- Bugfix: crond service missed preloaded icon library

### 0.8.2

Bugfix: duplicated Nginx services (missing version 1.16)

### 0.8.1

Bugfix: default Nginx service version had an incorrect preset that caused 403 Forbidden error.

### 0.8.0

- Matomo updated to 3.10.0
- Adminer updated to 4.7.2 
- Alpine Linux updated to 3.10.1

### 0.7.3

- Matomo and Adminer rebuilt against the latest PHP image
- Added new Nginx versions 1.17, 1.16

### 0.7.2

- Matomo and Adminer rebuilt against the latest PHP image
- Nginx:
    - Added new latest version 1.16
    - Updated to 1.15.12
    - Pagespeed version no longer shown in headers https://github.com/wodby/nginx/issues/32
- Alpine Linux updated to 3.9.4

### 0.7.1

- Matomo and Adminer rebuilt against the latest PHP image
- Nginx:
    - Updated to 1.15.11
    - Default static files expiration increased to 1 year https://github.com/wodby/nginx/pull/30
- Alpine Linux updated to 3.9.3 for Matomo, Adminer, MariaDB, Redis, OpenSMTPD

### 0.7.0

Matomo updated to 3.9.1 and rebuilt against the latest PHP image 

### 0.6.1

Matomo updated to 3.8.1 and rebuilt against the latest PHP image 

### 0.6.0

- Matomo updated to 3.8.0 and rebuilt against the latest PHP image
- We now fix permissions for `config/config.ini.php` so you can customize settings from SSH container 
- GeoIP 2 database now included, see [how enable geolocation](#geolocation)

### 0.5.0

* Matomo updated to 3.7.0 and rebased on the latest PHP image
* MariaDB:    
    * Patch updates: 10.3.11, 10.2.19
    * We now run `mysql_upgrade` automatically on stack upgrades      
    * Import action now allows `*.mysql` files      
* Redis patch updates: 5.0.3, 4.0.12
* Nginx patch updates: 1.15.7, 1.14.2
* Adminer updated to 4.7.0 and rebased on the latest PHP image 

### 0.4.9

* Matomo rebased on the latest PHP image
* Added Redis 5
* Nginx:
    * Patch updates: 1.15.6, 1.14.1
    * Nginx now uses real IP set from Edge
    * Bugfix: `txt` was missing from the default list of static extensions

### 0.4.8

Matomo patch update: 3.6.1

### 0.4.7

* Matomo rebased to the latest stable PHP image
* Adminer: 
    * Bugfix: some `$PHP_` env vars were ignored
    * Default memory limit set to 512M
    * Adminer and Webgrind rebuilt against the latest PHP image

### 0.4.6

* Matomo rebased to the latest stable PHP version
* Added Adminer service 

### 0.4.5

Matomo rebased to the latest stable PHP version 

### 0.4.4

PHP security updates

### 0.4.2

Minor Nginx fixes

### 0.4.1

* Matomo image updated to the latest PHP image
* Minor Nginx fixes

### 0.4.0

* Matomo updated to 3.6.0
* Patch updates for PHP, Nginx and MariaDB

### 0.3.1

* Matomo updated to 3.5.1
* Added Nginx 1.14, 1.15
* MariaBD:
    * Added new version 10.3
    * Version 10.2 updated to 10.2.15
    * Default `innodb_buffer_pool_size` set to `128M` that should significantly decrease memory usage
* PHP error reporting now exludes strict and deprecated errors

### 0.3.0

* Matomo updated to 3.5.0
* Added SSHD container
* Matomo image rebased to latest stable PHP 7.1 image (`wodby/php:7.1-4.4.2`)

### 0.2.1

* Bugfix: cron task failed

### 0.2.0

* PHP updated to 7.1.15 (security updates)
* Redis service added
* Docs: added instructions for redis and email configuration
* Bugfix: insufficient permissions for plugins install

### 0.1.0

* Initial release
