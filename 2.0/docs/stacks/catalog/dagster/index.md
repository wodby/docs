---
description: Deploy Dagster on Wodby with the Dagster catalog stack, which runs the Dagster webserver and daemon with the PostgreSQL database that stores its data.
---

# Dagster

The Wodby Dagster catalog stack runs the Dagster webserver and daemon with a PostgreSQL database. Dagster stores its
data in that database, so both services are required and cannot be excluded. The current composition is documented in
[`wodby/stack-dagster`](https://github.com/wodby/stack-dagster).

## Open the Dagster interface

Wodby protects the Dagster app service's public domains with HTTP basic authentication. Find the generated password in
**Apps > [App] > [Environment] > Endpoints > Auths**. Other services in the same app environment reach Dagster without
the password. You can turn the protection off when you create the app, or later by deleting the entry. See
[Auths](../../../apps/endpoints.md#auths).

## Add code locations

The stack deploys no user code. The webserver reads its code locations from the **Workspace** config
(`workspace.yaml`), which is empty by default. Open the Dagster app service's **Configuration > Configs** tab, override
the config, and add your code locations, for example gRPC servers that run elsewhere in the app environment. Then deploy
the app service. Dagster's own user code deployments are not created.

## Runs

The daemon queues runs and launches each one as a Kubernetes job. Runs do not execute inside the webserver or daemon
containers.

The **Wipe all run history** action deletes all run history and event logs. It cannot be undone.

## Data and backups

Dagster has no volume. Runs, events, and schedules are stored in the linked PostgreSQL database, so back up that
database. See [Backups](../../../apps/backups.md) and [Database details](../../../databases/index.md).

To change configuration, edit the **Workspace** config or add environment variables on the app service, then deploy it.

## Limits

The Dagster service is not scalable.
