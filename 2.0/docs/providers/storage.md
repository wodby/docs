# Storage providers

Storage providers are third-party services whose integrations expose the `storage` type. Use this group when you want Wodby to send backups to an object storage service.

Machine name: `storage`

Use a storage provider when:

- you want app or database backups copied to an external bucket or object container
- you want reusable backup destinations for manual backups and backup presets
- you want backup storage to live in your own cloud account

## Where it is used in Wodby

Storage provider integrations are used for:

- app backups
- database backups
- organization-wide, app-level, and database-level backup presets

Wodby stores backup archives in the selected bucket or container. It does not use storage integrations for live persistent volumes attached to running services.

## Supported providers

| Provider | Storage product |
| --- | --- |
| [Amazon Web Services](aws.md#s3) | S3 |
| [Azure](azure.md#blob-storage) | Blob Storage |
| [Google Cloud Platform](gcp.md#cloud-storage) | Cloud Storage |
| [DigitalOcean](digitalocean.md#spaces) | Spaces |

## Related pages

- [Integration types](../integrations/types.md)
- [Providers overview](index.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
