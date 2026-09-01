# Backblaze

## B2 Cloud Storage

Wodby provides a native integration with Backblaze B2 Cloud Storage. You can use a customer-owned B2 bucket for app and
database backups through Backblaze's S3-Compatible API.

### Before creating the integration

1. In the Backblaze web console, open `B2 Cloud Storage > Buckets` and copy the bucket's **S3 Endpoint**.
2. Open **Application Keys** and create an application key. The master application key does not work with the
   S3-Compatible API.
3. Grant **Read and Write** access only to the buckets Wodby may use.
4. Copy `keyID` as the Application Key ID and `applicationKey` as the Application Key.

Enter the exact bucket name when creating a backup or backup preset. To populate the bucket selector with existing
buckets instead, enable **Allow List All Bucket Names** on the application key. Bucket listing is optional.

The integration form requires the S3 Endpoint, Application Key ID, and Application Key. Wodby validates access to the
exact destination separately when you save a backup or backup preset.

## Related pages

- [Storage providers](storage.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
