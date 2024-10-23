# Application Backups

If an application's stack has services that provide [backups function](../services/backups.md) you can run backups for the corresponding app service. The backup process consist of three steps: 

- the actual backup process, the result stored in the container's ephemeral storage
- mirroring the backup to the third-party cloud storage, such as S3 or analogs
- cleaning up the backup from the container's ephemeral storage
