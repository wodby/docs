# Cachet stack documentation

Cachet can be configured with the following [environment variables](https://github.com/wodby/cachet#environment-variables)

## Cron

By default, we run the following cron command from [crond container](#crond) every hour:

```
/usr/local/bin/php -q ./artisan schedule:run
```

## Containers

### PHP

{!containers/php.md!}

### Crond

{!containers/php-crond.md!}

### [OpenSMTPD](../opensmtpd/index.md)

### [PostgreSQL](../postgres/index.md)

### [Redis](../redis/index.md)

## Changelog

This changelog is for Cachet stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/cachet/releases).

### 3.1.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🏔 Alpine Linux updated to 3.15

### 3.0.16

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 3.0.15

Cachet rebuilt against the latest PHP image

### 3.0.14

Cachet downgraded to PHP 7.1 (PHP 7.2 not fully supported)

### 3.0.13

Cachet rebased to PHP 7.2

### 3.0.12

- Cachet rebuilt against the latest PHP image
- Bugfix: crond service missed preloaded icon library

### 3.0.11

Bugfix: duplicated Nginx services (missing version 1.16)

### 3.0.10

Bugfix: default Nginx service version had an incorrect preset that caused 403 Forbidden error.

### 3.0.9

Cachet rebuilt against the latest PHP image

### 3.0.8

- Cachet and Adminer rebuilt against the latest PHP image
- Added new Nginx versions 1.17, 1.16

### 3.0.7

Cachet updated to 2.3.18

### 3.0.6

- Cachet updated to 2.3.17
- Cachet and Adminer rebuilt against the latest PHP image
- Nginx:
    - Added new latest version 1.16
    - Updated to 1.15.12
    - Pagespeed version no longer shown in headers https://github.com/wodby/nginx/issues/32
- Alpine Linux updated to 3.9.4

### 3.0.5

- Cachet and Adminer rebuilt against the latest PHP image
- Nginx:
  - Updated to 1.15.11
  - Default static files expiration increased to 1 year https://github.com/wodby/nginx/pull/30
- Alpine Linux updated to 3.9.3 for Cachet, PostgreSQL, Redis, OpenSMTPD

### 3.0.4

Cachet rebuilt against the latest PHP image

### 3.0.3

Cachet rebuilt against the latest PHP image

### 3.0.2

Cachet rebuilt against the latest PHP image

### 3.0.1

* Redis patch updates: 5.0.3, 4.0.12
* Nginx patch updates: 1.15.7, 1.14.2
* Adminer updated to 4.7.0 and rebased on the latest PHP image 

### 3.0.0

* We changed the way how Cachet works with environment variables and generate `APP_KEY`

### 1.1.11

Bugfix: environment variable for redis connection were missing

### 1.1.10

* Cachet rebased on the latest PHP image
* Added Redis 5
* Nginx:
    * Patch updates: 1.15.6, 1.14.1
    * Nginx now uses real IP set from Edge
    * Bugfix: `txt` was missing from the default list of static extensions
* PostgreSQL 11 added
* PostgreSQL patch updates: 10.6, 9.6.11, 9.5.15, 9.4.20, 9.3.25

### 1.1.9

* Cachet rebased to the latest stable PHP image
* Adminer: 
    * Bugfix: some `$PHP_` env vars were ignored
    * Default memory limit set to 512M
    * Adminer and Webgrind rebuilt against the latest PHP image

### 1.1.8

* Cachet rebased to the latest stable PHP version
* Added Adminer service 

### 1.1.6

Cachet rebased to the latest stable PHP version 

### 1.1.5

PHP security updates

### 1.1.4

Minor Nginx fixes

### 1.1.3

* Rebased Cachet to the latest PHP version
* Minor fixes for Nginx

### 1.1.2

* PHP updated to the latest stable version
* Patch updates for Nginx, PostgreSQL, Redis and OpenSMTPD 

### 1.1.1

* Cachet updated to 2.3.5
* Cachet image rebased to latest wodby/php image
* Added Nginx 1.14, 1.15
* PostgreSQL
    * Version 10 added
    * Version 9.6 updated to 9.6.9
* PHP error reporting now exludes strict and deprecated errors

### 1.1.0

* Nginx image `wodby/cachet-nginx` replaced with `wodby/php-nginx`
* Now when your upgrade stack with a new version of Cachet, your source code will be updated
* Default [memory request](../config.md#resources) set to:
    * Cachet: 64m
    * Crond: 4m
    * PostgreSQL: 64m
    * Redis: 4m
    * OpenSMTPD: 64m

### 1.0.1

* Updated [Redis (1.0.2)](https://wodby.com/docs/stacks/redis#changelog) and [Postgres (1.0.1)](https://wodby.com/docs/postgres#changelog) services

### 1.0.0

Initial release
