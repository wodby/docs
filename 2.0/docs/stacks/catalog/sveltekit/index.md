---
description: Deploy a SvelteKit application on Wodby with the SvelteKit catalog stack, a Node.js server with optional PostgreSQL, Valkey and mail services.
---

# SvelteKit

The Wodby SvelteKit catalog stack runs a Node.js (SvelteKit) app service with optional PostgreSQL, Valkey, Mailpit,
OpenSMTPD, Gotenberg, and OpenTelemetry Collector services. The app renders pages, runs form actions, and serves API
routes on a Node.js server. The current services and defaults are documented in
[`wodby/stack-sveltekit`](https://github.com/wodby/stack-sveltekit).

## Create the environment

Start from the [SvelteKit Boilerplate](https://github.com/wodby/sveltekit-boilerplate), or connect your own compatible
source repository. The app service is the only required service. The others are optional and not selected by default,
so select the ones your application uses when you create the environment. The app service links to PostgreSQL for the
database, Valkey for Redis, Mailpit for mail, and the OpenTelemetry Collector for telemetry. Change a link under
**Connections > Links** on the app service.

The app service's version is the Node.js version, and every version the service offers runs SvelteKit. The boilerplate
includes a health endpoint at `/healthz` and checks it after each deployment.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts.
- Build with the [Node.js adapter](https://svelte.dev/docs/kit/adapter-node): set `adapter: adapter()` from
  `@sveltejs/adapter-node` in the `sveltekit()` plugin in `vite.config.ts`, build with `vite build`, and start with
  `node build`. SvelteKit does not read `svelte.config.js`. The boilerplate is set up this way.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
  SvelteKit, the adapter, Vite, and Svelte can stay in `devDependencies`: the adapter bundles them into `build/`.
- Runtime variables are not available to `npm run build`. That includes link variables and secrets. See
  [Environment variables](#environment-variables) for how to read them.
- The application must listen on port `3000`, the adapter's default. Do not set `PORT`.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- The image build leaves out `build/` and `.svelte-kit/` and creates them again.
- Request bodies are limited to 512 KB. For larger uploads, set `BODY_SIZE_LIMIT` on the app service, for example to
  `10M` or `Infinity`.
- Files written inside the container are lost when it is replaced.

## Environment variables

Declare the variables your application reads in `src/env.ts` with `defineEnvVars` from `@sveltejs/kit/env`, and import
them in server code from `$app/env/private`. Add your own variables to the app service, see
[Environment variables](../../../apps/environment-variables.md).

- Keep variables dynamic, the default. A variable with `static: true` is fixed at build time, when runtime variables do
  not exist.
- SvelteKit checks the declared variables during `vite build` as well as when the server starts. A variable declared
  without a `schema` must be set, so the image build fails. Give every runtime variable a schema that accepts a missing
  value, such as `schema: (value) => value || undefined`, as the boilerplate's `src/env.ts` does.
- Variables declared with `public: true` reach the browser through `$app/env/public`. Never make a secret public.
- Server code can also read `process.env` when a request is handled. The `$env/dynamic/*` and `$env/static/*` modules
  still work but are deprecated.

## Domains and form actions

Wodby's gateway handles HTTPS and passes each request to the app with its original host name. The app service sets the
adapter's `PROTOCOL_HEADER`, `ADDRESS_HEADER`, and `XFF_DEPTH` for that, so:

- `url.origin` is the scheme and host name the visitor used, on every domain of the environment. A request without the
  scheme header, such as a check from inside the environment, is treated as `https`.
- Form actions pass SvelteKit's origin check on every domain of the environment. Do not set `paths.origin` in
  `vite.config.ts`: it is fixed at build time and allows only one domain. Use `csrf.trustedOrigins` only for other sites
  that must post to the application.
- `getClientAddress()` returns the visitor's address. It throws for a request that did not pass the gateway, such as a
  check from inside the environment, so do not call it on every request in `handle` or in `/healthz`.
- Do not set `ORIGIN`, `HOST_HEADER`, or `PORT_HEADER`. The Node.js adapter does not read `ORIGIN`.

On shutdown, open requests get 25 seconds to finish, set by `SHUTDOWN_TIMEOUT`. Then the `sveltekit:shutdown` event
runs, before the container is stopped.

## Connect the database, Valkey, and mail

Declare the variables your application uses in `src/env.ts` with a schema that accepts a missing value: the links are
optional, and the variables do not exist during the build. They do not reach the browser unless you declare them
public. A variable is present only while its link exists and the linked service is enabled. The mail link carries no
credentials.

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

- Setup installs dependencies from the lockfile, which also runs the `prepare` script (`svelte-kit sync` in the
  boilerplate). Run setup again after you change dependencies.
- The app service runs the Vite development server through Vite's API with your `vite.config.ts`, not with the `dev`
  script in `package.json`. Options in that script do not apply. `vite` must be a dependency of the project.
- The server listens on port `3000`. Do not change the port in your Vite configuration.
- Vite rejects host names it does not know. Allow the environment's hosts in `server.allowedHosts` of `vite.config.ts`.
  `WODBY_HOSTS` holds them as a JSON array; the boilerplate's `vite.config.ts` reads it.
- `NODE_ENV` is `development`. Saved files and new route files are picked up without a restart, and SvelteKit
  regenerates `.svelte-kit/` with the route types. The `npm run build` step does not run, and the origin check of form
  submissions is off.
- `build/`, `.svelte-kit/`, and `node_modules` are kept out of Git status.
- To start the server another way, set `WORKSPACE_NODE_COMMAND` on the app service. The command must listen on
  `$HOST:$PORT` and poll for file changes itself.
- A change to variables or linked services still needs a deployment of the environment.
