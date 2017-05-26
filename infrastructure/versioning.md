# Infrastructure Versioning

## Overview

This article covers server infrastructure versioning, to learn about stacks versioning see [this article](../stacks/README.md).

We constantly improve the infrastructure we deploy to our customers' servers. You can see the version of the infrastructure deployed to your server in the Dashboard on the servers list page. It's not always possible to update the infrastructure automatically so if you want update your infrastructure please [contact our support team](../product/support.md) to schedule the upgrade. 

You will be notified each time a new version of the infrastructure is released.

## Versions

Stable mainline versions: 5.x<br />
Support ends soon: 3.x<br />
Unsupported legacy versions: 0.1.0, 1.x, 2.x
 
## Changelog

* [5.3.0](#530)
* [5.2.0](#520)
* [5.1.0](#510)
* [5.0.0](#500)
* [3.5.0](#350)
* [3.4.0](#340)
* [3.3.0](#330)
* [3.2.0](#320)
* [3.1.0](#310)
* [3.0.0](#300)
* [2.0.0](#200)
* [1.0.0](#100)
* [0.1.0](#010)

### 5.3.0

#### Changes since 5.2.0

* New kubernetes version
* Improved agent installer
* Enabled unattended upgrades 
* Significantly improved performance (less load on CPU and disk IO)

#### Upgrade policy

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 5.2.0

#### Changes since 5.1.0

* Decoupled services for system containers
* Improved agent installer
* Bug fixes

#### Upgrade policy

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 5.1.0

#### Changes since 5.0.0

* Revamped DNS services
* Improved agent installer
* Bug fixes

#### Upgrade policy

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 5.0.0

#### Changes since 3.5.0

* New kubernetes
* New installer with frozen docker version
* Revamped wodby agent

#### Upgrade policy

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 3.5.0

#### Changes since 3.4.0

* Updated Nginx (1.10.1) for a system container Edge  
* New version of Wodby agent supporting containers upgrade
* New version of orchestration system

Release date: `July 1st, 2016`

#### Upgrade policy 3.5.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 3.4.0

#### Changes since 3.3.0

* includeSubdomains option removed from [HSTS header](hsts.md)
* Now `X-Robots-Tag` header added always (not only for 20x, 30x response codes)
* New version of Wodby agent. Now with automated infrastructure update (will be announced later)
* Exif extension added to PHP 5.6, 7
* Fixed bug when `X-Wodby-Node` header missed sometimes
* Added default nginx host for port 443 with self-signed certificates 

Release date: `June 16th, 2016`

#### Upgrade policy 3.4.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 3.3.0

#### Changes since 3.2.0

* $base_url orchestration for Drupal
* Auto generation of trusted host patterns for Drupal 8
* Drupal 7.x, 8.x multi-site support
* Drupal 8 and WordPress now come with PHP7 and Redis
* msmtp + opensmtpd replaced with postfix
* Workaround for Drupal `sites/default` auto permissions change. This caused problems when settings.php file was changed

#### Upgrade policy 3.3.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime 10-60 minutes depending on the app type.

### 3.2.0

#### Changes since 3.1.0

* <a href="../apps/domains.html#www-redirects">WWW redirect actions</a> for domains
* <a href="../apps/domains.html#basic-auth">Basic auth</a> configuration
* [Maintenance mode](../apps/maintenance-mode.md)
* Dev, staging instances and all instances accessible by technical `*.wod.by` domains not indexed by search engines (header X-Robots-Tag)  

#### Upgrade policy 3.2.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~10 minutes.

### 3.1.0

#### Changes since 3.0.0

* Enable <a href="../apps/domains.html#https-ssl-via-lets-encrypt">HTTPS</a> for domains (SSL certificates via Let's Encrypt) 
* <a href="../apps/backups.html#mirroring">Backup mirroring</a> features added.

#### Upgrade policy 3.0.0

[Contact our support team](../product/support.md) to schedule the upgrade. Downtime ~1 hour.

### 3.0.0

The latest stable version with completely reworked containers structure.

### 2.0.0

In this version we've moved git to the docroot and made major structural changes.

### 1.0.0

Production-ready version with lots of improvements.

### 0.1.0

The first public version of our infrastructure.
