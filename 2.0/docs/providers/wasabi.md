# Wasabi

## Object storage

Wodby provides a native integration with Wasabi object storage. You can use a customer-owned Wasabi bucket for app and
database backups through Wasabi's S3-compatible API.

### Before creating the integration

1. We recommend a sub-user whose policy grants object read and write access only to the buckets Wodby may use. Include
   `s3:AbortMultipartUpload` so failed uploads can be discarded, and `s3:GetBucketLocation` so Wodby can find each
   bucket's region. `s3:DeleteObject` is not required.
2. In the Wasabi Console, open **Access Keys**, create an access key for that sub-user, and copy the Access Key and
   Secret Key. Wasabi shows the secret key only once.

The integration form requires the Access Key and Secret Key. Leave the Service URL empty: Wodby finds the region of
each bucket, so one integration works with buckets in every region.

Enter a Service URL only if the key cannot use `s3:GetBucketLocation`. Use the URL of the region where your buckets
are, for example `s3.eu-central-2.wasabisys.com`; see
[Service URLs for Wasabi's storage regions](https://docs.wasabi.com/docs/what-are-the-service-urls-for-wasabi-s-different-storage-regions).
Use the regional name, not a country alias such as `s3.de-1.wasabisys.com`. For US East 1, `s3.wasabisys.com` also
works. The integration then works only with buckets in that region.

Enter the exact bucket name when creating a backup or backup preset. To pick from existing buckets instead, also allow
`s3:ListAllMyBuckets`. Bucket listing is optional. Wodby validates access to the exact destination when you save a
backup or backup preset.

!!! warning "Minimum storage duration"
    Wasabi charges for objects deleted before its minimum storage duration ends, as if they had been kept for the whole
    period. The duration depends on your Wasabi pricing plan. If you or a bucket lifecycle rule delete backups sooner,
    you still pay for the remaining days. See
    [Wasabi's minimum storage duration policy](https://docs.wasabi.com/docs/how-does-wasabis-minimum-storage-duration-policy-work).

## Related pages

- [Storage providers](storage.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
