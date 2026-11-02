# HTML

The Wodby HTML catalog stack serves static HTML sites with Nginx or, optionally, Apache HTTP Server. The current
services and defaults are documented in [`wodby/stack-html`](https://github.com/wodby/stack-html).

## Choose a web server

Nginx is enabled by default. Apache HTTP Server is available but disabled by default. Pick the one that matches how
your site handles routes:

- **Nginx** serves a directory request with the index file. A path that matches no file also falls back to the index
  file, which suits a single-page application.
- **Apache HTTP Server** serves a directory request with `index.html`. A path that matches no file gets no fallback.
  Add your own rewrite rule to a `.htaccess` file when you need one. `.htaccess` overrides are allowed in the document
  root.

## Build and deployment

Start from the [HTML boilerplate](https://github.com/wodby/html-boilerplate) or connect your own repository. See
[Application Builds](../../../apps/builds.md).

The build copies your repository into the image at `/var/www/html`. A changed file needs a new build and deployment.

Set the **Nginx docroot subdir** or **Apache docroot subdir** setting when the site is in a subdirectory of the
repository. Leave it empty to serve the repository root.

## Defaults you should know about

Both web servers answer `/.healthz` with status 204 and deny paths that start with a dot. Nginx still allows
`/.well-known/`. Both deny `wodby.yml` and `Makefile`. Apache also denies files ending in `.sh`, `.sql`, `.mysql`,
`.po`, `.tpl`, `.make` or `.test`, and it keeps directory listings off.

Nginx adds the `X-XSS-Protection`, `X-Frame-Options`, `X-Content-Type-Options` and `Content-Security-Policy` headers.
The default policy only restricts framing. Set `NGINX_HEADERS_CONTENT_SECURITY_POLICY` to change it.

## Change web server settings

Do not add an `nginx.conf` or `httpd.conf` to the repository. Set `NGINX_*` or `APACHE_*`
[environment variables](../../../apps/environment-variables.md) on the app service instead, or override the config
files that the service declares. Changes apply with the next deployment.
