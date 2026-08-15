# Migrate a Drupal stack to a newer major version

An app can continue to show an older Drupal stack after its codebase has been
upgraded to a newer Drupal major version. The app-level stack migration updates
that platform configuration and redeploys every instance on the managed stack
for the selected Drupal generation.

Supported transitions are:

* Drupal 8 to Drupal 9, 10, or 11.
* Drupal 9 to Drupal 10 or 11.
* Drupal 10 to Drupal 11.

!!! danger "Upgrade Drupal before migrating the stack"
    Stack migration does not update Drupal core, Composer dependencies, custom
    code, contributed modules, the database schema, or files. Upgrade and test
    the application itself first. Start migration only when the code and data
    on every instance are compatible with the selected Drupal major version.

## What migration changes

Migration changes the existing app in place. It does not create another app or
copy application data.

For every instance, Wodby creates a new stack revision derived from the current
managed target stack, preserves compatible service choices and configuration,
switches the instance to that revision, and redeploys it. The app's Drupal type
is updated only as part of the same app-wide operation.

When a manually configured `NGINX_VHOST_PRESET` or `DRUPAL_VERSION` value
already matches the target generation, the redundant override is removed so
the target stack's defaults become authoritative. A conflicting value blocks
migration instead of being silently discarded. Other compatible environment
variables and secrets are preserved.

## Requirements and preflight

Stack migration is available for eligible Drupal 8, 9, and 10 apps. The
dashboard checks the entire app before it enables the migration:

* The source must use an official stack derived from the app's current Drupal
  generation.
* The target must be the current managed stack for a newer Drupal generation in
  the same organization.
* Every app instance must be in **OK** status and have no pending stack revision.
* Every instance server must satisfy the target stack's infrastructure
  requirement.
* Apps with CI-based instances are currently not eligible.
* Enabled services that do not exist in the target stack block migration.
* Database, search, or Zookeeper implementation changes that require a data
  migration are not performed automatically and block migration.
* Conflicting Drupal or Nginx identity overrides block migration.

Disabled services that no longer exist can be removed with a warning. The
preflight page shows the target, blockers, warnings, and planned changes for
each instance before anything is modified.

## Prepare the app

1. Upgrade the Drupal codebase and dependencies using Drupal's supported major
   version upgrade process.
2. Apply the required Drupal database updates and configuration changes.
3. Deploy and test the upgraded application on every instance while it still
   uses the old stack metadata.
4. Create current database-and-files backups for important instances.
5. Release or discard pending stack changes and make sure every instance is in
   **OK** status.
6. Plan for a redeployment of every instance and the associated downtime.

If you temporarily set `NGINX_VHOST_PRESET` or `DRUPAL_VERSION` to run the newer
code on the old stack, leave matching values in place for preflight. Migration
recognizes and removes them when it switches to the corresponding target stack.

## Run the migration

1. Open the app in the dashboard.
2. Go to **Settings > Migrate**. This is the app settings page, not an individual
   instance's settings page.
3. Select the target Drupal stack.
4. Review all app-level and per-instance blockers, warnings, and planned
   changes. Resolve blockers and reload the page until migration is available.
5. Confirm that the application code is compatible with the selected Drupal
   version.
6. Start migration and wait for the task to redeploy every instance.

Do not edit app or stack settings after reviewing preflight. If relevant state
changes before the task starts, Wodby rejects the stale plan and asks you to
reload it.

## After migration

Verify every instance, including application pages, administrative pages,
scheduled jobs, uploads, logs, and integrations. Confirm that the app now shows
the selected Drupal generation and that the matching temporary identity
overrides are gone.

If an instance deployment fails, the app is marked degraded and remains on the
new stack revisions. Fix the deployment problem and redeploy the affected
instances through the normal instance deployment workflow. Stack migration
does not automatically roll the app back to its old generation.
