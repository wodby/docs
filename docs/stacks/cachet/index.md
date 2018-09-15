# Cachet stack documentation

Cachet can be configured with the following [environment variables](https://github.com/wodby/cachet#environment-variables)

## Mail delivery

{!email-delivery-warning.md!}

## Cron

By default we run the following cron command from [crond container](#crond) every hour:

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
