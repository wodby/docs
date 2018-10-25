# PHP stack containers

## Apache

{!containers/php-apache.md!}

## AthenaPDF

See [AthenaPDF stack documentation](../athenapdf/index.md).

## Blackfire

{!containers/blackfire.md!}

## Crond

{!containers/php-crond.md!}

## Mailhog

{!containers/mailhog.md!}

## MariaDB

See [MariaDB stack documentation](../mariadb/index.md).

## Memcached

{!containers/memcached.md!}

## Nginx

* Nginx can be configured with the following [environment variables](https://github.com/wodby/php-nginx#environment-variables)
* Default Nginx [virtual host config](https://github.com/wodby/php-nginx/blob/master/templates/vhost.conf.tpl)
* Installed [nginx modules](https://github.com/wodby/nginx/blob/master/test/nginx_modules)

!!! warning "Do not gzip pages in your PHP application"
    We already gzip content on Nginx side and it works faster. Having double gzip may cause issues.

Restarting nginx as default user:

```shell
sudo nginx -s reload
```
    
### Custom config

If the default config and available environment variables are not enough for your customizations you can replace the config with your own:

1. Copy `/etc/nginx/conf.d/php.conf` to your codebase, adjust to your needs
2. Deploy code with your config file
3. Add new environment variable `NGINX_CONF_INCLUDE` for nginx service, the value should the path to your *.conf file (e.g. `/var/www/html/nginx.conf`)

### Mod pagespeed

Nginx comes with [mod_pagespeed](https://www.modpagespeed.com/) which is disabled by default. To enable it add `NGINX_PAGESPEED=on` environment variable to Nginx service.

## Node.js

{!containers/node.md!}

## OpenSMTPD

See [OpenSMTPD stack documentation](../opensmtpd/index.md).

## PHP

{!containers/php.md!}
{!containers/php-dev.md!}

## PostgreSQL

See [PostgreSQL stack documentation](../postgres/index.md).

## Redis

See [Redis stack documentation](../redis/index.md).

## Rsyslog

{!containers/php-rsyslog.md!}

## SSHd

{!containers/php-sshd.md!}

## Varnish

See [Varnish stack documentation](../varnish/index.md).

## Webgrind

{!containers/webgrind.md!}

## XHProf viewer

{!containers/xhprof.md!}
