# WordPress stack

StackHub URL: 

* [Overview](#overview)
* [Containers](#containers)
  * [Solr](#solr)
  * [MariaDB](#mariadb)
  * [Redis](#redis)
  * [Varnish](#varnish)
* [Mail Transfer Agent](#mail-transfer-agent)
* [Local environment](#local-environment)
* [SSH](#ssh)
* [Cron](#cron)
* [WP CLI](#wp-cli)
* [Environment variables](#environment-variables)
* [Import](#import)

## Overview

[wodby/worpress-nginx]: https://github.com/wodby/worpress-nginx
[wodby/worpress-php]: https://github.com/wodby/worpress-php
[wodby/mariadb]: https://github.com/wodby/mariadb
[wodby/redis]: https://github.com/wodby/redis
[wodby/worpress-varnish]: https://github.com/wodby/worpress-varnish
[wodby/adminer]: https://github.com/wodby/adminer
[phpmyadmin/phpmyadmin]: https://hub.docker.com/r/phpmyadmin/phpmyadmin
[mailhog/mailhog]: https://hub.docker.com/r/mailhog/mailhog

| Container | Image |
| --------- | ----------- |
| Nginx | [wodby/worpress-nginx] |
| PHP | [wodby/worpress-php] |
| [MariaDB](#mariadb) | [wodby/mariadb] |
| [Redis](#redis) | [wodby/redis] |
| [Varnish](#varnish) | [wodby/worpress-varnish] |
| Mailhog | [mailhog/mailhog] |
| PhpMyAdmin | [phpmyadmin/phpmyadmin] |
| Adminer | [wodby/adminer] |

## Containers

### MariaDB

If you want to access the database outside of the Wodby infrastructure you will have to use SSH tunnel via the main container:

1\. Set up SSH tunnel on port `53306` (you can change it). You can find `<SSH Port>` on `[Instance] > Stack > SSH` page. For MySQL (port `3306` by default) use the following command:

```bash
$ ssh -L 53306:mariadb:3306 -p <SSH Port> wodby@<Server IP> -N
```

2\. Connect to the database (mysql) via the tunnel on port `53306`:

```bash
$ mysql --protocol=TCP -P53306 -udrupal -p<MySQL password> drupal
```

### Redis

1. Install and activate <a href="https://wordpress.org/plugins/redis-cache/" target="_blank">redis plugin</a>
2. Go to redis plugin settings page and click "enable object cache" button

### Varnish

1. Install and activate <a href="https://wordpress.org/plugins/vcaching/" target="_blank">Varnish Caching plugin</a>
2. Enable Varnish Caching as shown below:

![](_images/wp-varnish-caching.png)

#### Caching rules

Varnish ignores the following GET parameters for cache id generation:

```
utm_source
utm_medium
utm_campaign
utm_content
gclid
cx
ie
cof
siteurl
```

Set header `Cache-Control:no-cache` to tell Varnish to not cache this page.

#### Headers

* `X-Varnish-Cache`: HIT or MISS, corresponds to when the cache was found or not
* `Age: 34`: age of the cache in seconds
* `X-Varnish: 65658 65623` - the first number is the ID of a request, the second is the ID of cache inside of Varnish. When operating normally the first number changes with every request of the same page and the second stays the same.

#### CLI

Grouped list with the most usual entries from different logs:
```bash
$ varnishtop
```

A histogram that shows the time taken for the requests processing:
```bash
$ varnishhist
```

Varnish stats, shows how many contents on cache hits, resource consumption, etc..:
```bash
$ varnishstat
```

Log showing requests made to the web backend server:
```bash
$ varnishlog
```

## Mail Transfer Agent

MTA server (OpenSMTPD) included to the stack by default. Additionally, you can catch all your emails by adding a mail catcher service (Mailhog).

### Guaranteed delivery of transaction emails

To make sure your transaction emails will be guaranteed delivered we recommend to use Transaction email services such as:

* <a href="http://sendgrid.com/" target="_blank">SendGrid</a> (has a free version). 
* <a href="https://aws.amazon.com/ses/" target="_blank">AWS SES</a>
* <a href="http://mailchimp.com/" target="_blank">Mailchimp</a>

## Local environment

For local environment we recommend using [docker4wordpress](https://github.com/wodby/docker4wordpress) fully consistent with this stack.

## SSH

The copy of PHP container runs with SSHd. You can find access information on `[Instance] > Stack > SSH`

## Cron

The copy of PHP container runs with cron and runs every hour via `wp cron event run`.

## WP CLI

PHP container has pre-installed WP CLI. 

## Environment variables

| Variable  | Description |
| --------- | ----------- |
| `$APP_ROOT`               | `/var/www/html` by default |
| `$HTTP_ROOT`              | `/var/www/html` by default |
| `$WODBY_ENVIRONMENT_NAME` | |
| `$WODBY_ENVIRONMENT_TYPE` | |

## Import

There are different way to import existing WordPress website.

## From duplicator archive

Install <a href="https://wordpress.org/plugins/duplicator/" target="_blank">duplicator plugin</a> on your existing website. Go to admin part of your WordPress website and create a new package via duplicator.

Now navigate to `Apps > Deploy` and choose duplicator archive as data source on the 2nd step.

## From separate archives

Alternatively, you can import WordPress via separate archives for code, database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives.

## Manual

In case your WordPress website is huge it makes sense to import your database/files manually from the server. Follow these steps:

1. Deploy your WordPress website from a git repository without upload database and files
2. Once the app is deployed, go to `Stack > SSH` and copy SSH command
3. Connect the container by SSH and navigate to WordPress docroot (normally it's `/var/www/html`)
4. Copy your database archive here using wget or scp, unpack the archive
5. Import unpacked database dump using `wp dm import my-db-dump.sql`
6. Now let's import your files, cd to `/mnt/files`
7. Copy your files archive here using `wget` or `scp` and unpack the archive
8. That's it! Clear app cache from the dashboard and don't forget to remove archives and extracted db dump
