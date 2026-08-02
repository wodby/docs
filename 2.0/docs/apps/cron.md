# Application Cron Schedules

You can run cron jobs manually for app services that expose cron schedules.

Cron schedules and manual cron-job runs require an active paid subscription.

Cron schedules can exist at several levels:

- service level, provided by the service itself through the service template
- stack level, created through stack configuration or a stack template
- app level, created for a specific app instance

Cron schedules can be defined for enabled, non-external app services using standard crontab syntax.

Automatic cron schedules create jobs only while the app instance is running. If a run becomes due while the instance
is `Pausing`, `Paused`, `Resuming`, or `Errored`, Wodby skips that execution and advances the schedule. The missed run
is not queued or replayed when the instance becomes runnable again; run the cron job manually if it is still needed.

## Failure and recovery notifications

When an automatic cron schedule's latest conclusive run first changes to failed, Wodby emails organization admins who
have `Cron job failures and recoveries` enabled under `User settings > Notifications`. Repeated failed runs are
suppressed while the schedule remains failed. The first later successful conclusive run sends a recovery email.

A failed manual cron-job run emails the user who started it. Enabled schedules that are still failing also appear in
the weekly organization report's `Automation health` section.
