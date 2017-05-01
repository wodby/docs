# Containers

Infrastructure provided by Wodby is powered by docker containers. Our light-weight containers in most cases are based on <a href="http://alpinelinux.org" target="_blank">Alpine Linux</a>.
 
# Accessing containers

Some of the containers have SSH access, some of them not. If a container has SSHd, just copy and execute SSH command from `[Instance] > Stack > [CONTAINER]` page. 

## Accessing containers with no SSH (or obtaining root access)

If there's no SSH access to a container or you need to obtain **root access** to your container, you can always access from a server where they've been deployed by following these instructions:

* Connect to the server where app instance is deployed by SSH
* Navigate to `[Instance] > Stack > [CONTAINER]` in the Wodby Dashboard 
* Copy the `Access Command` command 
* Execute the copied command on the server as a root
* Now you're inside of the container with root privileges
