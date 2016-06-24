# Memcached

> Service: Cache storage

## Access

This container doesn't expose public ports. You can access memcache from the [nginx-php container](nginx-php/README.md) by using telnet. 

If you want to access the container itself please refer [to this article](access.md) (access with no SSH). 

## Integration with Drupal

1. Download and install <a href="https://www.drupal.org/project/memcache" target="_blank">memcache</a> module.

All configuration settings already specified in [wodby.settings.php](../bundles/drupal/wodby-settings-php.md).
