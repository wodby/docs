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

### 3.0.0

* ⭐️ Varnish 6.0 added
* We now compile varnish from sources, Alpine Linux updated to 3.8
* Patch updates: 4.1.10
* GeoIP module added and imported by default
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