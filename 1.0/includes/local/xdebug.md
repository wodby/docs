{!xdebug-log.md!}

### Debugging web requests

1. Uncomment these lines for PHP service in your docker-compose file (environment variables changed since xdebug 3.x)
    ```yml
    PHP_XDEBUG: 1                 
    PHP_XDEBUG_MODE: debug
    ```
2. Restart containers (`make`)    
3. Start debugging in IDE
4. Start your browser debug helper plugin ([Chrome](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en) or [Firefox](https://addons.mozilla.org/en-us/firefox/addon/the-easiest-xdebug)) and open the page you want to debug. Alternatively, enable auto start by adding `PHP_XDEBUG_REMOTE_AUTOSTART=1`

### Debugging CLI requests 

1. Enable Xdebug as described in the previous section
2. Uncomment the following environment variables for PHP service in your composer file
    ```yml
    PHP_IDE_CONFIG: serverName=my-ide
    ```
3. [Configure your IDE](#ide-configuration-to-debug-cli-requests)
4. Perform configuration as described below depending on your OS and Docker version:

#### Linux, Docker

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: 172.17.0.1` for PHP service
2. Restart containers (`make`)

#### macOS, Docker

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: host.docker.internal` for PHP service
2. Restart containers (`make`)

#### Windows

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: host.docker.internal` for PHP service
2. Restart containers (`make`)
3. Allow listen connection for your IDE in `Windows Firewall > Allow an app ..`

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
