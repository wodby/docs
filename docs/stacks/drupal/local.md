# Local environment with Docker4Drupal

Docker4Drupal is an open-source project ([GitHub page](https://github.com/wodby/docker4drupal)) that provides pre-configured `docker-compose.yml` file from to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

There are 2 options how to use docker4drupal – you can either run [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) Drupal from the image or mount your own Drupal codebase:

### Vanilla Drupal

1. Clone [docker4drupal repository](https://github.com/wodby/docker4drupal) and switch to the [latest stable tag](https://github.com/wodby/docker4drupal/releases) or download/unpack the source code from the [latest release](https://github.com/wodby/docker4drupal/releases)
2. Optional: for Drupal 7 or 6 comment out corresponding `DRUPAL_TAG` and `NGINX_TAG` in `.env` file
4. [Configure domains](#domains)
3. From project root directory run `docker-compose up -d` or `make up` to start containers. Give it 10-20 seconds to initialize after the start
5. That's it! Proceed with Drupal installation at http://drupal.docker.localhost:8000. Default database user, password and database name are all `drupal`, database host is `mariadb`
6. You can see status of your containers and their logs via portainer: http://portainer.drupal.docker.localhost:8000

### Mount my codebase

1. Download `docker4drupal.tar.gz` from the [latest stable release](https://github.com/wodby/docker4drupal/releases) and unpack to your Drupal project root. If you choose to clone [the repository](https://github.com/wodby/docker4drupal) delete `docker-compose.override.yml` as it's used to deploy vanilla Drupal
2. Ensure `NGINX_SERVER_ROOT` (or `APACHE_SERVER_ROOT`) is correct, by default set to `/var/www/html/web` for composer-based projects where Drupal is in `web` subdirectory
3. Ensure database access settings in your `settings.php` corresponds to values in `.env` file, e.g.:
    ```php
    $databases['default']['default'] = array (
      'database' => 'drupal', // same as $DB_NAME
      'username' => 'drupal', // same as $DB_USER
      'password' => 'drupal', // same as $DB_PASSWORD
      'host' => 'mariadb', // same as $DB_HOST
      'driver' => 'mysql', 	// same as $DB_DRIVER
      'port' => '3306',	// different for PostgreSQL
      'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql', // different for PostgreSQL
      'prefix' => '',
    );
    ```     
4. [Configure domains](#domains)
5. Optional: for Drupal 7 or 6 comment out corresponding `PHP_TAG` and `NGINX_TAG` in your `.env` file
6. Optional: [import existing database]()
7. Optional: uncomment lines in the compose file to run redis, solr, varnish, etc
8. Optional: macOS users please read [this](../_includes/docker-for-mac.md)
9. Optional: Windows users please read [this](../_includes/permissions.md#windows)
10. Run containers: `docker-compose up -d` or `make up` (see all [make commands](../_includes/make-commands.md))
11. That's it! Your drupal website should be up and running at http://drupal.docker.localhost:8000
12. You can see status of your containers and their logs via portainer: http://portainer.drupal.docker.localhost:8000

!!! info "Optional files"
    If you don't need to [run multiple projects](../_includes/multiple-projects.md) and don't use [docker-sync to improve volumes performance on macOS](../_includes/docker-for-mac.md) feel free to delete `traefik.yml` and `docker-sync.yml` that come with the `docker4drupal.tar.gz`

You can stop containers by executing `docker-compose stop` or `make stop`

Have a problem? See [known issues](../../local/known-issues.md), submit a new issue on [GitHub](https://github.com/wodby/docker4drupal/issues) or ask [community on Slack](http://slack.wodby.com)

Feel free to adjust volumes and ports in the compose file for your convenience. 

## Domains

[Traefik](https://hub.docker.com/_/traefik) container used for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `drupal.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 drupal.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:

| Service      | Domain                                          |
| ------------ | ----------------------------------------------- |
| `nginx/apache` | `http://drupal.docker.localhost:8000`           |
| `pma` | `http://pma.drupal.docker.localhost:8000`       |
| `adminer` | `http://adminer.drupal.docker.localhost:8000`   |
| `mailhog` | `http://mailhog.drupal.docker.localhost:8000`   |
| `solr` | `http://solr.drupal.docker.localhost:8000`      |
| `nodejs` | `http://nodejs.drupal.docker.localhost:8000`    |
| `node` | `http://front.drupal.docker.localhost:8000`     |
| `varnish` | `http://varnish.drupal.docker.localhost:8000`   |
| `portainer` | `http://portainer.drupal.docker.localhost:8000` |
| `webgrind` | `http://webgrind.drupal.docker.localhost:8000`  |

## Database import and export

{!stacks/_includes/local/db-import-export.md!}

## Make commands

{!stacks/_includes/local/make-commands.md!}

## Docker for mac

{!stacks/_includes/local/docker-for-mac.md!}

## Permissions issues

{!stacks/_includes/local/permissions.md!}

## Running multiple Projects

{!stacks/_includes/local/multiple-projects.md!}