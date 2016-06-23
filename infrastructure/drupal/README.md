# Drupal Infrastructure

This section contains information related to infrastructure deployed for [Drupal websites](../../apps/drupal/README.md). 

* [wodby.settings.php](wodby-settings-php.md)

## Available services

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
