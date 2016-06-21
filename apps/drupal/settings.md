# Drupal settings

* [General](#general)
    * [settings.php](#settingsphp)
    * [sites.php](#sitesphp)
    * [Files](#files)
    * [Configuration files](#configuration-files)
    * [Base URL](#base-url)
    * [Cron](#cron)
    * [Sending emails](#sending-emails)
    * [Drush](#drush)
* [Drupal 8](#drupal8)
    * [Trusted hosts patterns](#trusted-hosts-patterns)
    * [Sync directory](#sync-directory)
    * [Twig extension](#twig-extension)

## Basic settings

### settings.php

Wodby automatically adds include of `/srv/wodby.settings.php` to `settings.php` file inside of `sites/default`. If directory doesn't exist Wodby will create it automatically. If you want to use directory other than default please read the [article about multi-site](multi-site.md) configuration.

### sites.php

Wodby automatically generates `sites.php` only when [multi-site](multi-site.md) directory specified. When the multi-site directory specified `sites.php` will contain mapping of all [domains attached via Wodby](../domains.md) to the directory.     

### Files 

Files for Drupal located in `/srv/files` and symlinked to `sites/default/files`.

### Configuration files

Infrastructure configuration files such as nginx.conf located in `/srv/conf` directory.
  
### Base URL

The [domain](../domains.md) marked with primary flag will be used as a `$base_url` in settings.php file and as an `-l` parameter for [cron](#cron).

### Cron

By default cron runs every hour via `drush cron -l {{BASE_URL}}`. [Learn more](../../infrastructure/cron.md) about cron customization.

### Sending emails

Read more about sending emails in [Mail Transfer Agent (SMTP)](../../infrastructure/mta.md) article.

### Drush

Every web container of Drupal instance has pre-installed drush. You can use remotely by using [drush aliases](drush-aliases.md).

## Drupal 8

### Trusted host patterns

For Drupal 8 apps Wodby automatically adds trusted hosts patterns for all [domains attached via Wodby](../domains.md).

### Sync directory

For Drupal 8 apps Wodby automatically creates sync directory with a salt and specify it inside of `wodby.settings.php`.

### Twig extension

Twig C extension is <a href="https://github.com/twigphp/Twig/issues/1695" target="_blank">not yet supported for PHP7</a>.    