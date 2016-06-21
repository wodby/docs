# Redirects

If you need to make a redirect from one domain to another you can do it by customizing configuration files of [nginx](../../infrastructure/containers/nginx-php/nginx.md) or by adding the snippets below to your `settings.php` file.

## Redirect from one domain to another.

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