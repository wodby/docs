# Nginx

Official website: <a href="http://nginx.org/" target="_blank">http://nginx.org/</a>
 
* [Access](#access)
* [Version](#version)
* [Logs](#logs)
* [Configuration files](#configuration-files)
* [CLI](#cli)
    * [Rebooting nginx](#rebooting-nginx)
    * [Show installed modules](#show-installed-modules)

## Access

Nginx is a part of [nginx-php container](README.md).

## Version

The current version of Nginx can be found on `[Instance] > Bundle > Backend` page.

## Logs

Logs can be found under `/var/log/nginx`.

## Configuration files

Configuration files can be found under `/srv/conf/nginx`.

## CLI 

### Rebooting nginx

```bash
$ nginx -s reload
```

or

```bash
$ s6-svc -h /var/run/s6/services/nginx/
```

### Show installed modules

```bash
$ nginx -V
```