# Backups

Some stacks provide backups orchestration for services such as database. You can run backups manually for applications based on such stacks from the dashboard. Backups of an application instance will be stored on the same server where the instance is deployed.

## Auto backups

You can enable auto backups for your applications by specifying backup depth (backups older than this # of days will be cleaned up automatically) and time in UTC when to start the backup process.

To avoid extra load on your server, backups run successively per server.

## Mirroring

Wodby provides backup mirroring to different storages. You can either use your own storage (currently only AWS S3 supported) or Wodby Storage.

### Wodby Storage

The simplest way to setup backup mirroring is to use simply select Wodby Storage as a provider. The default location is US east region if not specified differently. Backups older than a year (365 days) since the moment of upload will be deleted automatically.

!!! warning "Backups limit size in Wodby storage"
    The maximum size of free mirrored backups in Wodby storage will be limited in the near future. So if you have heavy backups we recommend using your own S3 bucket.

### AWS S3

Specify the following AWS credentials to set up mirroring to your S3 bucket:

* AWS Access Key Id
* AWS Secret Access Key
* Bucket name
* Bucket region
​
## How backup process affect my server performance

We limit all backup-related tasks by CPU and RAM including mirroring to decrease the impact on your server performance. Additionally, we recommend to set auto backups start time to a night period when your application have the lowest traffic.
