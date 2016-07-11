# Redirects

* [Redirect from one domain to another](#redirect-from-one-domain-to-another)
* [Redirect from multiple domains](#redirect-from-multiple-domains)
* [Redirect from HTTP to HTTPS](#redirect-from-http-to-https)
* [Redirect requests for non-existing static files to Drupal](#redirect-requests-for-non-existing-static-files-to-drupal)
    * [Example: XML files](#example-xml-files)

If you need to make a redirect from one domain to another you can do it by customizing configuration files of [nginx](../../infrastructure/containers/nginx-php/nginx.md) or by adding the snippets below to your `settings.php` file.

## Redirect from one domain to another

```
if (isset($_SERVER['WODBY_ENVIRONMENT_TYPE']) && $_SERVER['WODBY_ENVIRONMENT_TYPE'] == 'prod' && php_sapi_name() != "cli") {
  if ($_SERVER['HTTP_HOST'] == 'redirect-from-domain.com') {
    header('HTTP/1.0 301 Moved Permanently');
    header('Location: http://redirect-to-domain.com' . $_SERVER['REQUEST_URI']);
    exit();
  }
}
```

## Redirect from multiple domains.

```
if (isset($_SERVER['WODBY_ENVIRONMENT_TYPE']) && $_SERVER['WODBY_ENVIRONMENT_TYPE'] == 'prod' && php_sapi_name() != "cli") {
  $redirect_from = array(
    'redirect-from-domain-1.com', 
    'redirect-from-domain-2.com',
  );

  if (in_array($_SERVER['HTTP_HOST'], $redirect_from)) {
    header('HTTP/1.0 301 Moved Permanently');
    header('Location: http://redirect-to-domain.com' . $_SERVER['REQUEST_URI']);
    exit();
  }
}
```

## Redirect from HTTP to HTTPS

You can enable this redirect by checking the corresponding option on a domain edit page from the adshboard.

## Redirect requests for non-existing static files

This might be useful when you want to generate static files via Drupal, like `rss.xml` and `sitemap.xml` (already handled).

### Example: XML files 

**1.** Connect to your [nginx-php container](../../infrastructure/containers/nginx-php/README.md) and open nginx config (example for Drupal 7, change the version number in the path for Drupal 6 or 8) with `nano` or `vi`:

```bash
$ nano /srv/conf/nginx/conf.d/app.d/drupal/7/config.conf
```

**2.** Find the following location and remove `xml` from the location pattern:

```
location ~* ^.+\.(?:css|cur|js|jpe?g|gif|htc|ico|png|xml|otf|ttf|eot|woff|svg)$ {
    access_log off;
    expires 30d;
    tcp_nodelay off;
    open_file_cache max=3000 inactive=120s;
    open_file_cache_valid 45s;
    open_file_cache_min_uses 2;
    open_file_cache_errors off;
}
```

**3.** Find the following locations:

```
location = /rss.xml {
    try_files $uri @drupal-no-args;
}

location = /sitemap.xml {
    try_files $uri @drupal-no-args;
}
```

and replace them with:

```
location ~* ^.+\.xml$ {
    try_files $uri @drupal-no-args;
}
```

**4.** Save the file and restart nginx:

```bash
$ nginx -s reload
```