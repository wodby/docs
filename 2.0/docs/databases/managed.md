# Managed Database Integration

## Overview

Wodby provides special "Cloud" external database services that integrate with third-party cloud providers.

- [GCP Cloud SQL for MySQL and PostgreSQL](../integrations/gcp.md#cloud-sql)
- [AWS RDS](../integrations/aws.md#rds)
- [Azure Databases](../integrations/azure.md#databases)
- [DigitalOcean Managed Databases](../integrations/digitalocean.md#managed-database)

## How to use an external database server from my app

- Go to the `Configure` page of your stack and add the appropriate _Cloud Database service_ (from listed above)
- To make sure your app will use the external database server instead of a container-based one, go to `Links` page of your stack service (from where database connection established) and update the DB link to use the _Cloud Database service_ instead of the container-based one
- Create a new external database server from `Databases` page
- Now, when creating a new app, you will be asked to choose an external database server for the _Cloud Database service_

## Reside with Kubernetes

When creating a new external managed database, you can choose a [Kubernetes cluster](../kubernetes/index.md) to reside this database with. The Kubernetes cluster must be created from the same integration as the database. When selected, it will use the same cloud network as the Kubernetes cluster for private connections and minimizing network latency.
