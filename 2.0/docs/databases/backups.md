# Database backups

From _"Databases > [Database] > Backup"_ you can run backups, which are different from snapshots, for individual DBs. When preparing a new backup, you can select one of the backup presets for this database or an organization-wide backup preset. Backup presets allow you to save time when entering backup destination details.

## Backup destination

When configuring a backup or backup preset, select the destination bucket only. You no longer need to select a region separately.

If the provider supports object storage classes, the storage class override is optional. If you set it, Wodby will use it for uploaded backup objects. If you leave it empty, the bucket's default storage class will be used.

## Backup presets

Backup presets are a way to save time when entering backup destination details. You can create an organization-wide preset and apply it to backup schedules.
