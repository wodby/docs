# Managed Database Integration

## Overview

Wodby provides special "Cloud" external database services that integrate with third-party cloud providers.

- [GCP Cloud SQL for MySQL and PostgreSQL](../integrations/gcp.md#cloud-sql)
- [AWS RDS](../integrations/aws.md#rds)
- [Azure Databases](../integrations/azure.md#databases)
- [DigitalOcean Managed Databases](../integrations/digitalocean.md#managed-database)

After adding a cloud database service to your stack, you will be asked to connect a
`database` integration when creating a new app.

## Reside with Kubernetes

When creating a new external managed database, you can choose a [Kubernetes cluster](../kubernetes/index.md) to reside this database with. The Kubernetes cluster must be created from the same integration as the database. When selected it will use the same cloud network as the Kubernetes cluster for private connections.
