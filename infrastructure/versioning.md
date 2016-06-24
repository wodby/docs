# Infrastructure versioning

## Overview

We constantly improve the infrastructure we deploy to our customers' servers. You can see the version of the infrastructure deployed to your server in the Dashboard on the servers list page. It's not always possible to update the infrastructure automatically so if you want update your infrastructure please [contact our support team](../product/support.md) to schedule the upgrade. 

You will be notified each time a new version of the infrastructure is released.

## Versions

Stable mainline versions: v3.x.x<br />
Unsupported legacy versions: v0.1.0, v1.0.0, v2.0.0
 
## Changelog

* [v3.5.0](#v350)
    * [Changes since v3.4.0](#changes-since-v340)
    * [Upgrade policy](#upgrade-policy-v350)
* [v3.4.0](#v340)
    * [Changes since v3.3.0](#changes-since-v330)
    * [Upgrade policy](#upgrade-policy-v340)
* [v3.3.0](#v330)
    * [Changes since v3.2.0](#changes-since-v320)
    * [Upgrade policy](#upgrade-policy-v330) 
* [v3.2.0](#v320)
    * [Changes since v3.1.0](#changes-since-v310)
    * [Upgrade policy](#upgrade-policy-v320)
* [v3.1.0](#v310)
    * [Changes since v3.0.0](#changes-since-v300)
    * [Upgrade policy](#upgrade-policy-v310)
* [v3.0.0](#v300)
* [v2.0.0](#v200)
* [v1.0.0](#v100)
* [v0.1.0](#v010)

### v3.5.0

#### Changes since v3.4.0

* Containers base OS Alpine Linux upgraded to 3.4
* [Nginx](containers/nginx-php/nginx.md) upgraded to 1.10.1 
* [PHP 5.6](containers/nginx-php/php.md) upgraded to 5.6.22
* [Postfix](containers/nginx-php/postfix.md) upgraded to 3.1.1
* [MariaDB](containers/mariadb.md) upgraded to 10.1.14
* [Redis](containers/redis.md) upgraded to 3.2.0
* Default option `always_populate_raw_post_data = -1` added to php.ini of [PHP 5.6](containers/nginx-php/php.md) 
* Added mysql_extension (in addition to mysqli_extension) to [PHP 5.6](containers/nginx-php/php.md)
* New container [Varnish](containers/varnish.md) is now available
* New container [PhpMyAdmin](containers/phpmyadmin.md) is now available
* Fixed the bug in all [PHP containers](containers/nginx-php/php.md) with an incorrect value of `error_reporting` for dev instances 

Release date: `June 24th, 2016`

#### Upgrade policy v3.5.0

[Contact our support team](../product/support.md) to schedule the upgrade. Instance downtime ~10 minutes.

### v3.4.0

#### Changes since v3.3.0

* includeSubdomains option removed from [HSTS header](hsts.md)
* Now `X-Robots-Tag` header added always (not only for 20x, 30x response codes)
* New version of Wodby agent. Now with automated infrastructure update (will be announced later)
* Exif extension added to [PHP 5.6, 7](containers/nginx-php/php.md)
* Fixed bug when `X-Wodby-Node` header missed sometimes
* Added default nginx host for port 443 with self-signed certificates 

Release date: `June 16th, 2016`

#### Upgrade policy v3.4.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### v3.3.0

#### Changes since v3.2.0

* <a href="../apps/drupal/settings.html#base-url">$base_url orchestration for Drupal</a>
* <a href="../apps/drupal/settings.html#trusted-hosts-patterns">Auto generation of trusted host patterns for Drupal 8</a>
* [Drupal 7.x, 8.x multi-site support](../apps/drupal/multi-site.md)
* Drupal 8 and WordPress now come with PHP7 and Redis
* [msmtp + opensmtpd replaced with postfix](mta.md)
* Workaround for Drupal `sites/default` auto permissions change. This caused problems when settings.php file was changed

#### Upgrade policy v3.3.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime 10-60 minutes depending on the app type.

### v3.2.0

#### Changes since v3.1.0

* <a href="../apps/domains.html#www-redirects">WWW redirect actions</a> for domains
* <a href="../apps/domains.html#basic-auth">Basic auth</a> configuration
* [Maintenance mode](../apps/maintenance-mode.md)
* Dev, staging instances and all instances accessible by technical `*.wod.by` domains not indexed by search engines (header X-Robots-Tag)  

#### Upgrade policy v3.2.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### v3.1.0

#### Changes since v3.0.0

* Enable <a href="../apps/domains.html#https-ssl-via-lets-encrypt">HTTPS</a> for domains (SSL certificates via Let's Encrypt) 
* <a href="../apps/backups.html#mirroring">Backup mirroring</a> features added.

#### Upgrade policy v3.0.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~1 hour.

### v3.0.0

The latest stable version with completely reworked containers structure.

### v2.0.0

In this version we've moved git to the docroot and made major structural changes.

### v1.0.0

Production-ready version with lots of improvements.

### v0.1.0

The first public version of our infrastructure.
