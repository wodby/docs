# Databases

## Overview

Databases are first-class resources in Wodby. They give you a shared place to manage:

- [DBs](dbs.md)
- [users](users.md)
- [backups](backups.md)
- [imports](imports.md)

A database can be project-owned or organization-owned. Use the database `Sharing` page to make it available to additional projects with either `Read/Use` or `Modify/Delete` access.

A database also has an [environment](../apps/env.md). For container-based databases created from an app, the environment usually matches the app instance environment.

## Deployment types

Wodby supports two main ways to run a database server:

| Type | Best when | How it works |
| --- | --- | --- |
| Container-based | The database belongs to one app stack | The database runs as part of your app deployment with attached persistent storage |
| [Managed](managed.md) | You want an external provider-managed database | Wodby connects to a cloud-managed database workflow through integrations |

### 1. Container-based

The database runs as part of your application stack in a container with attached persistent storage.

Add one of the database [services](../services/index.md) to your stack and choose storage size in stack configuration or during app creation.

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
