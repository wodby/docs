# Local environment with Docker4Python

Docker4Python is an open-source project ([GitHub page](https://github.com/wodby/docker4python)) that provides pre-configured `docker-compose.yml` file with images to spin up local environment on Linux, Mac OS X and Windows. 

## Requirements

* Install Docker ([Linux](https://docs.docker.com/engine/installation), [Docker for Mac](https://docs.docker.com/engine/installation/mac) or [Docker for Windows (10+ Pro)](https://docs.docker.com/engine/installation/windows))
* For Linux additionally install [docker compose](https://docs.docker.com/compose/install)

## Usage

{!local/db-data-persistence.md!}

1. Download `docker4python.tar.gz` from the [latest stable release](https://github.com/wodby/docker4python/releases) and unpack to your Python project root
2. Ensure database credentials match in your database config and `.env` files, see example for Python on Django below
3. [Configure domains](#domains) 
4. Optional: [import existing database](#database-import-and-export) 
5. Optional: uncomment lines in the compose file to change DBMS (PostgreSQL by default) or run Redis, Elasticsearch, etc
6. Optional: macOS users please read [this](#docker-for-mac)
7. Optional: Windows users please read [this](#permissions-issues)
8. By default python container will start Gunicorn HTTP server, update `$GUNICORN_APP` in `Dockerfile` for your application name. If you have your application in a subdirectory specify it in `$GUNICORN_PYTHONPATH`   
9. Build your python image by running `make build` or `docker-compose build`. This will create a new image with installed packages from your `requirements.txt`. If you're using `pipenv` uncomment the corresponding lines in Dockerfile to copy `Pipfile`, `Pipfile.lock` and run `pipenv install` instead of `pip`. If compilation of native extension for some of your packages fail you probably need to install additional dev packages, see example in `Dockerfile`  
10. Run containers: [`make`](#make-commands) or `docker-compose up -d`. Your codebase from `./` will be mounted to the python image with installed packages 
11. Your python application should be up and running at http://python.docker.localhost:8000
12. You can see status of your containers and their logs via portainer: http://portainer.python.docker.localhost:8000

You can stop containers by executing [`make stop`](#make-commands) or `docker-compose stop`.

!!! info "Static and media files on Django"
    If you're running Django make sure you have `STATIC_ROOT` specified in your settings file, if not, add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')`. The default Nginx [virtual host preset](https://github.com/wodby/nginx#django) uses `/static` and `/media` locations and the same directories in your application root. You can adjust them via [`$NGINX_DJANGO_` environment variables](https://github.com/wodby/nginx#environment-variables) 

Examples for Django database (PostgreSQL) and cache setup (`django-redis` package), add it to your `settings.py`:
```py
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': os.getenv('DB_USER', 'user'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

!!! info "Optional files"
    If you don't need to [run multiple projects](#running-multiple-projects) and don't use [docker-sync to improve volumes performance on macOS](#docker-for-mac) feel free to delete `traefik.yml` and `docker-sync.yml` that come with the `docker4python.tar.gz`

!!! success "Get updates"
    We release updates to images from time to time, you can find detailed changelog and update instructions on GitHub under [releases page](https://github.com/wodby/docker4python/releases)  
    
## Domains

Docker4Python uses [traefik](https://hub.docker.com/_/traefik) container for routing. By default, we use port `8000` to avoid potential conflicts but if port `80` is free on your host machine just replace traefik's ports definition in the compose file.

By default `BASE_URL` set to `python.docker.localhost`, you can change it in `.env` file.

Add `127.0.0.1 python.docker.localhost` to your `/etc/hosts` file (some browsers like Chrome may work without it). Do the same for other default domains you might need from listed below:  

| Service      | Domain                                        |
| ------------ | ------------------------------------------    |
| `nginx`      | `http://python.docker.localhost:8000`           |
| `adminer`    | `http://adminer.python.docker.localhost:8000`   |
| `mailhog`    | `http://mailhog.python.docker.localhost:8000`   |
| `solr`       | `http://solr.python.docker.localhost:8000`      |
| `kibana`     | `http://kibana.python.docker.localhost:8000`    |
| `node`       | `http://front.python.docker.localhost:8000`     |
| `varnish`    | `http://varnish.python.docker.localhost:8000`   |
| `portainer`  | `http://portainer.python.docker.localhost:8000` |

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
    up              Start up all container from the current docker-compose.yml 
    build           Build python image with packages from your requirements.txt or Pipfile 
    stop            Stop all containers for the current docker-compose.yml (docker-compose stop) 
    down            Same as stop
    prune           Stop and remove containers, networks, images, and volumes (docker-compose down)
    ps              List container for the current project (docker ps with filter by name)
    shell           Access Python container via shell as a default user  (docker exec -ti $CID sh)
    logs [service]  Show containers logs, use [service] to show logs of specific service
```

## Docker for mac

{!local/docker-for-mac.md!}

## Permissions issues

You might have permissions issues caused by non-matching uid/gid on your host machine and the default user in php container.

### Linux

### macOS

[Use `-dev-macos` version](#macos-permissions-issues) of python image where default `wodby` user has `501:20` uid/gid that matches default macOS user.

### Windows

Since you [can't change owner of mounted volumes](https://github.com/docker/for-win/issues/39) in Docker for Win, the only solution is to run everything as root, add the following options to `python` service in your docker-compose file:

```yml
  python:
    user: root
```

### Different uid/gid?

You can rebuild the base image [wodby/python](https://github.com/wodby/python) with custom user/group ids by using docker build arguments `WODBY_USER_ID`, `WODBY_GROUP_ID` (both `1000` by default)

## Running multiple Projects

{!local/multiple-projects.md!}