# Application Cron Schedules

You can run cron jobs manually for app services that expose cron schedules.

Cron schedules can exist at several levels:

- service level, provided by the service itself through the service template
- stack level, created through stack configuration or a stack template
- app level, created for a specific app instance

Cron schedules can be defined for enabled, non-external app services using standard crontab syntax.

Automatic cron schedules create jobs only while the app instance is running. If a run becomes due while the instance
is `Pausing`, `Paused`, `Resuming`, or `Errored`, Wodby skips that execution and advances the schedule. The missed run
is not queued or replayed when the instance becomes runnable again; run the cron job manually if it is still needed.
