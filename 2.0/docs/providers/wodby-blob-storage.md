# Wodby Blob Storage

Wodby Blob Storage is the built-in object storage destination for application and database backups. Choose it when
you want Wodby to store backup archives without creating a third-party storage integration or managing your own
bucket credentials.

Unlike Amazon S3, Google Cloud Storage, Azure Blob Storage, or DigitalOcean Spaces, Wodby Blob Storage does not require
an integration, bucket, region, or storage class. Wodby manages the storage location and provides expiring download
links for completed backups.

## Download links

Wodby manages the storage destination and may change its internal implementation without changing how you select, use,
or pay for Wodby Blob Storage.

The download action returns a time-limited signed URL. Its hostname is an implementation detail and is not guaranteed
to remain on a `wodby.com` domain. Treat the signed URL as a temporary credential and do not share it.

To store backups in a Cloudflare account and bucket that you manage, create a
[Cloudflare R2 storage integration](cloudflare.md#r2) instead. That is a third-party backup destination and is not
billed as Wodby Blob Storage.

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
- [Cloudflare R2](cloudflare.md#r2)
- [Billing](../pricing.md)
