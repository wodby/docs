# Varnish stack documentation

Varnish can be configured with the following [environment variables](https://github.com/wodby/varnish#environment-variables)

## CLI

Grouped list with the most usual entries from different logs:
```shell
varnishtop
```

A histogram that shows the time taken for the requests processing:
```shell
varnishhist
```

Varnish stats, shows how many contents on cache hits, resource consumption, etc..:
```shell
varnishstat
```

Log showing requests made to the web backend server:
```shell
varnishlog
```

## Reload varnish config without restart

```shell
varnishadmin
vcl.load newconfig01 /opt/local/etc/varnish.vcl
vcl.use newconfig01
quit
```

## Troubleshooting 503 (guru meditation) errors

You can get more details on 503 responses by filtering the logs:
```shell
varnishlog -q 'RespStatus == 503' -g request
```

A few reasons why you may get 503:

* A problem on backend, see backend container's logs
* Varnish may cache non-broken page from backend when backend gives 5xx, in this cases you will sometimes get 503 (fetch from backend) and sometimes 200 OK (from cache)
* Broken backend headers that prevent from parsing backend response's body, e.g. gzip encoding header when the body in fact is not gzipped (you should not gzip pages on your backend, we already do that on Nginx)  
* Timeouts on varnish are too low (unlikely, the defaults are high enough for 95% cases), you can increase them via environment variables
* Too big request or response headers 

## Further reading (official documentation)

* [Varnish book: 4.0 basics and workflow schema](https://book.varnish-software.com/4.0/chapters/VCL_Basics.html)
* [Built in subroutines](https://varnish-cache.org/docs/trunk/users-guide/vcl-built-in-subs.html)

## Changelog

This changelog is for Varnish stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/varnish/releases).

### 3.1.5

🏔 Alpine Linux updated to 3.18.3, 3.16.7

### 3.1.4

🏔 Alpine Linux upgraded to 3.17.3, 3.16.5

### 3.1.3

🐞 Incorrect architecture in Alpine Linux https://github.com/alpinelinux/docker-alpine/issues/303#issuecomment-1448126235

### 3.1.2

🏔 Alpine updated to 3.16.4

### 3.1.1

⬆️ Varnish 6.0.11

### 3.1.0

- ℹ️ This update requires server infrastructure at least 5.9.0
- 🏔 Alpine Linux updated to 3.15

### 3.0.25

🏔 Security updates for base OS Alpine Linux

### 3.0.24

🏔 Patch updates for base OS Alpine Linux

### 3.0.23

⬆️ Varnish 6.0.10

### 3.0.22

⬆️ Varnish 6.0.9

### 3.0.21

📜 Query params no longer stripped from static files https://github.com/wodby/varnish/issues/34

### 3.0.20

⬆️&nbsp; Varnish 6.0.8

### 3.0.19

📦&nbsp; Base OS Alpine Linux updated to 3.13.5

### 3.0.18

⬆️&nbsp; Base image Alpine Linux updated to 3.13.2

### 3.0.17

- ⬆️&nbsp; Base image Alpine Linux updated to 3.12.3
- 🦴&nbsp; `ImagePullPolicy` changed to `IfNotPresent`

### 3.0.16

Varnish 6.0.7

### 3.0.15

Base OS Alpine Linux updated to 3.12.0

### 3.0.14

Base OS Alpine Linux updated to 3.11.6

### 3.0.13

Varnish 6.0.6

### 3.0.12

- Added liveness check, improved performance of readiness checks

### 3.0.11

- Varnish updated to 6.0.5
- Varnish modules now installed from branch 6.0 https://github.com/varnish/varnish-modules/issues/144
- Drupal preset bugfix: private files access restricted with enabled static files cache https://github.com/wodby/varnish/issues/24
- Alpine Linux updated to 3.10.3

### 3.0.10

Security update 6.0.4

### 3.0.9

Alpine Linux updated to 3.10

### 3.0.8

- `webp` added to the list of default static file extensions
- PageSpeed downstream caching:
    - PS-CapabilityList now set to "fully general optimizations only" only if static files cache enabled
    - Bugfix: caching for text/html was disabled

### 3.0.7

Varnish now supports modpagespeed downstream caching https://github.com/wodby/varnish

### 3.0.6

- WordPress preset: added strict rule to avoid infinite loop in some cases https://github.com/wodby/varnish/pull/20 
- Alpine Linux updated to 3.9.4

### 3.0.5

Alpine Linux updated to 3.9.3

### 3.0.4

Bugfix: varnish GeoIP did not work (now uses `X-Real-IP` header instead of `X-Forwarded-For`) https://github.com/wodby/varnish/pull/18

### 3.0.3

- Patch updates: 4.1.11, 6.0.3
- Bugfix: cookie always stripped for static files requests

### 3.0.2

WordPress preset bugfix: varnish cached logged-in users

### 3.0.1

- We no longer set `X-Real-IP` header on Varnish
- Bugfix: cache purge sometimes did not work
- Bugfix: unrestricted cache purge from internal network did not work https://github.com/wodby/varnish/issues/14
- WordPress preset: 
    - Now all WP cookies except [`$VARNISH_WP_PRESERVED_COOKIES`](https://github.com/wodby/varnish#varnish_wp_preserved_cookies) stripped
    - Added support for woocommerce cookies https://github.com/wodby/varnish/issues/11

### 3.0.0

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

### 2.0.2

* `has_js` cookie no longer stripped

### 2.0.1

Bugfix: flush action from dashboard failed

### 2.0.0

* Default config without a preset now also caches (see [default behavior](https://github.com/wodby/varnish#default-behaviour))
* External purge now always restricted by purge key
* Unrestricted purge from the internal network can be optionally enabled (enabled by default)
* Cache for mobile devices can now be separated or disabled entirely
* Big files (by default >10M) won't be cached by default
* Static files cache disabled by default for all presets
* All varnish-related headers now start with X-VC-, e.g. X-Varnish-Cache is now X-VC-Cache
* Secondary storage can now be defined for all presets
* List of static files extensions expanded
* Analytics/marketing cookies and query params stripped, configurable
* New env vars to optionally preserve all cookies and query params
* Query params can be ignored to cache URLs as a single object
* Purge method now can be changed to regex and exact (respects query params)
* Hashes and trailing ? stripped from URL before passing to a backend
* All AJAX requests not cached
* Error pages 404 and >500 not cached with a configurable grace period
* Friendly varnish error message by default

### 1.2.0

Environment variable `VARNISHD_STORAGE_SIZE` has been dropped, we no longer add a predefined secondary storage. You can now add your custom secondary storage via `VARNISHD_SECONDARY_STORAGE` https://github.com/wodby/varnish/pull/4

### 1.1.0

* Default [memory request](../config.md#resources) set to 16m
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


### 1.0.3

* Varnish updated to 4.1.9
* Health check timeout increased to 30 seconds

### 1.0.2

* Varnish daemon env vars now start from VARNISHD_ to avoid collisions

### 1.0.1

* Health check improvement, now uses varnishadm instead of curl

### 1.0.0

Initial release