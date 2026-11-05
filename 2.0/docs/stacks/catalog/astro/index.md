# Astro

The Wodby Astro catalog stack runs a Node.js (Astro) app service with optional PostgreSQL, Valkey, Mailpit, OpenSMTPD,
Gotenberg, and OpenTelemetry Collector services. The app runs Astro's Node.js server, which renders pages on demand and
serves prerendered pages and assets. The current services and defaults are documented in
[`wodby/stack-astro`](https://github.com/wodby/stack-astro).

## Create the environment

Start from the [Astro Boilerplate](https://github.com/wodby/astro-boilerplate), or connect your own compatible source
repository. The app service is the only required service. The others are optional and not selected by default, so
select the ones your application uses when you create the environment. The app service links to PostgreSQL for the
database, Valkey for Redis, Mailpit for mail, and the OpenTelemetry Collector for telemetry. Change a link under
**Connections > Links** on the app service.

The app service's versions are Node.js versions: 26 by default, or 24 or 22.

The boilerplate includes a health endpoint at `/healthz` and checks it after each deployment.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts.
- Use the standalone server of Astro's [Node.js adapter](https://docs.astro.build/en/guides/integrations-guide/node/):
  `adapter: node({ mode: 'standalone' })` in `astro.config.mjs`, `astro build` as the build script, and
  `node ./dist/server/entry.mjs` as the start script. The boilerplate is set up this way. A static site without an
  adapter has no server to start, and the adapter's `middleware` mode needs a server of your own.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
- The service sets `HOST` to `0.0.0.0` and `PORT` to `3000`. The standalone server reads both when it starts, and
  `PORT` takes precedence over `server.port` in your configuration. Do not change them.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- The image build leaves out `dist` and `.astro` from your repository and builds them again.
- When a container is stopped, for example during a deployment, the server ends at once. Requests in progress are cut
  off.
- Files written inside the container are lost when it is replaced.

## Prerendered and on-demand pages

Astro prerenders pages while the image is built, unless a page sets `export const prerender = false` or the
configuration sets `output: 'server'`. The same server serves prerendered pages, files in `public/`, and pages rendered
on demand.

Runtime variables are not available to `npm run build`. That includes link variables and secrets, so prerendered pages
are built without them. Render on demand every page, endpoint, and Action that reads request data, cookies, or runtime
variables, as the boilerplate's home page and `/api/server-info` endpoint do.

## Environment variables

Read runtime variables on the server when a request is handled, in one of two ways:

- `process.env`.
- [`astro:env`](https://docs.astro.build/en/guides/environment-variables/#type-safe-environment-variables) fields
  declared with `context: 'server'` and `access: 'secret'`, imported from `astro:env/server`. Astro checks them when the
  server first uses them, not during the build, unless you set `env.validateSecrets` to `true`.

`import.meta.env` and `astro:env` fields with `access: 'public'` are replaced with their values at build time, so they
cannot hold runtime variables or secrets. Only `PUBLIC_` variables and `context: 'client'` fields reach the browser.
`astro.config.mjs` runs during the build and reads `process.env`, not `astro:env`.

See [Environment variables](../../../apps/environment-variables.md).

## Domains and form submissions

Wodby's gateway terminates TLS and passes the original `Host` header with `X-Forwarded-Proto: https`. Astro uses these
headers only for the domains listed in `security.allowedDomains`. Without a match, `Astro.url` is
`http://localhost:3000/...`.

The environment's domains are in `WODBY_HOSTS` at runtime, but not while the image is built, where `allowedDomains` is
fixed. The boilerplate handles this in two files. Keep both if you change them:

- `astro.config.mjs` sets `allowedDomains: [{}]`, which accepts every domain.
- `src/middleware.ts` rejects, with `400`, any request whose `X-Forwarded-Host` is not one of the domains in
  `WODBY_HOSTS`. Without it, a client could choose the host of `Astro.url` itself.

With this setup, `Astro.url` is `https://<your domain>/...`. `Astro.clientAddress` is the first `X-Forwarded-For`
value, which a client can set, so do not use it for access control.

Astro rejects form-encoded `POST`, `PUT`, `PATCH`, and `DELETE` requests from another origin to on-demand pages and
Actions with `403` (`security.checkOrigin`, on by default). When the browser sends no `Sec-Fetch-Site` header, Astro
compares the `Origin` header with the origin of `Astro.url`, which is why the domain setup above matters.

## Connect the database, Valkey, mail, and telemetry

On-demand pages, endpoints, Actions, and middleware read these variables when a request is handled. They are not
exposed to the browser. A variable is present only while its link exists and the linked service is enabled. The mail
link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |
| OpenTelemetry Collector | `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_HEADERS` |

Valkey writes nothing to disk unless you add a data volume, and it can evict any key at its memory limit. For a job
queue or sessions, set `VALKEY_MAXMEMORY_POLICY` to `noeviction` on the Valkey service and size `VALKEY_MAXMEMORY` to
fit.

The Node.js adapter stores [sessions](https://docs.astro.build/en/guides/sessions/) in the container's file system by
default. They are lost on every deployment and are not shared between replicas. Configure a Redis session driver with
the Valkey link before you use `Astro.session`.

Gotenberg has no link. Its address is `http://gotenberg:3000`; put it in your own configuration. See the
[Gotenberg guide](../gotenberg/index.md).

## Telemetry

The OpenTelemetry variables are the standard SDK settings, so an OpenTelemetry SDK in your application exports to the
Collector without further configuration. The boilerplate does not include one. Set `OTEL_SERVICE_NAME` to name the
application in traces.

The Collector accepts data only from inside the environment. It forwards traces, metrics, and logs to the OTLP/HTTP
endpoint in its **Upstream OTLP endpoint** setting, with the **Upstream Authorization header** setting if your backend
needs one.

## Mail

Mailpit captures every message and delivers none, so use it for development and testing. Its public domains are
protected by basic auth by default. Find the password under **Endpoints > Auths**, see
[Endpoints](../../../apps/endpoints.md#auths). Mailpit accepts SMTP without authentication or TLS, so configure the
application's mail transport without them.

For real delivery, enable OpenSMTPD, point the app service's mail link to it, and attach an SMTP provider. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Data and backups

PostgreSQL stores data on a `data` volume of 10 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

The app service has no volume, and no backup or import operation in Wodby.

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Setup installs dependencies from the lockfile. Run setup again after you change dependencies.
- The app service runs `astro dev` from `node_modules` with your Astro configuration, not the `dev` script in
  `package.json`. Options in that script do not apply. `astro` must be a dependency of the project.
- The development server listens on `0.0.0.0:3000`. `server.host` and `server.port` in your configuration do not apply.
- The development server rejects host names it does not know. Add the environment's hosts to `server.allowedHosts` in
  `astro.config.mjs`. `WODBY_HOSTS` holds them as a JSON array; the boilerplate's `astro.config.mjs` reads it.
- `NODE_ENV` is `development`. Saved files are picked up within seconds, without a restart. New files can take longer.
  The `npm run build` step does not run.
- `dist/` and `.astro/` are kept out of Git status.
- To start the server another way, set `WORKSPACE_NODE_COMMAND` on the app service. The command must listen on
  `$HOST:$PORT` and poll for file changes itself.
- A change to variables or linked services still needs a deployment of the environment.
