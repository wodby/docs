---
description: Deploy a Django application on Wodby with the Django catalog stack, which runs Gunicorn, PostgreSQL and Valkey, with an optional Celery worker.
---

# Django

The Wodby Django catalog stack runs a Django application with Gunicorn, PostgreSQL and Valkey. A Celery worker, Mailpit,
OpenSMTPD, Gotenberg and Cloud PostgreSQL are optional. The current services and defaults are documented in
[`wodby/stack-django`](https://github.com/wodby/stack-django).

## Build and deployment

Start from the [Django boilerplate](https://github.com/wodby/django-boilerplate) or connect your own repository. The
boilerplate is offered only for the Python versions it supports. See [Application Builds](../../../apps/builds.md).

The container runs Gunicorn on port 8080. The defaults assume the project package is named `myapp`. When it is not, set
both `GUNICORN_APP` (default `myapp.wsgi:application`) and `CELERY_APP` (default `myapp`) on the app service.
Gunicorn must be one of your application's dependencies.

After every deployment Wodby runs these commands, in this order:

1. `python manage.py migrate`
2. `python manage.py collectstatic --no-input`

`manage.py` must be in `/usr/src/app`, and `STATIC_ROOT` must be set. Do not add these commands to the start command or
the pipeline. Nothing in the stack serves the collected files, so your application serves its static files itself.

## Settings your project must read

The stack sets variables, but Django reads none of them by itself. Make `settings.py` read them:

| Variable | Use it for |
| --- | --- |
| `DJANGO_SECRET_KEY` | `SECRET_KEY`. Wodby generates it once, and it stays the same across deployments. |
| `DJANGO_DEBUG` | `DEBUG`. It is `true` in environments of type `dev` and absent in every other type. |
| `DATABASE_URL` | `DATABASES`. The whole connection as one URL, with credentials. |
| `CELERY_BROKER_URL` | The Celery broker. A `redis://` URL with the password, database `0`. |
| `SMTP_HOST`, `SMTP_PORT` | Mail settings, when Mailpit or OpenSMTPD is enabled. |

You can build `DATABASES` from the `DB_*` variables instead. Do not generate or commit another secret key. Never print or
commit the values of `DATABASE_URL` and `CELERY_BROKER_URL`: both contain a password.

A variable is present only while its link exists and the linked service is enabled, so the settings must work without
it. The mail link carries no credentials.

Set `ALLOWED_HOSTS` yourself. The environment's hosts are in `WODBY_HOSTS`, a JSON array. The internal host name is in
`WODBY_APP_SERVICE_NAME`. See [Environment variables](../../../apps/environment-variables.md).

## Background jobs with Celery

The optional Celery service runs `celery worker --loglevel=INFO` instead of Gunicorn. Your project needs `celery` among
its dependencies and a Celery application in the package named by `CELERY_APP`. The boilerplate configures it through
`CELERY_BROKER_URL`.

Valkey is required because it stores queued and unacknowledged work. The stack gives it a 5 GB `data` volume,
persistence, and the `noeviction` policy, so broker messages are not treated as disposable cache entries. Do not use
this Valkey instance for Django's cache. Add a separate cache service with an LRU policy so cache pressure cannot block
broker writes.

## Mail

Mailpit is disabled by default. Enable Mailpit to inspect mail in non-production environments. It captures every
message and delivers none of them. For real delivery, enable OpenSMTPD and attach an
[SMTP provider](../../../providers/smtp.md). See the [OpenSMTPD guide](../opensmtpd/index.md).

## Traces, metrics, and logs

The stack includes an OpenTelemetry Collector, disabled by default. When you enable it and set where it forwards data,
your application gets the standard OpenTelemetry SDK variables that point to it. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## Data and backups

PostgreSQL keeps data on a 20 GB `data` volume. A backup is a gzipped SQL dump of the environment's database. It carries
no role names and no grants, so you can import it into a database with another name and other users. A database import
replaces the whole data volume. The Valkey service has no backups or imports. See
[Application Backups](../../../apps/backups.md) and [Application Imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md), Gunicorn runs with its polling reloader, so a saved Python
file is picked up without a restart. A change to dependencies needs setup again. File changes do not apply migrations:
run `manage.py migrate` with the workspace's Python.
