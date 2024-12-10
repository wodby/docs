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

### 3.1.9

⬆️ Nginx 1.27.3

### 3.1.8

⬆️ Nginx 1.27.2

### 3.1.7

🏔️ Alpine Linux security updates (3.20.3)

### 1.0.14

- ⬆️ Nginx 1.27.1, 1.26.2
- ⬆️ Apache HTTPD 2.4.62

### 1.0.13

- Nginx:
    - ⭐️ Added 1.27
    - ⬆️ Updated to 1.26.1
    - 🪦 1.25 has reached end of life
    - ⬆️ Upload progress module updated to 0.9.3
- ⬆️ Apache HTTPd 2.4.61

### 1.0.12

- ⬆️ Apache HTTPd 2.4.59
- Nginx:
    - ⭐️ Added 1.26
    - ⬆️ Updated to 1.25.5
    - 🪦️ Nginx <= 1.24 has reached EOL

### 1.0.11

⬆️ Nginx 1.25.4

### 1.0.10

🏔 Alpine Linux upgraded to 3.19

### 1.0.9

- ⬆️ Nginx 1.25.3
- ⬆️ Apache HTTPd 2.4.58

### 1.0.8

🏔 Alpine Linux 3.18.4

### 1.0.7

🏔 Alpine Linux updated to 3.18.3, 3.16.7

### 1.0.6

⬆️ Nginx 1.25.1

### 1.0.5

- ⭐️ Nginx 1.25, 1.24 added
- 🏔 Alpine Linux upgraded to 3.18 for Apache HTTPD

### 1.0.4

⬆️ Apache HTTPD 2.4.57

### 1.0.3

- ⬆️ Apache HTTPD 2.4.56
- ⬆️ Nginx 1.23.4
- 🏔 Alpine Linux upgraded to 3.17.3, 3.16.5

### 1.0.2

🐞 Incorrect architecture in Alpine Linux https://github.com/alpinelinux/docker-alpine/issues/303#issuecomment-1448126235

### 1.0.1

🏔 Alpine updated to 3.17.2

### 1.0.0

- ⚠️ This version of stack requires server infrastructure 6.0.0+
- ⬆️ Apache 2.4.55
- 🏔 Alpine updated to 3.17 for Nginx

### 0.4.6

⬆️ Nginx 1.23.3

### 0.4.5

🏔 Base OS Alpine Linux updated to 3.16.3 for some of the images

### 0.4.3

⬆️ Nginx 1.23.2, 1.22.1

### 0.4.2

⭐️ Added Nginx 1.23, 1.22

### 0.4.1

⬆️ Apache 2.4.54

### 0.4.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🏔 Alpine Linux updated to 3.15

### 0.3.6

🏔 Security updates for base OS Alpine Linux

### 0.3.5

- ⬆️ Apache HTTPd 2.4.53
- 🏔 Patch updates for base OS Alpine Linux

### 0.3.4

⬆️ Nginx 1.21.6

### 0.3.3

- ⬆️ Nginx:
    - 📜 Default header `Content-Security-Policy` can now be changed with `$NGINX_HEADERS_CONTENT_SECURITY_POLICY ` https://github.com/wodby/nginx/pull/69
    - 📜 `webp` added to the default list of static file extensions
- ⬆️ Apache 2.4.52

### 0.3.2

📜 Nginx: added default `Content-Security-Policy` header (`frame-ancestors 'none'`)

### 0.3.1

- Nginx
    - ⭐️ Version 1.21 added
    - 🐞 Bugfix: default headers do not apply with disabled caching

### 0.3.0

- Nginx:
    - ⭐️ VTS module added, see `$NGINX_METRICS_` and `$NGINX_STATUS_` env vars for usage https://github.com/wodby/nginx/pull/61
    - 📜 `$NGINX_SET_REAL_IPS_FROM` was added to support multiple IP address for `set_real_ip_from` https://github.com/wodby/nginx/pull/62
    - 🥶 brotli and vts modules versions are now frozen https://github.com/wodby/nginx/pull/63
- Apache:
    - ⬆️ Updated to 2.4.51
    - 🥶 Rebased to [wodby/httpd](https://github.com/wodby/httpd) with frozen Alpine 3.13

### 0.2.37

⬆️ Nginx 1.21.4, 1.20.2

### 0.2.36

➕&nbsp; Added Nginx 1.21

### 0.2.35

⬆️&nbsp; Apache 2.4.48
⬆️&nbsp; Nginx 1.20.1

### 0.2.34

⬆️&nbsp; Apache 2.4.47

### 0.2.33

- Nginx:
    - ⭐️&nbsp; New major version 1.20 (now latest)
    - ⬆️&nbsp; Updated to 1.19.10
    - 🪦&nbsp; 1.18 dropped (EOL)
- 📦&nbsp; Base OS Alpine Linux updated to 3.13.5    

### 0.2.32

⬆️&nbsp; Nginx 1.19.8

### 0.2.31

- Nginx:
    - ⬆️&nbsp; Updated to 1.19.7
    - 🚨&nbsp; Pagespeed module dropped due to continued lack of OpenSSL 1.1 support https://github.com/apache/incubator-pagespeed-mod/issues/1856
    - ⬆️&nbsp; Alpine Linux updated from 3.8 to 3.13
    - 📜&nbsp; Added status endpoint https://github.com/wodby/nginx/pull/55

### 0.2.30

- Apache:
    - 🦴&nbsp; `AllowOverride` is now configurable https://github.com/wodby/apache/pull/10
    - 🦴&nbsp; `AllowOverride` is now set to `All` by default for html preset https://github.com/wodby/apache/pull/10      
    - 🦴&nbsp; Apache port is now configurable https://github.com/wodby/apache/issues/8

### 0.2.29

- Nginx:
    - ⬆️&nbsp; Updated to 1.19.6
    - 🐞&nbsp; Custom preset checked incorrectly https://github.com/wodby/nginx/issues/53
- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 0.2.28

Nginx 1.19.4

### 0.2.27

Nginx 1.19.3

### 0.2.26

- Apache 2.4.46
- Nginx 1.19.2

### 0.2.25

Nginx 1.19.1

### 0.2.24

- Nginx: new versions added: 1.19 and 1.18
- Apache: access to all hidden files except `.well-known` is now forbidden

### 0.2.23

- Nginx:
    - Updated to 1.17.10
    - Access to `/wp-content/uploads/woocommerce_uploads` is now forbidden
- Base OS Alpine Linux updated to 3.11.6

### 0.2.22

- Nginx:
    - Updated to 1.17.9
    - Added `/ads.txt` location support https://github.com/wodby/nginx/pull/44
    - Bugfix: 403 on `/.well-known` locations
- Apache HTTPd:
    - Updated to 2.4.43
    - Added `proxy_http_module` https://github.com/wodby/apache/issues/6

### 0.2.21

- Nginx:
  - `/.well-known` URIs excluded from denied hidden files location instead of explicitly allowed
  - Locations `wodby.yml` and `Makefile` are now forbidden
- Apache hidden files, directories, `wodby.yml`, `Makefile` and certain extension are now forbidden

### 0.2.20

- Nginx:
    - Updated to 1.17.6
    - Brotli compression level set to 1 https://github.com/wodby/nginx/issues/40
- Added liveness checks for Nginx and Apache
- Improved performance for Apache and Nginx readiness checks

### 0.2.19

- Nginx:
  - Updated to 1.17.5
  - Added brotli compression extension (enabled by default in addition to gzip) https://github.com/wodby/nginx/issues/37
- Alpine Linux updated to 3.10.3 for Nginx and Apache

### 0.2.18

Nginx 1.17.4

### 0.2.17

- Nginx 1.17.3, 1.16.1
- Apache 2.4.41

### 0.2.16

- Updated to 1.17.2
- Added default location `humans.txt` https://github.com/wodby/nginx/pull/35

### 0.2.15

Nginx updated to 1.17.1

### 0.2.14

Added new Nginx version 1.17

### 0.2.13

- Nginx:
    - Added new latest version 1.16
    - Updated to 1.15.12
    - Pagespeed version no longer shown in headers https://github.com/wodby/nginx/issues/32
- Alpine Linux updated to 3.9.4 for Nginx and Apache 

### 0.2.12

- Nginx:
    - Updated to 1.15.11
    - Default static files expiration increased to 1 year https://github.com/wodby/nginx/pull/30
- ❗️Apache security update: 2.4.39
- Alpine Linux updated to 3.9.3 for Nginx and Apache 

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
