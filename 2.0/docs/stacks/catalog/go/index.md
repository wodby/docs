# Go

The Wodby Go catalog stack runs a Go app service with optional PostgreSQL, Valkey, Mailpit, OpenSMTPD, Gotenberg, and
Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-go`](https://github.com/wodby/stack-go).

## Create the environment

Start from the [Go boilerplate](https://github.com/wodby/go-boilerplate), or connect your own compatible source
repository. The app service is the only required service. The others are optional and not selected by default, so select
the ones your application uses when you create the environment. The app service links to PostgreSQL for the database,
Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The service's Dockerfile runs `go mod download` when `go.mod` exists, builds the package at the repository root with
  `go build`, and starts the binary. The `main` package must be at the root of the repository.
- A Dockerfile from your repository replaces it and must still end with a command that starts the server. See
  [Application builds](../../../apps/builds.md).
- The application must listen on port `8080` on all interfaces. Wodby sets no `PORT` variable in a deployed environment,
  so default to `8080` in the code.
- Wodby sets no other variable for the application and generates no configuration file.
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

## Data and backups

PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Wodby compiles the checkout and restarts the application after each change, usually within a few seconds. A failed
  build leaves the previous build running; read the compiler errors in the service's logs.
- `go.mod` is required. A missing requirement or checksum fails the build, so fix it in the repository with `go get` or
  `go mod tidy`.
- Set `WORKSPACE_GO_PACKAGE` on the app service to build a package other than `.`, such as `./cmd/server`.
- A repository with a `go.work` file is refused unless you set `WORKSPACE_GO_COMMAND` on the app service.
