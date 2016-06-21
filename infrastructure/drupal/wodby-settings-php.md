# wodby.settings.php

Located under `/srv/conf` of the [Backend service](../../infrastructure/drupal/README.md) container.

**! Do not edit wodby.settings.php**, all changes to this file will be reset.

This file contains configuration settings for integration with Wodby [services](README.md) such as Database, Cache storage and Reverse Caching Proxy. 

Also, this file contains configurations for PHP sessions, files directory, trusted host patterns and sync directory.  

## Overriding settings

You can override settings specified in wodby.settings.php in your `sites/*/settings.php` file after the include of wodby.settings.php 
