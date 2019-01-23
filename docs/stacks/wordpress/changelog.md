# WordPress stack changelog

This is the changelog for WordPress stack deployed via Wodby, for docker4wordpress changes see [GitHub releases page](https://github.com/wodby/docker4wordpress/releases).

!!! caution "Changes between your version and the latest"
    Changes and upgrade instructions are relative to a preceding version, e.g. if you're upgrading from version 5.2.0 to 5.2.2 you should also look up version 5.2.1 changes.    
    
## 5.4.2

Bugfix: varnish cached logged-in users
    
## 5.4.1

- Alpine Linux for the services listed below updated to 3.8.2
- Vanilla WordPress updated to 5.0.3
- PHP:
    - ❕Patch updates: 7.3.1, 7.2.14, 7.1.26, 5.6.40
    - GeoIP extension removed https://github.com/wodby/php/issues/59
    - Updated libraries: ImageMagic (7.0.7.39), libjpeg-turbo, MariaDB client (10.2.19)
    - Updated php extensions: AMQP 1.9.4, APCu 5.1.16, Memcached 3.1.3, GRPC 1.17.0, event 2.4.3 
    - The following extensions now added to PHP 7.3: NewRelic, Blackfire, AMQP, Memcached
    - `/var/www/html/bin` added to `$PATH` https://github.com/wodby/php/issues/60
    - Bugfix: event extension could be not be disabled
- Apache:
  - ❕Security update 2.4.38
  - SSL module temporary disabled due to build failures https://github.com/wodby/apache/issues/5    
- Nginx:
    - Patch update: 1.15.8
    - GeoIP module deleted https://github.com/wodby/php/issues/59
    - PageSpeed module now respects `X-Forwarded-Proto` by default
    - Bugfix: dynamic modules image filter and xslt could not be enabled
    - Bugfix: `.well-known/*.txt` were not accessible https://github.com/wodby/nginx/issues/17
- Varnish:
    - Now all WP cookies except [`$VARNISH_WP_PRESERVED_COOKIES`](https://github.com/wodby/varnish#varnish_wp_preserved_cookies) stripped
    - Added support for woocommerce cookies https://github.com/wodby/varnish/issues/11
    - We no longer set `X-Real-IP` header on Varnish
    - Bugfix: cache purge sometimes did not work
    - Bugfix: unrestricted cache purge from internal network did not work https://github.com/wodby/varnish/issues/14
- MariaDB updates: 10.2.21, 10.3.12, ~~10.1.37~~ https://github.com/wodby/mariadb/issues/10
- Webgrind, XHProf, Adminer rebased to the latest PHP image

## 5.4.0

### Changes since 5.3.4

* Vanilla WordPress updated to 5.0
* PHP:
    * ⭐️Added PHP 7.3 ([some extensions not yet supported](https://github.com/wodby/php/issues?q=is%3Aissue+is%3Aopen+label%3A%22PHP+7.3%22))
    * Patch updates: 7.2.13, 7.1.25, 5.6.39
    * Update extensions: yaml 2.0.4, redis 4.2.0, apcu 5.1.14
    * ImageMagick library now comes with disabled openmp
    * Imagick extension enabled back
    * Bugfix: `/home/www-data` owned by wodby https://github.com/wodby/drupal-php/issues/62
* Varnish:
    * ⭐️ Varnish 6.0 added
    * We now compile varnish from sources, Alpine Linux updated to 3.8
    * Patch updates: 4.1.10
    * GeoIP module added and imported by default
    * Added [9 additional modules](https://github.com/wodby/varnish#installed-modules), not imported by default
    * ⭐️ We now [detect country code](https://github.com/wodby/varnish#geoip) and [currency (USD, EUR)](https://github.com/wodby/varnish#currency) and pass it to backend in headers, you can optionally uniquify cache per country or currency
    * ⭐️ You can now personify cache additionally by setting cookies starting with [`VCKEY-`](https://github.com/wodby/varnish#cache-personification)
    * `fbclid` added to stripped query params
    * Adjusted order of included files https://github.com/wodby/varnish/pull/7
    * Bugfix: duplications in `X-Forwarded-For`
    * Deprecated environment variables (listed in [5.2.0](#520)) no longer supported
* Nginx:
    * Patch updates: 1.15.7, 1.14.2
    * ⭐️ Added [ModSecurity with OWASP CRS](https://github.com/wodby/nginx#modsecurity) (disabled by default) https://github.com/wodby/nginx/pull/13, https://github.com/wodby/nginx/pull/14
    * PageSpeed is now dynamic module, [disabled by default](https://github.com/wodby/nginx#pagespeed)
    * `$NGINX_FASTCGI_INDEX` added to separate from index file https://github.com/wodby/nginx/pull/11
    * `index.html` added to index file for PHP-based presets https://github.com/wodby/nginx/pull/11
* MariaDB:    
    * Patch updates: 10.3.11, 10.2.19
    * We now run `mysql_upgrade` automatically on stack upgrades      
    * Import action now allows `*.mysql` files      
* Patch updates: 
    * Redis: 5.0.3, 4.0.12
    * Memcached: 1.5.12
    * Node: 10.14.2, 8.14.0, 6.15.1
    * Elasticsearch/Kibana: 5.6.14
* Adminer updated to 4.7.0  
* Webgrind, adminer and xhprof rebased to the latest PHP image
* ~~Apache patch update: 2.4.37~~ https://github.com/wodby/apache/issues/5
* ~~MariaDB patch update: 10.1.37~~ https://github.com/wodby/mariadb/issues/10

### Update instructions

* If you used [deprecated environment variables](#520) in Varnish updated them to the new version 
* If you used Nginx pagespeed module, add `$NGINX_PAGESPEED_ENABLED=1`, if you had `$NGINX_PAGESPEED=on` you can delete it since it's `on` by default

## 5.3.3

* Bugfix: Nginx did not convert deprecated environment variables to new
    
## 5.3.2

* Added new profiler service [xhprof viewer](https://wodby.com/docs/stacks/wordpress/containers/#xhprof-viewer) for analysis and graphical review of [xhprof traces](https://wodby.com/docs/stacks/wordpress/containers/#xhprof)
* Added Redis 5
* PHP:
    * ❗️imagick extension has been temporary disabled due to stability issues with ImageMagick library https://github.com/wodby/wordpress/issues/1
    * Patch updates: 7.2.12, 7.1.24
    * Added [event](https://pecl.php.net/package/event) extension
    * You can now disable extensions via `$PHP_EXTENSIONS_DISABLE` (separated by comma)
    * Extensions updates: igbinary 2.0.8, ast 1.0.0, grpc 1.16.0
    * `session.save_path` now set to `/mnt/files/sessions` by default for persistent sessions
    * ImageMagick downgraded to 7.0.7.32 with enabled openmp 
    * Bugfix: tideways xhprof extension could not be enabled
* Nginx:
    * Patch updates: 1.15.6, 1.14.1
    * Nginx now uses real IP set from Edge
    * Bugfix: it was not possible to access `*.txt` files from uploads directory
    * Bugfix: default security headers were missing
* Memcached patch update 1.5.12    
* MariaDB 10.0 `innodb_default_row_format` now set to `dynamic` by default
* Webgrind and Adminer rebased to the latest PHP image
* ~~Apache patch update 2.4.37~~ https://github.com/wodby/apache/issues/5
* ~~MariaDB patch update 10.1.17~~ https://github.com/wodby/mariadb/issues/10

## 5.3.1

* PHP:
    * Patch updates: 7.1.23, 7.2.11
    * uuid pecl extension added https://github.com/wodby/php/issues/43
    * oauth extension patch update: 2.0.3
    * PHP env vars moved from FPM config to the general PHP config
    * Bugfix: WP CLI bash completion warning https://github.com/wodby/wordpress-php/issues/4
* Nginx:
    * Patch update 1.15.5
    * real_ip params are now configurable https://github.com/wodby/nginx/issues/9
* Node:
    * Minor updates: 10.12, 8.12
    * Directory `/usr/src/app/node_modules/.bin` added to `$PATH`
* MariaDB patch update 10.3.10
* Adminer:
    * Bugfix: some `$PHP_` env vars were ignored
    * Default memory limit set to 512M
* Adminer and Webgrind rebased to the latest php image

## 5.3.0

### Changes

* PHP:
    * Rebased to Alpine 3.8 with updated runtime libraries
    * ❗️PHP 7.0 will no longer be maintained ([see why?](https://github.com/wodby/php/issues/40))
    * Argon2 password hash supported added to PHP 7.2
    * MongoDB extension updated to 1.5.3
    * WP CLI updated to 2.0.1  
    * Bugfix: segfault in PHP's `mail` function when sent to multiple recipients ([busybox bug](http://lists.busybox.net/pipermail/busybox/2017-August/085798.html))
    * Bugfix: xhprof tideways extension enabled twice
* MariaDB:
    * Patch update: 10.2.18
    * Improved performance for backup orchestration action
* Apache:
    * Patch update: 2.4.35
    * Option `Indexes` now disabled by default, can be enabled via `$APACHE_INDEXES_ENABLED`
* Adminer:
    * Added the default list of plugins, enabled via `$ADMINER_PLUGINS`
    * You can now change Adminer design via `$ADMINER_DESIGN` z   
    * Updated to the latest stable PHP image
* Nginx patch update: 1.15.4
* Varnish: `has_js` cookie no longer stripped
* Webgrind image updated to the latest stable PHP image

### Upgrade instructions

* Switch your application's PHP service implementation from 7.0 to 7.1

## 5.2.5

* PHP:
    * Libraries update: ImageMagick 7.0.8.11, FreeType 2.9.1
    * OpenMP disabled in ImageMagick due to stability issues
    * Bugfix: xhprof (tideways) extension could not be enabled

## 5.2.4

* PHP 
    * ❗️Security updates: 7.2.10, 7.1.22, 7.0.32, 5.6.38
    * Added `$PHP_PHAR_` env vars for Phar runtime configuration
    * Updated PHP extensions:
        * patch: apcu 5.1.12, ds 1.2.6, igbinary 2.0.7, xdebug 2.6.0
        * minor: mongodb 1.5.2, grpc 1.15.0
        * major: redis 4.1.1

## 5.2.3

* Nginx:
    * New 50x error page, use `$NGINX_ERROR_MESSAGE_50x` to add a custom message
    * Env vars `$NGINX_ERROR_PAGE_40x` replaced to `$NGINX_ERROR_40x_URI`

## 5.2.2

* PHP extension XHProf (tideways) updated to 5.0-beta2
* Nginx:
    * Nginx no longer hides 50x errors by default on non-prod instances
    * Setting `$NGINX_VHOST_PRESET` to empty value now disables usage of any presets
    * New `$NGINX_VHOST_NO_DEFAULTS` to disable default rules for virtual host
    * New default 50x error page, new `$NGINX_ERROR_MESSAGE_50x` to add a message on this page
* MariaDB patch update: 10.1.36
* Solr patch update: 6.6.5
* Varnish bugfix: flush action from dashboard failed
* Adminer and Webgrind rebased to the latest stable php image

## 5.2.1

Do not add trailing slashes for non-directory requests

## 5.2.0

### Changes

* Vanilla WordPress core updated to 4.9.8
* PHP:
    * Patch updates: 7.2.9, 7.1.21, 7.0.31, 5.6.37
    * `/var/www/html/vendor/bin` added to `$PATH`    
    * WP CLI upgraded to 2.0.0 and now freezed
    * Added bash completion for WP CLI
    * Added [rdkafka](https://pecl.php.net/package/rdkafka) extension
    * Added `~/.bash_profile` for `wodby` user    
    * PostgreSQL lib updated to 10.5
    * Bugfix: PHP 5.6 missed GMP library
    * Bugfix: incorrect owner on wodby's `~/.shrc`, `~/.bashrc`
    * Bugfix: entrypoint fails when command executed with `--[flag]`
    * Libraries and extensions versions moved out from env vars
* Nginx:
    * Image `wodby/wordpress-nginx` has been replaced with [`wodby/nginx`](https://github.com/wodby/nginx) with [`$NGINX_VHOST_PRESET=wordpress`](https://github.com/wodby/nginx/#virtual-hosts-presets)
    * Nginx updated to 1.15.3
    * Rebased to Alpine Linux 3.8
    * Use of `$NGINX_LOG_FORMAT_OVERRIDE` now prevails use of `$NGINX_LOG_FORMAT_SHOW_REAL_IP`
    * New env vars `$NGINX_ERROR_PAGE_` to customize 403/404 pages location
    * Extended list of static files extensions
    * New env vars `NGINX_STATIC_` to control settings for handling static content
    * New env var `NGINX_ALLOW_ACCESS_HIDDEN_FILES` to control access to files starting with a dot
    * Added pseudo-streaming server-side for `.flv`, `.mp4`, `.mov`, `.m4a` files
    * Env vars `$NGINX_STATIC_MP4_` for mp4 streaming configuration
    * Updated default values for `open_file_cache` settings
    * Default expires for static content set to `7d` by default
    * Bugfix: overriding log format via `$NGINX_LOG_FORMAT_OVERRIDE` produced an error
* Apache:
    * Image `wodby/php-apache` has been replaced with `wodby/apache` with `$APACHE_VHOST_PRESET=php`
    * Env var `$APACHE_SERVER_ROOT` renamed to `$APACHE_DOCUMENT_ROOT` (old name still supported)
    * MPM modules are now shared and can be changed (event is still the default)    
* MariaDB: 
    * MariaDB patch updates: 10.3.9, 10.2.17, 10.1.35
    * Image rebased to Alpine Linux 3.8
    * Backup action performance improvement: no intermediate file created
    * `ionice` no longer used in orchestration actions 
    * Bugfix: triggers duplicated during db dump
    * Bugfix: no privileges before import could cause failure
* Varnish:
    * Image `wodby/wordpress-varnish` now replaced with `wodby/varnish` and `$VARNISH_CONFIG_PRESET=wordpress`
    * External purge now always restricted by purge key
    * Unrestricted purge from the internal network can be optionally enabled (enabled by default)
    * Cache for mobile devices can now be separated or disabled entirely
    * Big files (by default >10M) won't be cached by default
    * Static files cache disabled by default for all presets
    * All varnish-related headers now start with `X-VC-`, e.g. `X-Varnish-Cache` is now `X-VC-Cache`
    * Secondary storage can now be defined for all presets
    * List of static files extensions expanded
    * Analytics/marketing cookies and query params stripped, configurable
    * New env vars to optionally preserve all cookies and query params
    * Query params can be ignored to cache URLs as a single object
    * Purge method now can be changed to regex and exact (respects query params)
    * Hashes and trailing ? stripped from URL before passing to a backend
    * All AJAX requests not cached
    * Error pages 404 and >500 not cached with a configurable grace period
    * Env vars changed for presets (old => new), old variant still supported:
     ```
      VARNISH_ADMIN_SUBDOMAIN => VARNISH_WP_ADMIN_SUBDOMAIN"
      ```
    * Friendly varnish error message by default
* Memcached returned as cache storage service option
* OpenSMTPD patch update: 6.0.3

### Upgrade instructions

* Nginx: if you overridden a virtual host config (via `$NGINX_CONF_INCLUDE`) you'll have to update it from the original `/etc/nginx/conf.d/vhost.conf` and re-apply your changes again

## 5.1.0

### Changes

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

### Upgrade instructions

* ❗Make sure the new default size of `innodb_buffer_pool_instances` (128M) is enough for your project, see [MariaDB stack documentation](../mariadb/index.md) to learn how to calculate the optimal size of `innodb_buffer_pool_size` for your application

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

### Changes

* All containers now have [resources request](../config.md#resources) as listed [here in Resources column](https://wodby.com/stacks/wordpress/docs/containers/), in addition, crond has CPU limit
* PHP:
    * Container default user has been changed to `wodby` (uid/gid 1000), see https://github.com/wodby/php#users-and-permissions for more details
    * PHP updated to 7.2.2, 7.1.14, 7.0.27 (security updates)
    * Rebased to Alpine Linux 3.7
    * Now when your upgrade stack with a new version of vanilla WordPress, your source code will be updated
    * You can [monitor PHP with NewRelic APM](https://wodby.com/stacks/wordpress/docs/containers/php/#newrelic-apm-monitoring)
    * `allow_url_fopen` and `default_socket_timeout` is now configurable
    * New php extensions added: newrelic, grpc, ds
    * Deprecated environment variables dropped (listed in [4.1.0 changes](#410))
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

* Make sure you don't use any of deprecated environment variables in PHP (listed in [4.1.0 changes](#410)) and Varnish (listed above) otherwise update their names
* If you used `WODBY_DIR_FILES` in your code replace it with `FILES_DIR`
* Make sure the default cron container 512M RAM limit is enough for your cron jobs, otherwise increase it manually from service configuration page

## 4.1.1

* Restored MariaDB 10.1 `innodb_large_prefix` setting (enabled by default) removed in 4.4.0

## 4.1.0

### Changes

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

### Upgrade instructions

* If you used `$WODBY_APP_NAME` update your code accordingly to the new value (machine name of the app)
* If you used `$WODBY_HOST_PRIMARY` (now contains host instead of URL) before you should replace it to `$WODBY_URL_PRIMARY`
* Upgrade downtime ~5 minutes

## 4.0.0

### Changes

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
