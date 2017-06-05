# Containers logs

Most of the applications provided by Wodby stream their logs to a container output. These logs stored on disk but they are **not persistent**, docker deletes container's logs after its restart. Read [docker logs](https://docs.docker.com/engine/reference/commandline/logs/) to learn more. However some applications do not write all logs to output, e.g. Jira/Confluence/Cachet write some of their logs on a disk. 

To get containers' output logs copy `Show logs command` from `[Instance] > Stack > [CONTAINER]` page and execute it from a host server. 
