---
description: Run a MariaDB database server on Wodby with the MariaDB catalog stack, with a 20 GB data volume by default and optional Adminer and phpMyAdmin.
---

# MariaDB

The Wodby MariaDB catalog stack runs a MariaDB database server, with optional Adminer and phpMyAdmin. The current
composition is documented in [`wodby/stack-mariadb`](https://github.com/wodby/stack-mariadb).

## Create an environment

MariaDB is enabled by default with a 20 GB `data` volume. Adminer and phpMyAdmin are disabled by default. Enable one
when you want a browser interface for the database. Each is linked to the MariaDB service automatically.

Wodby creates the database and its user. Both are named after the app and the app environment, and the user has all
privileges on that database only. The database uses the `utf8mb4` charset by default. The application does not create
them. A user you create by hand with a name Wodby later needs, but a different password, makes Wodby's create action
fail. Add further [DBs](../../../databases/dbs.md) and [users](../../../databases/users.md) on Wodby.

## Passwords

Wodby generates two [tokens](../../../apps/tokens.md) once per environment. Open the MariaDB app service's
**Configuration > Tokens** tab to reveal them:

- `password`: the password of the environment's database user.
- `root_password`: the `root` password. The container also has it in `MYSQL_ROOT_PASSWORD`.

Use the database user, not `root`, in applications.

## Connect to the database

The server listens on TCP port `3306`. Inside the app environment, the host is the name of the MariaDB app service.
The database has no public route. To reach it from outside the cluster, publish its port. See
[Publishing ports](../../../apps/endpoints.md#publishing-ports).

An app service linked to MariaDB receives the host, port, database name, user name, and password as environment
variables defined by its own link, for example `DB_HOST` and `DB_PASSWORD` on a PHP service. Read them in the
application instead of hardcoding them.

To open a shell in the database container, use the [web terminal](../../../apps/web-terminal.md). For example,
`mariadb -uroot -p"$MYSQL_ROOT_PASSWORD" -e 'SHOW DATABASES;'` lists the databases.

## Adminer and phpMyAdmin

Both have no persistent data. Wodby protects their public domains with basic auth by default. Reveal the generated
password on the environment's **Endpoints > Auths** page. See [Auths](../../../apps/endpoints.md#auths).

- **Adminer:** the login form is prefilled with the system, server, and database. Type the user name and password.
- **phpMyAdmin:** it connects only to the linked MariaDB server. Sign in with the environment's database user to see
  its database, or with `root` to see all databases.

## Server settings

The container rebuilds its configuration from environment variables on every start. Change a setting by setting a
[variable](../../../apps/environment-variables.md) on the MariaDB app service. Do not edit the generated file. Common
ones:

- `MYSQL_INNODB_BUFFER_POOL_SIZE`, `MYSQL_MAX_CONNECTIONS`, `MYSQL_MAX_ALLOWED_PACKET`
- `MYSQL_CHARACTER_SET_SERVER`, `MYSQL_COLLATION_SERVER`
- `MYSQL_WAIT_TIMEOUT`, `MYSQL_INNODB_LOCK_WAIT_TIMEOUT`, `MYSQL_TRANSACTION_ISOLATION`
- `MYSQL_SLOW_QUERY_LOG`, `MYSQL_LONG_QUERY_TIME`, `MYSQL_GENERAL_LOG`

A change applies on the next deployment of the service. Host names are not resolved, and connections use the server
character set.

## Backups and restore

Data is on the `data` volume. A backup is a gzipped SQL dump of the environment's database. In the backup's **Excluded
table contents** option, list table names or SQL `LIKE` patterns. Those tables keep their definition and lose their
rows. See [Application backups](../../../apps/backups.md).

To restore, run a database import from a backup or an uploaded file. See
[Application imports](../../../apps/imports.md). The import accepts `.gz`, `.tar.gz`, `.tgz`, and `.zip` archives
that contain exactly one `.sql` or `.mysql` file.

!!! warning
    A database import replaces the contents of the `data` volume. Data that is not in the dump is not kept.

## Upgrades

After a version upgrade, Wodby runs `mariadb-upgrade` and `mariadb-check` on the environment's database and on the
`mysql` system database.
