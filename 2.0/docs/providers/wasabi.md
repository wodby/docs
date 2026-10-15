# Wasabi

## Object storage

Wodby provides a native integration with Wasabi object storage. You can use a customer-owned Wasabi bucket for app and
database backups through Wasabi's S3-compatible API.

### Before creating the integration

1. Find the service URL of the region where your bucket is, for example `s3.eu-central-2.wasabisys.com`. See
   [Service URLs for Wasabi's storage regions](https://docs.wasabi.com/docs/what-are-the-service-urls-for-wasabi-s-different-storage-regions).
   Use the regional name, not a country alias such as `s3.de-1.wasabisys.com`. For US East 1, `s3.wasabisys.com` also
   works.
2. We recommend a sub-user whose policy grants object read and write access only to the buckets Wodby may use. Include
   `s3:AbortMultipartUpload` so failed uploads can be discarded. `s3:DeleteObject` is not required.
3. In the Wasabi Console, open **Access Keys**, create an access key for that sub-user, and copy the Access Key and
   Secret Key. Wasabi shows the secret key only once.

Enter the exact bucket name when creating a backup or backup preset. To pick from existing buckets instead, also allow
`s3:ListAllMyBuckets`. Bucket listing is optional.

The integration form requires the Service URL, Access Key, and Secret Key. One integration works with buckets in the
region of its service URL; create another integration for buckets in a different region. Wodby validates access to the
exact destination separately when you save a backup or backup preset.

!!! warning "Minimum storage duration"
    Wasabi charges for objects deleted before its minimum storage duration ends, as if they had been kept for the whole
    period. The duration depends on your Wasabi pricing plan. If you or a bucket lifecycle rule delete backups sooner,
    you still pay for the remaining days. See
    [Wasabi's minimum storage duration policy](https://docs.wasabi.com/docs/how-does-wasabis-minimum-storage-duration-policy-work).

## Related pages

- [Storage providers](storage.md)
- [Application backups](../apps/backups.md)
- [Database backups](../databases/backups.md)
