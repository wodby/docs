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

Managed database machine names are provider-facing. They must use lowercase letters, numbers, and dashes, start with a letter, end with a letter or number, and be 3 to 32 characters long.

## Encrypted connections

For a managed database on Amazon RDS, DigitalOcean or Azure, Wodby gives the app the server's CA certificate. Apps
from the PHP-based catalog stacks connect to the server over TLS when it has one:

- Laravel and Drupal 10 and 11 connect with TLS and verify the server certificate.
- WordPress connects with TLS but cannot verify the server certificate, because WordPress has no setting for a CA
  certificate.

Some servers accept only TLS connections, for example new Amazon RDS MariaDB servers. Apps on them need these TLS
settings to connect. To get them in an existing app environment, [upgrade its stack](../stacks/updates.md).

A custom service gets the CA certificate through its database link. See
[`links`](../services/template.md#links).

## Place it near Kubernetes

When creating a managed database, you can optionally associate it with a [Kubernetes cluster](../clusters/index.md).

The cluster must use the same cloud integration as the database. When you do this, Wodby can place the database in the same cloud network for private connectivity and lower latency.
