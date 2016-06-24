# WordPress bundle

This section contains information related to [WordPress](../../apps/wordpress/README.md) bundle.
 
* [Bundle versioning](versioning.md)

## Bundle services

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../../containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../../containers/redis.md)                |   |
| Search engine         | [Solr](../../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../../containers/varnish.md)            | &nbsp; |
