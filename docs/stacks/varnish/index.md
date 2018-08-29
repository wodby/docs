# Varnish stack documentation

Varnish can be configured with the following [environment variables](https://github.com/wodby/varnish#environment-variables)

## CLI

Grouped list with the most usual entries from different logs:
```bash
varnishtop
```

A histogram that shows the time taken for the requests processing:
```bash
varnishhist
```

Varnish stats, shows how many contents on cache hits, resource consumption, etc..:
```bash
varnishstat
```

Log showing requests made to the web backend server:
```bash
varnishlog
```

## Troubleshooting 503 (guru meditation) errors

You can get more details on 503 responses by filtering the logs:
```bash
varnishlog -q 'RespStatus == 503' -g request
```

A few reasons why you may get 503:

* A problem on backend, see backend container's logs
* Varnish may cache non-broken page from backend when backend gives 5xx, in this cases you will sometimes get 503 (fetch from backend) and sometimes 200 OK (from cache)
* Broken backend headers that prevent from parsing backend response's body, e.g. gzip encoding header when the body in fact is not gzipped (you should not gzip pages on your backend, we already do that on Nginx)  
* Timeouts on varnish are too low (unlikely, the defaults are high enough for 95% cases), you can increase them via environment variables 

## Further reading (official documentation)

* [Varnish book: 4.0 basics and workflow schema](https://book.varnish-software.com/4.0/chapters/VCL_Basics.html)
* [Built in subroutines](https://varnish-cache.org/docs/trunk/users-guide/vcl-built-in-subs.html)

## Changelog

This changelog is for Varnish stack on Wodby, to see image changes see tags description on [repository page](https://github.com/wodby/varnish/releases).

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