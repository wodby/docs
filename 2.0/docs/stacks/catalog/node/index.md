---
description: Deploy a Node.js application on Wodby with the Node.js catalog stack, starting from the Express.js boilerplate, with optional PostgreSQL and Valkey.
---

# Node.js

The Wodby Node.js catalog stack runs a Node.js app service with optional PostgreSQL, Valkey, Mailpit, OpenSMTPD,
Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-node`](https://github.com/wodby/stack-node).

## Create the environment

Start from the [Express.js boilerplate](https://github.com/wodby/expressjs-boilerplate), or connect your own compatible
source repository. The app service is the only required service. The others are optional and not selected by default, so
select the ones your application uses when you create the environment. The app service links to PostgreSQL for the
database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The container runs `npm run start` from the application directory. `package.json` must define a `start` script.
- The application must listen on port `3000` on all interfaces. Wodby sets `NODE_PORT` to `3000` and does not set
  `PORT`. Read `NODE_PORT`, or default to `3000`.
- `NODE_ENV` is `development` in environments of type `dev` and `production` in every other type.
- The service's Dockerfile only copies your build context. It does not run `npm install`. Install dependencies and
  produce any compiled output in your pipeline before the image is built, for example with `wodby ci run -- npm ci`, so
  that `node_modules` is part of the image. See [CI/CD](../../../cicd/index.md).
- A Dockerfile from your repository replaces the service's Dockerfile.
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

The application reads these variables itself. A variable is present only while its link exists and the linked service is
enabled. The mail link carries no credentials.

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

- The app service runs the `dev` script when `package.json` has one, otherwise `start`. Set `WORKSPACE_NODE_COMMAND` to
  use another command.
- `NODE_ENV` is always `development` there. Run workspace preparation again after changing dependencies.
