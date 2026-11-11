---
description: Deploy Strapi on Wodby with the Strapi catalog stack, a Node.js app service that keeps content in PostgreSQL and uploaded media on a volume.
---

# Strapi

The Wodby Strapi catalog stack runs a Node.js (Strapi) app service with PostgreSQL and optional Mailpit, OpenSMTPD, and
OpenTelemetry Collector services. Strapi keeps its content in PostgreSQL and uploaded media on a volume of the app
service. The current services and defaults are documented in
[`wodby/stack-strapi`](https://github.com/wodby/stack-strapi).

## Create the environment

Start from the [Strapi Boilerplate](https://github.com/wodby/strapi-boilerplate), a Strapi project in TypeScript, or
connect your own compatible source repository. The app service and PostgreSQL are required. Mailpit, OpenSMTPD, and the
OpenTelemetry Collector are optional and not selected by default. The app service links to PostgreSQL for the database,
Mailpit for mail, and the OpenTelemetry Collector for telemetry. Change a link under **Connections > Links** on the app
service.

The app service's version is the Node.js version.

## First sign-in

Wodby creates no Strapi account. After the first deployment, open the app's domain: Strapi redirects to the admin panel,
where you create the first administrator. Do this right away, because until an administrator exists anyone who opens the
admin panel can create one.

The boilerplate includes an example `Article` collection type. On its first start it lets the Public role read articles,
so `/api/articles` answers without a token. To stop that, remove the permission under
**Settings > Users & Permissions > Roles > Public**; it stays removed.

## Secrets

Wodby generates the secrets Strapi needs when the environment is created and sets them as secret variables:
`APP_KEYS`, `API_TOKEN_SALT`, `ADMIN_JWT_SECRET`, `TRANSFER_TOKEN_SALT`, `JWT_SECRET`, and `ENCRYPTION_KEY`. They are
tokens on the Strapi app service's **Configuration > Tokens** tab. See [Tokens](../../../apps/tokens.md).

Each environment has its own values, and they stay the same across deployments and stack upgrades. Keep them unchanged
unless you mean to rotate one. Changing a value has these effects:

| Changed | Effect |
| --- | --- |
| `APP_KEYS`, `ADMIN_JWT_SECRET`, `JWT_SECRET` | Everybody is signed out |
| `ENCRYPTION_KEY` | Stored API tokens can no longer be shown in the admin panel |
| `API_TOKEN_SALT` | Existing API tokens stop working |
| `TRANSFER_TOKEN_SALT` | Existing transfer tokens stop working |

The same applies when you copy a database to another environment, which has different values.

## Build and start

- The service's Dockerfile copies your build context, runs `npm run build` while the image is built, and starts the
  container with `npm run start`. `package.json` must define both scripts, normally `strapi build` and `strapi start`.
- The build compiles the TypeScript project and builds the admin panel. Changes to the admin panel, such as
  customizations in `src/admin`, take effect after a new build and deployment.
- The Dockerfile does not install dependencies. Install them in your pipeline before the image is built, for example
  with `wodby ci run -- npm ci`, so that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
- Runtime variables are not available to `npm run build`, and Strapi does not need them there. It reads the secrets and
  the database URL when it starts.
- The application must listen on port `3000`. The service sets `HOST` to `0.0.0.0` and `PORT` to `3000`;
  `config/server.ts` must read them, as Strapi's generated file does.
- The project must use PostgreSQL through the `pg` package.
- `NODE_ENV` is `production` in every environment type, including `dev`, because the container runs a production build.
  Do not set it to `development` for a deployed environment.
- Strapi's `GET /_health` answers without touching the database. The boilerplate checks it after each deployment.
- The service sets `STRAPI_TELEMETRY_DISABLED` to `true`.

### Behind the gateway

Wodby's gateway terminates TLS. Strapi must trust its forwarded headers: set `proxy: { koa: true }` in
`config/server.ts`. Without it, Strapi treats every request as plain HTTP. Its admin sign-in cookies are not marked
secure, cookies that require HTTPS cannot be set, and every client address is the gateway's. The boilerplate trusts the
headers and takes the client address from the last `X-Forwarded-For` entry, the one the gateway added.

The boilerplate's `config/server.ts` uses the environment's primary URL, `WODBY_PRIMARY_URL`, as Strapi's public URL,
so links in emails are absolute. Set `PUBLIC_URL` on the app service to use another address. The admin panel works on
every domain of the environment.

## Connect the database, mail, and telemetry

| Link | Variables |
| --- | --- |
| Database | `DATABASE_URL`, and also `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`) |
| Mail | `SMTP_HOST`, `SMTP_PORT` |
| OpenTelemetry Collector | `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_HEADERS` |

`DATABASE_URL` is a secret URL such as `postgresql://user:password@host:5432/db`, with the user name and password
encoded. In your `config/database.ts`, use it as the connection string when it is set, and do not combine it with the
separate variables. The boilerplate's file does this. The stack's PostgreSQL service does not use TLS.

A mail or telemetry variable is present only while its link exists and the linked service is enabled. The mail link
carries no credentials.

The OpenTelemetry variables are the standard SDK settings, so an OpenTelemetry SDK in your application exports to the
Collector without further configuration. The boilerplate does not include one. The Collector accepts data only from
inside the environment and forwards traces, metrics, and logs to the OTLP/HTTP endpoint in its
**Upstream OTLP endpoint** setting, with the **Upstream Authorization header** setting if your backend needs one.

## Mail

Strapi sends email such as password resets. The boilerplate's `config/plugins.ts` sends it through SMTP when
`SMTP_HOST` is set, and otherwise keeps Strapi's default email provider. Set `SMTP_FROM` on the app service to choose
the sender; it defaults to `no-reply@` followed by the primary domain.

Mailpit captures every message and delivers none, so use it for development and testing. Its public domains are
protected by basic auth by default. Find the password under **Endpoints > Auths**, see
[Endpoints](../../../apps/endpoints.md#auths).

For real delivery, enable OpenSMTPD, point the app service's mail link to it, and attach an SMTP provider. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Uploaded media

Strapi's local upload provider stores media in `public/uploads` and serves it at `/uploads/...`. On Wodby, that
directory is on the app service's `uploads` volume, 10 GB by default, so media survives deployments.

- Files committed to `public/uploads` in your repository are not included in the image.
- The boilerplate's `config/plugins.ts` accepts images, video, audio, PDF, Office documents, plain text, and CSV, and
  refuses SVG images and executables. Change the lists there to accept other types.
- To keep media in object storage instead, use a Strapi upload provider such as `@strapi/provider-upload-aws-s3`. The
  volume then stays empty.

## Data and backups

- PostgreSQL holds content, users, roles, settings, and API tokens on its `data` volume of 10 GB.
- The `uploads` volume holds uploaded media.

Back up the database and the `uploads` volume together as one recovery set. The PostgreSQL service has backups, which
are gzipped SQL dumps of the environment's database, and imports, which replace the contents of its `data` volume. The
Strapi app service has no backup or import operation in Wodby. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Setup installs dependencies from the lockfile. Run setup again after you change dependencies.
- The app service runs the `dev` script of `package.json`, `strapi develop` in the boilerplate. It serves the admin
  panel with hot reloading and restarts the server when you change code. The environment's domains work without
  configuration.
- The Content-Type Builder works only here. Content types you create are written to `src/api` and `src/components`, and
  Strapi updates the type definitions in `types/generated`. Commit these files, then build and deploy them to your other
  environments.
- A TypeScript error stops the server until you fix the file; it then restarts by itself.
- `NODE_ENV` is `development`, so the admin panel's cookies are not marked secure. The `npm run build` step does not
  run.
- The workspace uses its own environment's PostgreSQL database.
- Media uploaded in a workspace is written to `public/uploads` in the checkout, not to the `uploads` volume.
- `.strapi/`, `dist/`, `build/`, `.tmp/`, `.strapi-updater.json`, and `public/uploads/` are kept out of Git status.
- A change to variables or linked services still needs a deployment of the environment.

## Limits

- The Strapi app service is fixed to one replica, because the `uploads` volume can be attached to one container at a
  time.
- During a deployment, the old container stops before the new one starts, so the app is briefly unavailable.
