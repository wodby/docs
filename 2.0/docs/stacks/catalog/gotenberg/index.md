# Gotenberg

The Wodby Gotenberg catalog stack runs Gotenberg 8 for converting web pages, HTML, and office documents to PDF. The
current service definition and version choices are documented in
[`wodby/service-gotenberg`](https://github.com/wodby/service-gotenberg).

Applications in the same app can reach the service through its private endpoint:

```text
http://gotenberg:3000
```

Keep this endpoint private unless an external client must call it. After testing, disable the Gotenberg technical route
under **App instance → Endpoints → Routes**. Internal service-to-service requests continue to work.

## Migrate from AthenaPDF

Gotenberg is not a drop-in replacement for AthenaPDF. AthenaPDF accepts requests through `/convert` with an
authentication key, while Gotenberg 8 uses multipart `POST` requests to conversion-specific routes. Changing only the
hostname or port does not migrate the application client or CMS configuration.

When the Wodby 1 migration CLI maps `athenapdf` to `gotenberg`, it:

- adds the Gotenberg service to the target stack and preserves whether the source service is enabled
- sets `GOTENBERG_ENDPOINT` on the target PHP service to the private in-cluster URL, normally
  `http://gotenberg:3000`
- does not rewrite application code, Drupal configuration, WordPress plugin configuration, or custom AthenaPDF options

### Drupal

For Drupal 10.3 and Drupal 11, use the contributed
[Gotenberg module](https://www.drupal.org/project/gotenberg). It includes a Gotenberg client and an Entity Print
backend, but it does not convert configuration or custom code from the older
[Athena PDF API module](https://www.drupal.org/project/athenapdf_api).

```bash
composer require 'drupal/gotenberg:^1.0'
```

The Drupal module stores its base URL in Drupal configuration and does not read `GOTENBERG_ENDPOINT` automatically.
To use the endpoint supplied by Wodby, add an environment-specific override after the generated Wodby settings include:

```php
$config['gotenberg.settings']['base_url'] =
  getenv('GOTENBERG_ENDPOINT') ?: 'http://gotenberg:3000';
```

After importing the Wodby 1 database, remove or replace the stored `athenapdf_api` configuration and validate the
Gotenberg module configuration before switching traffic.

### WordPress and custom PHP

Wodby does not provide a WordPress-specific Gotenberg plugin. Use a plugin only if it explicitly supports the remote
Gotenberg 8 API, or update custom code to use an appropriate client. Composer-managed PHP applications can use the
[official Gotenberg PHP client](https://github.com/gotenberg/gotenberg-php):

```bash
composer require gotenberg/gotenberg-php:^2
```

Application code must read `GOTENBERG_ENDPOINT` explicitly.

### Authentication variables

Do not copy `GOTENBERG_HTTP_AUTH_USERNAME` or `GOTENBERG_HTTP_AUTH_PASSWORD` from a custom Wodby 1 stack as though they
were Drupal module settings. The module does not read them, and they are not Gotenberg 8 server configuration names.

If API basic authentication is required, configure Gotenberg 8 deliberately with
`GOTENBERG_API_BASIC_AUTH_USERNAME` and `GOTENBERG_API_BASIC_AUTH_PASSWORD` and enable its basic-auth setting. Prefer the
private service endpoint when only services inside the app need access.

### Migration checklist

1. Find every AthenaPDF dependency, including `ATHENAPDF_URL`, `ATHENAPDF_PASSWORD`, stored `athenapdf_api`
   configuration, custom clients, and calls to `/convert`.
2. Install a Gotenberg-aware module or client and configure it to use `GOTENBERG_ENDPOINT`.
3. Replace AthenaPDF requests with the corresponding Gotenberg multipart route. For example, use
   `/forms/chromium/convert/url` for a URL or `/forms/chromium/convert/html` with an `index.html` upload for HTML.
4. Map paper size, margins, media type, backgrounds, headers, footers, cookies, timeouts, and JavaScript wait behavior
   explicitly. The migration CLI does not translate AthenaPDF request options.
5. Replace AthenaPDF configuration stored in the imported database through a configuration import, deployment hook, or
   CMS administration page.
6. Compare representative PDFs before switching traffic, including fonts, images, authenticated assets, page breaks,
   headers, backgrounds, file size, and failure behavior.

See the Gotenberg documentation for
[URL conversion](https://gotenberg.dev/docs/convert-with-chromium/convert-url-to-pdf),
[HTML conversion](https://gotenberg.dev/docs/convert-with-chromium/convert-html-to-pdf), and
[supported clients](https://gotenberg.dev/docs/getting-started/clients).
