# HTML stack documentation

## Deployment

### CI/CD

!!! info "CI/CD tutorial"
    For a detailed instructions of setting up CI/CD workflow see the main [deployment article](/apps/deploy.md#cicd)

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
