# Java

The Wodby Java catalog stack runs a Java app service with optional PostgreSQL, Valkey, Mailpit,
OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-java`](https://github.com/wodby/stack-java).

Use it for applications built into a runnable jar with Maven or Gradle, such as ones on Quarkus, Micronaut, Javalin, or
no framework. For Spring Boot applications, use the [Spring Boot stack](../spring-boot/index.md), which also sets
Spring Boot's own connection settings.

## Create the environment

Start from the [Java boilerplate](https://github.com/wodby/java-boilerplate), a small web application on the JDK's
built-in HTTP server with no other dependencies, or connect your own compatible source repository. The app service is
the only required service. The others are optional and not selected by default, so select the ones your application
uses when you create the environment. The app service links to PostgreSQL for the database, Valkey for Redis, and
Mailpit for mail. Change a link under **Connections > Links** on the app service.

Choose the Java version with the app service's version. To use a managed database instead of the PostgreSQL container,
see [Managed databases](../../../databases/managed.md).

## Build and start

- The service's Dockerfile builds the repository with its own build setup and keeps only the runnable jar:
    - Maven, when `pom.xml` is at the repository root: the Maven wrapper (`mvnw`) when the repository has one, or else
      Maven from the image, runs `package` without compiling or running tests. The jar is taken from `target/`.
    - Gradle, when `build.gradle` or `build.gradle.kts` is at the root: the Gradle wrapper (`gradlew`) runs `assemble`.
      The jar is taken from `build/libs/`. A Gradle project without the wrapper fails to build.
- Run tests in your pipeline, as the boilerplate does with `./mvnw test`.
- Jars ending in `-sources`, `-javadoc`, `-tests` or `-plain`, and Maven's `original-*.jar`, are ignored. When the
  build leaves more than one other jar, such as in a multi-module project, add a
  [build variable](../../../apps/environment-variables.md#runtime-and-build-variables) `JAVA_BUILD_JAR` to the app
  service with the path of the jar to run, such as `app/target/app.jar`. `JAVA_BUILD_ARGS` adds arguments to Maven or
  Gradle, and `JAVA_BUILD_COMMAND` replaces the build command.
- The image keeps only that jar and starts it with `java -jar`, so the jar needs a `Main-Class` in its manifest and
  its dependencies inside it: a "fat" or "uber" jar, such as one built by the Maven Shade plugin or Gradle's Shadow
  plugin. Quarkus builds one with `quarkus.package.jar.type=uber-jar`; its default layout, a jar with a separate `lib/`
  directory, does not work.
- A Dockerfile from your repository replaces the service's, as in the boilerplate. It must still end with a command that
  starts the server. See [Application builds](../../../apps/builds.md).
- The application must listen on port `8080` on all interfaces. Wodby sets no `PORT` variable in a deployed
  environment, so default to `8080` in the code.
- The service is ready when port `8080` answers HTTP with a status below `500` at `/`. To check a health endpoint
  instead, add `JAVA_READY_PATH` to the app service, such as `/health`; that path must then answer `200`.
- The JVM sizes its heap from the container's memory limit (`JAVA_OPTS` is `-XX:MaxRAMPercentage=75.0`). Set the app
  service's memory limit instead of `-Xmx`.
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

The application reads these variables itself. A variable is present only while its link exists and the linked service
is enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`), `DATABASE_URL` |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

`DATABASE_URL` is a URL such as `postgresql://user:password@host:5432/db`, not a JDBC URL. Build the JDBC URL from the
other variables, such as `jdbc:postgresql://${DB_HOST}:${DB_PORT}/${DB_NAME}`, and pass `DB_USERNAME` and
`DB_PASSWORD` to the driver separately. Add the database's JDBC driver to your project.

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

- Wodby builds the checkout as above and restarts the application with the new build after each change, usually within
  a few seconds. A failed build leaves the previous build running; read the compiler errors in the service's logs.
- Setup downloads the project's dependencies with Maven or the Gradle wrapper. Dependencies and the build are kept in
  `.wodby-workspace/` in the checkout, so a restart downloads nothing again. Maven and Gradle in an SSH session use the
  same locations.
- `JAVA_BUILD_JAR`, `JAVA_BUILD_ARGS` and `JAVA_BUILD_COMMAND` apply here too when they have the runtime scope.
- `target/`, `build/`, `.gradle/` and `.wodby-workspace/` stay out of Git status without changes to `.gitignore`.
- Set `WORKSPACE_JAVA_WATCH` to `0` on the app service to stop rebuilding on changes, or `WORKSPACE_JAVA_COMMAND` to
  replace the start command.
