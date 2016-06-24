# PHP

By default PHP works via PHP-FPM under FastCGI with Nginx web server.  

* [Access](#access)
* [Versions](#versions)
* [Logs](#logs)
* [Configuration files](#configuration-files)
* [PHP-FPM](#php-fpm)
* [PHP extensions](#php-extensions)

## Access

PHP and PHP-fpm are parts of [nginx-php container](README.md).

## Versions

### PHP 7

| Version | Infrastructure |
| ------- | -------------- |
| 7.0.7 | [3.0+](../../versioning.md) |

### PHP 5.6

| Version | Infrastructure |
| ------- | -------------- |
| 5.3.29 | [3.0+](../../versioning.md) |
 
### PHP 5.3

| Version | Infrastructure |
| ------- | -------------- |
| 5.6.21 | [3.0+](../../versioning.md) |
| 5.6.22 | [3.5+](../../versioning.md) |

## Logs

Logs can be found under `/var/log/php` or `/var/log/php7` depending on the version.

## Configuration files

Configuration files can be found under `/srv/conf/php`.

## PHP-FPM

Rebooting PHP-FPM:
```bash
s6-svc -h /var/run/s6/services/php-fpm/
```

## PHP extensions 

To learn installed PHP extensions connect to the [nginx-php container](README.md) by SSH and execute:
```bash
$ php -m
```