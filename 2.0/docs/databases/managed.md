# Managed Databases

## Overview

Wodby supports managed databases through external cloud-database services connected with provider integrations.

- [GCP Cloud SQL for MySQL and PostgreSQL](../providers/gcp.md#cloud-sql)
- [AWS RDS](../providers/aws.md#rds)
- [Azure Databases](../providers/azure.md#databases)
- [DigitalOcean Managed Databases](../providers/digitalocean.md#managed-database)

## Use a managed database from an app

1. Create the managed database from `Databases` using the required cloud integration.
2. In your stack configuration, add the matching external cloud-database service.
3. In the relevant stack-service `Links` configuration, point the database link to that cloud-database service instead of a container-based database service.
4. Create or update an app from that stack. When Wodby asks you to choose a database server for the cloud-database service, select the managed database you created in step 1.

This lets the app use the managed database while keeping the rest of the application inside the Wodby deployment flow.

## Place it near Kubernetes

When creating a managed database, you can optionally associate it with a [Kubernetes cluster](../kubernetes/index.md).

The cluster must use the same cloud integration as the database. When you do this, Wodby can place the database in the same cloud network for private connectivity and lower latency.
