# Varnish

> Service: Reverse caching proxy

## Access

This container doesn't expose public ports. If you want to access the container itself please refer [to this article](access.md) (access with no SSH). 

## Versions

| Version | Stacks using |
| ----- | --------------------------------------- |
| 4.1.x | Drupal 6, Drupal 7, Drupal 8, WordPress |


## Integration with Drupal

### Drupal 7

1. Install and enable <a href="https://www.drupal.org/project/varnish" target="_blank">redis module</a> (**dev** version)
2. Enable Varnish integration from `App page > Cache > Cache settings`
3. Also, we recommend to install <a href="https://www.drupal.org/project/expire" target="_blank">expire module</a> to configure auto purge of pages when some content has been updated

### Drupal 8

1. Install and enable <a href="https://www.drupal.org/project/varnish" target="_blank">redis module</a>
2. Enable Varnish integration from `App page > Cache > Cache settings`
3. Also, we recommend to install <a href="https://www.drupal.org/project/expire" target="_blank">expire module</a> to configure auto purge of pages when some content has been updated

## Integration with WordPress

1. Install and activate <a href="https://wordpress.org/plugins/varnish-http-purge/" target="_blank">redis plugin</a>
2. Enable Varnish integration from `App page > Cache > Cache settings`