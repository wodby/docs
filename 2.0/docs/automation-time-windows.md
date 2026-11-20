---
description: Automation time windows set when Wodby may start automatic stack, infrastructure and Kubernetes upgrades and automatic backups.
---

# Automation time windows

Automation time windows define when Wodby may start scheduled automation. Upgrade windows restrict changes to running
workloads, while backup windows restrict when an automatic backup may begin.

Time windows are available for:

- automatic app environment stack upgrades
- automatic cluster infrastructure version upgrades
- automatic cluster infrastructure app stack upgrades
- automatic cluster Kubernetes version upgrades
- automatic backups from app, database, and organization-wide backup presets

Each supported upgrade setting has its own window. For example, a cluster can use different windows for infrastructure
version, infrastructure app, and Kubernetes version upgrades, and app environments that share a stack can use different
upgrade windows.

Catalog operations that do not change running workloads do not use time windows. Git auto-updates of services and
stacks, automatic stack service revision updates, and automatic sync of copied stacks with their origin can create new
catalog revisions at any time. An app environment's time window still controls when its running workload may be upgraded
to one of those revisions.

## Configure a window

For an automatic upgrade, enable `Time window` in its automation settings. For a backup preset, enable `Auto backups`.
Then select a start time, end time, time zone, and one or more days. All seven days are selected by default. The
`Every day`, `Weekdays`, and `Weekends` shortcuts provide quick ways to change the selection.

New app environments and clusters receive enabled `02:00` to `04:00` windows in the organization's default time zone for
each applicable automatic upgrade. The organization creation form preselects the creator's browser time zone and lets
them change it before creation; if browser detection is unavailable, Wodby uses `UTC`. Owners and admins can change it
under `Organization > Settings > General`.

New backup presets created in the dashboard default to a three-hour `02:00` to `05:00` window in the organization's
default time zone. Their backup timeout also defaults to three hours. The timeout is separate from the window: the
window controls when a backup may start, while the timeout limits how long the backup task may run.

The organization time zone is a creation default, not a live link. Changing it does not rewrite existing resource or
backup-preset windows, and each window can use a different time zone.

The searchable selector lists available IANA time zone names and follows daylight-saving changes for the selected
location. API clients that provide an explicit window without a time zone use `UTC`; clients that omit the days use
every day.

A valid window:

- uses 24-hour `HH:mm` times
- includes the start time and excludes the end time
- is at least one hour long
- has different start and end times
- selects at least one day

When the end time is later than the start time, the window is within one day. For example, `02:00` to `04:00` allows
automation from 02:00 up to, but not including, 04:00. When the end time is earlier, the window crosses midnight. For
example, `22:00` to `02:00` starts at 22:00 and ends at 02:00 the next day.

For a window that crosses midnight, the selected day is the day on which the window starts. For example, a Monday
`22:00` to `02:00` window remains open until 02:00 on Tuesday. Selecting Tuesday instead would open the next window at
22:00 on Tuesday.

## What the window controls

An upgrade window controls when Wodby may start an automatic upgrade. An upgrade that starts inside the window
continues normally if it runs past the end time. Manual upgrades are never restricted by an automation time window.

If an automatic upgrade becomes available outside its window, Wodby waits for a later window. Waiting does not mark the
resource as failed or send a notification.

Cluster upgrades preserve their required order. When both a cluster infrastructure version upgrade and an
infrastructure app upgrade are pending, Wodby waits for the infrastructure version upgrade first. An open
infrastructure app window does not bypass a closed infrastructure version window.

An automatic backup is scheduled for the beginning of the selected window and may start later while the window is
still open. If the window has already closed, Wodby skips that backup and waits for the next selected day; the missed
backup is not run later. A backup that starts inside the window may continue after it closes, subject to its backup
timeout. Manual backups are not restricted by the window.

## Pausing automatic backups

`Auto backups` is the only schedule state control in the dashboard. Turning it off on an existing preset pauses the
schedule but preserves its window, timeout, and override setting. Turning it on again resumes the saved schedule. A new
preset saved with `Auto backups` off has no automatic schedule.

## Notification emails

Success and failure emails for automatic app stack upgrades, cluster infrastructure version upgrades, and cluster
infrastructure app upgrades include the time when the upgrade started. When a time window is configured, the email
shows the start time in that window's time zone together with the configured interval and selected days. When no
window is configured, the email shows the start time in UTC and explicitly notes that the upgrade could run at any
time.
