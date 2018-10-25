!!! warning "Must know before using XDebug profiler" 
    * Xdebug profiling **significantly** decreases performance and increases resources usage. DO NOT USE it in production
    * Xdebug traces files may take a lot of disk space

Webgrind allows you view and analyze Xdebug profiler output and generate call graphs for visualisation. To use Webgrind first enable Xdebug extension with profiling by adding the following environment variables to your PHP container:

```
PHP_XDEBUG: 1
PHP_XDEBUG_PROFILER_ENABLE: 1
PHP_XDEBUG_PROFILER_ENABLE_TRIGGER: 1
PHP_XDEBUG_PROFILER_ENABLE_TRIGGER_VALUE: 1
```

Add `XDEBUG_PROFILE=1` param to GET or POST request (or set a cookie) you want to profile. Xdebug will generate profile files in `/mnt/files/xdebug/profiler`. Click Update in Webgrind to access the new information. See https://xdebug.org/docs/profiler to learn more about xdebug profiling.
