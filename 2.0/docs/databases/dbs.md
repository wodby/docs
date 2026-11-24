---
title: DBs inside a database server
description: Create and delete individual DBs inside a database server in Wodby, choosing the name, charset and collation of each DB.
---

# DBs

Inside a database server, you can create and delete individual DBs.

When creating a DB, specify:

- name
- charset
- collation

Creating and deleting DBs requires permission to modify the database. For a database that belongs to an app
environment, creating a DB also requires the `Configure` [permission](../access-control.md#environment-permissions) in
that environment type, and deleting a DB requires `Delete`.

For container-based databases created as part of an app, Wodby usually creates the app-specific DB and user automatically from the service configuration.
