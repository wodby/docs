# Local environment with Docker4Drupal

Docker4Drupal is an open-source project ([GitHub page](https://github.com/wodby/docker4drupal)) that provides pre-configured `docker-compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

There are 2 options how to use docker4drupal – you can either run [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) Drupal from the image or mount your own Drupal codebase:

### Vanilla Drupal

1. Clone [docker4drupal repository](https://github.com/wodby/docker4drupal) and switch to the [latest stable tag](https://github.com/wodby/docker4drupal/releases) or download/unpack the source code from the [latest release](https://github.com/wodby/docker4drupal/releases)
2. Optional: for Drupal 8 or 7 comment out corresponding `DRUPAL_TAG` and `NGINX_VHOST_PRESET` in `.env` file
4. [Configure domains](#domains)
3. From project root directory run `docker-compose up -d` or `make up` to start containers. Give it 10-20 seconds to initialize after the start
5. That's it! Proceed with Drupal installation at http://drupal.docker.localhost:8000. Default database user, password and database name are all `drupal`, database host is `mariadb`

### Mount my codebase

1. If you're starting a new project we recommend you to use [drupal/recommended-project](https://www.drupal.org/docs/develop/using-composer/starting-a-site-using-drupal-composer-project-templates)
2. Download and unpack `docker4drupal.tar.gz` from the [latest stable release](https://github.com/wodby/docker4drupal/releases) to your project root
3. Delete `docker-compose.override.yml` as it's used to deploy vanilla Drupal
4. Ensure `NGINX_SERVER_ROOT` (or `APACHE_DOCUMENT_ROOT`) is correct, by default set to `/var/www/html/web` for composer-based projects where Drupal is in `web` subdirectory
5. Ensure database access settings in your `settings.php` corresponds to values in `.env` file, e.g.:
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
6. [Configure domains](#domains)
7. Optional: for Drupal 8 or 7 update `NGINX_VHOST_PRESET` correspondingly in your `.env` file
8. Optional: uncomment lines in the compose file to run redis, solr, varnish, etc
9. Optional: [import existing database](#database-import-and-export)
10. Optional: macOS users please read [this](#docker-for-mac)
11. Optional: Windows users please read [this](#windows)
12. Run containers: [`make up`](#make-commands) or `docker-compose up -d`
13. Your drupal website should be up and running at http://drupal.docker.localhost:8000
14. You can see status of your containers and their logs via portainer: http://portainer.drupal.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker-compose stop`.

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) feel free to delete `traefik.yml` that comes within `docker4drupal.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4drupal/releases)      

## Domains

[Traefik](https://hub.docker.com/_/traefik) container used for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `drupal.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 drupal.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:

| Service        | Domain                                          |
|----------------|-------------------------------------------------|
| `nginx/apache` | `http://drupal.docker.localhost:8000`           |
| `pma`          | `http://pma.drupal.docker.localhost:8000`       |
| `adminer`      | `http://adminer.drupal.docker.localhost:8000`   |
| `mailhog`      | `http://mailhog.drupal.docker.localhost:8000`   |
| `solr`         | `http://solr.drupal.docker.localhost:8000`      |
| `nodejs`       | `http://nodejs.drupal.docker.localhost:8000`    |
| `node`         | `http://front.drupal.docker.localhost:8000`     |
| `varnish`      | `http://varnish.drupal.docker.localhost:8000`   |
| `portainer`    | `http://portainer.drupal.docker.localhost:8000` |
| `webgrind`     | `http://webgrind.drupal.docker.localhost:8000`  |

## Xdebug

{!local/xdebug.md!}

## Crond

Crond enabled by default and runs every hour. The default command is:
```
drush -r /var/www/html/web cron
```
You might need to change if your HTTP root is different. Runs from `www-data` user.

## Solr (Search API)

- Make sure your Drupal site already installed
- Uncomment `solr` and `zookeeper` services in your `docker-compose.yml`, start it (`make`) and wait until both services fully started
- Access Solr container via `make shell solr` and run `make init -f /usr/local/bin/actions.mk`. This will enable authentication for Solr Cloud mode and create a collection named `default` that will use `_default` config set
- Now access PHP container via `make shell` and install Search API Solr module `composer require drupal/search_api_solr`
- Enable Search API Solr Admin module `drush en -y search_api_solr_admin`
- Go to `Home » Administration » Configuration » Search and metadata » Search API` and create a new server of type `Solr Cloud with Basic Auth` with the following settings:
```
HTTP protocol: http
Solr host: solr
Solr port: 8983
Default Solr collection: default
---
HTTP BASIC AUTHENTICATION
Username: solr
Password: SolrRocks 
```
- After the server creation you should see the error message `You are using an incompatible Solr schema.`
- Click `+ Upload confiset`, check the checkbox on the page and submit to override the configset
- The Solr server is now ready to use!

## Database import and export

### MariaDB

{!local/mariadb.md!}

### PostgreSQL

{!local/postgres.md!}

## Make commands

Basic:

{!local/php-make-commands.md!}

Drupal-specific:

```
make drush [command] Execute drush command (runs with -r /var/www/html/web, you can override it via DRUPAL_ROOT=PATH)
```

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

{!local/php-permissions.md!}

## Running multiple Projects

{!local/multiple-projects.md!}
