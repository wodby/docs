# Cachet stack documentation

Cachet can be configured with the following [environment variables](https://github.com/wodby/cachet#environment-variables)

## Mail delivery

{!stacks/_includes/email-delivery-warning.md!}

## Cron

By default we run the following cron command from [crond container](#crond) every hour:

```
/usr/local/bin/php -q ./artisan schedule:run
```

## Containers

### PHP

{!stacks/_includes/containers/php.md!}

### Crond

{!stacks/_includes/containers/php-crond.md!}

### [OpenSMTPD](../opensmtpd/index.md)

### [PostgreSQL](../postgres/index.md)

### [Redis](../redis/index.md)

## Changelog

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

* Updated [Redis (1.0.2)](https://cloud.wodby.com/stackhub/7548eb5a-c61b-4480-9f36-2501917692b3/changelog) and [Postgres (1.0.1)](https://cloud.wodby.com/stackhub/68172333-6d47-46e0-afd9-08c2170a73b0/changelog) services

### 1.0.0

Initial release
