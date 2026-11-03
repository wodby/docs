# Kotlin

The Wodby Kotlin catalog stack runs a Kotlin app service on Java 25 or 21 with optional PostgreSQL, Valkey, Mailpit,
OpenSMTPD, Gotenberg, and Cloud PostgreSQL services. The current services and defaults are documented in
[`wodby/stack-kotlin`](https://github.com/wodby/stack-kotlin).

## Create the environment

Start from the [Kotlin boilerplate](https://github.com/wodby/kotlin-boilerplate), a [Ktor](https://ktor.io) application,
or connect your own compatible source repository. The app service is the only required service. The others are optional
and not selected by default, so select the ones your application uses when you create the environment. The app service
links to PostgreSQL for the database, Valkey for Redis, and Mailpit for mail. Change a link under
**Connections > Links** on the app service.

The app service's versions are Java versions: 25 by default, or 21. The Kotlin version is the one your Gradle build
pins with the Kotlin Gradle plugin. To run on both Java versions, compile for the older one, as the boilerplate does
with `jvmTarget` and Java's `targetCompatibility` set to 21.

To use a managed database instead of the PostgreSQL container, see [Managed databases](../../../databases/managed.md).

## Build and start

- The repository must contain the Gradle wrapper (`gradlew` and `gradle/wrapper/`) and a `build.gradle.kts` or
  `build.gradle` at its root. Gradle itself is not installed in the image; the wrapper downloads the version your
  project pins.
- The service's Dockerfile runs `./gradlew assemble`. Tests are not compiled or run, so run them in your pipeline, as
  the boilerplate's `.wodby/pipeline.yml` does with `./gradlew test`.
- The build must leave exactly one runnable jar in `build/libs/`, with the application's dependencies inside and the
  main class in its manifest. Jars ending in `-plain`, `-sources`, `-javadoc`, or `-tests` are not counted. With the
  [Shadow plugin](https://gradleup.com/shadow/), set the shadow jar's classifier to empty, the plain jar's to `plain`,
  and call `mergeServiceFiles()`, as the boilerplate does. Ktor's Gradle plugin can build such a jar with
  `buildFatJar`.
- A Dockerfile from your repository replaces the service's, for example for a build that makes several jars. Its last
  stage must start from the service image and run `java-app`, as in the boilerplate. See
  [Application builds](../../../apps/builds.md).
- The application must listen on port `8080` on all interfaces. Wodby sets no `PORT` variable in a deployed
  environment, so default to `8080` in the code. With Ktor's `embeddedServer`, pass `host = "0.0.0.0"`.
- The JVM's heap follows the container's memory limit: `JAVA_OPTS` on the app service defaults to
  `-XX:MaxRAMPercentage=75.0`. Change the service's memory limit rather than setting `-Xmx`.
- The app service is ready when `/` answers with a status below `500`. To check a health route instead, add a
  `JAVA_READY_PATH` variable with its path, such as `/healthz` from the boilerplate. That path must then answer `200`.
- Kubernetes stops the container with `SIGTERM` and waits up to 30 seconds. Ktor's `embeddedServer` finishes running
  requests and stops on its own.
- Files written inside the container are lost when it is replaced.

## Connect the database, Valkey, and mail

The application reads these variables itself. A variable is present only while its link exists and the linked service
is enabled. The mail link carries no credentials.

| Link | Variables |
| --- | --- |
| Database | `DB_HOST`, `DB_PORT`, `DB_NAME` (also `DB_DATABASE`), `DB_USERNAME`, `DB_PASSWORD`, `DB_DRIVER` (also `DB_CONNECTION`), `DATABASE_URL` |
| Valkey | `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD` |
| Mail | `SMTP_HOST`, `SMTP_PORT` |

`DATABASE_URL` is a URL such as `postgresql://user:password@host:5432/db`, not a JDBC URL. For JDBC-based libraries such
as Exposed, build the URL from the other variables, such as `jdbc:postgresql://$DB_HOST:$DB_PORT/$DB_NAME`, and pass
the user name and password separately.

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

## Data and backups

PostgreSQL stores data on a `data` volume of 20 GB. Its backups are gzipped SQL dumps of the environment's database. An
import replaces the contents of the `data` volume. See [Application backups](../../../apps/backups.md) and
[Application imports](../../../apps/imports.md).

## Development workspace

In a [development workspace](../../../apps/workspaces.md):

- Wodby builds the jar from the checkout and runs it. After each change it builds again and restarts the application,
  usually within 10 to 20 seconds on a small cluster. A failed build leaves the previous build running; read the
  Kotlin compiler's errors in the service's logs. Reload the browser page yourself.
- Setup downloads Gradle and the dependencies. They are kept in `.wodby-workspace/` in the checkout, so a restart
  downloads nothing again, and builds keep Gradle running between changes.
- `build/` and `.gradle/` stay out of Git status without changes to `.gitignore`. Add `.kotlin/` to your
  `.gitignore`, as the boilerplate does: Kotlin's Gradle plugin keeps its state there.
- Set `WORKSPACE_JAVA_WATCH` to `0` on the app service to stop rebuilding on changes, or `WORKSPACE_JAVA_COMMAND` to
  replace the start command.
- A change to variables or linked services still needs a deployment of the environment.
