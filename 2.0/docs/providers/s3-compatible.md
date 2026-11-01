# S3-compatible storage

## Object storage

Use any object storage that implements the Amazon S3 API, such as MinIO or Ceph, for app and database backups. For
Amazon S3, Cloudflare R2, Backblaze B2, DigitalOcean Spaces and Wasabi, use their own providers instead; see
[Storage providers](storage.md).

### Requirements

- The storage must be reachable over HTTPS from the public internet. Wodby checks buckets, reads backup sizes and
  creates download links itself, so endpoints on a private network, `localhost` or internal addresses are not
  accepted.
- The storage must accept path-style requests, such as `https://s3.example.com/BUCKET/backup.sql.gz`. MinIO and Ceph
  do.

### Before creating the integration

1. Create a policy that allows Wodby to use your backup buckets. On services with AWS-style policies, such as MinIO and
   Ceph, use this policy. Replace `BUCKET` with your bucket name, and repeat both resource entries for every other
   bucket Wodby may use.

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["s3:ListBucket"],
          "Resource": "arn:aws:s3:::BUCKET"
        },
        {
          "Effect": "Allow",
          "Action": ["s3:GetObject", "s3:PutObject", "s3:AbortMultipartUpload"],
          "Resource": "arn:aws:s3:::BUCKET/*"
        }
      ]
    }
    ```

    | Permission | Used to |
    | --- | --- |
    | `s3:ListBucket` | Check the backup destination when you save a backup or backup preset. |
    | `s3:GetObject` | Download and restore backups. |
    | `s3:PutObject` | Upload backups. |
    | `s3:AbortMultipartUpload` | Discard an upload that fails before it completes. |

    `s3:DeleteObject` is not required.

2. Create an access key for a user with that policy, and copy the access key ID and secret access key.

### Create the integration

The integration form asks for:

- **Endpoint URL**: the HTTPS address of the storage, for example `https://s3.example.com` or
  `https://minio.example.com:9000`, without a bucket name or path.
- **Region**: the region the storage expects. Leave it empty to use `us-east-1`.
- **Access Key ID** and **Secret Access Key**.

Enter the exact bucket name when creating a backup or backup preset. To pick from existing buckets instead, add this
statement to the policy:

```json
{
  "Effect": "Allow",
  "Action": "s3:ListAllMyBuckets",
  "Resource": "*"
}
```

Wodby validates access to the exact destination when you save a backup or backup preset.

## Related pages

- [Storage providers](storage.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
