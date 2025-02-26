# Local environment with Docker4Ruby

Docker4Ruby is an open-source project ([GitHub page](https://github.com/wodby/docker4ruby)) that provides pre-configured `compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

1. Download `docker4ruby.tar.gz` from the [latest stable release](https://github.com/wodby/docker4ruby/releases) and unpack to your Ruby project root
2. Ensure database credentials match in your database config and `.env` files, see example for Ruby on Rails below
3. [Configure domains](#domains) 
4. Optional: [import existing database](#database-import-and-export) 
5. Optional: uncomment lines in the compose file to change DBMS (PostgreSQL by default) or run Sidekiq, Valkey (redis), OpenSearch, etc
6. Optional: macOS users please read [this](#docker-for-mac)
7. Optional: Windows users please read [this](#permissions-issues)
8. By default, ruby container will start Puma HTTP server, if you want to change it modify `Dockerfile`
9. Build your ruby image by running `make build` or `docker compose build`. This will create a new image with installed gems from your `Gemfile.lock`. If compilation of native extension for some of your gems fail you probably need to install additional dev packages, see example in `Dockerfile`  
10. Run containers: [`make`](#make-commands) or `docker compose up -d`. Your codebase from `./` will be mounted to the ruby image with installed gems 
11. Your ruby application should be up and running at http://ruby.docker.localhost:8000
12. You can see status of your containers and their logs via portainer: http://portainer.ruby.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker compose stop`.

Examples for Ruby on Rails database setup, `config/database.yml`:
```yaml
development:
  adapter: <%= ENV['DB_ADAPTER'] %>
  encoding: unicode
  database: <%= ENV['DB_NAME'] %>
  pool: 5
  username: <%= ENV['DB_USER'] %>
  password: <%= ENV['DB_PASSWORD'] %>
  host: <%= ENV['DB_HOST'] %>
```

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) feel free to delete `traefik.yml` that comes within `docker4ruby.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4ruby/releases)  
    
## Domains

Docker4Ruby uses [traefik](https://hub.docker.com/_/traefik) container for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `ruby.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 ruby.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service      | Domain                                           |
|--------------|--------------------------------------------------|
| `nginx`      | `http://ruby.docker.localhost:8000`              |
| `adminer`    | `http://adminer.ruby.docker.localhost:8000`      |
| `mailpit`    | `http://mailpit.ruby.docker.localhost:8000`      |
| `solr`       | `http://solr.ruby.docker.localhost:8000`         |
| `node`       | `http://front.ruby.docker.localhost:8000`        |
| `varnish`    | `http://varnish.ruby.docker.localhost:8000`      |
| `portainer`  | `http://portainer.ruby.docker.localhost:8000`    |
| `opensearch` | `http://opensearch.drupal.docker.localhost:8000` |

## Database import and export

### MariaDB

{!local/mariadb.md!}

### PostgreSQL

{!local/postgres.md!}

## Make commands

We provide `Makefile` that contains commands to simplify the work with your local environment. You can run `make [COMMAND]` to execute the following commands:

```
Usage: make COMMAND

Commands:
    help            List available commands and their description
    up              Start up all container from the current compose.yml
    start           Start stopped containers      
    build           Build ruby image with gems from your Gemfile.lock 
    stop            Stop all containers for the current compose.yml (docker compose stop) 
    down            Same as stop
    prune [service] Stop and remove containers, networks, images, and volumes (docker compose down)
    ps              List container for the current project (docker ps with filter by name)
    shell [service] Access a container via shell as a default user (by default [service] is ruby)
    logs [service]  Show containers logs, use [service] to show logs of specific service
    mutagen         Starts mutagen-compose
```

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

You might have permissions issues caused by non-matching uid/gid on your host machine and the default user in php container.

### Linux

### macOS

[Use `-dev-macos` version](#macos-permissions-issues) of ruby image where default `wodby` user has `501:20` uid/gid that matches default macOS user.

### Windows

Since you [can't change owner of mounted volumes](https://github.com/docker/for-win/issues/39) in Docker for Win, the only solution is to run everything as root, add the following options to `ruby` service in your `compose.yml` file:

```yml
  ruby:
    user: root
```

### Different uid/gid?

You can rebuild the base image [wodby/ruby](https://github.com/wodby/ruby) with custom user/group ids by using docker build arguments `WODBY_USER_ID`, `WODBY_GROUP_ID` (both `1000` by default)

## Running multiple Projects

{!local/multiple-projects.md!}