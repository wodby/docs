# Memcached

> Service: Cache storage

* [Access](#access)
* [Version](#version)    
* [Integration with Drupal](#integration-with-drupal)

## Access

This container doesn't expose public ports. You can access memcache from the [nginx-php container](nginx-php/README.md) by using telnet. 

If you want to access the container itself please refer [to this article](access.md) (access with no SSH). 

## Version

The current version of Memcached can be found on `[Instance] > Bundle > Cache storage` page

## Integration with Drupal

1. Download and install <a href="https://www.drupal.org/project/memcache" target="_blank">memcache</a> module.

All configuration settings already specified in [wodby.settings.php](../../apps/drupal/settings.md).
