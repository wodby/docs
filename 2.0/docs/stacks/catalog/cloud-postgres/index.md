---
description: The Wodby Cloud PostgreSQL catalog stack declares a PostgreSQL server that runs at a cloud provider, outside the cluster, with no containers of its own.
---

# Cloud PostgreSQL

The Wodby Cloud PostgreSQL catalog stack declares a PostgreSQL database server that runs at a cloud provider, outside
the cluster. It has no containers, volumes, or configuration of its own. The current composition is documented in
[`wodby/stack-cloud-postgres`](https://github.com/wodby/stack-cloud-postgres). To run PostgreSQL inside the app
environment instead, use the [PostgreSQL guide](../postgres/index.md).

## Create an environment

1. Create the managed database first, from **Databases**, with the required cloud integration. See
   [Managed databases](../../../databases/managed.md) and [Database providers](../../../providers/databases.md).
2. Create the app from the **Cloud PostgreSQL** stack. When Wodby asks you to choose a database server for the service,
   select the managed database.

Managed database names must use lowercase letters, numbers, and dashes, start with a letter, end with a letter or
number, and be 3 to 32 characters long.

## Database, user, and password

Wodby declares one database and one user for the environment. Both are named after the app and the app environment.
The application does not create them. Wodby generates the user's password once per environment. Open the app
service's **Configuration > Tokens** tab to reveal the `password` token. See [Tokens](../../../apps/tokens.md).

## Connect to the database

The host and port are those of the managed database server, not an app service name inside the environment. An app
service linked to this service receives the host, port, database name, user name, and password as environment
variables defined by its own link, for example `DB_HOST` and `DB_PASSWORD` on a PHP service. Read them in the
application instead of hardcoding the provider's address.

For a managed database on Amazon RDS, DigitalOcean, or Azure, Wodby gives the app the server's CA certificate. Some
servers accept only TLS connections. See [Encrypted connections](../../../databases/managed.md#encrypted-connections).

## Limits

- There is no database container, so the [web terminal](../../../apps/web-terminal.md) has nothing to open for this
  service.
- This service has no server settings. Server parameters, storage, and versions are managed on the managed database
  itself.
- The service defines no backups, imports, or actions.
