# Next.js

The Wodby Next.js catalog stack runs a Node.js (Next.js) app service with optional PostgreSQL, Valkey, Mailpit,
OpenSMTPD, and Gotenberg services. The current services and defaults are documented in
[`wodby/stack-nextjs`](https://github.com/wodby/stack-nextjs).

## Create the environment

Start from the [Next.js Boilerplate](https://github.com/wodby/nextjs-boilerplate), or connect your own compatible source
repository. The app service is the only required service. The others are optional and not selected by default, so select
the ones your application uses when you create the environment. The app service links to PostgreSQL for the database,
Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts, normally `next build` and `next start`.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
- Runtime variables are not available to `npm run build`. That includes link variables and secrets. Render pages that
  need them at request time instead of prerendering them during the build.
- The application must listen on port `3000`, which `next start` does by default.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

Server-side code reads these variables. They are not exposed to the browser. A variable is present only while its link
exists and the linked service is enabled. The mail link carries no credentials.

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

PostgreSQL stores data on a `data` volume of 10 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- The app service runs `next dev` directly from `node_modules`, so options in the `dev` script of `package.json` do not
  apply. With Next.js 16 or later it adds `--webpack`.
- `NODE_ENV` is `development` there, and saved files are picked up without a restart. The `npm run build` step does not
  run.
