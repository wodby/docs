---
description: Deploy a Nuxt application on Wodby with the Nuxt catalog stack, which runs the Nuxt Node.js server with optional PostgreSQL, Valkey and mail services.
---

# Nuxt

The Wodby Nuxt catalog stack runs a Node.js (Nuxt) app service with optional PostgreSQL, Valkey, Mailpit, OpenSMTPD,
Gotenberg, and OpenTelemetry Collector services. The app renders pages and runs server routes on Nuxt's Node.js server.
The current services and defaults are documented in [`wodby/stack-nuxt`](https://github.com/wodby/stack-nuxt).

## Create the environment

Start from the [Nuxt Boilerplate](https://github.com/wodby/nuxt-boilerplate), or connect your own compatible source
repository. The app service is the only required service. The others are optional and not selected by default, so select
the ones your application uses when you create the environment. The app service links to PostgreSQL for the database,
Valkey for Redis, Mailpit for mail, and the OpenTelemetry Collector for telemetry. Change a link under
**Connections > Links** on the app service.

The app service's version is the Node.js version. The boilerplate includes a health endpoint at `/healthz` and
checks it after each deployment.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts.
- Build with Nuxt's default Node.js server output: `nuxt build` to build and `node .output/server/index.mjs` to start.
  Do not set another Nitro preset, and do not use `nuxt generate` as the build script. The boilerplate is set up this
  way.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md). Keep
  the `postinstall: nuxt prepare` script from Nuxt's starter; it needs no runtime variables.
- Runtime variables are not available to `npm run build`. That includes link variables and secrets. `nuxt.config.ts` is
  evaluated during the build, so values read there are fixed in the image. Read runtime values in server routes, server
  middleware, or server plugins when a request is handled.
- The application must listen on port `3000`, the Nitro server's default. Do not set `PORT` or `NITRO_PORT`.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- The image build leaves out `.nuxt`, `.output`, and `.data`; `nuxt build` creates them again.
- Files written inside the container are lost when it is replaced.

## Configure the application

Use Nuxt's [runtime config](https://nuxt.com/docs/guide/going-further/runtime-config) for settings that differ between
environments. Declare each key in `runtimeConfig` in `nuxt.config.ts` with an empty or default value. Then add a
variable to the app service named `NUXT_` plus the key path in upper snake case, such as `NUXT_API_SECRET` for
`runtimeConfig.apiSecret`. See [Environment variables](../../../apps/environment-variables.md).

- Only declared keys are overridden.
- Keys under `runtimeConfig.public` use the `NUXT_PUBLIC_` prefix and are sent to the browser. Never put secrets there.
- Values such as `true`, numbers, and JSON are parsed, so they do not arrive as strings.
- The production server does not read `.env` files.

Wodby generates `NUXT_APP_SECRET`, Nuxt's application secret, for each environment. It stays the same across
deployments and differs between environments. Nuxt's sessions (`useSession`), `deriveSecret`, and modules built on them
need it and fail when a request uses them without it. Changing the secret ends existing sessions and invalidates
anything signed with secrets derived from it.

## Connect the database, Valkey, and mail

Server routes read these variables from `process.env`. They do not reach the browser. They have no `NUXT_` prefix, so
they do not override runtime config. A variable is present only while its link exists and the linked service is
enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

The database link sets no `DATABASE_URL`. If your database library needs a URL, build it from these variables in server
code and URL-encode the user name and password.

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

## Telemetry

When you select the OpenTelemetry Collector, the app service's link to it sets the standard OpenTelemetry SDK
variables `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL` (`http/protobuf`), and
`OTEL_EXPORTER_OTLP_HEADERS` (the Collector's ingest token). An OpenTelemetry SDK in your application exports to the
Collector without further configuration. Set `OTEL_SERVICE_NAME` on the app service to name the application. The
Collector is reachable only inside the environment.

The Collector stores nothing. It forwards traces, metrics, and logs over OTLP/HTTP to another Collector or backend. On
the Collector app service, under **Configuration > Settings**, set **Upstream OTLP endpoint** to the receiver's base
URL and **Upstream Authorization header** to the header it expects, such as `Bearer <ingest token>`. See
[Settings tab](../../../apps/services.md#settings-tab).

The [Grafana Tempo](../tempo/index.md), [Loki](../loki/index.md), and
[VictoriaMetrics](../victoria-metrics/index.md) stacks each accept one kind of data. Turn off the other exports in the
application, for example with `OTEL_METRICS_EXPORTER=none` and `OTEL_LOGS_EXPORTER=none` when you send to Tempo.

## Data and backups

PostgreSQL stores data on a `data` volume of 10 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

The app service has no volume, backup, or import of its own.

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Setup installs dependencies from the lockfile. Run setup again after you change dependencies.
- The app service runs `nuxt dev` from `node_modules`, not the `dev` script in `package.json`. Options in that script
  do not apply. `nuxt` must be a dependency of the project.
- The server listens on port `3000`. Do not change the port in your Nuxt configuration.
- The development server answers `403` for host names it does not know. Allow the environment's hosts in
  `vite.server.allowedHosts` of `nuxt.config.ts`. `WODBY_HOSTS` holds them as a JSON array; the boilerplate's
  `nuxt.config.ts` reads it.
- `NODE_ENV` is `development`. Saved files, new pages, and new server routes are picked up without a restart. The
  `npm run build` step does not run.
- A change to `nuxt.config.ts` restarts the development server only if you add `watch: ['../nuxt.config.ts']` to it, as
  the boilerplate does when `CHOKIDAR_USEPOLLING` is set.
- `.nuxt`, `.output`, `.data`, and `node_modules` are kept out of Git status.
- To start the server another way, set `WORKSPACE_NODE_COMMAND` on the app service. The command must listen on
  `$HOST:$PORT` and poll for file changes itself.
- A change to variables or linked services still needs a deployment of the environment.
