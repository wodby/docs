# Application Backups

## Overview

If an application's stack has services that provide [backup functionality](../services/backups.md), you can run backups for the corresponding app service. The backup process consists of three steps:

- creating the backup archive in the container's ephemeral storage
- mirroring the backup to third-party object storage, such as S3 or another supported provider
- cleaning up the backup from the container's ephemeral storage

Backups are managed from `Apps > [Instance] > Backups`.

The app backup area has two tabs:

- `Backups` for one-off backups
- `Presets` for reusable destinations and automatic schedules

Only app services that expose backup actions are available in the backup flow.

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

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

## Related pages

- [Database backups](../databases/backups.md)
