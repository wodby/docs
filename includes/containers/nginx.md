Nginx can be configured with the following [environment variables](https://github.com/wodby/nginx#environment-variables)

Restarting nginx as default user:

```shell
sudo nginx -s reload
```

!!! warning "Do not gzip pages in your application"
    We already gzip content on Nginx side and it works faster. Having double gzip may cause issues.

### Modules

Installed [nginx modules](https://github.com/wodby/nginx/blob/master/test/nginx_modules).

#### PageSpeed

Nginx comes with [mod_pagespeed](https://www.modpagespeed.com/) which is disabled by default. To enable it add `NGINX_PAGESPEED_ENABLED=1` environment variable to Nginx service. For more details see https://github.com/wodby/pagespeed.

#### ModSecurity + OWASP

Nginx comes with [ModSecurity](https://modsecurity.org) which is disabled by default. To enable it add `NGINX_MODSECURITY_ENABLED=1` environment variable to Nginx service. For more details see https://github.com/wodby/modsecurity.
    
### Custom config

If a config preset and available environment variables are not enough for your customizations you can use you own virtual host config: 

1. Copy `/etc/nginx/conf.d/vhost.conf` to your codebase, adjust to your needs
2. Deploy code with your config file
3. Add new environment variable `NGINX_CONF_INCLUDE` for nginx service, the value should the path to your `*.conf` file (e.g. `/var/www/html/vhost.conf`). The specified file will be included in `/etc/nginx/nginx.conf`
