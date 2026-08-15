# Migrate an instance to another server

Wodby can migrate a supported application instance to another server in the
same organization. This is useful when moving from Infrastructure 6 to a new
Infrastructure 7 server, replacing a server, or redistributing applications.

Migration creates a separate instance in the same app. It deploys the source
stack and settings on the target server, then restores a selected backup. The
source instance is not changed, stopped, or deleted, so you can verify the copy
before switching traffic.

!!! info "A migration is a copy"
    The migration copy is a normal billable instance from the moment it is
    created and counts toward the organization's instance allowance. Wodby does
    not automatically delete the source after cutover.

## Requirements

The migration page runs a preflight check and lists anything that must be fixed.
In general, you need:

* A Drupal or WordPress source instance in **OK** status.
* A deployable stack whose services and persistent volumes can be recreated on
  the target. Unsupported custom stateful volumes block migration.
* Another healthy server in the same organization that satisfies the stack's
  infrastructure requirement.
* Permission to update the source instance and target server and to create an
  instance of the same type.
* A successful source backup containing both the database and files.
* Available instance capacity in the organization's plan.
* No existing migration copy for the source instance.

Servers with an incompatible infrastructure version or a conflicting custom
domain are not available as targets. The source and target must be different
servers.

Application code is not stored in the selected database-and-files backup. Git
repositories and CI images used by the source must remain available while the
copy is deployed. Wodby carries the deployed CI image references to the target.

## Prepare the source

1. [Connect the target server](../infrastructure/connecting-server.md) and wait
   until it is healthy in the dashboard.
2. Confirm that the source instance deploys successfully with its current stack
   and code source.
3. Lower the DNS TTL for custom domains if you want a faster cutover.
4. Enable maintenance mode under **Instance > Stack > Settings** to prevent
   writes while the final backup is created.
5. Create a fresh [backup](backups.md) containing both database and files, and
   wait for both components to finish successfully.

Maintenance mode is strongly recommended but is not enabled automatically. If
the site remains writable after the selected backup finishes, later changes are
not included in the migration copy.

## Create the migration copy

1. Open the source instance in the dashboard.
2. Go to **Settings > Migrate**.
3. Review and resolve any preflight blockers or warnings.
4. Select the target server.
5. Select the final database-and-files backup.
6. Click **Create migration copy** and wait for the task to finish.

The new instance receives a `migrate-*` name. Wodby copies the exact persisted
stack revision, instance settings, and custom-domain routing configuration,
deploys the copy, and restores the selected database and files. If the source
stack, settings, or active CI build changes after preflight, the task stops and
you must start again with a fresh migration copy.

## Verify and switch traffic

1. Open the migration copy and test it through its technical `*.wodby.cloud`
   domain. Check application pages, administration, uploaded files, cron jobs,
   outgoing mail, and logs.
2. Confirm whether maintenance mode should remain enabled on the copy. The
   source setting is copied with the other instance settings.
3. Update the custom domains' DNS records to the target server's IP address.
4. Wait for DNS to resolve to the target, then request new certificates from
   the target instance's **Domains** page.
5. Re-enable HTTPS redirects and HSTS as required, disable maintenance mode on
   the target, and run final application checks.
6. Keep the source instance until the cutover and rollback window are complete.
   Delete it manually when it is no longer needed.

Custom domain names are copied, but DNS is not changed. Existing custom
certificates are not migrated, and custom-domain TLS, HTTPS redirects, and HSTS
are reset on the target. The target's technical domain follows the normal
certificate workflow for its server infrastructure.

## Failure and retry

The source remains available if migration fails. Review the task log, delete an
incomplete migration copy, resolve the reported problem, create a new final
backup if the source has changed, and retry from **Settings > Migrate**.

Source deletion is blocked only while a migration copy is still applying its
saved settings. Deleting the incomplete copy releases that protection.
