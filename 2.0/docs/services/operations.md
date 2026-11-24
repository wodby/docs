---
description: Define actions, backups, imports and cron schedules in a Wodby service so applications can run maintenance and data workflows.
---

# Service operations

Service operations are workflows a service can expose for application maintenance, lifecycle hooks, recurring tasks,
data backup, and data import.

For the full manifest schema, see the [service template reference](template.md).

## Actions

Services can define actions that run commands in an app. Actions can be user-runnable from the app-service UI or run
automatically during deployment and upgrades. Each run creates a task with execution logs.

Actions run in the selected service workload. If an action does not specify `workload`, Wodby uses the service's
primary workload.

Deployment and upgrade actions run simultaneously unless dependencies are set between them.

### Action types

An action type defines how and when the action runs.

#### `button`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab in the Wodby dashboard.
Each run creates a task; command output is available in the task logs.

#### `output`

User-runnable action. Actions of this type are shown on the app service's `Actions` tab. Running the action creates a
task; output is associated with the task logs and is not returned directly by the run operation.

#### `pre_deploy`

Runs on every service deployment, before the new version of the service is installed, with the new version's image,
environment variables and settings. Use it for work the new version needs before it serves traffic, such as database
migrations. It can be limited to a specific build boilerplate.

- The previous version keeps serving while the action runs and until the rollout finishes.
- If the action fails, the deployment fails before the new version is installed and the previous version keeps
  serving. The deployment's task log shows the action output.
- On the service's first deployment there is no previous version, so the action runs right after the service is
  installed.
- When the deployment imports data, the action runs after the rollout instead, like `post_deploy`, so it never runs
  against data the import is about to replace.
- [Derivative services](derivatives.md) of the service are updated only after the action succeeds.
- It runs before the build's repository [pre-deployment scripts](../apps/deploys.md#pre-deployment-scripts).
- A `pre_deploy` action can depend only on other `pre_deploy` actions. Other deployment actions can depend on it.

!!! warning "Keep migrations compatible with the running version"
    A migration that removes or renames a table or column the previous version uses breaks it until the rollout
    finishes, and for good if the deployment fails. Add columns and tables first, and remove or rename them in a later
    release. Use `post_deploy` for updates the previous version can't run against.

#### `post_deploy`

Runs after every service deployment. If a deployment includes more than one service, the action runs only after all
deployments succeed. It can be limited to a specific build boilerplate.

#### `post_deploy_once`

Same as `post_deploy`, but runs only during the first deployment. It can be limited to a specific build boilerplate.

#### `post_upgrade`

Runs after an app environment is upgraded to a new stack revision.

#### `empty`

No-op action type used when a service needs to define an action placeholder without running a command. Empty actions are
not exposed as user-runnable app-service actions.

### App service actions

The app-service `Actions` tab shows only user-runnable service actions from the selected app service:

- `button`
- `output`

An app-service action can be disabled even when it appears in the tab. Actions are disabled when the app service or app
environment is not in a healthy `OK` state, and actions are not available for external or derivative app services.

Service actions are defined under the [`actions` section](template.md#actions) in a service template.

## Backups

Services can define data-backup behavior. There are three main backup methods.

### Simple files backup

Wodby archives the specified directory, optionally gzipped, and uploads it to the configured object storage. The
archive is not staged on the service's persistent volume.

### Staged backup through action

Wodby runs the configured command or args override to create the backup archive. The command must place the archive
in the specified volume path, after which Wodby uploads it to the configured object storage.

### Streamed backup through action

For compatible service and image versions, Wodby runs the service's streaming action and sends its output directly to
Wodby Blob Storage or supported third-party object storage, without creating a complete archive on the service's
persistent volume. If the action or the upload fails, no completed backup is left in storage.

Services declare exactly which option versions support this action. They must also retain the staged `create` and
`upload.filepath` definitions so older service revisions and unsupported versions have a compatible fallback.

Service backups are defined under the [`backups` section](template.md#backups) in a service template.

## Imports

Services can define data-import behavior. There are two main import methods.

### Simple files import

Wodby imports files directly into the running volume by unpacking the provided tar archive to the specified path.

This method is not transactional.

### Import through init volume

Wodby mounts the import archive into the init volume provided by the service, and a container performs the import during startup. This pattern is commonly used for databases.

This method is transactional: the import runs on a new persistent volume, and the service switches to that volume
only if the import succeeds.

Service imports are defined under the [`imports` section](template.md#imports) in a service template.

## Cron schedules

Services can define cron schedules for recurring tasks. Each schedule includes a name, a command or argument override,
and a cron expression. Every run creates a task with execution logs.

Use standard five-field crontab syntax such as `0 * * * *`. Cron schedules cannot run more often than once per hour.

Cron schedules are defined under the [`cron` section](template.md#cron) in a service template.
