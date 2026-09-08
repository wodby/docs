# Backups

Stacks that define database or file backup operations can create backups from
`Instance > Backups`. The primary backup archive is stored on the same server
as the application instance.

You can select the database, persistent files, or both when creating a manual
backup. Restoring a backup replaces only the selected components on the same
instance; it does not roll back application code, a CI build, or the stack
revision.

!!! warning "Test recovery before you need it"
    A completed backup task proves that an archive was created, not that your
    complete application recovery procedure has been tested. Periodically test
    restoring representative database and file backups.

## Automatic backups

Automatic backups require a paid organization. Database and file backups have
independent schedules: you can enable either component or run them at different
recurrences. At least one component must remain enabled while automatic backups
are enabled. Schedule times are evaluated in UTC.

If both components are due together, Wodby creates one automatic backup task
for both. Only one automatic backup is run on a server at a time, so instances
sharing a server are processed successively. A busy or unreachable server can
therefore delay a scheduled backup.

### Retention depth

The retention depth is shared by the database and file schedules. Automatic
backups older than that number of days are removed in small background batches.
Wodby preserves the newest successful automatic backup containing each
component, even when that backup is older than the configured depth. This keeps
a less frequently scheduled component from losing its only successful copy
when the other component runs more often.

The primary backup and a mirrored copy have separate retention policies.
Deleting or rotating the primary backup also schedules deletion of its mirrored
copy when mirroring is configured.

## Mirroring

Backup mirroring requires a paid organization and a compatible connected
server. It copies new backup components to a second storage location. You can
use Wodby Storage or your own AWS S3 bucket.

### Wodby Storage

Select Wodby Storage as the mirror provider and choose the available location.
If no location is selected, the default is US East. Mirrored files in Wodby
Storage are deleted two weeks after upload.

### AWS S3

Provide:

- AWS access key ID;
- AWS secret access key;
- bucket name; and
- bucket region.

Use credentials limited to the selected backup bucket. Replacing the access key
ID does not reveal the existing secret; submit a new secret when rotating the
credentials.

## Performance and scheduling

Backup and mirror tasks have CPU and memory limits to reduce their effect on
applications, but they still consume disk I/O, CPU, memory, and network
bandwidth. Schedule large backups for a low-traffic period and maintain enough
free disk space for the expected archive in addition to the live data.

## Failure reports

At 07:00 UTC Wodby evaluates every enabled database and file schedule
independently. After allowing for normal task execution time, it emails the
organization's owners and administrators when an enabled component has missed
its most recent scheduled successful backup. The report links to the instance
backup page and identifies the overdue component.

When investigating a report, inspect the backup task log and check server disk,
memory, CPU, and connectivity. See [Troubleshooting](../troubleshooting.md#backup-failures).
