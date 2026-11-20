Source: https://wodby.com/docs/2.0/providers/storage/

# Storage providers

Storage providers expose the `storage` type. Use this group when you want Wodby to send backups to an object storage service, either through Wodby Blob Storage or a connected third-party storage provider.

Machine name: `storage`

Use a storage provider when:

- you want app or database backups copied to an external bucket or object container
- you want reusable backup destinations for manual backups and backup presets
- you want backup storage to live in Wodby Blob Storage or your own cloud account

## Where it is used in Wodby

Storage provider integrations are used for:

- app backups
- database backups
- organization-wide, app-level, and database-level backup presets

Wodby stores backup archives in the selected bucket or container. It does not use storage integrations for live persistent volumes attached to running services.

## Supported providers

| Provider | Storage product |
| --- | --- |
| [Wodby](https://wodby.com/docs/2.0/providers/wodby-blob-storage/) | Blob Storage |
| [Amazon Web Services](https://wodby.com/docs/2.0/providers/aws/#s3) | S3 |
| [Azure](https://wodby.com/docs/2.0/providers/azure/#blob-storage) | Blob Storage |
| [Google Cloud Platform](https://wodby.com/docs/2.0/providers/gcp/#cloud-storage) | Cloud Storage |
| [DigitalOcean](https://wodby.com/docs/2.0/providers/digitalocean/#spaces) | Spaces |
| [Cloudflare](https://wodby.com/docs/2.0/providers/cloudflare/#r2) | R2 |
| [Backblaze](https://wodby.com/docs/2.0/providers/backblaze/#b2-cloud-storage) | B2 Cloud Storage |
| [Wasabi](https://wodby.com/docs/2.0/providers/wasabi/#object-storage) | Object storage |
| [S3-compatible storage](https://wodby.com/docs/2.0/providers/s3-compatible/#object-storage) | Any S3-compatible object storage, such as MinIO or Ceph |

When a provider grants bucket-list permission, Wodby shows the available buckets as suggestions. Bucket discovery is a
convenience rather than a requirement: you can enter the exact bucket or container name when credentials are scoped to
a specific destination and cannot list the account's other buckets.

## Related pages

- [Integration types](https://wodby.com/docs/2.0/integrations/types/)
- [Providers overview](https://wodby.com/docs/2.0/providers/)
- [Wodby Blob Storage](https://wodby.com/docs/2.0/providers/wodby-blob-storage/)
- [Application backups](https://wodby.com/docs/2.0/apps/backups/)
- [Database backups](https://wodby.com/docs/2.0/databases/backups/)
