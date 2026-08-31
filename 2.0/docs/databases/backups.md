# Database backups

From `Databases > [Database] > Backups` you can run one-off backups and manage backup presets.

One-off manual backups are available on all active plans when the selected destination is available to that plan.
Wodby Blob Storage requires a paid subscription; free organizations can continue using their own supported storage
integration. Creating or editing a backup preset normally requires an active paid subscription, whether or not the
preset includes an automatic schedule.

The database backup area has two tabs:

- `Backups` for one-off backups
- `Presets` for reusable destinations and automatic schedules

Backups are different from snapshots. A backup is created by the database or service backup workflow and then mirrored to object storage.

When preparing a new backup, you can select one of the backup presets for this database or an organization-wide backup preset.

## Excluding table contents

When the selected database backup type supports it, the `New backup` form shows `Excluded table contents`. Add one table
name or pattern per entry. The backup keeps each matching table's definition but omits its rows, so restoring the
backup creates the table without its previous data.

Container-based PostgreSQL and MariaDB backups support this option. PostgreSQL entries can use schema-qualified names
and patterns such as `public.cache_*`. MariaDB entries can use table names and SQL `LIKE` patterns such as `cache_%`.
Entries may contain letters, numbers, `_`, `.`, `-`, `*`, `?`, and `%`; unsupported characters are rejected before
the backup starts.

Leaving the field untouched uses the default exclusion list configured by the database service. To include all table
contents, edit the field and remove every entry before submitting; the resulting empty list overrides the service
default. The selected values are stored with the backup record.

A database backup preset can save table exclusions only when it selects one backup type for a container-based
database. Scheduled backups created from that preset use the saved exclusions. Presets that apply to any backup type,
and organization-wide presets, do not store table exclusions.

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

- for a project-owned database, the integration must be owned by or shared with the database's owner project
- for an organization-owned database or an organization-wide preset, the integration must be organization-owned in the same organization

Access to the integration through another project is not sufficient. These checks apply to one-off backups, presets,
scheduled runs, restores, and downloads.

## Backup presets

Backup presets save time when entering backup destination details, and they can also define automatic backups.

All backup presets are a paid feature. Turning `Auto backups` off does not normally make a preset available on the
free plan.

For Wodby 1 migrations, the REST API can save a Wodby Blob Storage preset on a free subscription only when it has an
automatic schedule and is disabled. Enabling the preset requires a paid subscription. See
[Wodby Blob Storage](../providers/wodby-blob-storage.md#availability) for the API representation.

Database presets can be scoped to:

- any DB in the database, or one specific DB
- if the database exposes named backup types, any backup type or one specific backup type

## Organization-wide presets

Create organization-wide presets from `Organization > Backups > Backup Presets` when the same destination or schedule should be reused across several databases or apps.

An organization-wide preset stores:

- Wodby Blob Storage or a third-party storage integration
- the destination bucket for a third-party integration
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

## Failure and recovery notifications

Wodby groups all backup artifacts created by the same preset occurrence into one result. Any failed artifact makes the
occurrence fail and sends one failure notification; repeated failures are suppressed until a later occurrence fully
succeeds. Recovery is reported only after every artifact in that later occurrence completes successfully.

Scheduled failure and recovery emails go to organization admins who have `Backup failures and recoveries` enabled
under `User settings > Notifications`. A failed manual backup still emails the user who started it. Enabled presets
that remain failed also appear in the weekly organization report's `Automation health` section.

## Related pages

- [Application backups](../apps/backups.md)
- [Wodby Blob Storage](../providers/wodby-blob-storage.md)
