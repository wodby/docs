# WordPress

The Wodby WordPress catalog stack combines a WordPress PHP runtime with its web, database, shared-storage, cache, mail,
and optional utility services. The current composition and version choices are documented in
[`wodby/stack-wordpress`](https://github.com/wodby/stack-wordpress).

Start with the Vanilla WordPress boilerplate offered by the stack or connect a compatible Composer-based repository.
The default WordPress root subdirectory is `web`; change the PHP app service's `WordPress root subdirectory` setting
when your repository uses another layout.

## Runtime configuration

The WordPress PHP runtime generates `wodby.wp-config.php` from the current app environment and linked services. It provides:

- `WP_HOME` and `WP_SITEURL` from the app environment's primary URL
- database credentials from the selected database link
- stable generated WordPress authentication keys and salts
- the table prefix from `WP_TABLE_PREFIX`, with `wp_` as the default
- Valkey or Redis connection constants when a cache service is linked
- reverse-proxy handling for HTTPS and the original client address

The Wodby-provided `wp-config.php` includes this file automatically. If your repository supplies its own
`wp-config.php`, include the generated configuration before `wp-settings.php`:

```php
require_once getenv('CONF_DIR') . '/wodby.wp-config.php';
```

Define application-specific constants before or after that include as appropriate. Do not edit the generated file in a
running container because it is recreated from the app configuration.

## Code and shared content

Treat WordPress core, plugins, and themes as build inputs. Manage them in the source repository and rebuild the app so
deployments remain reproducible. Changes written only to a running container do not become part of the next build.

The stack provides shared persistent storage for WordPress content. Use [application imports](../../../apps/imports.md)
for supported service-volume content and [database imports](../../../databases/imports.md) for SQL data.

## Cache, mail, and cron

When the Valkey service is linked, Wodby exposes it through the standard `WP_REDIS_*` constants used by compatible
WordPress object-cache plugins.

Mailpit is suitable for inspecting mail in non-production environments. For production delivery, enable OpenSMTPD and
attach an [SMTP provider integration](../../../providers/smtp.md).

The WordPress PHP service defines an hourly schedule for due WordPress cron events using the app environment's primary
URL. Change the schedule or run it manually from the app environment's [Cron](../../../apps/cron.md) page.
