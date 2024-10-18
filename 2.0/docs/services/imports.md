# Service imports

Service can define data imports. There are two types of how imports performed:

1. Simple files import from an archive
2. A mount of an archive to a path known to a container, a container will perform the import on a start-up. Normally used for databases  

In #1 we run import directly in the running volume. In #2 we switch replace persistent volume to a new volume with new data only if the import via start-uip was successful.
