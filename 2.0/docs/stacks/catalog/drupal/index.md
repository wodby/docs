# Drupal

The Wodby Drupal catalog stack provides separate Drupal 10 and Drupal 11 entries. The current service composition and
version choices are documented in [`wodby/stack-drupal`](https://github.com/wodby/stack-drupal).

Start with the Drupal CMS or Vanilla Drupal boilerplate offered by the stack, or connect a compatible Composer-based
repository. The default Drupal root subdirectory is `web`; change the PHP app service's `Drupal root subdirectory`
setting when your repository uses a different layout.

## Runtime configuration

The Drupal PHP runtime generates `wodby.settings.php` from the app environment's current environment and linked services.
The runtime setup adds this file to the active Drupal site's `settings.php` when it initializes the site.

The generated settings provide:

- database connection values from the selected database link
- public, private, temporary, and configuration-sync paths
- trusted-host patterns from the app environment routes
- generated hash and file-sync salts
- optional Valkey or Redis cache configuration when the Drupal Redis module is present
- the password override used by the [Drupal Solr integration](solr.md)

Do not edit the generated file inside a running container. Put application-specific overrides in your repository's
`settings.php` after the Wodby include. If a custom repository replaces `settings.php`, keep this include:

```php
include getenv('CONF_DIR') . '/wodby.settings.php';
```

## Files and configuration sync

The Drupal PHP service mounts shared file storage and links it to the active site's public files directory. Private
files and Wodby's default configuration-sync directory use the same persistent storage.

The generated sync directory contains a stable per-app salt. You can override `$settings['config_sync_directory']` in
your own `settings.php` when configuration belongs in the application repository instead.

Use [application imports](../../../apps/imports.md) for service files and [database imports](../../../databases/imports.md)
for database content. Use the [web terminal](../../../apps/web-terminal.md) when you need interactive access to a
running container.

## Cron and application actions

The Drupal PHP service defines an hourly Drush cron schedule using the app environment's primary URL. You can change the
schedule or run it manually from the app environment's [Cron](../../../apps/cron.md) page.

The service also exposes actions to:

- rebuild Drupal caches
- generate a one-time login link
- apply pending database updates

Run these from the app service operations in the dashboard. Use the [web terminal](../../../apps/web-terminal.md) for
other one-off Drush or Composer commands.

## Optional services

The catalog stack can link Drupal to a database, shared files, Valkey, mail, Gotenberg, and Solr. Optional services and
their defaults can change over time, so review the selected stack entry during app creation instead of relying on a
static container list.

For search setup, see [Connect Drupal to Solr](solr.md).
