# PHP stack containers

## Nginx

* Nginx can be configured with the following [environment variables](https://github.com/wodby/php-nginx#environment-variables)
* Default Nginx [virtual host config](https://github.com/wodby/php-nginx/blob/master/templates/vhost.conf.tpl)
* Installed [nginx modules](https://github.com/wodby/nginx/blob/master/test/nginx_modules)

### Custom config

If the default config and available environment variables are not enough for your customizations you can replace the config with your own:

1. Copy `/etc/nginx/conf.d/php.conf` to your codebase, adjust to your needs
2. Deploy code with your config file
3. Add new environment variable `NGINX_CONF_INCLUDE` for nginx service, the value should the path to your *.conf file (e.g. `/var/www/html/nginx.conf`)

### Mod pagespeed

Nginx comes with [mod_pagespeed](https://www.modpagespeed.com/) which is disabled by default. To enable it add `NGINX_PAGESPEED=on` environment variable to Nginx service.

## Apache

{!stacks/_includes/containers/php-apache.md!}

## PHP

{!stacks/_includes/containers/php.md!}

## Crond

{!stacks/_includes/containers/php-crond.md!}

## SSHd

{!stacks/_includes/containers/php-sshd.md!}

## Mailhog

{!stacks/_includes/containers/mailhog.md!}

## OpenSMTPD

See [OpenSMTPD stack documentation](../opensmtpd/index.md).

## MariaDB

See [MariaDB stack documentation](../mariadb/index.md).

## Node.js

{!stacks/_includes/containers/node.md!}

## Rsyslog

{!stacks/_includes/containers/rsyslog.md!}

## Blackfire

{!stacks/_includes/containers/blackfire.md!}

## Webgrind

{!stacks/_includes/containers/webgrind.md!}
