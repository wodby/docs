# Databases

## Overview

Databases are first-class resources in Wodby. They give you a shared place to manage:

- [DBs](dbs.md)
- [users](users.md)
- [backups](backups.md)
- [imports](imports.md)

Database ownership and sharing depend on how the database is deployed:

- A container-based database belongs to an app. It always uses the owning app's owner and project access list. To change who can use or modify it, open the app's `Sharing` page.
- A managed database is independent of an app. Use the database's `Sharing` page to change its owner or make it available to additional projects with either `Read/Use` or `Modify/Delete` access.

A database also has an [environment type](../apps/environment-types.md). For container-based databases created from
an app, the type matches the owning app environment.

The database details page also shows the current connection metadata and can reveal the current master password on
demand. A master password is a
[privileged secret](../access-control.md#secret-reveal-permissions), so only organization owners/admins and project
admins can reveal it, and recent [secret reveal confirmation](../user/security.md#secret-reveal-confirmation) is
required.

## Deployment types

Wodby supports two main ways to run a database server:

| Type | Best when | How it works |
| --- | --- | --- |
| Container-based | The database belongs to one app stack | The database runs as part of your app deployment with attached persistent storage |
| [Managed](managed.md) | You want an external provider-managed database | Wodby connects to a cloud-managed database workflow through integrations |

### 1. Container-based

The database runs as part of your application stack in a container with attached persistent storage.

Add one of the database [services](../services/index.md) to your stack and choose storage size in stack configuration or during app creation.

Its ownership and project access stay synchronized with the owning app. Moving the app to another owner project or changing the app's project access updates the database automatically; the database cannot be shared separately.

### 2. [Managed](managed.md)

The database server is deployed by a third-party cloud provider and connected through the required external service and cloud integration.

Supported managed database kinds include:

- MySQL
- MariaDB
- PostgreSQL

## Related pages

- [Managed databases](managed.md)
- [DBs](dbs.md)
- [Users](users.md)
- [Backups](backups.md)
