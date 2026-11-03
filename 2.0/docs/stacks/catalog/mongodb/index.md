# MongoDB

The Wodby MongoDB catalog stack runs a MongoDB 8.0 database server from the official MongoDB image, with an optional
Mongoku web interface. The current composition is documented in
[`wodby/stack-mongodb`](https://github.com/wodby/stack-mongodb).

## Create an environment

MongoDB is enabled by default with a 10 GB `data` volume. Mongoku is disabled by default. Enable it when you want a
browser interface for the database. It is linked to the MongoDB service automatically.

Wodby creates the database and its user. Both are named `<app>_<environment>`, after the app and the app environment.
The application does not create them. Wodby creates the database by adding a collection named `__wodby` to it. Leave
that collection in place.

Add further [DBs](../../../databases/dbs.md) and [users](../../../databases/users.md) on Wodby. A user gets the
`readWrite` role on each DB it has access to, and no other permissions.

## Passwords

Wodby generates two [tokens](../../../apps/tokens.md) once per environment. Open the MongoDB app service's
**Configuration > Tokens** tab to reveal them:

- `password`: the password of the environment's database user.
- `root_password`: the password of the administrator `root`.

Authentication is always on. Do not connect as `root` from an application.

## Connect to the database

The server listens on TCP port `27017`. Inside the app environment, the host is the name of the MongoDB app service.

Database users are stored in the `admin` database, not in the application database. A client must authenticate against
`admin`, so add `authSource=admin` to the connection string:

```text
mongodb://<user>:<password>@<host>:27017/<database>?authSource=admin
```

Without `authSource=admin`, MongoDB refuses a correct password. URL-encode the user name and password.

An app service linked to MongoDB receives the connection details as environment variables defined by its own link.
Read them in the application instead of hardcoding them. A connection URL that Wodby builds for a link already includes
`authSource=admin`. If you assemble the URL from separate host, port, user and password variables, add it yourself.

To open a shell in the database container, use the [web terminal](../../../apps/web-terminal.md). For example, this
lists the databases:

```bash
mongosh --quiet -u "$MONGO_INITDB_ROOT_USERNAME" -p "$MONGO_INITDB_ROOT_PASSWORD" \
  --authenticationDatabase admin --eval 'db.adminCommand({listDatabases: 1})'
```

## Access from outside the cluster

The database has no public domain. To reach it from outside the cluster, publish its port. See
[Publishing ports](../../../apps/endpoints.md#publishing-ports).

!!! warning
    The server does not use TLS. On a published port, passwords and data cross the network unencrypted. Unpublish the
    port when you no longer need it.

## Mongoku

Mongoku gets its own technical domain. Find it under **Endpoints > Domains**. See
[Technical domains](../../../apps/endpoints.md#technical-domains). Mongoku is configured with the app service's primary
URL, so open it at its primary domain.

Mongoku asks for its own user name and password. This sign-in is part of Mongoku, separate from the basic auth you can
add under **Endpoints > Auths**. Sign in with:

- user name: `admin`
- password: the `admin_password` token on the Mongoku app service's **Configuration > Tokens** tab. See
  [Tokens tab](../../../apps/services.md#tokens-tab).

Mongoku then opens the linked MongoDB server as the environment's database user, without asking for database
credentials. It has the same access as that user. The `admin`, `config` and `local` databases are hidden.

To prevent changes from the interface, turn on the **Read-only mode** setting on the Mongoku app service. See
[Settings tab](../../../apps/services.md#settings-tab).

Mongoku has no volume. Servers you add in it are lost when its container is replaced.

## Limits

- The MongoDB service runs a single standalone server, not a replica set. MongoDB does not support transactions on a
  standalone server, so application code that needs transactions does not work with this service.
- The service has no settings or configuration files to override. MongoDB runs with its default configuration.
- On x86-64 nodes, MongoDB 8.0 needs a CPU with AVX support.

## Backups and restore

Data is on the `data` volume. A backup is a `.tar.gz` archive. It holds a gzipped `mongodump` archive of the
environment's database, `dump.archive.gz`, and the script Wodby uses to restore it. The backup does not include users
or other databases. See [Application backups](../../../apps/backups.md).

The backup is first written to the `data` volume and then uploaded, so keep free space on the volume for a compressed
copy of the database.

To restore a downloaded backup outside Wodby, extract it and run
`mongorestore --archive=dump.archive.gz --gzip` with your connection options.

To restore on Wodby, run a database import from a backup or an uploaded file. See
[Application imports](../../../apps/imports.md). The import accepts `.tar.gz` and `.tgz` backups made by the MongoDB
service on Wodby. Collections are restored into this environment's database, even when the backup comes from an
environment with another database name.

!!! warning
    A database import replaces the contents of the `data` volume. Data that is not in the backup is not kept.
