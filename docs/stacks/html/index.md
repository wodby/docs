# HTML stack documentation

## Deployment

### CI/CD

!!! info "CI/CD tutorial"
    For a detailed instructions of setting up CI/CD workflow see the main [deployment article](../../apps/deploy.md#cicd)

The following services are CI services that will be built by default:

* HTTP server: `nginx` or `apache`

## Containers

### Nginx

{!containers/nginx.md!}

### Apache

{!containers/apache.md!}

See [details](https://github.com/wodby/apache#html) about virtual host preset.

## Changelog

This changelog is for HTML stack on Wodby, to see images changes see tags description on repository page: [nginx](https://github.com/wodby/nginx/releases) and [Apache](https://github.com/wodby/apache/releases).

### 0.2.11

- Nginx:
    - Updated to 1.15.10
    - Make extra config be able to work without defaults https://github.com/wodby/nginx/pull/27
- Apache base image changed from `wodby/httpd` to `httpd`

### 0.2.10

- Nginx:
  - Patch update: 1.15.9
  - `.map` added to the list of default static files extensions (`$NGINX_STATIC_EXT_REGEX`)
  - Bugfix: `$NGINX_LOG_FORMAT_OVERRIDE` had no effect
- `mod_include` added to Apache https://github.com/wodby/apache/issues/6

### 0.2.9

- Nginx:
  - Patch update: 1.15.8
  - GeoIP module deleted https://github.com/wodby/php/issues/59
  - PageSpeed module now respects `X-Forwarded-Proto` by default
  - Bugfix: dynamic modules image filter and xslt could not be enabled
- Apache:
  - ❕Security update 2.4.38
  - SSL module temporary disabled due to build failures https://github.com/wodby/apache/issues/5

### 0.2.8

* Nginx:
    * Patch updates: 1.15.7, 1.14.2
    * ⭐️  Added [ModSecurity with OWASP CRS](https://github.com/wodby/nginx#modsecurity) (disabled by default) https://github.com/wodby/nginx/pull/13, https://github.com/wodby/nginx/pull/14
    * PageSpeed is now dynamic module, [disabled by default](https://github.com/wodby/nginx#pagespeed)

Update instructions:

* If you used Nginx pagespeed module, add `$NGINX_PAGESPEED_ENABLED=1`, if you had `$NGINX_PAGESPEED=on` you can delete it since it's `on` by default   

### 0.2.7

* Nginx:
    * Patch updates: 1.15.6, 1.14.1
    * Nginx now uses real IP set from Edge

### 0.2.6

* Nginx:
    * Always try index file for / location before 404
    * Remove outdated `*.htm` from the default index file
    * Bugfix: txt was missing from the default list of static extensions

### 0.2.5

* Nginx:
    * Patch update 1.15.5
    * real_ip params are now configurable https://github.com/wodby/nginx/issues/9

### 0.2.4

* Apache:
    * Patch update: 2.4.35
    * Option `Indexes` now disabled by default, can be enabled via `$APACHE_INDEXES_ENABLED`
* Nginx patch update: 1.15.4

### 0.2.3

Nginx: `$NGINX_ERROR_PAGE_40x` replaced to `$NGINX_ERROR_40x_URI`

### 0.2.2

* Nginx no longer hides 50x errors by default, can be enabled via `$NGINX_HIDE_50x_ERRORS`
* Bugfix: env vars `$NGINX_ERROR_PAGE_*` had no effect
* Setting `$NGINX_VHOST_PRESET` to empty value now disables usage of any presets
* New `$NGINX_VHOST_NO_DEFAULTS` to disable default rules for virtual host
* New default 50x error page, new `$NGINX_ERROR_MESSAGE_50x` to add a message on this page

### 0.2.1

Do not add trailing slashes for non-directory requests

### 0.2.0

* Nginx:
    * Nginx patch update: 1.15.3
    * Bugfix: default 404 page did not work in Nginx
    * 403/404 pages now can be customized
    * Nginx image rebased to Alpine Linux 3.8
    * Extended list of static files extensions
    * `$NGINX_STATIC_` that controls settings for handling static content
    * `$NGINX_ALLOW_ACCESS_HIDDEN_FILES` to control access to files starting with a dot
    * Added pseudo-streaming server-side for `.flv` files
    * Added pseudo-streaming server-side for `.mp4`, `.mov`, `.m4a` files. See env vars `$NGINX_STATIC_MP4_*` for configuration
    * Added `.well-known` location by default
    * Updated default values for `open_file_cache` settings
    * Default expires for static content set to `7d` by default
    * Use `$NGINX_LOG_FORMAT_OVERRIDE` log format over `$NGINX_LOG_FORMAT_SHOW_REAL_IP`
Apache:     
    * MPM modules are now shared and can be configured (event is still the default)

### 0.1.0

Initial release
