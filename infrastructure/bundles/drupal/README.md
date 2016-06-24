# Drupal bundle

This section contains information related to [Drupal](../../apps/drupal/README.md) bundle. 

* [wodby.settings.php](wodby-settings-php.md)
* [Bundle versioning](versioning.md)

## Bundle services

### Drupal 8

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../containers/redis.md)                |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |

### Drupal 7

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../containers/redis.md)                |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |

### Drupal 6

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Memcached](../containers/memcached.md)        |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |
