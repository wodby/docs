---
description: Run a PostgreSQL database server on Wodby with the PostgreSQL catalog stack, with a 20 GB data volume by default and optional Adminer and pgAdmin.
---

# PostgreSQL

The Wodby PostgreSQL catalog stack runs a PostgreSQL database server, with optional Adminer and pgAdmin. The current
composition is documented in [`wodby/stack-postgres`](https://github.com/wodby/stack-postgres). For PostGIS, see the
[PostGIS guide](../postgis/index.md).

## Create an environment

PostgreSQL is enabled by default with a 20 GB `data` volume. Adminer and pgAdmin are disabled by default. Enable one
when you want a browser interface for the database. Each is linked to the PostgreSQL service automatically.

Wodby creates the database and its user. Both are named after the app and the app environment. The database uses the
`UTF8` encoding and the `en_US.utf8` locale. The application does not create them. A role you create by hand with a
name Wodby later needs, but a different password, makes Wodby's create action fail. Add further
[DBs](../../../databases/dbs.md) and [users](../../../databases/users.md) on Wodby.

## Passwords

Wodby generates two [tokens](../../../apps/tokens.md) once per environment. Open the PostgreSQL app service's
**Configuration > Tokens** tab to reveal them:

- `password`: the password of the environment's database user.
- `root_password`: the password of the administrator `postgres`.

Do not connect as `postgres` from an application.

## Connect to the database

The server listens on TCP port `5432`. Inside the app environment, the host is the name of the PostgreSQL app service.
The database has no public route. To reach it from outside the cluster, publish its port. See
[Publishing ports](../../../apps/endpoints.md#publishing-ports).

An app service linked to PostgreSQL receives the host, port, database name, user name, and password as environment
variables defined by its own link, for example `DB_HOST` and `DB_PASSWORD` on a PHP service. Read them in the
application instead of hardcoding them.

To open a shell in the database container, use the [web terminal](../../../apps/web-terminal.md). For example,
`PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U postgres -c '\l'` lists the databases and their owner roles.

## Ownership inside a database

Each managed database is owned by its own role, named `<database>:owner`, which cannot log in. Granting a user access
to the database makes that user a member of the role, and the user's sessions in that database act as the role.

- Objects are created in the `public` schema and belong to the owner role, whichever user created them. All users with
  access share the database's data.
- In such a session, `current_user` is the owner role and `session_user` is the user that logged in. Code that compares
  `current_user` with the login name sees the owner role.
- Only users granted access can connect to the database.

## Extensions

Wodby creates extensions as the administrator. Set `POSTGRES_DB_EXTENSIONS` on the PostgreSQL app service to a
comma-separated list of extensions to create in a database when Wodby creates it. pgvector is bundled with the image
but not enabled. Add `vector` to the list to enable it. To list the extensions in a database, run
`PGPASSWORD="$POSTGRES_PASSWORD" psql -h localhost -U postgres -d <database> -c '\dx'` in the web terminal.

## Adminer and pgAdmin

Wodby protects their public domains with basic auth by default. Reveal the generated password on the environment's
**Endpoints > Auths** page. See [Auths](../../../apps/endpoints.md#auths).

- **Adminer:** it has no persistent data. The login form is prefilled with the system, server, and database. Type the
  user name and password.
- **pgAdmin:** it has its own login, which is not a database credential. Sign in with the administrator email
  `user@domain.com` and the password in the pgAdmin app service's `admin_password` token. pgAdmin registers the
  linked database as a server named `PostgreSQL`. It connects as the environment's database user, not as `postgres`,
  and asks for no password. Wodby rewrites this server on every start, so changes to it inside pgAdmin do not last.
  The optional **pgAdmin configuration** volume keeps pgAdmin's own preferences and servers you add. Without it,
  they are lost when the container is replaced.

## Server settings

The container rebuilds its configuration from a template and environment variables on every start. Do not edit the
generated file. Use one of these instead:

- Set a [variable](../../../apps/environment-variables.md) on the PostgreSQL app service: `POSTGRES_MAX_CONNECTIONS`,
  `POSTGRES_SHARED_BUFFERS`, `POSTGRES_WORK_MEM`, `POSTGRES_MAINTENANCE_WORK_MEM`, `POSTGRES_EFFECTIVE_CACHE_SIZE`,
  `POSTGRES_MAX_WAL_SIZE`, `POSTGRES_TIMEZONE`, or `POSTGRES_SHARED_PRELOAD_LIBRARIES`.
- Override the service's **PostgreSQL config** file for a setting that no variable covers. It replaces the template.
  See [Configs tab](../../../apps/services.md#configs-tab).

A change applies on the next deployment of the service.

## Limits

The PostgreSQL service runs a single instance.

## Backups and restore

Data is on the `data` volume. A backup is a gzipped SQL dump of the environment's database. In the backup's
**Excluded table contents** option, list table patterns. Matching tables keep their definition and lose their rows.
See [Application backups](../../../apps/backups.md).

A backup carries no role names and no grants. You can import it into a database with another name and other users.

To restore, run a database import from a backup or an uploaded file. See
[Application imports](../../../apps/imports.md). The import accepts `.gz`, `.tar.gz`, `.tgz`, and `.zip` archives.
Wodby hands the imported objects to the database's owner role. Roles that a dump names, which this server does not
have, exist only while the dump is loaded.

!!! warning
    A database import replaces the contents of the `data` volume. Data that is not in the dump is not kept.
