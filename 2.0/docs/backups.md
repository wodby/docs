# Backups

Wodby supports both one-off backups and reusable backup presets.

Use one-off backups when you need to run a backup immediately. Use presets when you want to save backup destination settings once, or when you want Wodby to run backups automatically on a schedule.

## Quick decision

| Need | Use |
| --- | --- |
| Immediate backup of an app instance service | App backup |
| Immediate backup of a database or DB | Database backup |
| Reusable destination settings | Backup preset |
| Automatic scheduled backups across many resources | Organization-wide backup preset |

For scope-specific details, compare [Application backups](apps/backups.md) and [Database backups](databases/backups.md).

## Where backups are managed

Backups are managed in three places:

- `Organization > Backups > Backup Presets` for organization-wide presets
- `Apps > [Instance] > Backups` for app-instance backups and presets
- `Databases > [Database] > Backups` for database backups and presets

## Backup destination

Every backup uses a storage integration plus a destination bucket.

- the integration must be a storage integration
- the bucket is selected from that integration
- `Override storage class` is optional

If the storage provider supports storage classes, Wodby lets you override the class per backup or preset. If you leave it empty, the bucket default is used.

You no longer choose a region separately in the backup form.

## What a preset stores

A backup preset stores:

- the storage integration
- the destination bucket
- an optional storage class override
- optional scope filters, depending on where the preset is created
- an optional automatic schedule

Without automatic scheduling, a preset works as a reusable destination template. With automatic scheduling enabled, it also becomes part of the backup scheduler.

## Preset scopes

Wodby supports several preset scopes.

### Organization-wide

Created from `Organization > Backups > Backup Presets`.

These presets can optionally be limited to one environment. They are then offered in matching app and database backup forms for resources in that environment.

### App-instance-wide and app-service-wide

Created from `Apps > [Instance] > Backups > Presets`.

You can scope an app preset to:

- any app service in the app instance, or one specific app service
- any backup type exposed by that service, or one specific backup type

### Database-wide and DB-specific

Created from `Databases > [Database] > Backups > Presets`.

You can scope a database preset to:

- any DB in the database, or one specific DB
- if the database exposes named backup types, any backup type or one specific backup type

## How preset matching works

When you prepare a manual backup, the dashboard loads:

- presets created for that app instance or database
- organization-wide presets that match the resource environment

The form then narrows the available presets based on the app service, backup type, DB, or database backup type you selected.

If exactly one preset matches, the dashboard can prefill it automatically.

## Automatic backups

Presets can also schedule automatic backups.

The schedule fields are:

- start day
- start time in UTC
- duration in hours
- enabled or disabled state
- `Override other presets`

## Override behavior

`Override other presets` is intended for cases where more than one scheduled preset could apply to the same target.

If an override preset matches, Wodby skips other matching presets for that backup target. Use this when you want one schedule to be authoritative instead of running several overlapping schedules.

## Operational notes

- Organization-wide backup presets are managed centrally, but they are consumed from app and database backup flows.
- A storage integration that is still referenced by backup presets cannot be deleted until those presets are removed.

## Related pages

- [Organization](org.md)
- [Application backups](apps/backups.md)
- [Database backups](databases/backups.md)
