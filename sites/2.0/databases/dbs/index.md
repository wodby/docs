Source: https://wodby.com/docs/2.0/databases/dbs/

# DBs

Inside a database server, you can create and delete individual DBs.

When creating a DB, specify:

- name
- charset
- collation

Creating and deleting DBs requires permission to modify the database. For a database that belongs to an app
environment, creating a DB also requires the `Configure` [permission](https://wodby.com/docs/2.0/access-control/#environment-permissions) in
that environment type, and deleting a DB requires `Delete`.

For container-based databases created as part of an app, Wodby usually creates the app-specific DB and user automatically from the service configuration.
