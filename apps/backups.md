# Backups

## Manual and auto backups

[`Instance page > Backups`]

Wodby provides backups for database and files. The depth of backups by default is `7 days`. You can configure time when auto-backups run (in UTC). You can always restore from the selected backup in one click.

To avoid extra load on your server, backups run successively per server. You can always run a manual backup of your app's database/files. Backups files are available to download in tar.gz archives.

## Mirroring 

[`Instance page > Backups > Mirroring`]

Wodby provides backup mirroring to different storages. Currently only AWS S3 supported. You can either connect your own AWS S3 bucket or use AWS S3 bucket provided by Wodby.

### Mirroring to AWS S3 provided by Wodby

The simplest way to setup backup mirroring is to use simply select Wodby storage as the provider. We will store your backups in <a href="https://aws.amazon.com/s3/" target="_blank">AWS S3</a> bucket. The depth of the backups is `7 days`. Meaning that backups with age more than 7 days (since the moment of upload) will be deleted automatically.  

### Create your own Bucket

Please read official <a href="http://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html" target="_blank">Getting Started Guide</a> by AWS. 