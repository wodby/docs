# Database backups

From `Databases > [Database] > Backups` you can run one-off backups and manage backup presets.

The database backup area has two tabs:

- `Backups` for one-off backups
- `Presets` for reusable destinations and automatic schedules

Backups are different from snapshots. A backup is created by the database or service backup workflow and then mirrored to object storage.

When preparing a new backup, you can select one of the backup presets for this database or an organization-wide backup preset.

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

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

- start day
- start time in UTC
- duration in hours
- enabled or disabled state
- `Override other presets`

Use override when one preset should win over other matching scheduled presets.

## Related pages

- [Application backups](../apps/backups.md)
