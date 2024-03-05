# Local environment with Docker4Laravel

Docker4Laravel is an open-source project ([GitHub page](https://github.com/wodby/docker4laravel)) that provides pre-configured `compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

1. Download `docker4laravel.tar.gz` from the [latest stable release](https://github.com/wodby/docker4laravel/releases) and unpack to your Laravel project root
2. Make sure `NGINX_SERVER_ROOT` (or `APACHE_DOCUMENT_ROOT`) is set to your project public directory with `index.php` (by default `/var/www/html/public`)  
3. Ensure database credentials match in your database config and `.env` files
4. [Configure domains](#domains) 
5. Optional: [import existing database](#database-import-and-export) 
6. Optional: uncomment lines in the compose file to run redis, elasticsearch, kibana, etc
7. Optional: macOS users please read [this](#docker-for-mac)
8. Optional: Windows users please read [this](#permissions-issues)
9. Run containers: [`make up`](#make-commands) or `docker compose up -d`
10. Your laravel application should be up and running at http://laravel.docker.localhost:8000
11. You can see status of your containers and their logs via portainer: http://portainer.laravel.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker compose stop`.

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) feel free to delete `traefik.yml` that come within `docker4laravel.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4laravel/releases)  
    
## Domains

Docker4Laravel uses [traefik](https://hub.docker.com/_/traefik) container for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `laravel.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 laravel.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service        | Domain                                           |
|----------------|--------------------------------------------------|
| `nginx/apache` | `http://laravel.docker.localhost:8000`           |
| `pma`          | `http://pma.laravel.docker.localhost:8000`       |
| `adminer`      | `http://adminer.laravel.docker.localhost:8000`   |
| `mailhog`      | `http://mailhog.laravel.docker.localhost:8000`   |
| `solr`         | `http://solr.laravel.docker.localhost:8000`      |
| `kibana`       | `http://kibana.laravel.docker.localhost:8000`    |
| `node`         | `http://front.laravel.docker.localhost:8000`     |
| `varnish`      | `http://varnish.laravel.docker.localhost:8000`   |
| `portainer`    | `http://portainer.laravel.docker.localhost:8000` |
| `webgrind`     | `http://webgrind.laravel.docker.localhost:8000`  |

## Xdebug

{!local/xdebug.md!}

## Database import and export

### MariaDB

{!local/mariadb.md!}

### PostgreSQL

{!local/postgres.md!}

## Make commands

{!local/php-make-commands.md!}

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

{!local/php-permissions.md!}

## Running multiple Projects

{!local/multiple-projects.md!}