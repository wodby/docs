---
description: Deploy an ASP.NET Core application on .NET 10 with the Wodby ASP.NET Core catalog stack and optional PostgreSQL, Valkey, Mailpit and OpenSMTPD services.
---

# ASP.NET Core

The Wodby ASP.NET Core catalog stack runs an ASP.NET Core app service on .NET 10 with optional PostgreSQL, Valkey,
Mailpit, OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-aspnetcore`](https://github.com/wodby/stack-aspnetcore).

## Create the environment

Start from the [ASP.NET Core boilerplate](https://github.com/wodby/aspnetcore-boilerplate), or connect your own
compatible source repository. The app service is the only required service. The others are optional and not selected by
default, so select the ones your application uses when you create the environment. The app service links to PostgreSQL
for the database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the app service.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The service's Dockerfile publishes your project with the .NET SDK and runs the result on an image that has the
  ASP.NET Core runtime but no SDK. It publishes the only project file (`*.csproj`, `*.fsproj` or `*.vbproj`) at the
  repository root, or else the only one in a `src/<name>/` directory. When there are several, it takes the only web,
  worker, or executable project. Otherwise the build fails: add a
  [build variable](../../../apps/environment-variables.md#runtime-and-build-variables) `DOTNET_PROJECT` with the
  project's path, such as `src/Api/Api.csproj`, to the app service.
- When the repository has a `packages.lock.json`, the build restores exactly the locked package versions and fails if a
  lock file is out of date.
- A Dockerfile from your repository replaces the service's. Its last stage must start from the service image, as in the
  boilerplate. See [Application builds](../../../apps/builds.md).
- The project's target framework (`TargetFramework` in the project file) must match the .NET version you choose for
  the service.
- The application must listen on port `8080`. ASP.NET Core does that by default in this image; don't set other URLs in
  code. `launchSettings.json` is not used by a deployed application.
- The image includes ICU and the full culture data, so cultures, number and date formats, and collation work.
- Files written inside the container are lost when it is replaced.

## Environments and requests

- Development environments run the application as `Development`. Other environment types run it as `Production`, so
  `appsettings.Production.json` applies and the developer exception page is off.
- Wodby's gateway terminates HTTPS. ASP.NET Core is configured to use the forwarded headers, so request schemes,
  generated links, redirects, and client addresses are those of the visitor. Don't add HTTPS redirection in the
  application: checks inside the environment use plain HTTP.
- `WODBY_HOSTS` holds the environment's domains as a JSON array. The boilerplate answers only for those domains, the app
  service's name, and `localhost`, and returns `400 Bad Request` for others. Add more names to `AllowedHosts` in
  `appsettings.json`, separated by `;`.
- Settings from environment variables use `__` for nesting. A variable named `ConnectionStrings__Default` on the app
  service is read as the `Default` connection string.

## Connect the database, Valkey, and mail

The application reads these variables itself. Build connection strings from them with your client's connection string
builder, such as `NpgsqlConnectionStringBuilder`, which quotes values correctly. A variable is present only while its
link exists and the linked service is enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

Valkey writes nothing to disk unless you add a data volume, and it can evict any key at its memory limit. For a job
queue or sessions, set `VALKEY_MAXMEMORY_POLICY` to `noeviction` on the Valkey service and size `VALKEY_MAXMEMORY` to
fit.

Gotenberg has no link. Its address is `http://gotenberg:3000`; put it in your own configuration. See the
[Gotenberg guide](../gotenberg/index.md).

## Data Protection keys

ASP.NET Core protects authentication cookies and antiforgery tokens with
[Data Protection keys](https://learn.microsoft.com/aspnet/core/security/data-protection/configuration/overview). By
default the keys live inside the container, so they change with every deployment and differ between replicas: users are
signed out and forms fail. If your application uses cookies or antiforgery, persist the keys to Valkey or to the
database.

## Mail

Mailpit captures every message and delivers none, so use it for development and testing. Its public domains are
protected by basic auth by default. Find the password under **Endpoints > Auths**, see
[Endpoints](../../../apps/endpoints.md#auths). Mailpit accepts SMTP without authentication or TLS, so configure the
application's mail client without them.

For real delivery, enable OpenSMTPD, point the app service's mail link to it, and attach an SMTP provider. See the
[OpenSMTPD guide](../opensmtpd/index.md).

## Traces, metrics, and logs

The stack includes an OpenTelemetry Collector, disabled by default. When you enable it and set where it forwards data,
your application gets the standard OpenTelemetry SDK variables that point to it. See
[OpenTelemetry Collector in application stacks](../../../apps/observability.md#opentelemetry-collector-in-application-stacks).

## Data and backups

PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Wodby runs the project with `dotnet watch`. Code changes are applied to the running application, usually within a few
  seconds, or the application is rebuilt and restarted when a change can't be applied. A failed build leaves the
  running application up; read the compiler errors in the service's logs. Reload the browser page yourself.
- The workspace runs the application as `Development` unless you set `DOTNET_ENVIRONMENT` or `ASPNETCORE_ENVIRONMENT`
  on the app service.
- Setup restores the solution's packages when there is exactly one `*.sln` or `*.slnx` file at the repository root,
  otherwise the project's, and restores local tools from `.config/dotnet-tools.json`. With a `packages.lock.json`,
  restores fail instead of changing the lock file.
- The project is chosen as in the build. Set `WORKSPACE_DOTNET_PROJECT` on the app service to run another one, such as
  `src/Api/Api.csproj`, or `WORKSPACE_DOTNET_COMMAND` to replace the start command.
- `bin/` and `obj/` directories and the package cache stay out of Git status without changes to `.gitignore`.
