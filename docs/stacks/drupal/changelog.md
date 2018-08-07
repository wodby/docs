# Drupal stack changelog

This is the changelog for Drupal stack deployed via Wodby, for docker4drupal changes see [GitHub releases page](https://github.com/wodby/docker4drupal/releases).

## 5.1.0

* Drupal
    * Vanilla Drupal core updated to 8.5.4
    * We now set `$settings['reverse_proxy_addresses']` and `$settings['reverse_proxy']` in `wodby.settings.php` file. You can also add additional proxy addresses via env var `DRUPAL_REVERSE_PROXY_ADDRESSES`
* PHP
    * ⭐️ Added new PHP 7.2
    * Added php tidy extension
    * Added tideways xhprof extension https://github.com/wodby/drupal-php#49 (disabled by default)
    * `auto_prepend_file` and `auto_append_file` are now configurable
    * Updated PHP extensions: GRPC 1.12.0, igbinary 2.0.6, mongodb 1.4.4
* MariaDB:
    * New version 10.3 added (10.3.7)
    * MariaDB updates: 10.2.15, 10.1.34
    * `optimizer_prune_level` and `optimizer_search_depth` are now configurable https://github.com/wodby/mariadb/issues/4
    * ⭐️ Default `innodb_buffer_pool_size` set to `128M` that should significantly decrease memory usage by MariaDB container. See [MariaDB stack documentation](https://cloud.wodby.com/stackhub/3aa42a7c-db8b-40e9-aa3c-06218724fae6/overview) to learn how to calculate the optimal size of `innodb_buffer_pool_size` for your application
    * Default `innodb_buffer_pool_instances` set to `1`
* Nginx:
    * Added new Nginx 1.15, dropped legacy Nginx 1.12
    * ⭐️ Added [mog_pagespeed](https://www.modpagespeed.com/) module. Disabled by default, to enable add `NGINX_PAGESPEED=on` to nginx service
    * Added new modules:
    ```
    http_image_filter_module
    http_slice_module
    http_xslt_module
    stream_geoip_module
    stream_realip_module
    stream_ssl_preread_module
    ```
* Varnish
    * Environment variable `VARNISHD_STORAGE_SIZE` has been dropped, we no longer add a predefined secondary storage. You can now add your custom secondary storage via `VARNISHD_SECONDARY_STORAGE` https://github.com/wodby/varnish/pull/4
    * ❗Static files no longer cached unless you set `VARNISH_CACHE_STATIC_FILES` https://github.com/wodby/drupal-varnish/pull/4
    * Added `VARNISH_SECONDARY_STORAGE_CONDITION` to specify the condition when to use secondary storage https://github.com/wodby/drupal-varnish/pull/3
* Webgrind: error reporting now exludes strict and deprecated errors, rebased to latest PHP 7.1 image

## Upgrade instructions

* ❗Make sure the new default size of `innodb_buffer_pool_instances` (128M) is enough for your project, see [MariaDB stack documentation](https://cloud.wodby.com/stackhub/3aa42a7c-db8b-40e9-aa3c-06218724fae6/overview) to learn how to calculate the optimal size of `innodb_buffer_pool_size` for your application

## 5.0.7

* PHP:
    * **Security update**: 7.2.5, 7.1.17, 7.0.30
    * New php extensions added: [GMP](http://php.net/manual/en/book.gmp.php) and [igbinary](https://github.com/igbinary/igbinary/)
    * APCu extension updated to 5.0.11 for PHP 7.x
    * APCu serialized is now configurable with `$PHP_APCU_SERIALIZER`
    * Shell prompt in PHP containers now shows current user, application name and instance name
    * Added new helper script [`files_chown`](https://github.com/wodby/php#users-and-permissions)
    * Bugfix: iconv implementation missing [wodby/php#25](https://github.com/wodby/php/issues/25)
* Vanilla Drupal:
    * **Security update**: 8.5.3
    * Bugfix: drush cache permission issues [wodby/drupal#261](https://github.com/wodby/docker4drupal/issues/261)
* Drupal node container rebased to [`wodby/node`](https://github.com/wodby/node) with freezed node version
* Added Nginx 1.14, patch update for 1.13
* Nginx's `underscores_in_headers` is now configurable via `$NGINX_UNDERSCORES_IN_HEADERS`

## 5.0.6

* PHP [log errors max length](http://php.net/manual/en/errorfunc.configuration.php#ini.log-errors-max-len) set to unlimited
* Bugfix: PHP errors didn't show up in the container output
* Bugfix: `APACHE_LIMITED_ACCESS` support from 5.0.4 release was missing

## 5.0.5

* PHP:
    * Updated to 7.2.4, 7.1.16, 7.0.35 (**security update**)
    * Added [jpegoptim](https://github.com/tjko/jpegoptim)

## 5.0.4

* Vanilla Drupal updated to 8.5.1 (**security update**)
* Apache:
    * Updated to 2.4.33 (**security update**)
    * New environment variable `APACHE_LIMITED_ACCESS` to remove `Require all granted` when you need to limit access by IP

## 5.0.3

* PHP:
    * PHP extension grpc updated to 1.10.0
    * Added environment variables for PHP session runtime configuration
    * Improved error reporting and progress messages for public files directory init
    * Bugfix: global drush used instead of drush launcher
* Solr:
    * New 7.2 version
    * Patch update: 6.6.3
    * Solr 7.x config sources updated to search_api_solr `8.x-2.0-alpha3`
* Nginx updated to 1.13.10
* You can now override apache config with `APACHE_INCLUDE_CONF`

## 5.0.2

* Cron now runs from `www-data` user instead of `wodby`
* Vanilla Drupal updated to 8.5.0
* Drupal console launcher updated to 1.7.0 and freezed
* [`files_chmod`](https://github.com/wodby/php#users-and-permissions) script now sets permissions with execution allowed only for directories

## 5.0.1

* PHP updated to 7.2.3, 7.1.15, 7.0.28 (security updates)
* Global drush freezed to 8.x

## 5.0.0

### Changes since 4.4.1

* All containers now have [resources request](../config.md#resources) as listed [here in Resources column](https://wodby.com/stacks/drupal/docs/containers/), in addition, crond has CPU limit
* PHP:
    * Container default user has been changed to `wodby` (uid/gid 1000), see https://github.com/wodby/php#users-and-permissions for more details
    * PHP updated to 7.1.14, 7.0.27, 5.6.33 (security updates)
    * Rebased to Alpine Linux 3.7
    * Now when your upgrade stack with a new version of vanilla Drupal, your source code will be updated
    * You can [monitor PHP with NewRelic APM](https://wodby.com/stacks/drupal/docs/containers/php/#newrelic-apm-monitoring)
    * `allow_url_fopen` and `default_socket_timeout` is now configurable
    * New php extensions added: newrelic, grpc, ds
    * Global drush updated to 9.x for PHP 7.x
    * Drush launcher updated to 0.5.1
    * Deprecated environment variables dropped (listed in [4.4.0 changes](#4-4-0))
    * Added postgresql client bins (pg_dump, pg_restore, ...)
    * Added redis-cli
    * Updated php extensions: amqp 1.9.3, redis 3.1.6, mongodb 1.4.0, apcu 5.1.10
    * Environment variable `WODBY_DIR_FILES` replaced to `FILES_DIR`
    * Vanilla Drupal updated to 8.4.5
* MariaDB:
    * Updated to 10.1.31, 10.2.12
    * Rebased to Alpine Linux 3.7
* Nginx:
    * Updated to 1.13.9
    * Rebased to Alpine Linux 3.7
* Redis:
    * Updated to 4.0.8
    * Bugfix: redis 4 init could not disable THP on some servers
* OpenSMTPD:
    * Improved health check now runs smtp command
    * Messages queue is now persistent
* Varnish:
    * The following environment variables changed names (old version no longer supported), DEPRECATED > NEW:
    ```
    VARNISHD_THREAD_POOLS > VARNISHD_PARAM_THREAD_POOLS
    VARNISHD_THREAD_POOL_ADD_DELAY > VARNISHD_PARAM_THREAD_POOL_ADD_DELAY
    VARNISHD_THREAD_POOL_MIN > VARNISHD_PARAM_THREAD_POOL_MIN
    VARNISHD_THREAD_POOL_MAX > VARNISHD_PARAM_THREAD_POOL_MAX
    ```
    * Changed default values:
    ```
    VARNISHD_PARAM_THREAD_POOL_ADD_DELAY from 2 to 0.000
    VARNISHD_PARAM_THREAD_POOLS from 1 to 2
    VARNISHD_PARAM_THREAD_POOL_MAX from 1000 to 5000
    ```
    * Added additional env vars that control varnishd params (https://github.com/wodby/varnish/issues/1)
* Bugfix: auth issue in Apache (https://github.com/wodby/php-apache/issues/1)

### Upgrade instructions

* Make sure you don't use any of deprecated environment variables in PHP (listed in [4.4.0 changes](#4-4-0)) and Varnish (listed above) otherwise update their names
* If you used `WODBY_DIR_FILES` in your code replace it with `FILES_DIR`
* Make sure the default cron container 512M RAM limit is enough for your cron jobs, otherwise increase it manually from service configuration page

## 4.4.1

* Vanilla Drupal updated to 8.4.3
* Fixed missing tags for vanilla with PHP 7.0
* Restored MariaDB 10.1 `innodb_large_prefix` setting (enabled by default) removed in 4.4.0

## 4.4.0

### Changes since 4.3.0

* PHP:
    * PHP updated to 7.1.12, 7.0.26
    * PHP extensions updated: memcached 3.0.4, ast 0.1.6
    * Added packages: tig, nano, tmux, less, libjpeg-turbo-utils
    * PHPunit deleted from image to avoid composer conflicts
    * Env vars naming fixes (old names still supported), old > new:
    ```
    PHP_APCU_ENABLE > PHP_APCU_ENABLED
    PHP_FPM_SLOWLOG_TIMEOUT > PHP_FPM_REQUEST_SLOWLOG_TIMEOUT
    PHP_FPM_MAX_CHILDREN > PHP_FPM_PM_MAX_CHILDREN
    PHP_FPM_START_SERVERS > PHP_FPM_PM_START_SERVERS
    PHP_FPM_MIN_SPARE_SERVERS > PHP_FPM_PM_MIN_SPARE_SERVERS
    PHP_FPM_MAX_SPARE_SERVERS > PHP_FPM_PM_MAX_SPARE_SERVERS
    PHP_FPM_MAX_REQUESTS > PHP_FPM_PM_MAX_REQUESTS
    PHP_FPM_STATUS_PATH > PHP_FPM_PM_STATUS_PATH
    ```
    * New `-dev` image tags (replacing `-debug`) for CI/CD (TBA)
    * Env var `WODBY_HOST_PRIMARY` value now contains host (instead of URL) as it should, `WODBY_URL_PRIMARY` has been added for the URL value. See environment variables section
    * Drush launcher added
    * Improved validation and error reporting for drush import
    * Git email and name now can be configured via environment variables
* Nginx:
    * Nginx updated to 1.13.7, 1.12.2
    * Fixed broken health check
    * New env var `NGINX_NO_DEFAULT_HEADERS` to hide default headers
    * We now show request real IP in access logs
    * New env var `NGINX_DRUPAL_FILE_PROXY_URL` to set up static files proxy
* MariaDB:
    * New MariaDB 10.2.11
    * MariaDB updated to 10.1.29
    * Shutdown grace period increased to 5 minutes
    * Deployment strategy no longer can be changed
    * Optimized default config (my.cnf) values
    * New environment variables to configure recovery options
    * Default user/group in a container now `mysql`
    * Backup action now runs with `nice` and `ionice` to prioritize CPU and I/O time for this process
    * Improved error reporting during import
* Solr:
    * New Solr versions 7.0.1 and 7.1.0 have been added
    * Solr versions updated and freezed: 6.6.2, 6.5.1, 6.4.2, 6.3.0, 5.5.5, 5.4.1
    * Config set source search_api_solr updated to 8.x-1.2
    * We now create a default solr core named `default` automatically if no cores found
* Redis:
    * Redis updated to 3.2.11, 4.0.2
    * Fixed init failure when there's no `/sys/kernel/mm/transparent_hugepage/enabled`
* Varnish:
    * Varnish updated to 4.1.9
    * Cache hash id now respects protocol (http/https)
* Global environment variables changes:
    * `$WODBY_APP_NAME` no longer contains instance machine name, only application machine name
    * `$WODBY_ENVIRONMENT_` variables have been deprecated and replaced with `$WODBY_INSTANCE_`
    * New variables `$WODBY_INSTANCE_UUID` and `$WODBY_APP_UUID`
* Apache updated to 2.4.29
* Vanilla Drupal updated to 8.4.2
* Health checks timeout increased to 30 seconds for all services
* OpenSMTPD now supports relay auth without password
* Files backup and mirroring actions now run with `nice` and `ionice` to prioritize CPU and I/O time for this process

### Update instructions from 4.3.0

* If you used `$WODBY_APP_NAME` update your code accordingly to the new value (machine name of the app)
* If you used `$WODBY_HOST_PRIMARY` (now contains host instead of URL) before you should replace it to `$WODBY_URL_PRIMARY`
* Upgrade downtime ~5 minutes

## 4.3.0

### Changes since 4.2.1

* User `www-data` is now default in php, nginx and apache containers
* PHP:
    * PHP updated to 7.0.24, 7.1.10
    * Default vanilla Drupal updated to 8.4.0
    * Core extension pcntl is now enabled in PHP 7.x
    * Libressl added
    * Extensions update: redis 3.1.4, mongodb 1.3.0
    * New extension geoip
    * Default `post_max_size`, `upload_max_filesize` set to 32m
    * Optimized default opcache settings
    * New env var `PHP_MAX_FILE_UPLOADS` to control `max_file_uploads`
    * Bugfix: apcu (PHP 7.x) could cause segfaults in some cases
    * Bugfix: path to CA certificates specified in ldap config
    * Bugfix: files backup could fail when files changed during the process
    * Bugfix: missing quotes in `wodby.sites.php`
* Nginx:
    * Nginx updated to 1.13.5
    * Nginx config revamped: upstream name changed from `backend` to `php` and moved from `nginx.conf` to `drupal.conf`
    * Default `client_max_body_size` set to 32m
    * Bugfix: broken static files on Drupal's 8 update.php page
* Apache:
    * Apache updated to 2.4.28
    * Image has been replaced to generic [`wodby/php-apache`](https://github.com/wodby/php-apache)
* Varnish
    * Env vars for daemon launch params now have prefix `VARNISHD_` to avoid collisions
    * New env vars `VARNISH_EXCLUDE_URLS` and `VARNISH_STATIC_FILES` for customization
    * Default exclude URLs now consider language prefixes
* OpenSMTPD bugfix: health probes caused warning in logs

### Update instructions from 4.2.1

* !!! If you forked `drupal.conf`, you must get the latest version from the source (`/etc/nginx/conf.d/drupal.conf`) and re-apply your changes. If you used `NGINX_SERVER_EXTRA_CONF_FILEPATH`, update usage of `backend` upstream to `php`
* Make sure that the new default value (32m) of php's `post_max_size`, `upload_max_filesize` and nginx's `client_max_body_size` is enough for you
* If you customized varnish launch params, update corresponding env vars prefix to `VARNISHD_`

## 4.2.1

### Changes since 4.2.0

* Improved backward compatibility, the following environment variables are now available from PHP-FPM

## 4.2.0

### Changes since 4.1.9

* PHP updated to 7.1.9, 7.0.23
* PHPUnit updated to 6.3
* New service Blackfire agent for profiling via blackfire.io, see [usage instructions](#blackfire)
* Environment varibles now cleared in PHP-FPM by default except for `WODBY_APP_NAME`, `WODBY_ENVIRONMENT_TYPE`, `WODBY_ENVIRONMENT_NAME`. You can disable it by adding environment variable `PHP_FPM_CLEAR_ENV` with `no` value to Drupal (PHP) container
* OpenSMTPD now supports relay without auth
* Bugfix: PHP-FPM health probes sometimes could fail

### Upgrade notes

Downtime < 5 minutes

## 4.1.9

### Changes since 4.1.8

* Vanilla Drupal updated to 8.3.7
* MariaDB and its client updated to 10.1.26
* Athenapdf versions freeze to 2.10.0
* Bugfix: PHP-FPM health probes sometimes could fail

### Upgrade notes

Downtime 5-10 minutes

## 4.1.8

* Updated service: [Redis (1.0.3)](https://cloud.wodby.com/stackhub/7548eb5a-c61b-4480-9f36-2501917692b3/changelog)
* PHP containers now have health checks and can be upgraded without downtime
* We no longer support `sites/*/files` directories under version control
* Drush modules added: registry rebuild and patchfile
* PHP update: 7.1.8, 7.0.22
* Vanilla Drupal update: 8.3.6
* Nginx update: 1.13.4
* Experimental redis 4.0 added
* You can now enable PHP slowlog via environment variable `PHP_FPM_SLOWLOG_TIMEOUT`
* Improved Varnish health checks, now use varnishadm instead of curl
* Varnish bugfix: duplicated X-Forwarded-For header
* Varnish bugfix: unrestricted purge/ban, now allowed only from internal network

## 4.1.7

* New container [webgrind](https://github.com/jokkedk/webgrind) – Xdebug profiling web frontend
* Additional environment variables for Xdebug extension configuration including tracing and profiling
* PHP extensions update: ast 0.1.5; yaml 2.0.2
* Improvement: better handling of failed deployments
* Bugfix: some environment variable could be unavailble in SSH container

## 4.1.6

* Solr: fixed persistent data paths configuration

## 4.1.5

* New fast health-check endpoints for Nginx and Apache2 hidden from access logs by default
* Updated services: [Redis (1.0.2)](https://cloud.wodby.com/stackhub/7548eb5a-c61b-4480-9f36-2501917692b3/changelog), [MariaDB (1.0.3)](https://cloud.wodby.com/stackhub/3aa42a7c-db8b-40e9-aa3c-06218724fae6/changelog), [AthenaPDF (1.0.1)](https://cloud.wodby.com/stackhub/249c859b-9368-41cc-b6a6-6148e6a77337/changelog)
* PHP extension redis updated to 3.1.3
* Number of default PHP-FPM workers set to 8

## 4.1.4

* PHP updates: [7.1.7](http://php.net/ChangeLog-7.php#7.1.7), [7.0.21](http://php.net/ChangeLog-7.php#7.0.21) with security fixes
* Nginx updates: [1.13.3](http://nginx.org/en/CHANGES), [1.12.1](http://nginx.org/en/CHANGES-1.12) with a fix in the range filter vulnerability (CVE-2017-7529).
* Apache2 updates: [2.4.27](http://www.apache.org/dist/httpd/CHANGES_2.4.27)
* Vanilla Drupal updates: [8.3.5](https://www.drupal.org/project/drupal/releases/8.3.5)
* Solr: new versions 6.6 and 6.5 for Drupal 8
* Solr: search_api_solr version updated from to 8.x-1.0 (default solr configs used from this module)
* Nginx: Content-Type is now set only if not empty https://github.com/wodby/drupal-nginx/issues/27
* Bugfix: some files could be delete during drush import
* Bugfix: vanilla Drupal always re-synced Drupal sources https://github.com/wodby/drupal/issues/2
* Solr versions are now frozen https://github.com/wodby/solr#versions
* Redis version is now frozen https://github.com/wodby/redis#versions

## 4.1.3

* New Apache container
* New Adminer container
* Nginx updated to 1.13.2
* Drupal headers no longer hidden by default, configurable via Nginx/Apache environment variables
* MariaDB now recovers privileges in case of an error during import
* Drupal node container freeze

## 4.1.2

* Updated [MariaDB](https://cloud.wodby.com/stackhub/3aa42a7c-db8b-40e9-aa3c-06218724fae6) with bug fixes
* PHP extension APCu is now configurable
* All PHP extensions are now frozen
* Runtime Alpine Linux libraries used by PHP extension are now frozen
* Dropped few environment variables
* Updated vanilla Drupal: 8.3.4

## 4.1.1

* Updated PHP: 7.1.5 > 7.1.6, 7.0.19 > 7.0.20
* OpenSMTPD can now relay emails to 3rd party SMTP servers
* OpenSMTPD rebased to Alpine 3.6 with freezed version
* Environment variables for OpenSMTPD configuration
* OpenSMTPD now writes logs to container output
* Increased max_allowed_packet for MariaDB daemon
* PHP expose header now disabled by default
* Nginx images rebased to Alpine 3.6
* Updated vanilla Drupal

## 4.1.0

* Bug fix: git checkout in php container sometimes failed
* Bug fix: varnish cache flush action failed
* Bug fix: some environment variables missed in SSH container
* MariaDB: No longer lock table during backups (--single-transaction)
* MariaDB: Excludes cache tables data from backups. See [backups section](#backups) for more details
* Nginx: New version: 1.13.0 > 1.13.1
* PHP: All images rebased to Alpine Linux 3.6 and now use LibreSSL instead of OpenSSL
* PHP: Fixed segfault caused by imagick extension
* PHP: MongoDB extension downgraded to 1.1.10
* New [AthenaPDF](#athenapdf) container – drop-in replacement for wkhtmltopdf
* New [Rsyslog](#rsyslog) container
* New [Node.js](#nodejs) container

## 4.0.1

* Bug fixes and stabilization improvements
* Images versions freeze
* PHP versions freeze

## 4.0.0

### Changes since 3.x

* All-new revamped docker container images consistent with docker4drupal
* Improved performance of containers
* Revamped orchestration with better logging and performance
* Optional services now can be enabled/disabled on the working app
* Services configuration via environment variables from the dashboard
* Services' containers now can can be scaled (# of replicas)
* Detailed log output for orchestration tasks
* Redesigned scalability for cluster deployments

There's no backward compatibility with stacks 3.x
