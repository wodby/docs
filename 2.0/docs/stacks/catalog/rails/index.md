---
description: Deploy a Rails application on Wodby with the Rails catalog stack, which runs it with a Sidekiq worker, PostgreSQL and Valkey.
---

# Rails

The Wodby Rails catalog stack runs a Ruby (Rails) app service with a Sidekiq worker, PostgreSQL, and Valkey. Mailpit,
OpenSMTPD, Gotenberg, and Cloud PostgreSQL are optional. The current services and defaults are documented in
[`wodby/stack-rails`](https://github.com/wodby/stack-rails).

## Create the environment

Start from the [Rails boilerplate](https://github.com/wodby/rails-boilerplate), or connect your own compatible source
repository. The app service, PostgreSQL, and Valkey are required and cannot be excluded. Select Mailpit, OpenSMTPD,
Gotenberg, or Cloud PostgreSQL when you create the environment if your application uses them. The app service links to
PostgreSQL for the database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the
app service. To use a managed database, see [Managed databases](../../../databases/managed.md).

## Application settings

- `RAILS_ENV` is `development` in environments of type `dev` and `production` in every other type. An environment of
  type `test` is a deployed application, not Rails' test environment.
- `SECRET_KEY_BASE` is a secret that Wodby generates. Rails reads it by itself, so do not generate or commit another
  one. Find it on the app service's **Configuration > Tokens** tab as `secret_key_base`.
- `RAILS_MASTER_KEY` is not set. If your application uses encrypted credentials, add the key as a secret variable on the
  app service. See [Environment variables](../../../apps/environment-variables.md).

## Build and start

- The service's Dockerfile installs `vips`, runs `bundle install`, and runs `rails assets:precompile` with
  `RAILS_ENV=production` and a dummy secret key when the application has that task. Runtime variables and the database
  are not available during the build.
- The container runs Puma on port `8080` with a configuration Wodby generates. A `config/puma.rb` in the repository is
  not loaded. Set `PUMA_WORKERS`, `PUMA_THREADS`, and the other `PUMA_*` variables on the app service instead.
- Puma and a `config.ru` at the repository root are required. Add Puma to your `Gemfile`.
- After every deployment Wodby runs `bundle exec rails db:prepare`, which prepares the schema and runs pending
  migrations. During the first deployment only, it then runs `bundle exec rails db:seed`. Your start command and
  pipeline do not need to run migrations.
- Files written inside the container are lost when it is replaced.

## Host authorization

Wodby mounts a config named **Host authorization** at `config/initializers/wodby_host_authorization.rb`. It is not part
of your repository. Change it as a config of the app service on Wodby. It adds every host of the environment and the
service's internal host name to `config.hosts`, and it excludes requests to `/healthz` from host authorization. Do not
add the environment's hosts to `config.hosts` in the code. Serve your health endpoint at `/healthz`.

## Connect the database, Valkey, and mail

Rails reads `DATABASE_URL` by itself, and its values take precedence over `config/database.yml`. Do not put a host,
user, or password in `database.yml`. The app service also receives the `DB_*` and `REDIS_*` variables with the same
connection details in separate parts. Never print or commit the values of the URL variables, because they contain
passwords.

| Link | Variables |
| --- | --- |
| Database | `DATABASE_URL` |
| Valkey | `REDIS_URL` (database `0`) |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

Wodby does not configure a job queue, cache, or mailer for your application. Your application decides what to do with
`REDIS_URL`, `SMTP_HOST`, and `SMTP_PORT`, and must start without them when a link is absent.

The Sidekiq worker runs `bundle exec sidekiq` instead of Puma and reads `REDIS_URL` by itself. Add `sidekiq` to your
`Gemfile`. The Rails boilerplate uses Sidekiq, and its worker is enabled by default.

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

- PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database.
  By default they keep the definitions of `solid_cache_entries` and `solid_cable_messages` but omit their rows. See
  [Excluding table contents](../../../apps/backups.md#excluding-table-contents).
- An import into PostgreSQL replaces the contents of the `data` volume. See
  [Application imports](../../../apps/imports.md).
- Valkey stores queue data on a `data` volume of 5 GB with persistence on and the `noeviction` memory policy. The Valkey
  service declares no backups or imports.

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- The application starts with `bundle exec rails server` on port `8080`, and `RAILS_ENV` is `development` whatever the
  environment type.
- Starting the server does not run migrations or seeds. Keep Rails' default `config.file_watcher`,
  `ActiveSupport::FileUpdateChecker`, because an evented file watcher is not reliable on the checkout's network storage.
