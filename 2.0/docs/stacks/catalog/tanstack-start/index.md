# TanStack Start

The Wodby TanStack Start catalog stack runs a Node.js (TanStack Start) app service with optional PostgreSQL, Valkey,
Mailpit, OpenSMTPD, and Gotenberg services. The app renders pages and runs server functions on a Node.js server. The
current services and defaults are documented in
[`wodby/stack-tanstack-start`](https://github.com/wodby/stack-tanstack-start).

For a single-page app that uses TanStack Router without TanStack Start, use the [React stack](../react/index.md): it
serves the static build with Nginx.

## Create the environment

Start from the [TanStack Start Boilerplate](https://github.com/wodby/tanstack-start-boilerplate), or connect your own
compatible source repository. The app service is the only required service. The others are optional and not selected by
default, so select the ones your application uses when you create the environment. The app service links to PostgreSQL
for the database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

The boilerplate includes a health endpoint at `/healthz` and checks it after each deployment.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts.
- Build with TanStack Start's Node.js server output: add the `nitro()` plugin from `nitro/vite` to `vite.config.ts`,
  build with `vite build`, and start with `node .output/server/index.mjs`. The boilerplate is set up this way.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
- Runtime variables are not available to `npm run build`. That includes link variables and secrets. Read them in
  server functions, server routes, or middleware when a request is handled, not when a module loads.
- The application must listen on port `3000`, the Nitro server's default.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- The image build keeps your repository's `.gitignore`. Keep `.output` listed in it: Tailwind CSS skips the files
  listed there, and without that entry a stylesheet imported with `?url` can be linked under a name that does not
  exist. Importing the stylesheet with a plain `import` in the root route avoids this in any case.
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

Server functions and server routes read these variables from `process.env`. They do not reach the browser: only
variables prefixed with `VITE_` that exist at build time are compiled into client code. A variable is present only
while its link exists and the linked service is enabled. The mail link carries no credentials.

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

- Setup installs dependencies from the lockfile. Run setup again after you change dependencies.
- The app service runs the Vite development server through Vite's API with your Vite configuration file, not with the
  `dev` script in `package.json`. Options in that script do not apply. `vite` must be a dependency of the project.
- The server listens on port `3000`. Do not change the port in your Vite configuration.
- Vite rejects host names it does not know. Allow the environment's hosts in `server.allowedHosts` of your Vite
  configuration. `WODBY_HOSTS` holds them as a JSON array; the boilerplate's `vite.config.ts` reads it.
- `NODE_ENV` is `development`. Saved files and new route files are picked up without a restart, and the route tree in
  `src/routeTree.gen.ts` is regenerated; keep that file in Git. The `npm run build` step does not run.
- `.output`, `.nitro`, and `.tanstack` are kept out of Git status.
- To start the server another way, set `WORKSPACE_NODE_COMMAND` on the app service. The command must listen on
  `$HOST:$PORT` and poll for file changes itself.
