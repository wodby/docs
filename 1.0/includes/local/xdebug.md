{!xdebug-log.md!}

### Debugging web requests

Make sure you have `PHP_EXTENSIONS_DISABLE` env var overridden in your compose file to enable Xdebug (default value is `xdebug,xhprof`). 

1. Uncomment these lines for PHP service in your `compose.yml` file (environment variables changed since xdebug 3.x)
    ```yml
    PHP_XDEBUG_MODE: debug
    ```
2. Restart containers (`make`)
3. Start debugging in IDE
4. Start your browser debug helper plugin ([Chrome](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en) or [Firefox](https://addons.mozilla.org/en-us/firefox/addon/the-easiest-xdebug)) and open the page you want to debug. Alternatively, enable auto start by adding `PHP_XDEBUG_START_WITH_REQUEST: "yes"`

### Debugging CLI requests 

1. Enable Xdebug as described in the previous section
2. Uncomment the following environment variables for PHP service in your composer file
    ```yml
    PHP_IDE_CONFIG: serverName=my-ide
    ```
3. [Configure your IDE](#ide-configuration-to-debug-cli-requests)
4. Restart containers (`make`)

Also, you might need to [update your hosts](https://github.com/wodby/docker4drupal/issues/193) file.

### IDE configuration

You must additionally configure your IDE to debug CLI requests.

#### PHPStorm

1. Open `Run > Edit Configurations` from the main menu, choose `Defaults > PHP Web Page` in the left sidebar
2. Click to `[...]` to the right of `Server` and add a new server
    * Enter name `my-ide` (as specified in `PHP_IDE_CONFIG`)
    * Enter any host, it does not matter
    * Check `Use path mappings`, select path to your project and enter `/var/www/html` in the right column (Absolute path on the server) 
3. Choose newly created server in "Server" for PHP Web Page
4. Save settings
