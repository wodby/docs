# Rust

The Wodby Rust catalog stack runs a Rust app service on the latest stable Rust release, with optional PostgreSQL,
Valkey, Mailpit, OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented
in [`wodby/stack-rust`](https://github.com/wodby/stack-rust).

## Create the environment

Start from the [Rust boilerplate](https://github.com/wodby/rust-boilerplate), an
[axum](https://github.com/tokio-rs/axum) web application, or connect your own compatible source repository. The app
service is the only required service. The others are optional and not selected by default, so select the ones your
application uses when you create the environment. The app service links to PostgreSQL for the database, Valkey for
Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The service's Dockerfile builds the project with `cargo build --release` and starts the binary. The project must build
  exactly one binary, or name one with `default-run` in `Cargo.toml`. A project with a `Cargo.toml` at the repository
  root is required.
- Commit `Cargo.lock`. When it is present, the build uses it as is and fails if it is out of date; update it with
  `cargo update` and commit the result.
- A Dockerfile from your repository replaces the service's, as in the boilerplate. It must still end with a command that
  starts the server. See [Application builds](../../../apps/builds.md).
- The boilerplate's pipeline checks formatting with `cargo fmt`, lints with `cargo clippy`, and runs `cargo test` before
  it builds the image.
- Binaries are built for Alpine Linux and linked statically. The image includes OpenSSL and `pkg-config`, so crates that
  link OpenSSL build without changes. For other C libraries, use your own Dockerfile and install their static packages.
- A `rust-toolchain.toml` in the repository selects another Rust version. It is downloaded when the build starts.
- The application must listen on port `8080` on all interfaces. Wodby sets no `PORT` variable in a deployed environment,
  so default to `8080` in the code.
- The app service is ready when the application answers `200` at `/`. An application without a page at `/` is never
  served.
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
application's mail client without them.

For real delivery, enable OpenSMTPD, point the app service's mail link to it, and attach an SMTP provider. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Logs

The boilerplate logs every request and reads the log level from `RUST_LOG`, `info` by default. Set `RUST_LOG` on the
app service, for example to `debug`, to change it.

## Data and backups

PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Wodby compiles the checkout with `cargo build` and restarts the application after each change, usually within a few
  seconds. A failed build leaves the previous build running; read the compiler errors in the service's logs.
- Setup downloads the project's crates and compiles it once, so the first start is quick. A compile error doesn't stop
  setup.
- `Cargo.lock` is never changed: an outdated lock file fails the build, so fix it in the repository with
  `cargo update`.
- When the project builds several binaries and has no `default-run`, set `WORKSPACE_RUST_BIN` on the app service to the
  one to run, or `WORKSPACE_RUST_PACKAGE` to choose a member of a Cargo workspace. `WORKSPACE_RUST_COMMAND` replaces the
  start command.
- Compiled files and downloaded crates stay out of Git status without changes to `.gitignore`. Running `cargo` yourself
  in the workspace terminal doesn't restart the application.
- Compiling takes more memory and CPU than running the application. If builds are slow or stop, raise the app service's
  resources.
