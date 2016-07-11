# MariaDB 

> Service: Database

* [Accessing container](#accessing-container)
* [Accessing database](#accessing-database)
    * [Access via tunnel](#access-via-tunnel)
    * [Access via PhpMyAdmin](#access-via-phpmyadmin)
    * [Access via drush](#access-via-drush)
* [Version](#version)    
* [Configuration files](#configuration-files)

## Accessing container 

This container doesn't expose public ports. If you want to access the container itself please refer [to this article](access.md) (access with no SSH).

## Accessing database

### Access via drush

Please read [drush article](../../apps/drupal/drush.md).

### Access via PhpMyAdmin

You can deploy optional container with [PhpMyAdmin](phpmyadmin.md) to access the database.  

### Access via tunnel

If you want to access the database outside of the Wodby infrastructure you will have to use SSH tunnel via the main container: 

1. Set up SSH tunnel on port `53306` (you can change it). You can find <SSH Port> <Node IP> on the main container page. For MySQL (port `3306` by default) use the following command:
```
$ ssh -L 53306:services:3306 -p <SSH Port> wodby@<Node IP> -N
``` 

2. Connect to the database (mysql) via the tunnel on port `53306`:
```bash
$ mysql --protocol=TCP -P53306 -uwodby -p<MySQL password> wodby
```

## Version

The current version of MariaDB can be found on `[Instance] > Bundle > Database` page.

## Configuration files

The configuration files located under `/srv/conf/` of the mysql container.