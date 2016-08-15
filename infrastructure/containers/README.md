# Containers

Infrastructure provided by Wodby is powered by docker containers. Our light-weight containers are based on <a href="http://alpinelinux.org" target="_blank">Alpine Linux</a>.
 
* [How to access containers](access.md)

The following containers are currently available:

| Service | Available containers | Enabled by default | SSH access |
| --------------------- | -------------------------------- | - | - |
| Backend               | [Nginx-php](nginx-php/README.md) | ✓ | ✓ |
| Database              | [MariaDB](mariadb.md)            | ✓ |   |
| Cache storage         | [Redis](redis.md)                | ✓ |   |
| Mail server           | [OpenSMTPD](opensmtpd.md)        | ✓ |   |
| Mail catcher          | [Mailhog](mailhog.md)            |   |   |
| Search engine         | [Solr](apache-solr.md)           |   |   |
| Database management   | [PhpMyAdmin](phpmyadmin.md)      |   |   |
| Reverse caching proxy | [Varnish](varnish.md)            |   |   |
