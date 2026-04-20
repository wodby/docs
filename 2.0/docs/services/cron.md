# Cron schedules

Services can define cron schedules for recurring tasks. Each schedule includes a name, a command or argument override,
and a cron expression. Every run creates a task with execution logs.

Use standard five-field crontab syntax such as `0 * * * *`. Cron schedules cannot run more often than once per hour.

Cron schedules are defined under the [`cron` section](template.md#cron) in a service template.
