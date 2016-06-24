# Varnish

> Service: Reverse caching proxy

* [Access](#access)
* [Version](#version)    
* [Integration with Drupal](#integration-with-drupal)

## Access

This container doesn't expose public ports. If you want to access the container itself please refer [to this article](access.md) (access with no SSH). 

## Version

The current version of Varnish can be found on `Instance > Containers > Reverse caching proxy` page

## Integration with Drupal

### Drupal 7

1. Install and enable <a href="https://www.drupal.org/project/varnish" target="_blank">varnish module</a> (use the dev version)
2. Enable Varnish integration from `App page > Cache > Cache settings`
3. Go to `Home » Administration » Configuration » Development` page of Drupal website and
    * Check *Cache pages for anonymous users*
    * Check *Compress cached pages.*
    * Check *Aggregate and compress CSS files.*
    * Check *Aggregate JavaScript files.*    
4. Also, we recommend to install <a href="https://www.drupal.org/project/expire" target="_blank">expire module</a> to configure auto purge of pages when some content has been updated. After installation go to `Home » Administration » Configuration » System` and select *External expiration* at the "Module status" tab.

### Drupal 8

1. Install and enable <a href="https://www.drupal.org/project/varnish" target="_blank">varnish module</a>
2. Enable Varnish integration from `App page > Cache > Cache settings`
3. Go to `Home » Administration » Configuration » Development` page of Drupal website and enter the following settings (copy from `Instance > Containers > Reverse caching proxy` page of Wodby Dashboard): 
    * Varnish version = 4.x
    * Varnish Control Terminal = <Internal hostname>:6082
    * Varnish Control Key = <Secret>

## Integration with WordPress

1. Install and activate <a href="https://wordpress.org/plugins/varnish-http-purge/" target="_blank">varnish plugin</a>
2. Enable Varnish integration from `App page > Cache > Cache settings`