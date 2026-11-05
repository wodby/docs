# FastAPI

The Wodby FastAPI catalog stack runs a Python (FastAPI) app service with optional PostgreSQL, Valkey, Mailpit,
OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-fastapi`](https://github.com/wodby/stack-fastapi).

## Create the environment

Start from the [FastAPI boilerplate](https://github.com/wodby/fastapi-boilerplate), or connect your own compatible
source repository. The app service is the only required service. The others are optional and not selected by default, so
select the ones your application uses when you create the environment. The app service links to PostgreSQL for the
database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The container runs Gunicorn with Uvicorn workers on port `8080`. Do not add a `uvicorn` start command to the
  Dockerfile and do not change the port.
- `GUNICORN_APP` is `main:app`: the object `app` in `main.py` at the root of the repository. Set the variable on the app
  service if your application lives elsewhere.
- Gunicorn and `uvicorn-worker` are not in the image. Add both to your dependencies, or Gunicorn fails to start.
- Set the number of workers with `GUNICORN_WORKERS`. Other Gunicorn settings are `GUNICORN_*` variables on the app
  service. A Gunicorn configuration file in the repository is not loaded.
- The service's Dockerfile installs `requirements.txt` when the file exists. A Dockerfile from your repository replaces
  it and must install the dependencies itself. See [Application builds](../../../apps/builds.md).
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

The application reads these variables itself. FastAPI has no settings convention of its own, so read these names. A
variable is present only while its link exists and the linked service is enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

Valkey writes nothing to disk unless you add a data volume, and it can evict any key at its memory limit. For a job
queue or sessions, set `VALKEY_MAXMEMORY_POLICY` to `noeviction` on the Valkey service and size `VALKEY_MAXMEMORY` to
fit.

Gotenberg has no link. Its address is `http://gotenberg:3000`; put it in your own configuration. See the
[Gotenberg guide](../gotenberg/index.md).

## Mail

Mailpit captures every message and delivers none, so use it for development and testing. Its public domains are
protected by basic auth by default. Find the password under **Endpoints > Auths**, see
[Endpoints](../../../apps/endpoints.md#auths). Mailpit accepts SMTP without authentication or TLS, so configure the
application's mail transport without them.

For real delivery, enable OpenSMTPD, point the app service's mail link to it, and attach an SMTP provider. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Traces, metrics, and logs

The stack includes an OpenTelemetry Collector, disabled by default. When you enable it and set where it forwards data,
your application gets the standard OpenTelemetry SDK variables that point to it. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## Data and backups

PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- The application starts with Uvicorn and `--reload`, so a saved Python file is picked up without a restart.
- Run workspace preparation again after changing dependencies.
