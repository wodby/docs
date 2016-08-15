# WordPress bundle

This section contains information related to [the bundle](README.md) for [WordPress websites](../../apps/wordpress/README.md).
    
## Containers

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../containers/redis.md)                |   |
| Mail server           | [OpenSMTPD](../containers/opensmtpd.md)        |   |
| Mail catcher          | [Mailhog](../containers/mailhog.md)            |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |

## Changelog

* [3.2.1](#321)
    * [Changes since 3.2.0](#changes-since-320)
    * [Upgrade policy](#upgrade-policy-321)
* [3.2.0](#320)
    * [Changes since 3.1.1](#changes-since-311)
    * [Upgrade policy](#upgrade-policy-320)
* [3.1.1](#311)
    * [Changes since 3.0.0](#changes-since-310)
    * [Upgrade policy](#upgrade-policy-311)
* [3.1.0](#310)
    * [Changes since 3.0.0](#changes-since-300)
    * [Upgrade policy](#upgrade-policy-310)
* [3.0.0](#300)

### 3.3.0

#### Changes since 3.2.1

* Postfix replaced with an optional container [OpenSMTPD](../containers/opensmtpd.md) (enabled by default)
* New optional container with [Mailhog](../containers/mailhog.md) to catch all outbound emails from your instance 

Release date: `August 15th, 2016`

#### Upgrade policy 3.3.0

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~5 minutes.

### 3.2.1

#### Changes since 3.2.0

* Updated containers' base OS Alpine Linux 3.4.2
* Fixed <a href="https://httpoxy.org/#mitigate-nginx" target="_blank">HTTPoxy vulnerability</a>
* New PHP version 5.6.24 with security updates
* New PHP version 7.0.9 with security updates

Release date: `July 27th, 2016`

#### Upgrade policy 3.2.1

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~5 minutes.

### 3.2.0

#### Changes since 3.1.1

* Added a new tool for [Sass compilation](../../apps/sass.md)
* Fixed a few bugs in [nginx](../containers/nginx-php/nginx.md) config

Release date: `July 14th, 2016`

#### Upgrade policy 3.2.0

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~5 minutes.

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
* [PHP 5.6](../containers/nginx-php/php.md) upgraded to 5.6.22
* [Postfix](../containers/nginx-php/postfix.md) upgraded to 3.1.1
* [MariaDB](../containers/mariadb.md) upgraded to 10.1.14
* [Redis](../containers/redis.md) upgraded to 3.2.0
* Default option `always_populate_raw_post_data = -1` added to php.ini of [PHP 5.6](../containers/nginx-php/php.md) 
* Added mysql_extension (in addition to mysqli_extension) to [PHP 5.6](../containers/nginx-php/php.md)
* Fixed the bug in all [PHP containers](../containers/nginx-php/php.md) with an incorrect value of `error_reporting` for dev instances 

Release date: `June 24th, 2016`

#### Upgrade policy 3.1.0

[Contact our support team](../../product/support.md) to schedule the upgrade. Instance downtime ~10 minutes.

### 3.0.0

Initial bundle version.