# Local environment with Docker4WordPress

Docker4WordPress is an open-source project ([GitHub page](https://github.com/wodby/docker4wordpress)) that provides pre-configured `docker-compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

There are 2 options how to use docker4wordpress – you can either run [vanilla](https://en.wikipedia.org/wiki/Vanilla_software) WordPress from the image or mount your own WordPress codebase:

### Vanilla WordPress

1. Clone [docker4wordpress repository](https://github.com/wodby/docker4wordpress) and switch to the [latest stable tag](https://github.com/wodby/docker4wordpress/releases) or download/unpack the source code from the [latest release](https://github.com/wodby/docker4wordpress/releases)
2. [Configure domains](#domains)
3. From project root directory run `docker-compose up -d` or `make up` to start containers. Give it 10-20 seconds to initialize after the start
4. That's it! Proceed with WordPress installation at http://wp.docker.localhost:8000. Default database user, password and database name are all `wordpress`, database host is `mariadb`
5. You can see status of your containers and their logs via portainer: http://portainer.wp.docker.localhost:8000

### Mount my codebase

1. Download `docker4wordpress.tar.gz` from the [latest stable release](https://github.com/wodby/docker4wordpress/releases) and unpack to your WordPress project root. If you choose to clone [the repository](https://github.com/wodby/docker4wordpress) delete `docker-compose.override.yml` as it's used to deploy vanilla WordPress
2. Ensure database credentials match in your `wp-config.php` and `.env` files 
3. [Configure domains](#domains)
4. Optional: [import existing database](#database-import-and-export)
5. Optional: uncomment lines in the compose file to run redis, varnish, phpmyadmin, etc
8. Optional: macOS users please read [this](#docker-for-mac)
9. Optional: Windows users please read [this](#windows)
10. Run containers: [`make up`](#make-commands) or `docker-compose up -d`
11. Your WordPress website should be up and running at http://wp.docker.localhost:8000
12. You can see status of your containers and their logs via portainer: http://portainer.wp.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker-compose stop`.

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) and don't use [docker-sync to improve volumes performance on macOS](#docker-for-mac) feel free to delete `traefik.yml` and `docker-sync.yml` that come with the `docker4wordpress.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4wordpress/releases)  
    
## Domains

[Traefik](https://hub.docker.com/_/traefik) container used for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `wp.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 wp.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service        | Domain                                      |
| ------------   | -----------------------------------------   |
| `nginx/apache` | `http://wp.docker.localhost:8000`           |
| `pma`          | `http://pma.wp.docker.localhost:8000`       |
| `adminer`      | `http://adminer.wp.docker.localhost:8000`   |
| `mailhog`      | `http://mailhog.wp.docker.localhost:8000`   |
| `varnish`      | `http://varnish.wp.docker.localhost:8000`   |
| `portainer`    | `http://portainer.wp.docker.localhost:8000` |
| `webgrind`     | `http://webgrind.wp.docker.localhost:8000`  |

## Database import and export

{!local/db-import-export.md!}

## Make commands

{!local/php-make-commands.md!}

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

{!local/php-permissions.md!}

## Running multiple Projects

{!local/php-multiple-projects.md!}