* PHP can be configured with the following [environment variables](https://github.com/wodby/php#environment-variables)
* Available [php extensions](https://github.com/wodby/php#php-extensions) 

### Environment variables

!!! warning "Variables availability"
    Environment variables (except ones provided by Wodby) won't be available in PHP-FPM because we set `PHP_FPM_CLEAR_ENV=yes` by default for security reasons. You can set it to `yes` to make all environment variables available in your code. 

In addition to [global environment variables](/infrastructure/env-vars.md), we provide the following variables in PHP container that you can use in your [post-deployment scripts](/apps/post-deployment-scripts.md) or settings files:

| Variable              | Description                                   |
| --------------------- | --------------------------------------------  |
| `$APP_ROOT`           | `/var/www/html` by default                    |
| `$HTTP_ROOT`          | e.g. `/var/www/html/web`                      |
| `$CONF_DIR`           | `/var/www/conf` by default                    |
| `$WODBY_APP_NAME`     | My app                                        |
| `$WODBY_HOST_PRIMARY` | example.com                                   |
| `$WODBY_URL_PRIMARY`  | http://example.com                            |
| `$WODBY_HOSTS`        | `[ "example.com", "dev.example.org.wod.by" ]` |

Deprecated variables:

| Variable             | Instead use    |
| -------------------- | -------------- |
| `$WODBY_APP_ROOT`    | `$APP_ROOT`    |
| `$WODBY_APP_DOCROOT` | `$HTTP_ROOT`   |
| `$WODBY_CONF`        | `$CONF_DIR`    |
| `$WODBY_DIR_CONF`    | `$CONF_DIR`    |

### Files directory permissions

Public files directory (symlink to `/mnt/files/public`) that used for uploads owned by `www-data` user (PHP-FPM user) by default and the default container user (`wodby`) has no writing permissions. So if you run a command that creates files in a public directory you will get insufficient permissions error. You can fix this problem by giving writing permissions for files directory to the owner's group (user `wodby` is a member of `www-data` group) by using one of the [helper scripts](https://github.com/wodby/php#helper-scripts):

```shell
sudo files_chmod /mnt/files/public
```

When you [manually import files](index.md#manual-import) under `wodby` user you should change files ownership to `www-data` user to let PHP-FPM create new files in directories, run the following command to change the ownership:

```shell
sudo files_chown /mnt/files/public
```

!!! info "Helper scripts scope" 
    `files_chmod` and `files_chown` are the only `sudo` commands available to `wodby` user and can be applied **only to directories** under `/mnt/files` .  
        
For mode details about users and permissions in PHP container see https://github.com/wodby/php#users-and-permissions

### Codebase directory permissions

The codebase owned by the default `wodby` (uid/gid `1000`) user. If you need to give writing permissions to PHP-FPM (`www-data` user with uid/gid `82`) to a directory outside on public files directory you can either access a container as root user or change it from the host server (single-server infrastructure): 

```shell
chown -R 1000:82 /srv/wodby/instances/[INSTANCE_UUID]/app/path-to-directory
chmod -R 775 /srv/wodby/instances/[INSTANCE_UUID]/app/path-to-directory
```
