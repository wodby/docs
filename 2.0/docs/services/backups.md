# Service backups

Service can define data backups. There are two main methods of backups:

## 1. Simple files backup

We create a tarball with files from the specified directory. The tarball can optionally be gzipped.

The tarball will be uploaded to a cloud storage bucket of a connected integration.

## 2. Through action

We run a kubernetes job with provided overridden args/command to create the backup archive. We expect to get an archive placed in the same volume as the result. The resulting archive will be uploaded to a cloud storage bucket of a connected integration.
