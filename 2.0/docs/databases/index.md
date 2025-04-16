# Databases

## Deployment types

Database server is a first-class citizen on Wodby, we support two different ways of deploying your database server:

### 1. Container-based

Deployed as a part of your application stack and runs in a container with an attached persistent storage. Add one of the database [services](../services/index.md) to your stack and specify desired storage size in a stack configuration or when creating a new app.

### 2. [Managed](managed.md)

A database server will be deployed on a third-party cloud provider, requires a special external cloud service and cloud integration. 

## Overview

Databases provide a layer for managing access to your [DBs](dbs.md), [users](users.md), [backups](backups.md) and [imports](imports.md).

A database is a sharable entity and can be shared to multiple projects.

A database has an [environment](../apps/env.md), for container-based databases the environment will be set to the same as instance's.

Right now we support the following database kinds:

- MySQL
- MariaDB
- PostgreSQL
