# Database backups

From `Databases > [Database] > Backups` you can run one-off backups and manage backup presets.

One-off manual backups are available on all active plans. Creating or editing any backup preset requires an active
paid subscription, whether or not the preset includes an automatic schedule.

The database backup area has two tabs:

- `Backups` for one-off backups
- `Presets` for reusable destinations and automatic schedules

Backups are different from snapshots. A backup is created by the database or service backup workflow and then mirrored to object storage.

When preparing a new backup, you can select one of the backup presets for this database or an organization-wide backup preset.

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

The connected storage provider credentials must allow Wodby to list/select buckets, check the selected bucket's location
when the provider requires it, and upload/read backup objects. For provider-specific requirements, see
[Storage providers](../providers/storage.md).

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

All backup presets are a paid feature. Turning `Auto backups` off does not make a preset available on the free plan.

Database presets can be scoped to:

- any DB in the database, or one specific DB
- if the database exposes named backup types, any backup type or one specific backup type

## Organization-wide presets

Create organization-wide presets from `Organization > Backups > Backup Presets` when the same destination or schedule should be reused across several databases or apps.

An organization-wide preset stores:

- the storage integration
- the destination bucket
- an optional storage class override
- an optional environment filter
- an optional automatic schedule

When you create a manual backup, the dashboard combines:

- matching database presets
- matching organization-wide presets for the same environment

If only one preset matches the selected DB and backup type, the dashboard can prefill it automatically.

Organization-wide presets are also available in [Application backups](../apps/backups.md).

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

## Related pages

- [Application backups](../apps/backups.md)
