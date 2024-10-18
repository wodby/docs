# Databases

Databases represent following database management instances:

1. Container-based, deployed as a part of your applications deployment
2. External managed databases instances

Databases provide a layer for managing access to your DBMS, databases, backups and imports. 

For #2 we currently support the following managed database solutions: 

- [GCP Cloud SQL for MySQL and PostgreSQL](../integrations/gcp.md#cloud-sql)
- [AWS RDS](../integrations/aws.md#rds)
- [Azure Databases](../integrations/azure.md#databases)
- [DigitalOcean Managed Databases](../integrations/digitalocean.md#managed-database)

A database is a sharable entity and can be shared to multiple projects.

A database has an [environment](../apps/env.md), for container-based databases the environment will be set to the same as instance's.

Right now we support the following database kinds:

- MySQL
- MariaDB
- PostgreSQL

## Reside with Kubernetes

When creating a new external managed database, you can choose a Kubernetes cluster to reside this database with. The Kubernetes cluster must be created from the same integration as the database. When selected it will use the same cloud network as the Kubernetes cluster for private connections.
