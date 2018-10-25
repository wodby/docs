XHProf viewer allows you view and analyze XHProf traces output and generate call graphs for visualisation. To use XHProf first enable Tideways XHProf profiler by adding environment variable `$PHP_XHPROF=1`

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

!!! warning "Must know before using XHProf" 
    * XHProf decreases performance and increases resources usage. Be careful while using in production
    * XHProf traces files may take a lot of disk space
