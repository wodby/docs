# Backups

Some stacks provide backups orchestration for services such as database. You can run backups manually for applications based on such stacks from the dashboard. Backups of an application instance will be stored on the same server where the instance is deployed.  

## Auto Backups

You can enable auto backups for your applications by specifying backup depth (backups older than this # of days will be cleaned up automatically) and time in UTC when to start the backup process. 

To avoid extra load on your server, backups run successively per server. 

## Mirroring 

Wodby provides backup mirroring to different storages. You can either use your own storage (currently only AWS S3 supported) or Wodby Storage.

### Wodby Storage

The simplest way to setup backup mirroring is to use simply select Wodby Storage as a provider. 
 
Backups older than 7 days (since the moment of upload) stored in Wodby Storage will be deleted automatically. **Limitation for Wodby Storage will soon be updated to X MB/GB per instance.**

### AWS S3

To mirror backups to your own AWS S3 bucket you'll need to specify the following information:

* AWS Access Key Id
* AWS Secret Access Key
* Bucket name
* Bucket region