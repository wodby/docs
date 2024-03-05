# Local environment with Docker4PHP

Docker4PHP is an open-source project ([GitHub page](https://github.com/wodby/docker4php)) that provides pre-configured `compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

1. Download `docker4php.tar.gz` from the [latest stable release](https://github.com/wodby/docker4php/releases) and unpack to your PHP project root
2. Make sure `NGINX_SERVER_ROOT` (or `APACHE_DOCUMENT_ROOT`) is set to your project public directory with `index.php` (by default `/var/www/html/public`)  
3. Ensure database credentials match in your database config and `.env` files
4. For PHP <8.2 switch mail sending to `ssmtp` (see [why](#mail-sending)) 
5. [Configure domains](#domains) 
6. Optional: [import existing database](#database-import-and-export) 
7. Optional: uncomment lines in the compose file to run redis, elasticsearch, kibana, etc
8. Optional: macOS users please read [this](#docker-for-mac)
9. Optional: Windows users please read [this](#permissions-issues)
10. Run containers: [`make up`](#make-commands) or `docker compose up -d`
11. Your php application should be up and running at http://php.docker.localhost:8000
12. You can see status of your containers and their logs via portainer: http://portainer.php.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker compose stop`.

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) feel free to delete `traefik.yml` that come within `docker4php.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4php/releases)  
    
## Domains

Docker4PHP uses [traefik](https://hub.docker.com/_/traefik) container for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `php.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 php.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service        | Domain                                       |
|----------------|----------------------------------------------|
| `nginx/apache` | `http://php.docker.localhost:8000`           |
| `pma`          | `http://pma.php.docker.localhost:8000`       |
| `adminer`      | `http://adminer.php.docker.localhost:8000`   |
| `mailhog`      | `http://mailhog.php.docker.localhost:8000`   |
| `solr`         | `http://solr.php.docker.localhost:8000`      |
| `kibana`       | `http://kibana.php.docker.localhost:8000`    |
| `node`         | `http://front.php.docker.localhost:8000`     |
| `varnish`      | `http://varnish.php.docker.localhost:8000`   |
| `portainer`    | `http://portainer.php.docker.localhost:8000` |
| `webgrind`     | `http://webgrind.php.docker.localhost:8000`  |

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

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

{!local/php-permissions.md!}

## Running multiple Projects

{!local/multiple-projects.md!}