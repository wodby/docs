# Containers logs

To get containers logs copy and execute `Show logs command` (can be found on `[Instance] > Stack > [CONTAINER]` page) from a host server. 

Containers' logs stored on disk but **not persistent**, docker deletes container's logs after its restart. Read [docker logs](https://docs.docker.com/engine/reference/commandline/logs/) to learn more.

Please note that some applications do not write all logs to output, e.g. Jira/Confluence/Cachet write some of their logs on a disk, in this case you would need to [access the container](access.md). 