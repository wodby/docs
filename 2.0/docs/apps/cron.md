# Application Cron Schedules

You can run cron jobs manually for app services that expose cron schedules.

Cron schedules can exist at several levels:

- service level, provided by the service itself through the service template
- stack level, created through stack configuration or a stack template
- app level, created for a specific app instance

Cron schedules can be defined for enabled, non-external app services using standard crontab syntax.
