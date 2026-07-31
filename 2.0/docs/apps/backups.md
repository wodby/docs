# Application Backups

## Overview

If an application's stack has services that provide [backup functionality](../services/operations.md#backups), you can run backups for the corresponding app service. The backup process consists of three steps:

- creating the backup archive in the container's ephemeral storage
- mirroring the backup to third-party object storage, such as S3 or another supported provider
- cleaning up the backup from the container's ephemeral storage

Backups are managed from `Apps > [App] > [Instance] > Data > Backups`.

The app instance `Data` area includes:

- `Backups` for one-off backups
- `Backup presets` for reusable destinations and automatic schedules
- `Imports` for data imports

Only app services that expose backup actions are available in the backup flow.

One-off manual backups are available on all active plans. Creating or editing a backup preset requires an active paid
subscription, including presets that do not enable an automatic schedule.

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

If a scheduled backup fails, Wodby emails organization admins who have the `Backup failed` notification enabled. The
notification is enabled by default and can be changed under `User settings > Notifications`. The email links to the
backup task logs, where the `Check storage capacity` step shows the exact preflight error.

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

The connected storage provider credentials must allow Wodby to list/select buckets, check the selected bucket's location
when the provider requires it, and upload/read backup objects. For provider-specific requirements, see
[Storage providers](../providers/storage.md).

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

!!! note
    A backup destination's object storage class, such as an S3 archive class, is separate from the
    [Kubernetes storage class](storage.md) used by the app service's persistent volume.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

All backup presets are a paid feature. Turning `Auto backups` off does not make a preset available on the free plan.

App presets can be scoped to:

- any app service in the app instance, or one specific app service
- any backup type exposed by that service, or one specific backup type

## Organization-wide presets

Create organization-wide presets from `Organization > Backups > Backup Presets` when the same destination or schedule should be reused across several apps or databases.

An organization-wide preset stores:

- the storage integration
- the destination bucket
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

- start day
- start time in UTC
- duration in hours
- enabled or disabled state
- `Override other presets`

Use override when one preset should win over other matching scheduled presets.

An automatic backup targeting an app instance, app service, or container-backed database runs only while its app
instance is running. If the backup becomes due while the instance is `Pausing`, `Paused`, `Resuming`, or `Errored`,
Wodby skips that execution and advances the schedule. The missed backup is not queued or replayed when the instance
becomes runnable again.

## Related pages

- [Database backups](../databases/backups.md)
