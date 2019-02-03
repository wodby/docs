# WordPress stack documentation

[WordPress stack](https://cloud.wodby.com/stacks/wordpress)

!!! info "Docker4WordPress"
    This is the overview for Wordpress stack deployed via Wodby. For local environment (Docker4WordPress) documentation see [this article](local.md)

## Deployment 

See [main code deployment article](../../apps/deploy.md) to learn about code deployment options on Wodby.

### Vanilla WordPress

For demo purposes and simple WordPress installations you can use Vanilla WordPress deployment option. In this case WordPress code that comes with the Docker image will be used. In case of changes all data made to your codebase will persist but there will be no versions control.

### Direct git integration

We recommend using [Composer](https://getcomposer.org/) to manage dependencies in your repository. Dependencies will be installed via [post-deployment scripts](../../apps/post-deployment-scripts.md):

1. Fork [our boilerplate](https://github.com/wodby/wordpress-composer)
2. Create `wodby.yml` in repository root (our boilerplate already has it) with the following content:
  ```yml
    pipeline:
    - name: Install dependencies
      type: command
      command: composer install --prefer-dist -n --no-dev
      directory: $APP_ROOT
  ```
3. Enter `web` (it's a directory name with WordPress root in our boilerplate) in `Codebase dir` input on the 3rd step of new application deployment form

### CI/CD

{!php-cicd.md!}

## Import

!!! important "No top level directory"
    While importing files from a tarball or an archive make sure there's no top level directory. The contents of the archive/tarball will be unpacked inside the `uploads/` directory

There are different ways to import files and database for WordPress website.

### From duplicator archive

Install [duplicator plugin](https://wordpress.org/plugins/duplicator/) on your existing website. Go to admin part of your WordPress website and create a new package via duplicator.

Now navigate to `Apps > Deploy` and choose duplicator archive as data source on the 3rd step.

### From separate archives

Import WordPress via separate archives for database and files. We support `.zip`, `.gz`, `.tar.gz`, `.tgz` and `.tar` archives. This option is available on the 3rd step of a new instance deployment form and also on `[Instance] > Import` page of existing instance.

### Manual import

In case your import data is huge it makes sense to import it manually from the server. Follow these steps:

1. Deploy your WordPress application without importing data
2. Gzip your SQL dump 
    ```shell
    gzip db-dump.sql
    ```
3. Create a tarball for your files:
    ```shell
    tar cvf files.tar -C /path/to/wp-content/uploads .
    ```
4. Download your archives: 
    * If your archive/tarball available by URL you can connect to the PHP container via SSH (the SSH connection command can be found under `App Instance > Stack > SSH server`) and download the archive via `wget [URL]`
    * You can copy an archive/tarball from your local computer (or any other machine) to the PHP container via `scp`, you can find the example SCP command from `App Instance > Stack > SSH server`
5. Unpack your SQL dump archive `gunzip db-dump.sql.gz`     
6. Import unpacked database dump:
    * Connect to database via `wp db cli`
    * Drop database for wipe existing tables: 
    ```sql
    DROP DATABASE wordpress;
    CREATE DATABASE wordpress;
    ```
    * Run import `wp db import db-dump.sql`
7. Now let's import your files (`wp-content/uploads` is a symlink to `/mnt/files/public`):
    ```shell 
    tar xvf files.tar -C /mnt/files/public
    ```
8. If you get permissions error during the previous step you should give your user (`wodby`) writing permissions:
    ```shell
    sudo files_chmod /mnt/files/public
    ```    
9. Make sure that the public files can be read by others (non-owner user/group) so the HTTP server can serve them:
    ```shell
    chmod -R o=rX /mnt/files/public/
    ```    
10. Fix permissions for files directory so PHP (`www-data` user) have access to it:
    ```shell
    sudo files_chown /mnt/files/public
    ``` 
11. That's it! Clear WP cache and remove import artifacts

### Import between instances

You can import database and files from one instance to another regardless of whether instances are on the same server or not. Go to `[Instance] > Import` tab and select an instance where you'd like to import database/files from.

## Upgrading WordPress

!!! tldr "Use composer"
    We recommend managing WordPress core and plugins dependencies with composer, you can find a boilerplate at https://github.com/wodby/wordpress-composer

Add the following lines to your `wp-config.php` to disable all automatic updates:

```php
define( 'WP_AUTO_UPDATE_CORE', false );
```

### Upgrading core

Upgrading WordPress core requires a full writing permissions on the entire codebase, we do not provide such wide permissions for security reasons. So you'll have to upgrade your core either manually via your git or by upgrading your stack if you deployed a vanilla WordPress. 

### Upgrading themes and plugins

If your theme or plugin introduces a new directory or a file under a non-standard path, you'll have to grant writing permissions manually by changing the owner's group to `:www-data` and adding writing permissions to the group. Connect to your app instance by SSH and run:

```shell
chown :www-data YOUR_FILE
chmod 664 YOUR_FILE
```

Or if you want to set writing permission on a directory recursively:

```shell
chown :www-data -R YOUR_DIR
chmod 664 -R YOUR_DIR
```

## WordPress config

### wp-config.php

The `wodby.wp-config.php` file contains configuration settings for integration with Wodby services such as Database connection, Cache storage and Reverse Caching Proxy settings. You can override settings specified in `wodby.wp-config.php` in your `wp-config.php` file after the include.

Wodby automatically adds include of `wodby.wp-config.php` to `wp-config.php` file in WP root with every deployment if there's no occurrences of `wodby.wp-config.php` in your config file, otherwise we assume you've already added the include manually. If `wp-config.php` file does not exist Wodby will create it automatically.

Do not edit `wodby.wp-config.php`, all changes to this file will be reset.

Use environment variable `$WP_TABLE_PREFIX` to override your table prefix (`$table_prefix`).

### Files

Files for WordPress located in `/mnt/files/public` and symlinked to `wp-content/uploads`.

### Base URL

The domain marked with primary flag will be used as a `WP_HOME` and `WP_SITEURL` in `wodby.wp-config.php` file.

## Mail delivery

{!email-delivery.md!}

## Cron

By default we run the following cron command from [crond container](containers.md#crond) every hour:

```
wp cron event run --due-now --path="${HTTP_ROOT}" --url="${BASE_URL}"
``` 

You can customize crontab from `[Instance] > Stack > Settings` page.   

## Cache control

You can clear caches and control cache settings from `[Instance] > Cache` page. The following actions are available:

* Clear application cache
* Clear redis cache (if enabled)
* Clear varnish cache (if enabled)
* Clear all caches
* Enable/disable opcache

## Multi-site 

WordPress multi-site supported, both subdomains and subdirectories based.
