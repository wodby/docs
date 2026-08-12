# Application Backups

## Overview

If an application's stack has services that provide [backup functionality](../services/operations.md#backups), you can run backups for the corresponding app service. The backup process consists of three steps:

- creating the backup archive in the container's ephemeral storage
- mirroring the backup to Wodby Blob Storage or a supported third-party object storage provider
- cleaning up the backup from the container's ephemeral storage

Backups are managed from `Apps > [App] > [Instance] > Data > Backups`.

The app instance `Data` area includes:

- `Backups` for one-off backups
- `Backup presets` for reusable destinations and automatic schedules
- `Imports` for data imports

Only app services that expose backup actions are available in the backup flow.

One-off manual backups are available on all active plans when the selected destination is available to that plan.
Wodby Blob Storage requires a paid subscription; free organizations can continue using their own supported storage
integration. Creating or editing a backup preset normally requires an active paid subscription, including presets
that do not enable an automatic schedule.

## K3S storage capacity preflight

Before an app-service backup runs on K3S, its task includes a `Check storage capacity` step. For volumes using the
default K3S local-path provisioner, Wodby checks the backing node for Kubernetes `DiskPressure` and reads available
bytes reported by the kubelet.

Known disk pressure stops the backup before the backup job is created. Existing service backup definitions do not
declare their peak temporary-space requirement, so a byte-for-byte capacity comparison is usually not possible. Wodby
shows the available capacity as a warning and continues unless Kubernetes reports disk pressure.

If Kubernetes does not expose volume statistics, the API permission is unavailable, or the storage provisioner does
not have a capacity resolver, Wodby records that capacity could not be verified and allows the backup to continue.
This task-time check is not continuous low-disk monitoring.

K3S backup and import tasks share a cluster storage-operation slot so two preflights cannot approve competing work
against the same local disk at the same time.

## Backup destination

Choose [Wodby Blob Storage](../providers/wodby-blob-storage.md) to let Wodby manage the object storage destination. It
does not require a storage integration, bucket, region, or storage class.

For a third-party destination, select the storage integration and destination bucket. You do not need to select a
region separately.

The connected storage provider credentials must allow Wodby to list/select buckets, check the selected bucket's location
when the provider requires it, and upload/read backup objects. For provider-specific requirements, see
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

- any app service in the app instance, or one specific app service
- any backup type exposed by that service, or one specific backup type

## Organization-wide presets

Create organization-wide presets from `Organization > Backups > Backup Presets` when the same destination or schedule should be reused across several apps or databases.

An organization-wide preset stores:

- Wodby Blob Storage or a third-party storage integration
- the destination bucket for a third-party integration
- an optional storage class override
- an optional environment filter
- an optional automatic schedule

When you create a manual backup, the dashboard combines:

- matching app-instance presets
- matching organization-wide presets for the same environment

If only one preset matches the selected app service and backup type, the dashboard can prefill it automatically.

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

An automatic backup targeting an app instance, app service, or container-backed database runs only while its app
instance is running. If the backup becomes due while the instance is `Pausing`, `Paused`, `Resuming`, or `Errored`,
Wodby skips that execution and advances the schedule. The missed backup is not queued or replayed when the instance
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
