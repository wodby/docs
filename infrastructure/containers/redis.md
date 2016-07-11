# Redis 

> Service: Cache storage

* [Access](#access)
* [Version](#version)
* [Integration with Drupal](#integration-with-drupal)
    * [Drupal 7](#drupal-7)
    * [Drupal 8](#drupal-8)
* [Integration with WordPress](#integration-with-wordpress)

## Access

This container doesn't expose public ports. 

You can connect to redis from [nginx-php container](nginx-php/README.md) by executing the following command:

```bash
$ redis-cli -h $REDIS_SERVICE_HOST -p $REDIS_SERVICE_PORT -a $WODBY_REDIS_PASSWORD
```

If you want to access the container itself please refer [to this article (with no SSH)](access.md).

## Version

The current version of Redis can be found on `[Instance] > Bundle > Cache storage` page.

## Integration with Drupal

All configuration settings already specified in [wodby.settings.php](../../apps/drupal/settings.md).

### Drupal 7

1. Install and enable <a href="https://www.drupal.org/project/redis" target="_blank">redis</a> module

### Drupal 8

1. Install and enable <a href="https://www.drupal.org/project/redis" target="_blank">redis</a> module
2. Enable Redis integration from `App page > Cache > Cache settings`

## Integration with WordPress

1. Install and activate <a href="https://wordpress.org/plugins/redis-cache/" target="_blank">redis plugin</a>
2. Go to redis plugin settings page and click "enable object cache" button