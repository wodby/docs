# Ruby stack containers

## AthenaPDF

See [AthenaPDF stack documentation](../athenapdf/index.md).

## Mailhog

{!containers/mailhog.md!}

## MariaDB

See [MariaDB stack documentation](../mariadb/index.md).

## Memcached

{!containers/memcached.md!}

## Node.js

{!containers/node.md!}

## Nginx

* Nginx can be configured with the following [environment variables](https://github.com/wodby/nginx#environment-variables)
* Installed [nginx modules](https://github.com/wodby/nginx/blob/master/test/nginx_modules)
* For ruby we use virtual host preset [http-proxy](https://github.com/wodby/nginx#http-proxy-application-server)

!!! warning "Do not gzip pages in your Ruby application"
    We already gzip content on Nginx side and it works faster. Having double gzip may cause issues.

Restarting nginx as default user:

```shell
sudo nginx -s reload
```

### Mod pagespeed

Nginx comes with [mod_pagespeed](https://www.modpagespeed.com/) which is disabled by default. To enable it add `NGINX_PAGESPEED=on` environment variable to Nginx service.

## OpenSMTPD

See [OpenSMTPD stack documentation](../opensmtpd/index.md).

## PostgreSQL

See [PostgreSQL stack documentation](../postgres/index.md).

## Redis

See [Redis stack documentation](../redis/index.md).

## Rsyslog

Rsyslog can be used to stream your applications logs. It's similar to using syslog, however there's no syslog in Ruby container (one process per container). Rsyslog will stream all incoming logs to a container output.

## Ruby

Ruby can be configured with the following [environment variables](https://github.com/wodby/ruby#environment-variables). By default the container starts Puma HTTP server.

## Sidekiq

A duplicate of the main Ruby container runs with Sidekiq (instead of HTTP server). 

## Varnish

See [Varnish stack documentation](../varnish/index.md).
