### NewRelic

You can add NewRelic APM monitoring for PHP by adding environment variables `PHP_NEWRELIC_ENABLED=1` and `PHP_NEWRELIC_LICENSE` with your license number to PHP-FPM container. Application name will be automatically set to `[Wodby Application Name] - [Wodby Instance Name]`, if you want to change it, use `PHP_NEWRELIC_APPNAME`. 

### Profiling

!!! warning "Must know before using profiler" 
    * Both XHProf and Xdebug profiling decreases performance and increases resources usage, especially xdebug. Try to avoid using in production
    * Traces files take a lot of disk space and may cause out of disk space very quickly

#### XHProf

Enable XHProf extension (from Tideways) by adding the environment variable `$PHP_XHPROF=1` to your PHP container.

Use the following example snippet to profile your code:

```php
// Start profiling.
if (extension_loaded('tideways_xhprof')) {
    tideways_xhprof_enable(TIDEWAYS_XHPROF_FLAGS_MEMORY | TIDEWAYS_XHPROF_FLAGS_CPU);
}

// Code which should be profiled.
// ...

// Store profile.
if (extension_loaded('tideways_xhprof')) {
    $xhprof_out = '/mnt/files/private/xhprof';
    
    if (!file_exists($xhprof_out)) {
        mkdir($xhprof_out);
    }

    file_put_contents(sprintf('%s/%s.%s.xhprof', $xhprof_out, uniqid(), 'web'), serialize(tideways_xhprof_disable()));
}
```    

Once traces files generated you can view and analyze your traces via [XHProf viewer](#xhprof-viewer)

#### Xdebug profiler

Enable XDebug profiling by adding the following environment variables to your PHP container:

```
PHP_XDEBUG: 1
PHP_XDEBUG_PROFILER_ENABLE: 1
PHP_XDEBUG_PROFILER_ENABLE_TRIGGER: 1
PHP_XDEBUG_PROFILER_ENABLE_TRIGGER_VALUE: 1
```

Add `XDEBUG_PROFILE=1` param to GET or POST request (or set a cookie) you want to profile. Xdebug will generate profile files in `/mnt/files/xdebug/profiler`. Click Update in Webgrind to access the new information. See https://xdebug.org/docs/profiler to learn more about xdebug profiling.

Once traces files generated you can view and analyze your traces via [Webgrind](#webgrind)

### Xdebug

!!! info "Debugging locally"
    For using xdebug locally see [documentation for local environment](local.md)

Follow these steps to debug your application instance remotely with [xdebug](http://xdebug.org/docs/install):

1. Enable xdebug for your instance from `[Instance] > Stack > Settings`
2. Set up forwarding for xdebug: copy _Xdebug SSH tunnel_ command from `[Instance] > Stack > PHP` and run on your local machine
3. Make sure you have your IDE xdebug listener running on port 9000
4. Start debugging in IDE
5. Start your browser debug helper plugin ([Chrome](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en) or [Firefox](https://addons.mozilla.org/en-us/firefox/addon/the-easiest-xdebug)) and open the page you want to debug

For xdebug troubleshooting enable logs by adding `$PHP_XDEBUG_REMOTE_LOG=/tmp/php-xdebug.log` environment variable to PHP container.

{!xdebug-log.md!}
