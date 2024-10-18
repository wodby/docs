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

Right now we support the following database engines:

- MySQL
- MariaDB
- PostgreSQL

## DBs

You can create and delete individual databases (DB) in your database management system. 

To create a new database you need to specify a name, charset and a collation.

## Users

You can create and delete individual users of your database management system from _"Databases > [Database] > Users"_ page.

To create a new user enter the username, password and DBs the user need to have access to.

## Backups

From _"Databases > [Database] > Backup"_ you can run backups (different from snapshot) for individual DBs. When preparing a new backup, you can select on of the backup presets for this database or an organization-wide backup preset. Backup preset allow you to save time on entering backup destination details. 

## Import

From _"Databases > [Database] > Import"_ you can run import for individual DBs. You can either:

- Upload your backup archive from the dashboard  
- Specify a public URL where the backup archive can be downloaded from  
- Specify existing backup  

## Reside with Kubernetes

When creating a new external managed database, you can choose a Kubernetes cluster to reside this database with. The Kubernetes cluster must be created from the same integration as the database. When selected it will use the same cloud network as the Kubernetes cluster for private connections.
