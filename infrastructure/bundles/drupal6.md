# Drupal 6 bundle

This section contains information related to [the bundle](README.md) for [Drupal 6 websites](../../apps/drupal/README.md). 

## Containers

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Memcached](../containers/memcached.md)        |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |

## Changelog

* [3.1.1](#311)
    * [Changes since 3.0.0](#changes-since-310)
    * [Upgrade policy](#upgrade-policy-311)
* [3.1.0](#310)
    * [Changes since 3.0.0](#changes-since-300)
    * [Upgrade policy](#upgrade-policy-310)
* [3.0.0](#300)

### 3.1.1

#### Changes since 3.1.0

* Persistent configuration files and data directory for [Redis container](../containers/redis.md) 
* Persistent configuration files for [MariaDB container](../containers/mariadb.md)
* Fixed an issue inside of [Nginx-php container](../containers/nginx-php/README.md) that user IP detected incorrectly when the app is behind a reverse proxy

Release date: `June 30th, 2016`

#### Upgrade policy 3.1.1

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~5 minutes.

### 3.1.0

Minimal [server infrastructure version](../versioning.md) 3.0.0 is required.

#### Changes since 3.0.0

* [Nginx](../containers/nginx-php/nginx.md) upgraded to 1.10.1 
* [Postfix](../containers/nginx-php/postfix.md) upgraded to 3.1.1
* [MariaDB](../containers/mariadb.md) upgraded to 10.1.14
* Fixed the bug in all [PHP containers](../containers/nginx-php/php.md) with an incorrect value of `error_reporting` for dev instances 

Release date: `June 24th, 2016`

#### Upgrade policy 3.1.0

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~10 minutes.

### 3.0.0

Initial bundle version.