We provide [`Makefile`](https://github.com/wodby/docker4drupal/blob/master/docker.mk) file that contains commands to simplify the work with your local environment. You can run `make [COMMAND]` to execute the following commands:

```
Usage: make COMMAND

Commands:
    up              Start up all container from the current docker-compose.yml 
    stop            Stop all containers for the current docker-compose.yml (docker-compose stop) 
    down            Same as stop
    prune           Stop and remove containers, networks, images, and volumes (docker-compose down)
    ps              List container for the current project (docker ps with filter by name)
    shell           Enter PHP container as default user (docker exec -ti $CID sh)
    drush [command] Execute drush command (runs with -r /var/www/html/web, you can override it via DRUPAL_ROOT=PATH)
    logs [service]  Show containers logs, use [service] to show logs of specific service
```
