# Local environment with Docker4WordPress

Docker4WordPress is an open-source project ([GitHub page](https://github.com/wodby/docker4wordpress)) that provides pre-configured `compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

There are 2 options how to use docker4wordpress – you can either run [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) WordPress from the image or mount your own WordPress codebase:

### Vanilla WordPress

1. Clone [docker4wordpress repository](https://github.com/wodby/docker4wordpress) and switch to the [latest stable tag](https://github.com/wodby/docker4wordpress/releases) or download/unpack the source code from the [latest release](https://github.com/wodby/docker4wordpress/releases)
3. [Configure domains](#domains)
4. From project root directory run `docker compose up -d` or `make up` to start containers. Give it 10-20 seconds to initialize after the start
5. That's it! Proceed with WordPress installation at http://wp.docker.localhost:8000. Default database user, password and database name are all `wordpress`, database host is `mariadb`
6. You can see status of your containers and their logs via portainer: http://portainer.wp.docker.localhost:8000

### Mount my codebase

1. If you're starting a new project we recommend you to fork [wodby/wordpress-composer](https://github.com/wodby/wordpress-composer) project
2. Download and unpack `docker4wordpress.tar.gz` from the [latest stable release](https://github.com/wodby/docker4wordpress/releases) to your project root
3. Delete `compose.override.yml` as it's used to deploy vanilla WordPress
4. Ensure database credentials match in your `wp-config.php` and `.env` files
6. [Configure domains](#domains)
7. Optional: uncomment lines in the compose file to run valkey (redis), varnish, phpmyadmin, etc
8. Optional: [import existing database](#database-import-and-export)
9. Optional: macOS users please read [this](#docker-for-mac)
10. Optional: Windows users please read [this](#windows)
11. Run containers: [`make up`](#make-commands) or `docker compose up -d`
12. Your WordPress website should be up and running at http://wp.docker.localhost:8000
13. You can see status of your containers and their logs via portainer: http://portainer.wp.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker compose stop`.

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) feel free to delete `traefik.yml` that comes within `docker4wordpress.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4wordpress/releases)  
    
## Domains

[Traefik](https://hub.docker.com/_/traefik) container used for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `wp.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 wp.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service        | Domain                                           |
|----------------|--------------------------------------------------|
| `nginx/apache` | `http://wp.docker.localhost:8000`                |
| `pma`          | `http://pma.wp.docker.localhost:8000`            |
| `adminer`      | `http://adminer.wp.docker.localhost:8000`        |
| `mailpit`      | `http://mailpit.wp.docker.localhost:8000`        |
| `varnish`      | `http://varnish.wp.docker.localhost:8000`        |
| `portainer`    | `http://portainer.wp.docker.localhost:8000`      |
| `webgrind`     | `http://webgrind.wp.docker.localhost:8000`       |
| `opensearch`   | `http://opensearch.drupal.docker.localhost:8000` |

## Mail sending

{!local/php-mail.md!}

## Xdebug

{!local/xdebug.md!}

## Database import and export

### MariaDB

{!local/mariadb.md!}

### PostgreSQL

{!local/postgres.md!}

## Make commands

{!local/php-make-commands.md!}

WordPress-specific:

```
make wp [command] Execute wp cli command (runs with --path /var/www/html, you can override it via WP_ROOT=PATH)
```

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

{!local/php-permissions.md!}

## Running multiple Projects

{!local/multiple-projects.md!}