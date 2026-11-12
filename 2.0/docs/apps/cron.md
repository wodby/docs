---
description: Define cron schedules for app services at service, stack or app level, run cron jobs manually, and control overlapping runs and failure notifications.
---

# Application Cron Schedules

You can run cron jobs manually for app services that expose cron schedules.

Cron schedules and manual cron-job runs require an active paid subscription.

Cron schedules can exist at several levels:

- service level, provided by the service itself through the service template
- stack level, created through stack configuration or a stack template
- app level, created for a specific app environment

Cron schedules can be defined for enabled, non-external app services using standard crontab syntax.

Automatic cron schedules create jobs only while the app environment is running and the target app service has a usable
runtime. The app service must be enabled, non-external, successfully deployed, and in the `OK` state. If a run becomes
due before the first successful deployment, while the environment is not running, or while the target service is not
usable, Wodby skips that execution and advances the schedule. The missed run is not queued or replayed when the
environment or service becomes runnable again.

Manual cron-job runs use the same runtime checks. If the environment or target service is not ready, Wodby returns an
error without creating a cron-job task. Retry the manual run after both are running if the missed work is still needed.

## Overlapping runs

An automatic schedule runs one job at a time. If a run becomes due while the schedule's previous run, automatic or
manual, is still queued or running, Wodby skips the new run and advances the schedule. The skipped run is not queued or
replayed. A job that takes longer than its interval therefore runs back to back instead of piling up runs behind it.

A previous run created more than two hours ago no longer blocks new runs. Manual runs always start, even while another
run of the same schedule is in progress.

## Cron runs in task lists

Every cron-job run, automatic or manual, is recorded as a task. Task lists hide these runs by default so that frequent
schedules do not push other activity out of view. Select `cron` next to the `Name` column heading to show them. The
active tasks menu in the header never shows cron runs. To see a schedule's run history, open
`Apps > [App] > [Environment] > Cron`.

## Failure and recovery notifications

When an automatic cron schedule's latest conclusive run first changes to failed, Wodby emails organization admins who
have `Cron job failures and recoveries` enabled under `User settings > Notifications`. Repeated failed runs are
suppressed while the schedule remains failed. The first later successful conclusive run sends a recovery email.

A failed manual cron-job run emails the user who started it. Enabled schedules that are still failing also appear in
the weekly organization report's `Automation health` section.
