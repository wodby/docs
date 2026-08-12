# Wodby Blob Storage

Wodby Blob Storage is the built-in object storage destination for application and database backups. Choose it when
you want Wodby to store backup archives without creating a third-party storage integration or managing your own
bucket credentials.

Unlike Amazon S3, Google Cloud Storage, Azure Blob Storage, or DigitalOcean Spaces, Wodby Blob Storage does not require
an integration, bucket, region, or storage class. Wodby manages the storage location and provides expiring download
links for completed backups.

## Availability

Wodby Blob Storage is available on paid subscriptions. Manual backups and enabled automatic backup presets that use
it are rejected on the free Developer plan.

The REST API has one migration-only exception for moving Wodby 1 configurations: a free organization may create an
automatic Wodby Blob Storage preset when the preset is disabled. Enabling that preset still requires a paid
subscription. For this API representation, use `integrationId: 0`, an empty `bucket`, `auto: true`, and
`disabled: true`.

## Billing

Wodby Blob Storage costs **$0.05 per stored GB**. There is no included free storage, and data transfer is not billed.
Usage is based on the organization's current completed backup data stored by Wodby. Failed, expired, and deleted
backup objects stop contributing after storage cleanup and the next usage synchronization.

## Related pages

- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
- [Storage providers](storage.md)
- [Billing](../pricing.md)
