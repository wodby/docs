# Wodby Blob Storage

Wodby Blob Storage is the built-in object storage destination for application and database backups. Choose it when
you want Wodby to store backup archives without creating a third-party storage integration or managing your own
bucket credentials.

Unlike a third-party storage destination, Wodby Blob Storage does not require an integration, bucket, or storage class.
Choose **United States** or **Europe** in the **Region** field when creating a backup or backup preset. **United
States** is selected by default. Wodby manages the storage location and provides expiring download links for completed
backups.

The selected region is saved with each backup. Changing a preset's region affects backups created from that preset in
the future; it does not move or replace existing backups.

## Download links

The download action returns a time-limited signed URL on `blob.wodby.com`. Treat the signed URL as a temporary
credential and do not share it.

## Voiding backup files

You can permanently remove the stored file for a completed Wodby Blob Storage backup without deleting its backup
record. Open the backup details and select **Void backup file**, then confirm the irreversible action.

After the file is voided:

- the backup record and its metadata remain available for history and auditing
- the file cannot be downloaded or used as the source of an import
- previously generated download links stop working
- the action cannot be undone and the file cannot be recovered

The action is disabled while a pending or running import is using the backup. Wait for the import to finish or cancel
it before voiding the file.

**Void backup file** is available only for Wodby Blob Storage. For a third-party storage destination, manage the
object's lifecycle through that storage provider.

To store backups in a Cloudflare account and bucket that you manage, create a
[Cloudflare R2 storage integration](cloudflare.md#r2) instead. That is a third-party backup destination and is not
billed as Wodby Blob Storage.

## Availability

Wodby Blob Storage is available on paid subscriptions. Manual backups and enabled automatic backup presets that use
it are rejected on the free Developer plan.

Disabled presets imported from Wodby 1 require a paid subscription before you can enable them.

## Billing

Wodby Blob Storage costs **$0.05 per stored GB**. There is no included free storage, and data transfer is not billed.
Usage is based on the organization's current completed backup data stored by Wodby. Failed, expired, and deleted
backup objects stop contributing after storage cleanup and the next usage synchronization. A successfully voided file
also stops contributing after the next usage synchronization.

## Related pages

- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
- [Storage providers](storage.md)
- [Cloudflare R2](cloudflare.md#r2)
- [Billing](../pricing.md)
