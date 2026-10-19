# Wasabi

## Object storage

Wodby provides a native integration with Wasabi object storage. You can use a customer-owned Wasabi bucket for app and
database backups through Wasabi's S3-compatible API.

### Before creating the integration

Create a Wasabi user that can reach only the buckets Wodby may use:

1. In the Wasabi Console, open **Policies**, select **Create Policy**, and paste this policy. Replace `BUCKET` with
   your bucket name, and repeat both resource entries for every other bucket Wodby may use.

    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": ["s3:GetBucketLocation", "s3:ListBucket"],
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
    | `s3:GetBucketLocation` | Find the bucket's region. |
    | `s3:ListBucket` | Check the backup destination when you save a backup or backup preset. |
    | `s3:GetObject` | Download and restore backups. |
    | `s3:PutObject` | Upload backups. |
    | `s3:AbortMultipartUpload` | Discard an upload that fails before it completes. |

    `s3:DeleteObject` is not required.

2. Open **Users**, create a user with programmatic access, and attach the policy.
3. Create an access key for that user and copy the Access Key and Secret Key. Wasabi shows the secret key only once.

The integration form asks for the Access Key and Secret Key. Wodby finds the region of each bucket, so one integration
works with buckets in every region.

Enter the exact bucket name when creating a backup or backup preset. To pick from existing buckets instead, add this
statement to the policy:

```json
{
  "Effect": "Allow",
  "Action": "s3:ListAllMyBuckets",
  "Resource": "*"
}
```

!!! warning "Minimum storage duration"
    Wasabi charges for objects deleted before its minimum storage duration ends, as if they had been kept for the whole
    period. The duration depends on your Wasabi pricing plan. If you or a bucket lifecycle rule delete backups sooner,
    you still pay for the remaining days. See
    [Wasabi's minimum storage duration policy](https://docs.wasabi.com/docs/how-does-wasabis-minimum-storage-duration-policy-work).

## Related pages

- [Storage providers](storage.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
