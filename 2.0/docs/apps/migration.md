# App environment cluster migration

App environment cluster migration moves an existing environment and its persistent data from one Kubernetes cluster to
another cluster in the same Wodby organization. The app environment keeps its identity and configuration; Wodby deploys
its services on the target cluster, restores supported data, and switches its managed technical routes.

This is a **cold migration**. Wodby stops source writers before creating the final backups, and the environment remains
unavailable while its data is backed up, restored, and deployed on the target. Plan a maintenance window whose length
allows for the size of your data and the deployment time of your services.

## Requirements

Before starting a migration, make sure:

- You have Write access to the app.
- The app environment is a standard application environment, not an infrastructure app environment.
- The environment has an active deployment, has status `OK`, uses platform-managed routing, and is not in maintenance
  mode.
- The source and target clusters have status `OK`, belong to the same organization, and the target cluster is available
  to the app's owner project when the app is project-owned.
- The source cluster supports the maintenance response required to freeze public traffic, and the target cluster supports
  the current app-owned routing resources. Upgrade cluster infrastructure first if the migration reports a missing
  routing capability.
- [Wodby Blob Storage](../providers/wodby-blob-storage.md) is available. Migration backups always use Wodby Blob Storage,
  which requires a paid subscription.
- Every app service that owns a persistent volume provides matching
  [backup](../services/operations.md#backups) and [import](../services/operations.md#imports) operations. A disabled data
  service with a migration backup/import operation must be enabled first.
- Every build-backed app service has an active build that Wodby can reuse on the target cluster.

The first version of cluster migration supports only managed technical routes. Before migrating:

- remove [App Access](access.md)
- remove private routes
- remove or disable custom routes
- unpublish TCP and UDP ports

You can recreate these access and endpoint settings after the migration completes.

Create or connect the target cluster before opening the migration form. The target must be different from the current
cluster. A cluster that still contains a retained source from an earlier migration cannot be reused as a target until
that retained source is cleaned up.

## Start a migration

1. Open `Apps > [App] > [Environment] > Settings > Migration`.
2. Review any prerequisite warnings and resolve every blocker.
3. Select the target cluster.
4. For each root persistent volume, select the storage class that should receive the restored data on the target. Wodby
   selects the target cluster's single default class automatically when one is available.
5. Select `Review migration`.
6. Review the downtime and target-cluster confirmation, then select `Start migration`.

Changing the target cluster clears and revalidates the storage-class selections. Shared volumes and volumes that reuse
another volume do not need an independent mapping; their owning storage service or source volume controls the class.

The environment status changes to `Migrating`, and operations that could change its configuration or runtime are blocked
until the migration completes or the source is restored. The source and target clusters also serialize conflicting app
and storage work while the task is running.

## What Wodby does

The migration task performs these steps in order:

1. Enable a maintenance response on managed public routes, drain active app work, and stop source writers.
2. Create final service-native backups in Wodby Blob Storage.
3. Stop the remaining workloads on the source cluster.
4. Deploy the environment on the target cluster and restore each migration backup.
5. Switch the environment's managed technical routing and DNS to the target cluster.
6. Return the environment to normal operation and retain the stopped source runtime for seven days.

Open the migration's task to follow detailed logs. The Migration page also shows the current phase and migration status.
Expand a migration-history row to inspect the backup and restore created for each data component.

## Failure and rollback

If the migration task fails before completion, Wodby automatically attempts to:

- remove the staged target runtime
- restore the environment's source-cluster, deployment, storage, and database references
- reinstall the source service releases
- restore source routing without the maintenance response
- point managed technical DNS back to the source cluster

A migration shows `Rolled back` when recovery completes. If automatic recovery cannot finish, the migration remains
`Failed` or `Rollback failed`; correct the underlying cluster, storage, or deployment problem, then select `Roll back`
from the migration history.

Do not treat a successful migration as a reversible failover. After cutover, the target may accept new writes, so a
completed migration cannot be rolled back to the retained source. To move back, first clean up the retained source and
then start a new forward migration with the former source cluster as the new target.

## Retained source and cleanup

After a successful cutover, Wodby keeps the stopped source namespace for seven days. It does not receive traffic or new
writes, but its Kubernetes resources and persistent volumes can continue to incur infrastructure and storage costs.

Wodby schedules cleanup after the retention time expires. The cleanup job runs hourly, so deletion may begin after the
displayed retention deadline rather than at the exact minute. To remove the retained source earlier, select `Clean up
source` in migration history and confirm the permanent deletion.

Source cleanup does not delete the migration backups. Those backups remain available according to the normal
[backup destination and retention](backups.md) behavior.

While either cluster is still required by a migration or retained source, Wodby blocks operations that could make
recovery unsafe, including deleting the app environment, deleting either cluster, or changing cluster sharing in a way
that removes required access.

## Related pages

- [App environments](environments.md)
- [Application backups](backups.md)
- [Application imports](imports.md)
- [Application persistent storage](storage.md)
- [Maintenance mode](maintenance.md)
- [Kubernetes clusters](../clusters/index.md)
