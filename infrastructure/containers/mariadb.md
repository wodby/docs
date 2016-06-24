# MariaDB 

> Service: Database

* [Accessing container](#accessing-container)
* [Accessing database](#accessing-database)
    * [Access via tunnel](#access-via-tunnel)
    * [Access via PhpMyAdmin](#access-via-phpmyadmin)
    * [Access via drush](#access-via-drush)
* [Versions](#versions)
* [Integration with Drupal](#integration-with-drupal)
* [Integration with WordPress](#integration-with-wordpress)

## Accessing container 

This container doesn't expose public ports. If you want to access the container itself please refer [to this article](access.md) (access with no SSH).

## Accessing database

### Access via drush

You can connect the database by executing the following command in the Drupal docroot inside of the [nginx-php container](nginx-php/README.md):

```bash
$ drush sql-cli
```

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

## Versions

| Version | Infrastructure |
| ------- | -------------- |
| 10.1.12 | [3.0+](../../versioning.md) | 
| 10.1.14 | [3.5+](../../versioning.md) | 

## Configuration files

The configuration files located under `/srv/conf/` of the mysql container.

## Integration with Drupal

The configuration settings specified in [wodby.settings.php](../drupal/wodby-settings-php.md).

## Integration with WordPress