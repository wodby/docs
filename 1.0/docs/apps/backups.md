# Backups

Some stacks provide backups orchestration for services such as database. You can run backups manually for applications based on such stacks from the dashboard. Backups of an application instance will be stored on the same server where the instance is deployed.

!!! question "How running backups affect my apps performance?"
    We limit all backup and mirroring tasks by CPU and RAM to minimize the impact on your applications performance. Auto-backups run successively within a server. 

## Auto backups

You can enable auto backups for your applications by specifying backup depth (backups older than this # of days will be cleaned up automatically) and time in UTC when to start the backup process.

To avoid extra load on your server, backups run successively per server.

## Mirroring

Wodby provides backup mirroring to different storages. You can either use your own storage (currently only AWS S3 supported) or Wodby Storage.

### Wodby Storage

The simplest way to setup backup mirroring is to use simply select Wodby Storage as a provider. The default location is US east region if not specified differently. Backups older than two weeks since the moment of upload will be deleted automatically.

### AWS S3

Specify the following AWS credentials to set up mirroring to your S3 bucket:

* AWS Access Key Id
* AWS Secret Access Key
* Bucket name
* Bucket region

## How backup process affect my server performance

We limit all backup-related tasks by CPU and RAM including mirroring to decrease the impact on your server performance. Additionally, we recommend setting auto backups start time to a night period when your application has the lowest traffic.

## How do I know my application auto backup fails

We sends a daily report about failed auto backups for the past 24 hours at 7:00 UTC.
