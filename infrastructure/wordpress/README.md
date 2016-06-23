# WordPress Infrastructure

This section contains information related to infrastructure deployed for [WordPress websites](../../apps/wordpress/README.md). 

## Available services

| Service | Available containers | Mandatory |
| --------------------- | ---------------------------------------------- | - |
| Backend               | [Nginx-php](../containers/nginx-php/README.md) | ✓ |
| Database              | [MariaDB](../containers/mariadb.md)            | ✓ |
| Cache storage         | [Redis](../containers/redis.md)                |   |
| Search engine         | [Solr](../containers/apache-solr.md)           |   |
| Database management   | [PhpMyAdmin](../containers/phpmyadmin.md)      |   |
| Reverse caching proxy | [Varnish](../containers/varnish.md)            | &nbsp; |
