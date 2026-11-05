# Spring Boot

The Wodby Spring Boot catalog stack runs a Spring Boot app service on Java 25 or 21 with PostgreSQL, and optional
Valkey, Mailpit, OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented
in [`wodby/stack-spring-boot`](https://github.com/wodby/stack-spring-boot).

The Spring Boot service is based on the [Java service](../java/index.md): it builds and starts the application the same
way, and adds the settings Spring Boot reads by itself.

## Create the environment

Start from the [Spring Boot boilerplate](https://github.com/wodby/spring-boot-boilerplate), a Spring Boot 4 web
application that stores notes in PostgreSQL, or connect your own compatible source repository. The app service and
PostgreSQL are required. The other services are optional and not selected by default. The app service links to
PostgreSQL for the database, Valkey for Redis, and Mailpit for mail. Change a link under **Connections > Links** on the
app service.

Choose Java 25 or 21 with the app service's version. To use a managed database instead of the PostgreSQL container, see
[Managed databases](../../../databases/managed.md).

## Build and start

- The service builds the repository with Maven or the Gradle wrapper and runs the jar, as described for the
  [Java stack](../java/index.md#build-and-start). Spring Boot's Maven and Gradle plugins build a runnable jar with its
  dependencies inside, so no extra build setup is needed. The boilerplate's pipeline runs `./mvnw test` before it builds
  the image.
- The application must listen on port `8080`, Spring Boot's default.
- The service is ready when `/actuator/health` answers `200`, so add `spring-boot-starter-actuator` to the project.
  Without Actuator, set `JAVA_READY_PATH` on the app service to another path that answers `200`, such as `/`.
- Graceful shutdown is on by default in Spring Boot. Keep its timeout below 30 seconds, the time the container gets to
  stop.

## Environments and requests

- Development environments activate the `dev` profile, so `application-dev.properties` applies. Other environment types
  use the default profile. To choose profiles yourself, set `SPRING_PROFILES_ACTIVE` on the app service.
- Wodby's gateway terminates HTTPS. On Kubernetes, Spring Boot uses the gateway's forwarded headers by itself, so
  redirects and generated links use the public domain and HTTPS. Don't add HTTPS redirection in the application:
  checks inside the environment use plain HTTP.

## Connect the database, Valkey, and mail

The links set the variables Spring Boot reads by itself, so `application.properties` needs no datasource, Redis or mail
connection settings. Variables override settings in `application.properties`, so local defaults there, such as
`jdbc:postgresql://localhost:5432/app`, are fine. A variable is present only while its link exists and the linked
service is enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD` |
| Valkey | `SPRING_DATA_REDIS_HOST`, `SPRING_DATA_REDIS_PORT`, `SPRING_DATA_REDIS_PASSWORD` |
| Mail | `SPRING_MAIL_HOST`, `SPRING_MAIL_PORT` |

`SPRING_DATASOURCE_URL` is a JDBC URL such as `jdbc:postgresql://postgres:5432/db`, without the username and password.
It starts with `jdbc:postgresql:`, `jdbc:mariadb:` or `jdbc:mysql:` to match the linked database, so the project needs
that database's JDBC driver. The
[Java stack's variables](../java/index.md#connect-the-database-valkey-and-mail), such as `DB_HOST`, are set as well.

Valkey and mail are used only when the project has `spring-boot-starter-data-redis` or `spring-boot-starter-mail`.
Valkey writes nothing to disk unless you add a data volume, and it can evict any key at its memory limit. For a job
queue or sessions, set `VALKEY_MAXMEMORY_POLICY` to `noeviction` on the Valkey service and size `VALKEY_MAXMEMORY` to
fit.

Gotenberg has no link. Its address is `http://gotenberg:3000`; put it in your own configuration. See the
[Gotenberg guide](../gotenberg/index.md).

## Database migrations

Wodby runs no migration step. Add Flyway or Liquibase to the project: Spring Boot runs them at startup, so every
deployment migrates the database before the application serves requests, and replicas starting together wait for each
other. The boilerplate keeps its migrations in `src/main/resources/db/migration` and lets Hibernate only validate the
schema.

## Mail

Mailpit captures every message and delivers none, so use it for development and testing. Its public domains are
protected by basic auth by default. Find the password under **Endpoints > Auths**, see
[Endpoints](../../../apps/endpoints.md#auths). Mailpit accepts SMTP without authentication or TLS, so configure the
application's mail settings without them.

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

In a [development workspace](../../../apps/workspaces.md), Wodby rebuilds the checkout and restarts the application
after each change, usually within a few seconds, as described for the
[Java stack](../java/index.md#development-workspace). A failed build leaves the previous build running; read the
compiler errors in the service's logs. The `dev` profile follows the environment type, as in other environments.
