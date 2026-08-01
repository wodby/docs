# Automation time windows

Automation time windows let you restrict when Wodby may start automatic upgrades that change running workloads. A
window is optional. When it is disabled or not configured, an automatic upgrade can start at any time.

Time windows are available for:

- automatic app instance stack upgrades
- automatic cluster infrastructure version upgrades
- automatic cluster infrastructure app stack upgrades

Each supported upgrade setting has its own window. For example, a cluster can use different windows for infrastructure
version upgrades and infrastructure app upgrades, and app instances that share a stack can use different upgrade
windows.

Catalog operations that do not change running workloads do not use time windows. Git auto-updates of services and
stacks, automatic stack service revision updates, and automatic sync of copied stacks with their origin can create new
catalog revisions at any time. An app instance's time window still controls when its running workload may be upgraded
to one of those revisions.

## Configure a window

Enable `Time window` in the automation settings, then select a start time, end time, and time zone.

The dashboard proposes `02:00` to `04:00` in your browser's current time zone for a newly enabled window. If the browser
time zone is unavailable, it uses `UTC`. This is only an editable starting value; time windows are disabled by default.
The searchable selector lists available IANA time zone names and follows daylight-saving changes for the selected
location. API clients that provide a window without a time zone use `UTC`.

A valid window:

- uses 24-hour `HH:mm` times
- includes the start time and excludes the end time
- is at least one hour long
- has different start and end times

When the end time is later than the start time, the window is within one day. For example, `02:00` to `04:00` allows
automation from 02:00 up to, but not including, 04:00. When the end time is earlier, the window crosses midnight. For
example, `22:00` to `02:00` starts at 22:00 and ends at 02:00 the next day.

## What the window controls

The window controls when Wodby may dispatch an automatic upgrade task. A task that starts inside the window continues
normally if it runs past the end time. Manual upgrades are never restricted by an automation time window.

If an eligible automatic operation is detected outside its window, Wodby defers it quietly. It does not create an
update task, mark the resource as failed, or send a success or failure notification for that deferred check. Periodic
reconciliation checks the resource again and can start the operation during a later window.

Cluster upgrades preserve their required order. When both a cluster infrastructure version upgrade and an
infrastructure app upgrade are pending, Wodby waits for the infrastructure version upgrade first. An open
infrastructure app window does not bypass a closed infrastructure version window.

## Notification emails

Success and failure emails for automatic app stack upgrades, cluster infrastructure version upgrades, and cluster
infrastructure app upgrades include the time when the upgrade task started. When a time window is configured, the email
shows the start time in that window's time zone together with the configured daily interval. When no window is
configured, the email shows the start time in UTC and explicitly notes that the upgrade could run at any time.
