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

{!php-cicd.md!}

## Drush

You can execute drush commands remotely via drush aliases. Download drush aliases from `Profile > Misc > Drush aliases` page and place them to `~/.drush`. Execute commands (replace `[tokens]` with the real values) like this:

```shell
 drush @[organization].[application].[instance] [drush command]
```

The domain marked as primary will be used as `-l` for drush aliases.

## Import

!!! important "No top level directory"
    While importing files from a tarball or an archive make sure there's no top level directory. The contents of the archive/tarball will be unpacked inside files directory
    
There are different ways to import files and database for Drupal website.

### From separate archives

Import Drupal via separate archives for database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives. This option is available on the 3rd step of a new application deployment form and also on `App instance > Import` page of existing instance.

### Manual import

In case your import data is huge it makes sense to import it manually from the server. Follow these steps:

1. Deploy your Drupal application without importing data
2. Gzip your SQL dump 
    ```shell
    gzip db-dump.sql
    ```
3. Create a tarball for your files:
    ```shell
    tar cvf files.tar -C /path/to/sites/default/files .
    ```
4. Download your archives: 
    * If your archive/tarball available by URL you can connect to the PHP container via SSH (the SSH connection command can be found under `App Instance > Stack > SSH server`) and download the archive via `wget [URL]`
    * You can copy an archive/tarball from your local computer (or any other machine) to the PHP container via `scp`, you can find the example SCP command from `App Instance > Stack > SSH server`
5. Unpack your SQL dump archive `gunzip db-dump.sql.gz`     
6. Import unpacked database dump:
    * Connect to database via `drush sqlc`
    * Drop database for wipe existing tables: 
    ```sql
    DROP DATABASE drupal;
    CREATE DATABASE drupal;
    ```
    * Run import `drush sqlc < db-dump.sql`
7. Now let's import your files:
    * If you have only public files (`sites/*/files` is a symlink to `/mnt/files/public`):
    ```shell
    tar xvf files.tar -C /mnt/files/public
    ```
    * If you have both `private/` and `public/` files directories (backups created by Wodby contains both)
    ```shell
    tar xvf files.tar -C /mnt/files/
    ```
8. If you get permissions error during the previous step you should give your user (`wodby`) writing permissions:
    ```shell
    sudo files_chmod /mnt/files/public
    sudo files_chmod /mnt/files/private
    ```
9. Make sure that the public files can be read by others (non-owner user/group) so the HTTP server can serve them:
    ```shell
    chmod -R o=rX /mnt/files/public/
    ```
10. Fix permissions for files directory so PHP (`www-data` user) have access to it:
    ```shell
    sudo files_chown /mnt/files/public
    sudo files_chown /mnt/files/private
    ``` 
11. That's it! Clear Drupal cache and remove import artifacts

### From drush archive

!!! warning "Outdated"
    This method is outdated. The latest versions of drush no longer have archive-dump command

This option is available on the 3rd step of a new application deployment form.

First, make sure you have [Drush installed](http://www.drush.org/en/master/install/), go to your Drupal root directory and execute a command:

```shell
drush archive-dump
```

or

```shell
drush ard
```

You should see output like:

```shell
drush ard
Archive saved to /Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
/Users/johndoe/drush-backups/archive-dump/20150604001227/drupalapp.20150604_001228.tar.gz
```

Now navigate to `Apps > Deploy` and choose drush archive on the 3rd step

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

When you deploy a new Drupal application you can optionally specify `Site directory` on the 3rd step, if not specified we use `default`. If directory does not exist Wodby will create it automatically. For example if you have a directory `sites/my-drupal-site/*` you should specify `my-drupal-site`. This directory will be used to locate [`settings.php`](#settingsphp) file and for building [`sites.php`](#sitesphp) mapping. The default [cron job](#cron) and orchestrations performed from Wodby dashboard such Drupal cache flush will be applied for this site.

### settings.php

`wodby.settings.php` file contains configuration settings for integration with Wodby services such as Database connection, Cache storage and Reverse Caching Proxy settings. You can override settings from this file in your `sites/*/settings.php` file after the include of `wodby.settings.php`.  

Wodby automatically adds the include of `wodby.settings.php` to [default site's](#default-site) `settings.php` with every deployment if there's no occurrences of `wodby.settings.php` in your settings file, otherwise we assume you've already added the include manually. 

Do not edit `wodby.settings.php`, all changes to this file will be reset with the next deployment.

### sites.php

Wodby automatically adds the include of `wodby.sites.php` to `sites.php`. The file `wodby.sites.php` generated automatically and contains the mapping of all attached domains to the site directory you've specified for this application.

### Trusted hosts patterns

All domains attached to an HTTP server (Nginx or Apache) or Varnish will be added to Drupal's trusted hosts patterns. 

### Sync directory

Wodby automatically creates sync directory with a salt and specify it inside of `wodby.settings.php`.

### Files

Files for Drupal located in `/mnt/files` and symlinked to `sites/[SITE NAME]/files`.

### Base URL

The domain marked with primary flag will be used as a `$base_url` in [`settings.php`](#settingsphp) file and as an `-l` parameter for the [default cron job](#cron). 

## Mail delivery

{!email-delivery.md!}

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
2. In your [`sites.php`](#sitesphp) file the following lines with include and your domains to directories mapping:
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
