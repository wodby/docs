# Accessing containers

How to access a container as root:

* Connect to the server where app instance is deployed by SSH
* Navigate to `Instance > Stack > [CONTAINER]` in the Wodby Dashboard 
* Copy the `Access Command` command 
* Execute the copied command on the server as a root
* Now you're inside of the container with root privileges

Some containers run with a duplicate SSHd container, in this case you can copy and execute SSH command from `Instance > Stack > [SSH CONTAINER]` page. 
