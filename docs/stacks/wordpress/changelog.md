# WordPress stack changelog

This is the changelog for WordPress stack deployed via Wodby, for docker4wordpress changes see [GitHub releases page](https://github.com/wodby/docker4wordpress/releases).

## 5.1.0

* Vanilla WordPress core updated to 4.9.6
* PHP
  * Added php tidy extension
  * Added tideways xhprof extension https://github.com/wodby/drupal-php#49 (disabled by default)
  * `auto_prepend_file` and `auto_append_file` are now configurable
  * Updated PHP extensions: GRPC 1.12.0, igbinary 2.0.6, mongodb 1.4.4
* MariaDB:
  * New version 10.3 added (10.3.7)
  * MariaDB updates: 10.2.15, 10.1.34
  * `optimizer_prune_level` and `optimizer_search_depth` are now configurable https://github.com/wodby/mariadb/issues/4
  * ⭐️ Default `innodb_buffer_pool_size` set to `128M` that should significantly decrease memory usage by MariaDB container
  * Default  `innodb_buffer_pool_instances` set to `1`
* Nginx:
  * Added new Nginx 1.15
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
  * Unrestricted purge is now allowed in internal network (from containers within the same instance)
* Webgrind: error reporting now exludes strict and deprecated errors, rebased to latest PHP 7.1 image

## Upgrade instructions

* ❗Make sure the new default size of `innodb_buffer_pool_instances` (128M) is enough for your project, see [MariaDB stack documentation](https://cloud.wodby.com/stackhub/3aa42a7c-db8b-40e9-aa3c-06218724fae6/overview) to learn how to calculate the optimal size of `innodb_buffer_pool_size` for your application

## 5.0.11

* PHP:
  * **Security update**: 7.2.5, 7.1.17, 7.0.30, 5.6.36
  * New php extensions added: [GMP](http://php.net/manual/en/book.gmp.php) and [igbinary](https://github.com/igbinary/igbinary/)
  * APCu extension updated to 5.0.11 for PHP 7.x
  * APCu serialized is now configurable with `$PHP_APCU_SERIALIZER`
  * Shell prompt in PHP containers now shows current user, application name and instance name
  * Added new helper script [`files_chown`](https://github.com/wodby/php#users-and-permissions)
  * Bugfix: iconv implementation missing [wodby/php#25](https://github.com/wodby/php/issues/25)
* Varnish purge via HTTP is now unrestricted with a purge key, see [updated docs](https://wodby.com/stacks/wordpress/docs/containers/varnish/)
* Added Nginx 1.14, patch update for 1.13
* Nginx's `underscores_in_headers` is now configurable via `$NGINX_UNDERSCORES_IN_HEADERS`

## 5.0.10

* PHP [log errors max length](http://php.net/manual/en/errorfunc.configuration.php#ini.log-errors-max-len) set to unlimited
* Bugfix: PHP errors didn't show up in the container output
* Bugfix: `APACHE_LIMITED_ACCESS` support from 5.0.6 release was missing

## 5.0.9

* Vanilla WordPress updated to [4.9.5](https://wordpress.org/news/2018/04/wordpress-4-9-5-security-and-maintenance-release/) (**security and maintenance release**)

## 5.0.8

* PHP 5.6 version returned

## 5.0.7

* PHP:
  * Updated to 7.2.4, 7.1.16, 7.0.35 (**security update**)
  * Added [jpegoptim](https://github.com/tjko/jpegoptim)
  * Added [writable permission to FPM for 'wp-content/wp-rocket-config/'](https://github.com/wodby/docker4wordpress/issues/31)

## 5.0.6

* Apache:
  * Updated to 2.4.33 (**security update**)
  * New environment variable `APACHE_LIMITED_ACCESS` to remove `Require all granted` when you need to limit access by IP

## 5.0.5

* Nginx updated to 1.13.10
* PHP extension grpc updated to 1.10.0
* Added environment variables for PHP session runtime configuration
* Improved error reporting and progress messages for public files directory init
* Bugfix: apache settings file didn't include when virtual host config overridden with `APACHE_INCLUDE_CONF`

## 5.0.4

* Bugfix: vanilla WordPress didn't work with PHP 7.2
* Bugfix: `wp-admin/` with apache redirected to homepage
* Bugfix: some caching plugins didn't work because of unsufficient permissions
* Added `APACHE_INCLUDE_CONF` to override apache config
* Database service is now optional in case you want to have a stand-alone DB server
* Redis service is not included by default

## 5.0.3

* Cron now runs from `www-data` user instead of `wodby`
* [`files_chmod`](https://github.com/wodby/php#users-and-permissions) script now sets permissions with execution allowed only for directories

## 5.0.2

* Bugfix: translation update fail due to insufficient permissions

## 5.0.1

* PHP updated to 7.2.3, 7.1.15, 7.0.28 (security updates)
* Bugfix: insufficient permissions for plugins update
* Bugfix: missing `~/.ssh` directory for www-data user required by some plugins

## 5.0.0

### Changes since 4.4.1

* All containers now have [resources request](../config.md#resources) as listed [here in Resources column](https://wodby.com/stacks/wordpress/docs/containers/), in addition, crond has CPU limit
* PHP:
  * Container default user has been changed to `wodby` (uid/gid 1000), see https://github.com/wodby/php#users-and-permissions for more details
  * PHP updated to 7.2.2, 7.1.14, 7.0.27 (security updates)
  * Rebased to Alpine Linux 3.7
  * Now when your upgrade stack with a new version of vanilla WordPress, your source code will be updated
  * You can [monitor PHP with NewRelic APM](https://wodby.com/stacks/wordpress/docs/containers/php/#newrelic-apm-monitoring)
  * `allow_url_fopen` and `default_socket_timeout` is now configurable
  * New php extensions added: newrelic, grpc, ds
  * Deprecated environment variables dropped (listed in [4.4.0 changes](#440))
  * Added postgresql client bins (pg_dump, pg_restore, ...)
  * Added redis-cli
  * Updated php extensions: amqp 1.9.3, redis 3.1.6, mongodb 1.4.0, apcu 5.1.10
  * Environment variable `WODBY_DIR_FILES` replaced to `FILES_DIR`
  * Bugfix: cache clearing from dashboard didn't work for subdirectories
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

* Make sure you don't use any of deprecated environment variables in PHP (listed in [4.4.0 changes](#440)) and Varnish (listed above) otherwise update their names
* If you used `WODBY_DIR_FILES` in your code replace it with `FILES_DIR`
* Make sure the default cron container 512M RAM limit is enough for your cron jobs, otherwise increase it manually from service configuration page

## 4.1.1

* Restored MariaDB 10.1 `innodb_large_prefix` setting (enabled by default) removed in 4.4.0

## 4.1.0

### Changes since 4.0.0

* PHP:
  * New PHP 7.2
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
  * Improved validation and error reporting for duplicator import
  * Git email and name now can be configured via environment variables
* Nginx:
  * Nginx updated to 1.13.7, 1.12.2
  * Fixed broken health check
  * New env var `NGINX_NO_DEFAULT_HEADERS` to hide default headers
  * We now show request real IP in access logs
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
* Redis:
  * Redis updated to 3.2.11, 4.0.2
  * Fixed init failure when there's no `/sys/kernel/mm/transparent_hugepage/enabled`
* Global environment variables changes:
  * `$WODBY_APP_NAME` no longer contains instance machine name, only application machine name
  * `$WODBY_ENVIRONMENT_` variables have been deprecated and replaced with `$WODBY_INSTANCE_`
  * New variables `$WODBY_INSTANCE_UUID` and `$WODBY_APP_UUID`
* Varnish updated to 4.1.9
* Apache updated to 2.4.29
* Vanilla WordPress updated to 4.9.1
* Health checks timeout increased to 30 seconds for all services
* OpenSMTPD now supports relay auth without password
* Files backup and mirroring actions now run with `nice` and `ionice` to prioritize CPU and I/O time for this process

### Update instructions from 4.0.0

* If you used `$WODBY_APP_NAME` update your code accordingly to the new value (machine name of the app)
* If you used `$WODBY_HOST_PRIMARY` (now contains host instead of URL) before you should replace it to `$WODBY_URL_PRIMARY`
* Upgrade downtime ~5 minutes

## 4.0.0

### Changes since 3.x

* All-new revamped containers consistent with [docker4wordpress](http://github.com/wodby/docker4wordpress/)
* Improved performance of containers (especially I/O)
* Revamped orchestration with better logging and performance
* Optional services now can be enabled/disabled on the working app
* Services configuration via environment variables from the dashboard
* This stack is now suited for container-based cluster
* Log streaming is now available
* Detailed log output for orchestration tasks
* New services: apache, webgrind, blackfire, rsyslog, athenapdf

There's no backward compatibility with stacks 3.x
