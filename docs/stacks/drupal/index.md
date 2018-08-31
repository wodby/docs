# Drupal stack documentation

Stack pages:

* [Drupal 8](https://cloud.wodby.com/stacks/drupal8)
* [Drupal 7](https://cloud.wodby.com/stacks/drupal7)
* [Drupal 6](https://cloud.wodby.com/stacks/drupal6)
* [Docker4Drupal (local environment)](https://github.com/wodby/docker4drupal)

## Deployment

See [main code deployment article](../../apps/deploy.md) to learn about code deployment options on Wodby. 

### Vanilla Drupal

For demo purposes and simple Drupal installations you can use Vanilla Drupal deployment option. In this case Drupal code that comes with the Docker image will be used. In case of changes all data made to your codebase will persist but there will be no versions control.

### Direct git integration

We recommend using [Composer](https://getcomposer.org/) to manage dependencies in your repository. Dependencies will be installed via [post-deployment scripts](../../apps/post-deployment-scripts.md):

1. Fork [our boilerplate](https://github.com/wodby/drupal-composer) or use the original [composer template for Drupal](https://github.com/drupal-composer/drupal-project)
2. Create `wodby.yml` in repository root (our boilerplate already has it) with the following content:
  ```yml
  pipeline:
    - name: Install dependencies
      type: command
      command: composer install --prefer-dist -n --no-dev
      directory: $APP_ROOT
  ```
3. On the 3rd step of new application deployment form:
    * Specify `web` in `Codebase dir` (default name of subdir with Drupal's codebase) 
    * Make sure git branch matches to your Drupal version

### CI/CD

{!stacks/_includes/php-cicd.md!}

## Drush

You can execute drush commands remotely via drush aliases. Download drush aliases from `Profile > Misc > Drush aliases` page and place them to `~/.drush`. Execute commands (replace `[tokens]` with the real values) like this:

```bash
$  drush @[organization].[application].[instance] [drush command]
```

The domain marked as primary will be used as `-l` for drush aliases.

## Import

### From drush archive

This option is available on the 3rd step of a new application deployment form.

First, make sure you have [Drush installed](http://www.drush.org/en/master/install/), go to your Drupal root directory and execute a command:

```bash
$ drush archive-dump
```

or

```bash
$ drush ard
```

You should see output like:

```bash
$ drush ard
Archive saved to /Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
/Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
```

Now navigate to `Apps > Deploy` and choose drush archive on the 3rd step

### From separate archives

Import Drupal via separate archives for database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives. This option is available on the 3rd step of a new application deployment form and also on `[Instance] > Import` page of existing instance.

### Manual import

In case your import data is huge it makes sense to import it manually from the server. Follow these steps:

1. Deploy your Drupal application without importing data
2. Once the app is deployed, go to `Stack > SSH` and copy SSH command
3. Connect to the container by SSH
4. Copy your database archive here via `wget` or `scp`, make sure it's gzipped
5. Import unpacked database dump using `drush sql-cli < my-db-dump.sql`
6. Now let's import your files, cd to `/mnt/files`, use public and private subdirectories according to your needs
7. Copy your files archive here via `wget` or `scp` and unpack the archive
8. That's it! Clear Drupal cache and remove import artifacts

### Import between instances

You can import database and files from one instance to another regardless of whether instances are on the same server or not. Go to `[Instance] > Import` tab and select an instance where you'd like to import database/files from.

## Backups

### Files

Both public and private files directories under `sites/*/files` will be backed up. Codebase will not be backed up.  

### Database

MariaDB backups run with [--single-transaction](https://dev.mysql.com/doc/refman/5.7/en/mysqldump.html) option to avoid tables locks.

Data of the following tables excluded from DB dump:

```
cache
cache_%
ctools_object_cache
ctools_views_cache
flood
history
queue
search_index
semaphore
sequences
sessions
watchdog
```

## Drupal settings

### Default site

When you deploy a new Drupal application you can optionally specify `Site directory` on the 3rd step, if not specified we use `default`. If directory does not exist Wodby will create it automatically. For example if you have a directory `sites/my-drupal-site/*` you should specify `my-drupal-site`. This directory will be used to locate [`settings.php`](#settings-php) file and for building [`sites.php`](#sites-php) mapping. The default [cron job](#cron) and orchestrations performed from Wodby dashboard such Drupal cache flush will be applied for this site.

### settings.php

Wodby automatically adds the include of `wodby.settings.php` to [default site's](#default-site) `settings.php`. The `wodby.settings.php` file contains configuration settings for integration with Wodby services such as Database, Cache storage and Reverse Caching Proxy. You can override settings from this file in your `sites/*/settings.php` file after the include of `wodby.settings.php`. If your `settings.php` file already has the line with `wodby.settings.php` include the include will not be added again. Do not edit `wodby.settings.php`, all changes to this file will be reset with the next deployment.

### sites.php

Wodby automatically adds the include of `wodby.sites.php` to `sites.php`. The file `wodby.sites.php` generated automatically and contains the mapping of all attached domains to the site directory you've specified for this application.

### Trusted hosts patterns

All domains attached to an HTTP server (Nginx or Apache) or Varnish will be added to Drupal's trusted hosts patterns. 

### Sync directory

Wodby automatically creates sync directory with a salt and specify it inside of `wodby.settings.php`.

### Files

Files for Drupal located in `/mnt/files` and symlinked to `sites/[SITE NAME]/files`.

### Base URL

The domain marked with primary flag will be used as a `$base_url` in [`settings.php`](#settings-php) file and as an `-l` parameter for the [default cron job](#cron). 

## Mail delivery

{!stacks/_includes/email-delivery.md!}

## Cron

By default we run the following cron command from [crond container](containers.md#crond) every hour:

```
drush -r "${HTTP_ROOT}" -l "${WODBY_HOST_PRIMARY}" cron
``` 

`$WODBY_HOST_PRIMARY` is a domain marked as primary. You can customize crontab from `[Instance] > Stack > Settings` page.

## Redirects

If you need to make a redirect from one domain to another you can do it by customizing configuration files of nginx or by adding the snippets below to your `settings.php` file.

Redirect from one domain to another:

```php
if (isset($_SERVER['WODBY_ENVIRONMENT_TYPE']) && $_SERVER['WODBY_ENVIRONMENT_TYPE'] == 'prod' && php_sapi_name() != "cli") {
    if ($_SERVER['HTTP_HOST'] == 'redirect-from-domain.com') {
      header('HTTP/1.0 301 Moved Permanently');
      header('Location: http://redirect-to-domain.com' . $_SERVER['REQUEST_URI']);
      exit();
    }
}
```

Redirect from multiple domains:

```php
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

Redirect from HTTP to HTTPS can be enabled on a domain edit page from the dashboard.

## Multi-site 

There two ways how you can deploy your multi-site Drupal application via Wodby

### Deploy sites as separate app instances 

Deploy every site as a separate application instance by specifying the [default site](#default-site) of every subsite. In this scheme every site will be deployed as a separate [application instance](../../apps/instances.md) with its own database. 

### Deploy all sites in one instance

Perform the following modifications in your code:

1. Add the following include in `sites/*/settings.php` of all sites, specify db prefix for every site:
    ```php
    include '/var/www/conf/wodby.settings.php';
    // After the include specify db prefix for every site.
    // $databases['default']['default']['prefix'] = 'site_prefix_';
    ```
2. In your [`sites.php`](#sites-php) file the following lines with include and your domains to directories mapping:
    ```php
    include '/var/www/conf/wodby.sites.php';

    // Add mapping after the include to override:
    $sites['your.domain.com'] = 'dir.name.under.sites';
    ```

Also, you'll have to update [cron](#cron) jobs to run it for every site, not only the primary. Please note that all dashboard orchestration such as Drupal cache clear will be applied only to the default site.

In this scheme every site will use the database by default.  

## Cache control

You can clear caches and control cache settings from `[Instance] > Cache` page. The following actions are available:

* Clear application cache (drush cc)
* Clear redis cache (if enabled)
* Clear varnish cache (if enabled)
* Clear all caches
* Enable/disable opcache
* Enable/disable redis integration
