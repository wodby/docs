# MySQL

The Wodby MySQL catalog stack runs a MySQL database server, with an optional phpMyAdmin. The current composition is
documented in [`wodby/stack-mysql`](https://github.com/wodby/stack-mysql).

## Create an environment

MySQL is enabled by default with a 20 GB `data` volume. phpMyAdmin is disabled by default. Enable it when you want a
browser interface for the database. It is linked to the MySQL service automatically.

Wodby creates the database and its user. Both are named after the app and the app environment, and the user has all
privileges on that database only. The database uses `utf8mb4` with the `utf8mb4_0900_ai_ci` collation. The application
does not create them. A user you create by hand with a name Wodby later needs, but a different password, makes
Wodby's create action fail. Add further [DBs](../../../databases/dbs.md) and [users](../../../databases/users.md) on
Wodby.

## Passwords

Wodby generates two [tokens](../../../apps/tokens.md) once per environment. Open the MySQL app service's
**Configuration > Tokens** tab to reveal them:

- `password`: the password of the environment's database user.
- `root_password`: the `root` password. The container also has it in `MYSQL_ROOT_PASSWORD`, and `root` may connect
  from any host.

Use the database user, not `root`, in applications.

## Connect to the database

The server listens on TCP port `3306`. Inside the app environment, the host is the name of the MySQL app service.
The database has no public route. To reach it from outside the cluster, publish its port. See
[Publishing ports](../../../apps/endpoints.md#publishing-ports).

An app service linked to MySQL receives the host, port, database name, user name, and password as environment
variables defined by its own link, for example `DB_HOST` and `DB_PASSWORD` on a PHP service. Read them in the
application instead of hardcoding them.

To open a shell in the database container, use the [web terminal](../../../apps/web-terminal.md). For example,
`mysql -uroot -p"$MYSQL_ROOT_PASSWORD" -e 'SHOW DATABASES;'` lists the databases.

## phpMyAdmin

phpMyAdmin has no persistent data and connects only to the linked MySQL server. Wodby protects its public domains
with basic auth by default. Reveal the generated password on the environment's **Endpoints > Auths** page. See
[Auths](../../../apps/endpoints.md#auths). On the phpMyAdmin login page, sign in with the environment's database user
to see its database, or with `root` to see all databases.

## Server settings

On every start the container writes its configuration from a template and environment variables. Do not edit the
generated file. Use one of these instead:

- Set a [variable](../../../apps/environment-variables.md) on the MySQL app service: `MYSQL_INNODB_BUFFER_POOL_SIZE`,
  `MYSQL_MAX_CONNECTIONS`, `MYSQL_MAX_ALLOWED_PACKET`, `MYSQL_WAIT_TIMEOUT`, `MYSQL_TRANSACTION_ISOLATION`,
  `MYSQL_CHARACTER_SET_SERVER`, or `MYSQL_COLLATION_SERVER`. These are applied only when you set them:
  `MYSQL_SQL_MODE`, `MYSQL_SLOW_QUERY_LOG`, `MYSQL_LONG_QUERY_TIME`, `MYSQL_PERFORMANCE_SCHEMA`,
  `MYSQL_INNODB_REDO_LOG_CAPACITY`, `MYSQL_INNODB_IO_CAPACITY`, `MYSQL_LOWER_CASE_TABLE_NAMES`.
- Override the service's **MySQL config** file for a setting that no variable covers. It replaces the template. See
  [Configs tab](../../../apps/services.md#configs-tab).

A change applies on the next deployment of the service.

## Limits

The MySQL service runs a single instance.

## Backups and restore

Data is on the `data` volume. A backup is a gzipped SQL dump of the environment's database. In the backup's
**Excluded table contents** option, list table names or SQL `LIKE` patterns. Those tables keep their definition and
lose their rows. See [Application backups](../../../apps/backups.md).

To restore, run a database import from a backup or an uploaded file. See
[Application imports](../../../apps/imports.md). The import accepts a `.sql` or `.mysql` file, or a `.gz`,
`.tar.gz`, `.tgz`, or `.zip` archive that contains exactly one such file.

!!! warning
    A database import replaces the contents of the `data` volume. Data that is not in the dump is not kept.
