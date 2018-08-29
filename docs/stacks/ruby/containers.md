# Ruby stack containers

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

## Ruby

Ruby can be configured with the following [environment variables](https://github.com/wodby/ruby#environment-variables)

### Mod pagespeed

Nginx comes with [mod_pagespeed](https://www.modpagespeed.com/) which is disabled by default. To enable it add `NGINX_PAGESPEED=on` environment variable to Nginx service.

## Mailhog

{!stacks/_includes/containers/mailhog.md!}

## OpenSMTPD

See [OpenSMTPD stack documentation](../opensmtpd/index.md).

## MariaDB

See [MariaDB stack documentation](../mariadb/index.md).

## Node.js

{!stacks/_includes/containers/node.md!}
