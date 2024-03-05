We provide `Makefile` that contains commands to simplify the work with your local environment. You can run `make [COMMAND]` to execute the following commands:

```
Usage: make COMMAND

Commands:
    help            List available commands and their description 
    up              Start up all container from the current compose.yml 
    start           Start stopped containers 
    stop            Stop all containers for the current compose.yml (docker compose stop) 
    down            Same as stop
    prune [service] Stop and remove containers, networks, images, and volumes (docker compose down)
    ps              List container for the current project (docker ps with filter by name)
    shell [service] Access a container via shell as a default user (by default [service] is php)
    logs [service]  Show containers logs, use [service] to show logs of specific service
    mutagen         Start mutagen container and runs mutagen project
```
