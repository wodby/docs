# Accessing containers

!!! tip "Stacks with SSHd container"
    Some stacks provide an SSHd container to access your codebase, in this case you can copy and execute SSH command from `Instance > Stack > SSHd` page. 

## Access container as default user

* Connect to the server where app instance is deployed by SSH
* Navigate to `Instance > Stack > [CONTAINER]` from Wodby dashboard
* Copy the `Access Command` command
* Execute the copied command on the server as root
* Now you're inside of the container as container default user

## Access container as root

If you need root permissions inside a container and container's default user is not root, follow these steps:

1. Access a container as a default user and get container hostname by executing the following command:
    ```shell
    echo $HOSTNAME
    ```
    
2. Execute the following command from a host server as root by replacing `[HOSTNAME]` with your value
    ```shell
    docker exec -ti --user=root $(docker ps | grep [HOSTNAME] | grep -v pause | awk '{ print $1 }') sh
    ``` 
