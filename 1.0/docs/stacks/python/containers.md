# Python stack containers

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

{!containers/nginx.md!}

Default virtual host preset: [`django`](https://github.com/wodby/nginx#django). If you don't use Django and don't need its locations, you can replace the preset to [`http-proxy`](https://github.com/wodby/nginx#http-proxy-application-server).     

## OpenSMTPD

See [OpenSMTPD stack documentation](../opensmtpd/index.md).

## PostgreSQL

See [PostgreSQL stack documentation](../postgres/index.md).

## Redis

See [Redis stack documentation](../redis/index.md).

## Valkey

See [Valkey stack documentation](../valkey/index.md).

## Rsyslog

Rsyslog can be used to stream your applications logs. It's similar to using syslog, however there's no syslog in Python container (one process per container). Rsyslog will stream all incoming logs to a container output.

## Python

Python can be configured with the following [environment variables](https://github.com/wodby/python#environment-variables). By default the container starts Gunicorn HTTP server.

## Varnish

See [Varnish stack documentation](../varnish/index.md).
