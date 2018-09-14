We provide `Makefile` that contains commands to simplify the work with your local environment. You can run `make [COMMAND]` to execute the following commands:

```
Usage: make COMMAND

Commands:
    up              Start up all container from the current docker-compose.yml 
    stop            Stop all containers for the current docker-compose.yml (docker-compose stop) 
    down            Same as stop
    prune           Stop and remove containers, networks, images, and volumes (docker-compose down)
    ps              List container for the current project (docker ps with filter by name)
    shell           Access PHP container via shell as a default user  (docker exec -ti $CID sh)
    logs [service]  Show containers logs, use [service] to show logs of specific service
```
