# Python

The Wodby Python catalog stack runs a Python web application with Gunicorn. PostgreSQL, Valkey, Mailpit, OpenSMTPD,
Gotenberg and Cloud PostgreSQL are available as optional services, all disabled by default. The current services and
defaults are documented in [`wodby/stack-python`](https://github.com/wodby/stack-python).

## Build and deployment

Start from the [Python boilerplate](https://github.com/wodby/python-boilerplate) or connect your own repository. The
code is copied to `/usr/src/app`. The service's Dockerfile runs `pip install -r requirements.txt` when that file exists
and does nothing else. If your pipeline passes a Dockerfile from the repository, that file installs the dependencies
instead. See [Application Builds](../../../apps/builds.md).

The container runs Gunicorn on port 8080 with a configuration that Wodby writes on every start:

- Set `GUNICORN_APP` on the app service to your WSGI callable as `module:callable`. The default is
  `myapp.wsgi:application`.
- Gunicorn must be one of your application's dependencies. The image does not include it.
- Do not add a Gunicorn configuration file to the repository. The container does not load it. Set `GUNICORN_WORKERS`,
  `GUNICORN_WORKER_CLASS`, `GUNICORN_TIMEOUT` or the other `GUNICORN_*` variables on the app service instead. Changes
  apply with the next deployment.

The app service has no volume. Files written inside the container are lost when it is replaced.

## Database, Valkey and mail

Nothing in the image reads link variables. Your application reads them. A variable is present only while its link
exists and the linked service is enabled. With the defaults, no link variables are set.

| Link | Variables |
| --- | --- |
| **DBMS** (PostgreSQL) | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| **Mail Transfer Agent** | `SMTP_HOST`, `SMTP_PORT` |
| **Redis** (Valkey) | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |

The mail link carries no credentials. Mailpit captures every message and delivers none of them, and an application that
requires SMTP authentication or TLS fails against it. For real delivery, enable OpenSMTPD and attach an
[SMTP provider](../../../providers/smtp.md). See the [OpenSMTPD guide](../opensmtpd/index.md).

Valkey is a cache by default. It evicts keys when its memory limit is reached and starts empty after a restart unless
you add its `data` volume. For a job queue or other data you must keep, set `VALKEY_MAXMEMORY_POLICY` to `noeviction`
and size `VALKEY_MAXMEMORY` on the Valkey app service.

## Environment

`WODBY_HOSTS` is a JSON array of the environment's hosts, not a comma-separated string. Use `WODBY_PRIMARY_URL` for
links generated outside a request. Other services reach the application at `WODBY_APP_SERVICE_NAME` on port 8080. See
[Environment variables](../../../apps/environment-variables.md).

## Data and backups

PostgreSQL keeps data on a 20 GB `data` volume. A backup is a gzipped SQL dump of the environment's database. It carries
no role names and no grants, so you can import it into a database with another name and other users. A database import
replaces the whole data volume. See [Application Backups](../../../apps/backups.md) and
[Application Imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md), setup installs dependencies into `.wodby-workspace/venv`
with `uv sync --locked` when `uv.lock` exists, otherwise with `pip install -r requirements.txt`. One of the two files
must exist. Run setup again after you change dependencies.

The server starts with `python -m gunicorn --reload` on `$HOST:$PORT` (`0.0.0.0:8080` by default). The generated Gunicorn
configuration and the `GUNICORN_*` tuning variables are not used. Set `WORKSPACE_PYTHON_COMMAND` on the app service to
replace the start command. A custom command must reload by itself. A change to variables or linked services still needs
a deployment.
