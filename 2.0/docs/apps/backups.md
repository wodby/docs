# Application Backups

## Overview

If an application's stack has services that provide [backup functionality](../services/operations.md#backups), you can
run backups for the corresponding app service. Wodby runs the service's backup operation and writes the result to
Wodby Blob Storage or a supported third-party object storage provider.

File backups stream directly to their destination. A database backup also streams when its deployed service revision
declares streaming support for the selected database version. This applies to Wodby Blob Storage and supported
third-party object storage destinations. The complete archive is not staged on the source persistent volume.

For a streamed upload to third-party object storage, Wodby publishes the final object only after the backup producer
reports success. A failed or canceled backup does not leave a completed partial or temporary object.

For Wodby Blob Storage, Wodby prepares a backup-specific signed upload and sends the stream directly to that endpoint.
The backup job succeeds only after the producer reports success. If the producer or upload fails, Wodby removes the
backup object.

Backups are managed from `Apps > [App] > [Environment] > Data > Backups`.

The app environment `Data` area includes:

- `Backups` for one-off backups
- `Backup presets` for reusable destinations and automatic schedules
- `Imports` for data imports

Only app services that expose backup actions are available in the backup flow.

One-off manual backups are available on all active plans when the selected destination is available to that plan.
Wodby Blob Storage requires a paid subscription; free organizations can continue using their own supported storage
integration. Creating or editing a backup preset normally requires an active paid subscription, including presets
that do not enable an automatic schedule.

## Streaming compatibility

Streaming is selected from the app service's deployed service revision and selected version. Existing apps continue
using their revision's behavior until they are updated to a service revision that declares streaming support. Wodby
does not infer support from an image tag or attempt an unsupported command in an older container.

Database backups use the established staged workflow when the deployed service revision is older or the selected
version is not listed for streaming. In that workflow, the database action creates a complete archive at the service's
configured volume path, Wodby uploads it, and a cleanup job removes the local archive.

For external object storage, a streamed backup keeps its final multipart or resumable upload incomplete until the
producer reports success. A producer failure or cancellation aborts the upload, so a failed backup does not publish a
partial object and the storage integration does not need permission to delete completed objects.

!!! note
    Streaming removes the full backup archive from the source persistent-volume demand. It does not remove normal
    database, network, memory, or object-storage resource usage during the backup.

## Excluding table contents

When the selected service backup type supports it, the `New backup` form shows `Excluded table contents`. Add one table
name or pattern per entry. The backup keeps each matching table's definition but omits its rows, so restoring the
backup creates the table without its previous data.

Container-based PostgreSQL and MariaDB backups support this option. PostgreSQL entries can use schema-qualified names
and patterns such as `public.cache_*`. MariaDB entries can use table names and SQL `LIKE` patterns such as `cache_%`.
Entries may contain letters, numbers, `_`, `.`, `-`, `*`, `?`, and `%`; unsupported characters are rejected before
the backup starts.

The form shows the service's resolved default exclusion list below the field. Leaving the field untouched uses that
default. To include all table contents, edit the field and remove every entry before submitting; the resulting empty
list overrides the service default. Each completed backup record shows the effective exclusions used for that backup,
including exclusions inherited from the service default.

An app backup preset can save explicit table exclusions only when it selects one app service and one backup type.
Scheduled backups created from that preset use the saved exclusions. If the preset leaves the field untouched, each
scheduled backup resolves the service default when it is created and stores that effective list with its own backup
record. Presets that apply to any service or backup type, and organization-wide presets, do not store table exclusions.

## K3S storage capacity preflight

Before an app-service backup runs on K3S, its task includes a `Check storage capacity` step. For volumes using the
default K3S local-path provisioner, Wodby checks the backing node for Kubernetes `DiskPressure` and reads available
bytes reported by the kubelet.

Known disk pressure stops the backup before the backup job is created. For a file backup or a database backup selected
for streaming, Wodby knows that the operation needs zero additional persistent-volume bytes because it does not stage
an archive there. The preflight still checks the volume's node for `DiskPressure`, but it does not show the unknown
peak-demand warning solely because of backup size.

Staged database backup definitions do not declare their peak temporary-space requirement, so a byte-for-byte capacity
comparison is not possible. For those backups, Wodby can show the available capacity as a warning and continue unless
Kubernetes reports disk pressure.

If Kubernetes does not expose volume statistics, the API permission is unavailable, or the storage provisioner does
not have a capacity resolver, Wodby records that capacity could not be verified and allows the backup to continue.
This task-time check is not continuous low-disk monitoring.

K3S backup and import tasks share a cluster storage-operation slot so two preflights cannot approve competing work
against the same local disk at the same time.

## Backup destination

Choose [Wodby Blob Storage](../providers/wodby-blob-storage.md) to let Wodby manage the object storage destination. It
does not require a storage integration, bucket, or storage class. Select **Europe** or **United States** as the storage
region. The selected region is saved with each backup; changing a preset affects only backups created afterward.

For a third-party destination, select the storage integration, then select an available bucket or enter its exact name.
You do not need to select a region separately.

The connected storage provider credentials must allow Wodby to access the exact bucket and upload/read backup objects.
Bucket-list permission is optional and is used to populate the selector. For provider-specific requirements, see
[Storage providers](../providers/storage.md).

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

The storage integration must also match the backup target's [ownership boundary](../sharing.md#creation-import-and-copy-forms):

- for a project-owned app, the integration must be owned by or shared with the app's owner project
- for an organization-owned app or an organization-wide preset, the integration must be organization-owned in the same organization

Access to the integration through another project is not sufficient. These checks apply to one-off backups, presets,
scheduled runs, restores, and downloads.

!!! note
    A backup destination's object storage class, such as an S3 archive class, is separate from the
    [Kubernetes storage class](storage.md) used by the app service's persistent volume.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

All backup presets are a paid feature. Turning `Auto backups` off does not normally make a preset available on the
free plan.

For Wodby 1 migrations, the REST API can save a Wodby Blob Storage preset on a free subscription only when it has an
automatic schedule and is disabled. Enabling the preset requires a paid subscription. See
[Wodby Blob Storage](../providers/wodby-blob-storage.md#availability) for the API representation.

App presets can be scoped to:

- any app service in the app environment, or one specific app service
- any backup type exposed by that service, or one specific backup type

## Organization-wide presets

Create organization-wide presets from `Organization > Backups > Backup Presets` when the same destination or schedule should be reused across several apps or databases.

An organization-wide preset stores:

- Wodby Blob Storage or a third-party storage integration
- the destination bucket for a third-party integration
- an optional storage class override
- an environment scope: any environment, one exact environment, or one or more environment types
- a backup category: any backup, files only, or databases only
- an optional automatic schedule

Use an exact environment when the preset should apply only to that environment. Use environment types when the preset
should follow every current and future environment of the selected types. Available types are `Production`, `Staging`,
`Testing`, `Development`, and `Feature`. You cannot combine an exact environment with environment types. Leaving both
selections empty applies the preset to every environment.

The backup category is based on the resource that owns the backup:

- `Any` includes file and database backups
- `Files only` includes backups from non-database app services
- `Databases only` includes standalone database backups and backups from database-owning app services

When a preset does not select one exact environment, including when it selects environment types, a third-party
storage integration must be available in all environments.

When you create a manual backup, the dashboard combines:

- matching app environment presets
- organization-wide presets that match the app environment and the selected app service's backup category

If only one preset matches the selected app service and backup type, the dashboard can prefill it automatically.

Automatic organization-wide presets use the same environment and category filters when selecting resources. An
organization-wide override suppresses another matching scheduled preset only when the override also applies to that
resource's environment and backup category.

Organization-wide presets are also available in [Database backups](../databases/backups.md).

## Automatic backups

Enable `Auto backups` in a preset when you want scheduled backups.

Scheduled presets include:

- start and end times
- an IANA time zone
- one or more days of the week
- a backup timeout in hours
- `Override other presets`

New presets default to an every-day `02:00` to `05:00` window in the organization's default time zone and a three-hour
backup timeout. The window controls when the backup may start; the timeout limits how long a started backup may run.
For details about day selection, overnight windows, time zones, and missed windows, see
[Automation time windows](../automation-time-windows.md).

Turning `Auto backups` off pauses an existing schedule while preserving its window, timeout, and override setting.
Turning it on again resumes the saved schedule. A new preset saved with `Auto backups` off has no automatic schedule.

Use override when one preset should win over other matching scheduled presets.

Automatic schedules created by the previous dashboard used exact UTC launch times. Daily and single-weekday schedules
are migrated to three-hour UTC windows beginning at the same time, without changing the selected day or backup
timeout. Custom cron expressions remain on the legacy exact-time schedule.

An automatic backup targeting an app environment, app service, or container-backed database runs only while its app
environment is running. If the backup becomes due while the environment is `Pausing`, `Paused`, `Resuming`, or `Errored`,
Wodby skips that execution and advances the schedule. The missed backup is not queued or replayed when the environment
becomes runnable again.

## Failure and recovery notifications

Wodby groups all backup artifacts created by the same preset occurrence into one result. Any failed artifact makes the
occurrence fail and emails organization admins who have `Backup failures and recoveries` enabled under
`User settings > Notifications`. Additional artifact failures and later failed occurrences are suppressed while the
preset remains failed.

Recovery is reported only after every artifact in a later preset occurrence completes successfully. A failed manual
backup still emails the user who started it. Enabled presets that remain failed also appear in the weekly organization
report's `Automation health` section.

Failure emails link to the backup task logs. For a K3S storage preflight failure, the `Check storage capacity` step
shows the exact error.

## Related pages

- [Database backups](../databases/backups.md)
- [Wodby Blob Storage](../providers/wodby-blob-storage.md)
