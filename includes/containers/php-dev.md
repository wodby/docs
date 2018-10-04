### NewRelic

You can add NewRelic APM monitoring for PHP by adding environment variables `PHP_NEWRELIC_ENABLED=1` and `PHP_NEWRELIC_LICENSE` with your license number to PHP-FPM container. Application name will be automatically set to `[Wodby Application Name] - [Wodby Instance Name]`, if you want to change it, use `PHP_NEWRELIC_APPNAME`. 

### Profiling

You can profile your PHP application either via Xdebug traces (+[Webgrind](#webgrind)) or Tideways XHProf extensions.

### Xdebug (remote)

Follow these steps to debug your application instance remotely with [xdebug](http://xdebug.org/docs/install):

1. Enable xdebug for your instance from `[Instance] > Stack > Settings`
2. Set up forwarding for xdebug: copy _Xdebug SSH tunnel_ command from `[Instance] > Stack > PHP` and run on your local machine
3. Make sure you have your IDE xdebug listener running on port 9000
4. Start debugging in IDE
5. Start your browser debug helper plugin ([Chrome](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en) or [Firefox](https://addons.mozilla.org/en-us/firefox/addon/the-easiest-xdebug)) and open the page you want to debug

### Xdebug (local)

#### Debugging web requests

1. Uncomment these lines for PHP service in your docker-compose file
    ```yml
    PHP_XDEBUG: 1                 
    PHP_XDEBUG_DEFAULT_ENABLE: 1
    ```
2. Restart containers (`make`)    
3. Start debugging in IDE
4. Start your browser debug helper plugin ([Chrome](https://chrome.google.com/webstore/detail/xdebug-helper/eadndfjplgieldjbigjakmdgkmoaaaoc?hl=en) or [Firefox](https://addons.mozilla.org/en-us/firefox/addon/the-easiest-xdebug)) and open the page you want to debug. Alternatively, enable auto start by adding `PHP_XDEBUG_REMOTE_AUTOSTART=1`

#### Debugging CLI requests 

1. Enable Xdebug as described in the previous section
2. Uncomment the following environment variables for PHP service in your composer file
    ```yml
    PHP_XDEBUG_REMOTE_CONNECT_BACK: 0    
    PHP_IDE_CONFIG: serverName=my-ide
    ```
3. [Configure your IDE](#ide-configuration-to-debug-cli-requests)
4. Perform configuration as described below depending on your OS and Docker version:

##### Linux, Docker

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: 172.17.0.1` for PHP service (if you have docker 18.03+ you can specify `host.docker.internal` instead of the IP address)
2. Restart containers (`make`)

##### macOS, Docker

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: 10.254.254.254` for PHP service (just a random IP that very likely won't be used by anything else).
2. Restart containers (`make`)
3. You also need to have loopback alias with IP from above. You need this only once and that settings stays active until logout or restart:
    ```shell
    sudo ifconfig lo0 alias 10.254.254.254
    ```
4. To add the loopback alias after a reboot, add the following contents to `/Library/LaunchDaemons/docker4drupal.loopback.plist`:
    ```xml
    <plist version="1.0">
      <dict>
        <key>Label</key>
        <string>Default Loopback alias</string>
        <key>ProgramArguments</key>
        <array>
          <string>/sbin/ifconfig</string>
          <string>lo0</string>
          <string>alias</string>
          <string>10.254.254.254</string>
          <string>netmask</string>
          <string>255.255.255.0</string>
        </array>
        <key>RunAtLoad</key>
        <true/>
      </dict>
    </plist>
    ```

##### Windows

1. Uncomment `PHP_XDEBUG_REMOTE_HOST: 10.0.75.1` for PHP service (default IP of Docker NAT).
2. Restart containers (`make`)
3. Allow listen connection for your IDE in `Windows Firewall > Allow an app ..`

Also, you might need to add the following lines to your hosts file (see related [github issue](https://github.com/wodby/docker4drupal/issues/193)):
```
0.0.0.0			localhost
10.0.75.1		localhost
```

#### IDE configuration

You must additionally configure your IDE to debug CLI requests.

##### PHPStorm

1. Open `Run > Edit Configurations` from the main menu, choose `Defaults > PHP Web Page` in the left sidebar
2. Click to `[...]` to the right of `Server` and add a new server
    * Enter name `my-ide` (as specified in `PHP_IDE_CONFIG`)
    * Enter any host, it does not matter
    * Check `Use path mappings`, select path to your project and enter `/var/www/html` in the right column (Absolute path on the server) 
3. Choose newly created server in "Server" for PHP Web Page
4. Save settings
