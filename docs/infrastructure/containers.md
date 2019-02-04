# Containers

Most of the container images provided in our managed stacks are based on the light-weight Linux distribution [Alpine Linux](https://alpinelinux.org/) (based on musl libc). All images are public and available on [Docker Hub](https://hub.docker.com/r/wodby/), their sources can be found on [GitHub](https://github.com/wodby/).

## Accessing containers

### via SSH container

Some stacks provide an SSHd container to access your codebase, you can find the SSH command on `Instance > Stack > SSHd` page. We'll automatically add your public SSH keys to this container. You can add your public keys from `Profile > Keys > Add new key` page. 

### as default user

If your stack does not have sshd container or you need to access a different container follow these steps:

* Connect to the server where app instance is deployed by SSH
* Navigate to `Instance > Stack > [CONTAINER]` from Wodby dashboard
* Copy the `Access Command` command
* Execute the copied command on the server as root
* Now you're inside of the container as container default user

### as root

If you need root permissions inside a container and container's default user is not root, follow these steps:

1. Access a container as a default user and get container hostname by executing the following command:
    ```shell
    echo $HOSTNAME
    ```
    
2. Execute the following command from a host server as root by replacing `[HOSTNAME]` with your value
    ```shell
    docker exec -ti --user=root $(docker ps | grep [HOSTNAME] | grep -v pause | awk '{ print $1 }') sh
    ``` 

### Accessing containers data from host

Containers persistent data can be accessed from the host server under `/srv/wodby/instances/[INSTANCE_UUID]​`

!!! warning "This may cause unexpected issues"
    Be careful while modifying containers' files as root – it could cause unexpected permissions issues because containers have a default user different from root

### Accessing container from local environment

```shell
# Get container id 
docker ps -a
# Access container via shell
docker exec -ti [container id] sh
```
